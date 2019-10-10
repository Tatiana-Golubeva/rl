import gym
from gym import error, spaces, utils
from gym.utils import seeding
import numpy as np
from gym.envs.classic_control import rendering
from env.snake import Snake


class SnakeEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self, blocks=4, block_size=50, start_snake_len=1):
        self.blocks = blocks
        self.width = block_size * blocks
        self.start_snake_len = start_snake_len
        self.snake = None

        self.action_space = spaces.Discrete(3)
        self.observation_space = spaces.Box(
            dtype=np.float32,
            low=np.array([0, 0, 0, -1, -1]),
            high=np.array([1, 1, 1, 1, 1]),
        )

        self.seed()
        self.viewer = None

    def seed(self, seed=None):
        return np.random.seed()

    def step(self, action):
        if action != 0:
            self.snake.direction = self.snake.directions[self.snake.direction[action]]

        info = {}

        self.snake.update()
        info['food_eaten'] = self.snake.food_eaten

        raw_pos, reward, done = self.snake.get_raw_positions()
        info['food'] = self.snake.cnt_food

        pos = np.array(raw_pos, dtype=np.float32)
        pos /= self.blocks

        return tuple(pos), reward, done, info

    def reset(self):
        self.snake = Snake(self.blocks, self.width // self.blocks, self.start_snake_len)
        raw_pos = self.snake.get_raw_positions()
        pos = np.array(raw_pos[0], dtype=np.float32)
        pos /= self.blocks
        return pos

    def render(self, mode='human'):

        w = self.snake.len_blocks

        if self.viewer is None:
            self.viewer = rendering.Viewer(self.width, self.width)
            food = self._create_block(w)
            self.food_trans = rendering.Transform()
            food.add_attr(self.food_trans)
            food.set_color(*self.snake.food.clr)
            self.viewer.add_geom(food)

            head = self._create_block(w)
            self.head_trans = rendering.Transform()
            head.add_attr(self.head_trans)
            head.set_color(*self.snake.head.clr)
            self.viewer.add_geom(head)

            self.body = []
            for i in range(len(self.snake.body)):
                body = self._create_block(w)
                body_trans = rendering.Transform()
                body.add_attr(body_trans)
                body.set_color(*self.snake.body[0].clr)

                self.body.append(body_trans)
                self.viewer.add_geom(body)

        self.food_trans.set_translation(self.snake.food.x, self.snake.food.y)
        self.head_trans.set_translation(self.snake.head.x, self.snake.head.y)

        if len(self.snake.body) > len(self.body):
            body = self._create_block(w)
            body_trans = rendering.Transform()
            body.add_attr(body_trans)
            body.set_color(*self.snake.body[0].clr)

            self.body.append(body_trans)
            self.viewer.add_geom(body)
        elif len(self.snake.body) < len(self.body):
            self.body, trash = self.body[len(self.body) - len(self.snake.body):], \
                               self.body[:len(self.body) - len(self.snake.body)]
            for i in range(len(trash)):
                trash[i].set_translation(-w, -w)

        for i in range(len(self.body)):
            self.body[i].set_translation(self.snake.body[i].x, self.snake.body[i].y)

        self.viewer.render()

    def _create_block(self, w):
        return rendering.FilledPolygon([(0, 0), (0, w), (w, w), (w, 0)])

    def close(self):
        if self.viewer:
            self.viewer.close()
            self.viewer = None

from gym.envs.registration import register
from env.snake_env import SnakeEnv
register(
    id='Snake-v0',
    entry_point='env:SnakeEnv',
)

import random


class Block:
    def __init__(self, x, y, w, clr):
        self.x = x
        self.y = y
        self.w = w
        self.clr = clr


class Snake:
    directions = {"LEFT": ((-1, 0), "DOWN", "UP"),
                  "RIGHT": ((1, 0), "UP", "DOWN"),
                  "UP": ((0, 1), "LEFT", "RIGHT"),
                  "DOWN": ((0, -1), "RIGHT", "LEFT")}

    def __init__(self, blocks, len_blocks, start_snake_len=5):
        self.blocks = blocks
        self.len_blocks = len_blocks
        self.start_snake_len = start_snake_len
        self.move_reward = -0.25
        self.death_reward = -15
        self.food_reward = 10

        x, y = self.blocks // 2, self.blocks // 2
        self.direction = self.directions["UP"]
        self.game_over = False

        self.body = []
        for i in range(self.start_snake_len):
            block_x = x * self.len_blocks
            block_y = (y - i - 1) * self.len_blocks
            self.body.append(Block(block_x, block_y, self.len_blocks, (0, 255, 0)))

        head_x = x * self.len_blocks
        head_y = y * self.len_blocks
        self.head = Block(head_x, head_y, self.len_blocks, (0, 255, 255))

        self.food = None
        self.generate_food()
        self.food_eaten = False
        self.cnt_food = 0
        self.cnt_steps = 0

    def generate_food(self):
        while True:
            x, y = random.randint(0, self.blocks - 1), random.randint(0, self.blocks - 1)
            if self.head.x == x * self.len_blocks and self.head.y == y * self.len_blocks:
                continue

            flag = False
            for body_pnt in self.body:
                if body_pnt.x == x * self.len_blocks and body_pnt.y == y * self.len_blocks:
                    flag = True
                    continue
            if flag:
                continue

            food_x = x * self.len_blocks
            food_y = y * self.len_blocks
            self.food = Block(food_x, food_y, self.len_blocks, (255, 0, 0))
            break

    def update(self):
        bound = (self.blocks - 1) * self.len_blocks
        if (self.head.x < 0) or (self.head.x > bound) or (self.head.y < 0) or (self.head.y > bound):
            self.game_over = True
            return

        self.head.clr = (0, 255, 0)
        self.body = [self.head] + self.body[:]
        new_head_x = self.head.x + self.direction[0][0] * self.len_blocks
        new_head_y = self.head.y + self.direction[0][1] * self.len_blocks
        self.head = Block(new_head_x, new_head_y, self.len_blocks, (0, 255, 255))
        self.head.clr = (0, 255, 255)

        if self.food is None:
            self.generate_food()

        if self.food.x == self.head.x and self.food.y == self.head.y:
            self.generate_food()
            self.food_eaten = True
        else:
            self.body = self.body[:-1]

        for body_pnt in self.body:
            if body_pnt.x == self.head.x and body_pnt.y == self.head.y:
                self.game_over = True

    def get_raw_positions(self):
        reward = self.move_reward
        self.cnt_steps += 1
        if self.food_eaten:
            self.cnt_food += 1
            self.food_eaten = False
            reward += self.food_reward
        elif self.game_over:
            reward += self.death_reward
        # from head to bounds
        positions = [
            self.head.x // self.len_blocks,  # left
            self.blocks - (self.head.x // self.len_blocks) - 1,  # right
            self.head.y // self.len_blocks,  # down
            self.blocks - (self.head.y // self.len_blocks) - 1,  # up
        ]

        for body_pnt in self.body:
            if body_pnt.x == self.head.x:
                if body_pnt.y < self.head.y:
                    positions[2] = min(positions[2], (self.head.y - body_pnt.y) // self.len_blocks - 1)
                else:
                    positions[3] = min(positions[3], (- self.head.y + body_pnt.y) // self.len_blocks - 1)
            elif body_pnt.y == self.head.y:
                if body_pnt.x < self.head.x:
                    positions[0] = min(positions[0], (self.head.x - body_pnt.x) // self.len_blocks - 1)
                else:
                    positions[1] = min(positions[1], (- self.head.x + body_pnt.x) // self.len_blocks - 1)

        food_crd = [
            (-self.head.x + self.food.x) // self.len_blocks,
            (-self.head.y + self.food.y) // self.len_blocks,
        ]

        if self.direction == self.directions['UP']:
            positions = [positions[3], positions[0], positions[1]]
        if self.direction == self.directions['LEFT']:
            positions = [positions[0], positions[2], positions[3]]
            if food_crd[0] * food_crd[1] > 0:
                food_crd[1] *= -1
            else:
                food_crd[0] *= -1
            food_crd[0], food_crd[1] = food_crd[1], food_crd[0]
        if self.direction == self.directions['DOWN']:
            positions = [positions[2], positions[1], positions[0]]
            food_crd[0] *= -1
            food_crd[1] *= -1
        if self.direction == self.directions['RIGHT']:
            positions = [positions[1], positions[3], positions[2]]
            if food_crd[0] * food_crd[1] > 0:
                food_crd[0] *= -1
            else:
                food_crd[1] *= -1
            food_crd[0], food_crd[1] = food_crd[1], food_crd[0]

        positions.extend(food_crd)

        return positions, reward, self.game_over

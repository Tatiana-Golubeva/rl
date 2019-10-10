import random
import numpy as np
from collections import defaultdict
import gym
import env


class QlearningAgent:
    def __init__(self, alpha, epsilon, discount,
                 get_legal_actions):
        self.get_legal_actions = get_legal_actions
        self._q_values = \
            defaultdict(lambda: defaultdict(lambda: 0))
        self.alpha = alpha
        self.epsilon = epsilon
        self.discount = discount

    def get_q_value(self, state, action):
        return self._q_values[state][action]

    def set_q_value(self, state, action, value):
        self._q_values[state][action] = value


def get_value(self, state):
    """
      Возвращает значение функции полезности,
      рассчитанной по Q[state, action],
    """
    possible_actions = self.get_legal_actions(state)
    value = max([self.get_q_value(state, action) for action in possible_actions])

    return value


def get_policy(self, state):
    """
      Выбирает лучшее действие, согласно стратегии.
    """
    possible_actions = self.get_legal_actions(state)

    actions_dict = {action: self.get_q_value(state, action) for action in possible_actions}
    best_action = sorted(actions_dict, key=lambda x: actions_dict[x], reverse=True)[0]

    return best_action


def get_action(self, state):
    """
      Выбирает действие, предпринимаемое в данном
      состоянии, включая исследование (eps greedy)
      С вероятностью self.epsilon берем случайное
      действие, иначе действие согласно стратегии
      (self.get_policy)
    """
    state = tuple(state)
    possible_actions = self.get_legal_actions(state)
    epsilon = self.epsilon
    expl = random.random()
    if expl < epsilon:
        action = np.random.choice(possible_actions)
    else:
        action = self.get_policy(state)

    return action


def update(self, state, action, next_state, reward):
    """
      функция Q-обновления
    """
    state = tuple(state)
    next_state = tuple(next_state)
    gamma = self.discount
    learning_rate = self.alpha

    q_value_tgt = reward + gamma * self.get_value(next_state)
    q_value = learning_rate * q_value_tgt + (1 - learning_rate) * self.get_q_value(state, action)

    self.set_q_value(state, action, q_value)


def play_and_train(env, agent, t_max=10 ** 4):
    """функция запускает полную игру,
    используя стратегию агента (agent.get_action(s))
    выполняет обновление агента (agent.update(...))
    и возвращает общее вознаграждение
    """
    total_reward = 0.0
    s = env.reset()

    for t in range(t_max):
        a = agent.get_action(s)
        next_s, r, done, info = env.step(a)
        agent.update(s, a, next_s, r)
        s = next_s
        total_reward += r
        if done:
            print(info)
            print(total_reward)
            break

    return total_reward


QlearningAgent.get_value = get_value
QlearningAgent.get_policy = get_policy
QlearningAgent.get_action = get_action
QlearningAgent.update = update

env = gym.make('Snake-v0')
n_actions = env.action_space.n
agent = QlearningAgent(alpha=0.7, epsilon=0.1,
                       discount=0.9,
                       get_legal_actions=lambda s: range(
                           n_actions))

rewards = []
for i in range(700):

    rewards.append(play_and_train(env, agent))
    env.render()
    # if i % 100 == 0:
    #     print('mean reward =', np.mean(rewards[-10:]))

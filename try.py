import gym
import env

env = gym.make('Snake-v0')

for i in range(100):
    env.reset()
    n_actions = env.action_space.n
    sum_reward = 0
    for t in range(1000):
        env.render()
        pos, reward, done, info = env.step(env.action_space.sample())
        sum_reward += reward
        if done:
            print('episode {} finished after {} timesteps'.format(i, t))
            print("episode reward: ", sum_reward)
            print(info)
            break

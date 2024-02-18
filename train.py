
import gym

env = gym.make("UAVAgent-v0")
observation, info = env.reset(seed=42)

for _ in range(1000):
    action = env.action_space.sample()
    observation, reward, terminated, truncated, _ = env.step(action)
    
    if terminated or truncated:
        observation, info = env.reset()

env.close()

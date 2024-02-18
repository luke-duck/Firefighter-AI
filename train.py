import gym

class UAVAgent(gym.env):
    def __init__(self, game, uav):
        self.uav = uav
        self.game = game
        # total number of boxes is 81. 0 for burnt, 1 for burning, 2 for neither
        self.observation_space = gym.spaces.Box(0, 2, shape=(81,), dtype=int)
        self.action_space = gym.spaces.Discrete(4)
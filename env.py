import gym

class UAVAgent(gym.Env):
    def __init__(self, game) -> None:
        self.game = game
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(low=0, high=100, shape=(1,), dtype=int64)
    
    def _get_obs(self):
        obs = []

        for cell in self.game.cells:
            obs.append(cell.color)
       
        obs.append(self.game.uav.x)
        obs.append(self.game.uav.y)

        return obs

    def reset(self):
        self.game.init()

    def step(self, action):
        uav = self.game.uav

        if action == 0:
            uav.moveRight() 
        elif action == 1:
            uav.moveLeft()
        elif action == 2:
            uav.moveUp()
        elif action == 3:
            uav.moveDown()

        terminated = True
        truncated = False
        
        return self._get_obs(), self.game.getScore(), terminated, truncated, {}  

import gym
from assets.Gameloop import UAVAgent, cells
import gym.spaces
from assets.Cell import FireStatus

class UAVAgent(gym.Env):
    def __init__(self) -> None:
        self.action_space = gym.spaces.Discrete(4)
        self.observation_space = gym.spaces.Box(low=0, high=100, shape=(1,), dtype=int)
    
    def _get_obs(self):
        obs = []

        for cell in cells:
            obs.append(cell.color)
       
        obs.append(uav.x)
        obs.append(uav.y)

        return obs

    def reset(self):
        for cell in cells:
            cell.current_state = FireStatus.NOT_BURNED
    
    def step(self, action):
        reward = 0

        if action == 0:
            uav.move_right() 
        elif action == 1:
            uav.move_left()
        elif action == 2:
            uav.move_up()
        elif action == 3:
            uav.move_down()

        terminated = True
        truncated = False

        for cell in cells:
            if cell.current_state == FireStatus.BURNING:
                reward = 0
            if cell.current_state == FireStatus.NOT_BURNED:
                terminated = False
                reward = 1

        return self._get_obs(), reward, terminated, truncated, {}  

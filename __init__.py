
from gym.envs.registration import register

register(
    id='UAVDrone-v0',
    entry_point='env.UAVAgent',
    max_episode_steps=300,
)

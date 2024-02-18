# Firefighter-AI
**Reinforcement Learning for Fire Control by UAVs**
2024 Binghamton University 24 hour hackathon project

**Environment**

The environment represents a 2D top down view of the drone of a forest fire and is based on the Alexandridis model

![image](https://github.com/luke-duck/Firefighter-AI/assets/81270095/72135868-b7a0-48ef-b5b9-51ae5d3a4fe8)

1) Burned cell is black and cannot spread fire
2) Burning cell is red and the fire can spread to neighboring cells
3) Burning cells become burned after some time

Our 3D environment created with python and blender takes in a json file of the current game state and displays the result in a 3D view

![image](https://github.com/luke-duck/Firefighter-AI/assets/81270095/c99a6f65-bea3-43c9-b9ea-85fe565cbd0f)


We also experimented with wind angles and speed (Wind.py) but settled on using some randomness for fire spreading to green cells instead.

**Algorithm**

Attempted using OpenAI gym and PLE for reinforcement learning but were not able to get any results within 24 hours. The learning algorithm observes the current cell state (Burning, Burned, Not Burned) and chooses which cell to move the drone next. The UAV is awarded points for extinguishing fires.

**Citations**
<pre>
@article{alvarez2023forest,
  title={Forest Fire Localization: From Reinforcement Learning Exploration to a Dynamic Drone Control},
  author={Alvarez, J. and Belbachir, A. and Belbachir, F. and et al.},
  volume={109},
  year={2023},
  doi={10.1007/s10846-023-02004-z},
  url={https://doi.org/10.1007/s10846-023-02004-z}
}
</pre>

import gym
import tic_tac_toe

from gym.envs.registration import register

# Env registration
# ==========================

register(
    id='TicTacToe-v1',
    entry_point='tic_tac_toe:TicTacToeEnv',
    reward_threshold=1000
)

env = gym.make('TicTacToe-v1', symbols=[-1, 1], board_size=3, win_size=3) 

user = 0
done = False
reward = 0

# Reset the env before playing
state = env.reset()

while not done:
    env.render(mode=None)
    if user == 0:
        state, reward, done, infos = env.step([env.action_space.sample(), -1])
    elif user == 1:
        state, reward, done, infos = env.step([env.action_space.sample(), 1])
       
    # If the game isn't over, change the current player
    if not infos['already_used_position']:
        user = 0 if user == 1 else 1
    
    if done:
        if reward == 10:
            print("Draw !")
        elif reward == -20:
            print("Infos : " + str(infos))
            if user == 0:
                print("Player o Wins ! Reward : " + str(reward))
            elif user == 1:
                print("Player x Wins ! Reward : " + str(-reward))
        elif reward == 20:
            if user == 0:
                print("Player o Wins ! Reward : " + str(reward))
            elif user == 1:
                print("Player x Wins ! Reward : " + str(reward))
env.render(mode=None)
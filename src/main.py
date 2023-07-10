import gym
import numpy as np
import Environment.tic_tac_toe as TicTacToe
from Agents.agent import Agent
from gym.envs.registration import register


# Register the custom environment
register(
    id='TicTacToe-v1',
    entry_point='Environment.tic_tac_toe:TicTacToeEnv',
    reward_threshold=1000
    )
 

def main():
    step = 0
    wins_x = 0
    wins_o = 0
    wins_draw = 0

    board_size = 3

    agent = Agent(1, board_size**2)

    play_forever = True
    while play_forever:
        user = 0
        done = False
        reward = 0
        env = gym.make('TicTacToe-v1', symbols=[1, 2], board_size=board_size, win_size=3)

        # Reset the env before playing
        state = env.reset()

        while not done:
            # env.render(mode=None)
            if user == 0:
                action = agent.get_action(state['state'])
                state, reward, done, infos = env.step([action, 1])
                # state, reward, done, infos = env.step([env.action_space.sample(), 1])
                updated_state = agent.update(state['state'], reward)
            elif user == 1:
                state, reward, done, infos = env.step([env.action_space.sample(), 2])
            
            # If the game isn't over, change the current player
            if not infos['already_used_position']:
                user = 0 if user == 1 else 1
            
            if done:
                if reward == 10:
                    wins_draw += 1
                    # print("Draw !")
                elif reward == -20:
                    print("Infos : " + str(infos))
                    if user == 0:
                        wins_o += 1
                        # print("Player o Wins ! Reward : " + str(reward))
                    elif user == 1:
                        wins_x += 1
                        # print("Player x Wins ! Reward : " + str(-reward))
                elif reward == 20:
                    if user == 0:
                        wins_o += 1
                        # print("Player o Wins ! Reward : " + str(reward))
                    elif user == 1:
                        wins_x += 1
                        # print("Player x Wins ! Reward : " + str(reward))

        # env.render(mode=None)
        if step % 100 == 0:
            print(f'X win percentage: {np.round(wins_x/(wins_x+wins_o+wins_draw)*100,0)}')
            #step = 0
            wins_x = 0
            wins_o = 0
            wins_draw = 0
        step += 1
    temp = 1

    
if __name__ == "__main__":
    main()
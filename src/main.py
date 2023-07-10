import gym
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
    user = 0
    done = False
    reward = 0
    board_size = 3

    agent = Agent(board_size**2)
    env = gym.make('TicTacToe-v1', symbols=[1, 2], board_size=board_size, win_size=3)

    # Reset the env before playing
    state = env.reset()

    while not done:
        env.render(mode=None)
        if user == 0:
            state, reward, done, infos = env.step([env.action_space.sample(), 1])
            # updated_state = agent.update(state['state'], reward)
            # temp=1
        elif user == 1:
            state, reward, done, infos = env.step([env.action_space.sample(), 2])
        
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

    
if __name__ == "__main__":
    main()
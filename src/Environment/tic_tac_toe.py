import os
import gym
import numpy
from gym import spaces, error
import xml.etree.ElementTree as ET


class TicTacToeEnv(gym.Env):
    def __init__(self, symbols, board_size=3, win_size=3):
        super(TicTacToeEnv, self).__init__()
        self.win_size = win_size
        self.board_size = board_size
        self.symbols = {
            symbols[0]: "x",
            symbols[1]: "o"
        }
        self.action_space = spaces.Discrete(self.board_size * self.board_size)
        settings_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'settings.xml')
        self.load_xml_settings(settings_file)
        self.render_mode = None
        self.observation_space = spaces.Dict(
            {
                'state' : spaces.Discrete(n=9)
            }
        )

    def load_xml_settings(self, settings_file):
        settings_tree = ET.parse(settings_file)
        settings_root = settings_tree.getroot()
        for child in settings_root:
            if child.tag == 'Rewards':
                self.set_rewards(child)

    def set_rewards(self, rewards_section):
        self.rewards = {}
        for reward in rewards_section:
            self.rewards[reward.attrib['description']] = int(reward.attrib['reward'])

    def reset(self):
        self.state_vector = (self.board_size * self.board_size) * [0]
        return {'state': self.state_vector}

    # ------------------------------------------ GAME STATE CHECK ----------------------------------------
    def is_win(self):
        if self.check_horizontal():
            return True

        if self.check_vertical():
            return True

        return self.check_diagonal()

    def check_horizontal(self):
        grid = self.state_vector
        cnt = 0
        for i in range(0, self.board_size * self.board_size, self.board_size):
            cnt = 0
            k = i
            for j in range(1, self.board_size):
                (cnt, k) = (cnt + 1, k) if (grid[k] == grid[i + j] and grid[k] != 0) else (0, i + j)
                if cnt == self.win_size - 1:
                    return True

        return False

    def check_vertical(self):
        grid = self.state_vector
        cnt = 0
        for i in range(0, self.board_size):
            cnt = 0
            k = i
            for j in range(self.board_size, self.board_size * self.board_size, self.board_size):
                (cnt, k) = (cnt + 1, k) if (grid[k] == grid[i + j] and grid[k] != 0) else (0, i + j)
                if cnt == self.win_size - 1:
                    return True

        return False

    def check_diagonal(self):
        grid = self.state_vector
        m = self.to_matrix(grid)
        m = numpy.array(m)

        for i in range(self.board_size - self.win_size + 1):
            for j in range(self.board_size - self.win_size + 1):
                sub_matrix = m[i:self.win_size + i, j:self.win_size + j]

                if self.check_matrix(sub_matrix):
                    return True

        return False

    def to_matrix(self, grid):
        m = []
        for i in range(0, self.board_size * self.board_size, self.board_size):
            m.append(grid[i:i + self.board_size])
        return m

    def check_matrix(self, m):
        cnt_primary_diag = 0
        cnt_secondary_diag = 0
        for i in range(self.win_size):
            for j in range(self.win_size):
                if i == j and m[0][0] == m[i][j] and m[0][0] != 0:
                    cnt_primary_diag += 1

                if i + j == self.win_size - 1 and m[0][self.win_size - 1] == m[i][j] and m[0][self.win_size - 1] != 0:
                    cnt_secondary_diag += 1

        return cnt_primary_diag == self.win_size or cnt_secondary_diag == self.win_size

    def is_draw(self):
        for i in range(self.board_size * self.board_size):
            if self.state_vector[i] == 0:
                return False
        return True

    # ------------------------------------------ ACTIONS ----------------------------------------
    def step(self, action_symbol): #action, symbol):
        is_position_already_used = False

        action = action_symbol[0]
        symbol = action_symbol[1]

        if self.state_vector[action] != 0:
            is_position_already_used = True

        if is_position_already_used:
            reward_type = 'bad_position'
            done = False
        else:
            self.state_vector[action] = symbol

            if self.is_win():
                reward_type = 'win'
                done = True
            elif self.is_draw():
                reward_type = 'draw'
                done = True
            else:
                reward_type = 'still_in_game'
                done = False

        return {'state': self.state_vector}, self.rewards[reward_type], done, {'already_used_position': is_position_already_used}

    # ------------------------------------------ DISPLAY ----------------------------------------
    def get_state_vector_to_display(self):
        new_state_vector = []
        for value in self.state_vector:
            if value == 0:
                new_state_vector.append(value)
            else:
                new_state_vector.append(self.symbols[value])
        return new_state_vector

    def print_grid_line(self, grid, offset=0):
        print(" " + "-" * (self.board_size * 4 + 1))
        for i in range(self.board_size):
            if grid[i + offset] == 0:
                print(" | " + " ", end='')
            else:
                print(" | " + str(grid[i + offset]), end='')
        print(" |")

    def display_grid(self, grid):
        for i in range(0, self.board_size * self.board_size, self.board_size):
            self.print_grid_line(grid, i)

        print(" " + "-" * (self.board_size * 4 + 1))
        print()

    def render(self, mode=None, close=False):
        self.display_grid(self.get_state_vector_to_display())

    def close(self):
        return None

    def seed(self, seed=None):
        return [seed]

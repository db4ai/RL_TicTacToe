import numpy as np
import random

board_count = 0

class state_space():
    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.states = {}
        self.boards = []
        self.initialize()

    def initialize(self):
        grid = [0,0,0,0,0,0,0,0,0]
        val = int('0',base=3)
        for i in range(3**9):
            temp_val = val
            for j in range(len(grid)):
                grid[j] = np.mod(temp_val,3)
                temp_val = int(np.floor(temp_val/3))
            val += 1
            self.add_state(grid)

    # Add a state to the state space if it is unique
    def add_state(self, grid):

        # debug_grid = [0,1,2,3,4,5,6,7,8]
        # print("Original grid")
        # self.grid_print(debug_grid)
        # print("Flip horizontal")
        # self.grid_print(self.grid_flip_horizontal(debug_grid))
        # print("Flip vertical")
        # self.grid_print(self.grid_flip_vertical(debug_grid))
        # print("Flip 45")
        # self.grid_print(self.grid_flip_45(debug_grid))
        # print("Flip 225")
        # self.grid_print(self.grid_flip_225(debug_grid))
        # print("Rotate clockwise")
        # self.grid_print(self.grid_rotate_clockwise(debug_grid))
        
        ids = []
        # Normal and mirrors
        ids.append(self.grid_to_string(grid))
        ids.append(self.grid_to_string(self.grid_flip_horizontal(grid)))
        ids.append(self.grid_to_string(self.grid_flip_vertical(grid)))
        ids.append(self.grid_to_string(self.grid_flip_45(grid)))
        ids.append(self.grid_to_string(self.grid_flip_225(grid)))
        # Rotate 90 degreas, add with mirros
        rotated_grid = grid
        for i in range(3):
            rotated_grid = self.grid_rotate_clockwise(rotated_grid)
            ids.append(self.grid_to_string(rotated_grid))

        # Check if any of the keys exist in the board dictionary
        found_board = False
        for id in ids:
            found_board = found_board or (id in self.states)

        # Add the board if it doesn't exist
        if not found_board:
            id = ids[0]
            self.boards.append(grid.copy())  
            self.states[id] = random.uniform(0,1)   
            global board_count 
            board_count += 1
            return True
        return False

    # Get a unique state from the state space
    def get_state(self, id_string):
        grid = [int(i) for i in list(id_string)]

        ids = []
        # Normal and mirrors
        ids.append(self.grid_to_string(grid))
        ids.append(self.grid_to_string(self.grid_flip_horizontal(grid)))
        ids.append(self.grid_to_string(self.grid_flip_vertical(grid)))
        ids.append(self.grid_to_string(self.grid_flip_45(grid)))
        ids.append(self.grid_to_string(self.grid_flip_225(grid)))
        # Rotate 90 degreas, add with mirros
        rotated_grid = grid
        for i in range(3):
            rotated_grid = self.grid_rotate_clockwise(rotated_grid)
            ids.append(self.grid_to_string(rotated_grid))

        # Get the board from the state space, convert ids to a set in case there are duplicates
        state = None
        count = 0
        for id in set(ids):
            if id in self.states: 
                state_value = {'state': id, 'value': self.states[id]}
                count += 1

                # Print an error if there are duplicate states found
                if count > 1: 
                    print(f'DUPLICATE STATE FOUND {grid} <-> {id}')
        
        return state_value

    # convert the grid list to a string
    def grid_to_string(self, grid):
        return (f'{grid[0]}{grid[1]}{grid[2]}'
                f'{grid[3]}{grid[4]}{grid[5]}'
                f'{grid[6]}{grid[7]}{grid[8]}')

    def grid_flip_horizontal(self, grid):
        return [grid[6], grid[7], grid[8],
                grid[3], grid[4], grid[5],
                grid[0], grid[1], grid[2]]

    def grid_flip_vertical(self, grid):
        return [grid[2], grid[1], grid[0],
                grid[5], grid[4], grid[3],
                grid[8], grid[7], grid[6]]
    
    def grid_flip_45(self, grid):
        return [grid[8], grid[5], grid[2],
                grid[7], grid[4], grid[1],
                grid[6], grid[3], grid[0]]

    def grid_flip_225(self,grid):
        new_grid = self.grid_flip_45(grid)
        new_grid = self.grid_rotate_clockwise(new_grid)
        new_grid = self.grid_rotate_clockwise(new_grid)
        return new_grid

    def grid_rotate_clockwise(self, grid):
        return [grid[6], grid[3], grid[0],
                grid[7], grid[4], grid[1],
                grid[8], grid[5], grid[2]]
    
    def grid_print(self, grid):
        print(f'{grid[0]}{grid[1]}{grid[2]}')
        print(f'{grid[3]}{grid[4]}{grid[5]}')
        print(f'{grid[6]}{grid[7]}{grid[8]}')

class TD_Learning():
    def __init__(self, grid_size):
        # Save the parameters
        self.name = "Value Function"
        self.grid_size = grid_size

        # Initialize the history
        self.state_id_history = []
        self.reward_history = []

        # Hyperparameters
        self.alpha = 0.1
        self.gamma = 0.9

        # Create the state space
        self.state_space = state_space(self.grid_size)
        print(f'Number of unique states: {len(self.state_space.states)}')

        state_value = self.get_unique_state('012012012')
        state_value = self.set_state(state_value['state'], 0.5)

        temp = 1

    # Get the unique state from the state space given a string such as '012012012'
    # The given string may not match the unique identifier and the returned dictionary will have the unique id for the given string
    def get_unique_state(self, state_id):
        return self.state_space.get_state(state_id)
    
    # Update the unique state
    # Returns the updated state_value dictionary
    def set_state(self, state_id, value):
        # First make sure the state_id is the unique state id
        state_value = self.get_unique_state(state_id)
        self.state_space.states[state_value['state']] = value
        return self.get_unique_state(state_value['state'])
    
    # Update the value function
    def update(self, state_id, reward):
        # Save the state and reward to the history
        self.state_id_history.append(state_id)
        self.reward_history.append(reward)

        # Get the current unique state
        current_state = self.get_unique_state(state_id)

        # Wait until we have enough history to perform updates
        if len(self.reward_history) > 1:
            update_state_id = self.state_id_history[-2]
            update_state_value = self.get_unique_state(update_state_id)
            update_state_value = update_state_value['value']
            new_value = update_state_value + self.alpha*(reward + self.gamma*current_state['value'] - update_state_value)
            return self.set_state(update_state_value['state'], new_value)
        else:
            return None

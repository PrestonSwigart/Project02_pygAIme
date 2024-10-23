import numpy as np
import random


class QLearningAgent:
    def __init__(self, state_size, action_size):
        self.state_size = state_size
        self.action_size = action_size
        self.q_table = np.zeros((state_size, action_size))
        self.learning_rate = 0.1
        self.discount_factor = 0.95
        self.exploration_rate = 1.0
        self.exploration_decay = 0.995
        self.min_exploration_rate = 0.01

    def discretize_state(self, height, obs1_x, obs2_x, obs3_x):
        index = max(0, min(obs1_x, obs2_x, obs3_x))

        # Cap index to ensure it doesn't exceed state_size
        index = min(index, self.state_size - 1)

        return index

    def choose_action(self, state):
        if random.uniform(0, 1) < self.exploration_rate:
            return random.randint(0, self.action_size - 1)  # Explore
        else:
            return np.argmax(self.q_table[state])  # Exploit

    def update(self, state, action, reward, next_state):
        # Convert states to integer indices
        state_index = int(state)
        next_state_index = int(next_state)

        # Ensure the indices are within bounds
        if state_index < 0 or state_index >= self.q_table.shape[0]:
            raise IndexError(f"State index out of bounds: {state_index}")
        if next_state_index < 0 or next_state_index >= self.q_table.shape[0]:
            raise IndexError(f"Next state index out of bounds: {next_state_index}")

        # Perform Q-learning update
        best_next_action = np.argmax(self.q_table[next_state_index])
        target = reward + self.discount_factor * self.q_table[next_state_index][best_next_action]
        self.q_table[state_index][action] += self.learning_rate * (target - self.q_table[state_index][action])

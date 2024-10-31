import numpy as np


class QLearningAgent:
    def __init__(self):
        self.q_table = np.zeros(([2000, 2000, 2000]))
        self.exploration_decay = 0.99975
        self.epsilon = 1
        self.learning_rate = 0.9
        self.discount_factor = 0.9

    #yeah
    def get_next_action(self, state1, state2, state3):
        # if a randomly chosen value between 0 and 1 is less than epsilon,
        # then choose the most promising value from the Q-table for this state. (thanks random website)
        self.epsilon *= self.exploration_decay
        if np.random.random() > self.epsilon:
            return np.argmax(self.q_table[state1, state2, state3])
        else:
            return np.random.randint(3)


    #bad method that returns the closest object that isnt behind
    def nearestObject(self, obs1_x, obs2_x, obs3_x):
        # if the nearest object is too close
        if max(0, min(obs1_x, obs2_x, obs3_x)) == 0:
            if obs1_x <= 0 and obs2_x <= 0:
                return max(0, int(obs3_x)) - ((max(0, int(obs3_x))) % 5)
            elif obs2_x <= 0 and obs3_x <= 0:
                return max(0, int(obs1_x)) - ((max(0, int(obs1_x))) % 5)
            elif obs1_x <= 0 and obs3_x <= 0:
                return max(0, int(obs2_x)) - ((max(0, int(obs2_x))) % 5)
            elif obs1_x <= 0:
                return int(max(0, min(obs2_x, obs3_x))) - ((int(max(0, min(obs2_x, obs3_x)))) % 5)
            elif obs2_x <= 0:
                return int(max(0, min(obs1_x, obs3_x))) - ((int(max(0, min(obs1_x, obs3_x)))) % 5)
            elif obs3_x <= 0:
                return int(max(0, min(obs1_x, obs2_x))) - ((int(max(0, min(obs1_x, obs2_x)))) % 5)
            else:
                return 0
        else:
            return min(obs1_x, obs2_x, obs3_x) - min(obs1_x, obs2_x, obs3_x) % 5

    #update AI
    def update(self, state, action, reward, next_state):
        best_next_action = np.argmax(self.q_table[next_state])
        target = reward + self.discount_factor * self.q_table[next_state][best_next_action]
        self.q_table[state][action] += self.learning_rate * (target - self.q_table[state][action])

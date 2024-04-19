import random
from collections import deque
import torch
import torch.nn as nn


ACTIONS = 21  # total available action number


class BrainDQN(nn.Module):

    def __init__(self, mem_size, epsilon):
        super(BrainDQN, self).__init__()

        self.train = None
        self.replay_memory = deque()
        self.actions = ACTIONS
        self.mem_size = mem_size
        self.epsilon = epsilon

        self.DQN = nn.Sequential(
            nn.Linear(25, 64), nn.ReLU(),
            nn.Linear(64, 128), nn.ReLU(),
            nn.Linear(128, 256), nn.ReLU(),
            nn.Linear(256, 512), nn.ReLU(),
            nn.Linear(512, 256), nn.ReLU(),
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, self.actions)
        )

    def forward(self, o):
        q = self.DQN(o)
        return q

    def set_train(self):
        self.train = True

    def set_eval(self):
        self.train = False

    def store_transition(self, current_state, next_state, action_, reward):
        self.replay_memory.append((current_state, action_, reward, next_state))
        if len(self.replay_memory) > self.mem_size:
            self.replay_memory.popleft()

    def get_action_randomly(self):
        action_index = random.randrange(self.actions)
        return action_index

    def get_optim_action(self, current_state):
        state_var = current_state.unsqueeze(0)
        q_value = self.forward(state_var)
        _, action_index = torch.max(q_value, dim=1)
        action_index = action_index.item()
        return action_index

    def get_action(self, current_state):
        if self.train and random.random() <= self.epsilon:
            return self.get_action_randomly()
        return self.get_optim_action(current_state)



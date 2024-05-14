from collections import deque
import torch
import torch.nn as nn
from torch.distributions import Categorical


class ActorCritic(nn.Module):
    def __init__(self):
        super(ActorCritic, self).__init__()

        self.replay_memory = deque()

        self.critic = nn.Sequential(
            nn.Linear(25, 64), nn.ReLU(),
            nn.Linear(64, 128), nn.ReLU(),
            nn.Linear(128, 256), nn.ReLU(),
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 1)
        )

        self.actor = nn.Sequential(
            nn.Linear(25, 64), nn.ReLU(),
            nn.Linear(64, 128), nn.ReLU(),
            nn.Linear(128, 256), nn.ReLU(),
            nn.Linear(256, 256), nn.ReLU(),
            nn.Linear(256, 128), nn.ReLU(),
            nn.Linear(128, 64), nn.ReLU(),
            nn.Linear(64, 21), nn.Softmax(dim=1)
        )

    def get_policy(self, x):
        probs = self.actor(x)
        dist = Categorical(probs)
        return dist

    def get_action_for_test(self, x):
        y = self.actor(x)
        action = torch.argmax(y, dim=1)

        return action.item()

    def get_value(self, x):
        return self.critic(x)




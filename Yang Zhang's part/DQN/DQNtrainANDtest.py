import torch.optim as optim
from Configuration.env import *
import matplotlib.pyplot as plt
from DQN import *

load = False


def train_dqn():
    dqn_train = BrainDQN(5000, 0.1)
    dqn_train = dqn_train.cuda()
    dqn_target = BrainDQN(5000, 0.1)
    dqn_target = dqn_target.cuda()

    share_simulator = Simulator()
    share_simulator.set_initial_state()

    if load:
        filename = 'checkpoint-round-600.pth.tar'  # 1
        print('load previous model weight: {}'.format(filename))
        checkpoint = torch.load(filename)
        dqn_train.DQN.load_state_dict(checkpoint["state_dict_DQN"])

    optimizer = optim.RMSprop(dqn_train.parameters(), lr=5e-4)
    criterion = nn.MSELoss()

    for i in range(1, 201):
        current_state = share_simulator.current_state
        current_state = current_state.cuda()

        action_index = dqn_train.get_action_randomly()
        estimated_next_state = share_simulator.get_next_state(action_index, current_state.to("cpu")).cuda()
        reward = torch.tensor([share_simulator.get_reward()]).cuda()

        action = torch.zeros(21).cuda()
        action[action_index] = 1
        dqn_train.store_transition(current_state.unsqueeze(0), estimated_next_state.unsqueeze(0), action.unsqueeze(0),
                                   reward)
    # start training

    total_R = []
    Final_profit = []
    max_R = 0

    print("Staring training")
    for episode in range(1, 601):
        share_simulator.set_initial_state()
        r_s = 0

        for i in range(1, 201):
            current_state = share_simulator.current_state
            current_state = current_state.cuda()

            action_index = dqn_train.get_action(current_state)
            estimated_next_state = share_simulator.get_next_state(action_index, current_state.to("cpu")).cuda()
            reward = share_simulator.get_reward()
            r_s += reward
            reward = torch.tensor([reward]).cuda()

            action = torch.zeros(21).cuda()
            action[action_index] = 1
            dqn_train.store_transition(current_state.unsqueeze(0), estimated_next_state.unsqueeze(0),
                                       action.unsqueeze(0), reward)

            minibatch = random.sample(dqn_train.replay_memory, 4)
            state_batch = torch.cat([data[0] for data in minibatch])
            action_batch = torch.cat([data[1] for data in minibatch])
            reward_batch = torch.cat([torch.tensor([data[2]]) for data in minibatch])
            next_state_batch = torch.cat([data[3] for data in minibatch])

            q_value_next = dqn_target.forward(next_state_batch)
            q_value = dqn_train.forward(state_batch)
            max_q, _ = torch.max(q_value_next, dim=1)

            for i in range(4):
                reward_batch[i] += 0.99 * max_q[i].item()
            q_value = torch.sum(torch.mul(action_batch, q_value), dim=1)

            y = reward_batch.cuda()
            loss = criterion(q_value, y)

            optimizer.zero_grad()

            loss.backward()
            optimizer.step()

        total_R.append(r_s)
        Final_profit.append(share_simulator.total_money - 5000)

        print(f"Total reward in {episode} episode th is {r_s}")

        if r_s > max_R:
            max_R = r_s
            save_checkpoint({
                'episode': episode,
                'state_dict_DQN': dqn_train.DQN.state_dict(),
                'max_R_so_far': r_s,
                "epsilon": dqn_train.epsilon,
            }, True, 'best_so_far_dqn-episode-%d.pth.tar' % episode)

            print(f'save checkpoint, episode = {episode}, max_R = {max_R}')

        if episode % 20 == 0:
            dqn_train.load_state_dict(dqn_target.state_dict())

    x = range(len(total_R))

    fig, axs = plt.subplots(2, 1, figsize=(14, 10))

    max_total_R = max(total_R)
    max_total_R_index = total_R.index(max_total_R)
    axs[0].plot(x, total_R, marker='s', linestyle='-', color='b', label='Total reward')
    axs[0].axvline(x=max_total_R_index, color='g', linestyle='--')
    axs[0].text(max_total_R_index, max_total_R, f'({max_total_R_index}, {max_total_R})', color='g')
    axs[0].set_title('Total reward')
    axs[0].set_xlabel('Episode')
    axs[0].set_ylabel('Total reward in each episode')
    axs[0].legend()
    axs[0].grid(True)

    max_Final_profit = max(Final_profit)
    max_Final_profit_index = Final_profit.index(max_Final_profit)
    axs[1].plot(x, Final_profit, marker='o', linestyle='-', color='r', label='Final profit')
    axs[1].axvline(x=max_Final_profit_index, color='g', linestyle='--')
    axs[1].text(max_Final_profit_index, max_Final_profit, f'({max_Final_profit_index}, {max_Final_profit})', color='g')
    axs[1].axhline(y=0, color='y', linestyle='-')
    axs[1].set_title('Profit')
    axs[1].set_xlabel('Episode')
    axs[1].set_ylabel('Final profit in each episode')
    axs[1].legend()
    axs[1].grid(True)

    plt.tight_layout()
    plt.show()


def test():
    dqn_agent = BrainDQN(5000, -1)
    dqn_agent = dqn_agent.cuda()
    share_simulator = Simulator()
    filename = 'best_so_far_dqn-episode-363.pth.tar'
    print('load previous model weight: {}'.format(filename))
    checkpoint = torch.load(filename)
    dqn_agent.DQN.load_state_dict(checkpoint["state_dict_DQN"])

    Final_profit = []
    for episode in range(1, 101):

        share_simulator.set_initial_state()

        for i in range(1, 201):
            current_state = share_simulator.current_state
            current_state = current_state.cuda()

            action_index = dqn_agent.get_action(current_state)
            estimated_next_state = share_simulator.get_next_state(action_index, current_state.to("cpu")).cuda()
            reward = share_simulator.get_reward()

        fp = share_simulator.total_money - 5000

        Final_profit.append(fp)

        print(f"Final profit in {episode} th is {fp}")

    profit_time = 0
    for i in Final_profit:
        if i > 0:
            profit_time += 1

    print(profit_time, sum(Final_profit) / len(Final_profit))


if __name__ == '__main__':
    test()

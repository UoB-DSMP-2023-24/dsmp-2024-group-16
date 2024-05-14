from A2C import ActorCritic
import torch.optim as optim
from Configuration.env import *
import matplotlib.pyplot as plt

load = False


def train():
    a2c_agent = ActorCritic()
    a2c_agent = a2c_agent.cuda()
    share_simulator = Simulator()

    if load:
        filename = 'checkpoint-round-600.pth.tar'  # 1
        print('load previous model weight: {}'.format(filename))
        checkpoint = torch.load(filename)
        a2c_agent.actor.load_state_dict(checkpoint["state_dict_actor"])
        a2c_agent.critic.load_state_dict(checkpoint["state_dict_critic"])

    actor_optimizer = optim.Adam(a2c_agent.actor.parameters(), lr=5e-4)
    critic_optimizer = optim.Adam(a2c_agent.critic.parameters(), lr=5e-4)

    values = []
    estimated_values = []

    for j in range(40):
        share_simulator.set_initial_state()

        for i in range(1, 201):
            current_state = share_simulator.current_state
            current_state = current_state.cuda()
            current_state = current_state.unsqueeze(0)

            dist = a2c_agent.get_policy(current_state)

            action = dist.sample()
            value = a2c_agent.get_value(current_state).squeeze(0)
            estimated_next_state = share_simulator.get_next_state(action.item(), current_state.squeeze(0).to("cpu"))
            estimated_next_state = estimated_next_state.unsqueeze(0).cuda()
            reward = share_simulator.get_reward()

            values.append(value)
            estimated_value = torch.tensor([reward]).cuda() + a2c_agent.get_value(estimated_next_state).squeeze(0)

            estimated_values.append(estimated_value)

        values_t = torch.cat(values)
        estimated_values_t = torch.cat(estimated_values)
        advantage = estimated_values_t - values_t

        critic_loss = advantage.pow(2).mean()

        print("critic loss is ", critic_loss.item())

        critic_optimizer.zero_grad()
        critic_loss.backward()
        critic_optimizer.step()

        values = []
        estimated_values = []

    log_probs = []
    entropy = []

    total_R = []
    Final_profit = []

    max_R = 0

    print("Staring training")
    for episode in range(1, 601):

        share_simulator.set_initial_state()

        r_s = []

        for i in range(1, 201):
            current_state = share_simulator.current_state
            current_state = current_state.cuda()
            current_state = current_state.unsqueeze(0)

            dist = a2c_agent.get_policy(current_state)

            action = dist.sample()

            i_log_prob = dist.log_prob(action)
            value = a2c_agent.get_value(current_state).squeeze(0)

            log_probs.append(i_log_prob)
            entropy.append(dist.entropy())
            values.append(value)

            estimated_next_state = share_simulator.get_next_state(action.item(), current_state.squeeze(0).to("cpu"))

            estimated_next_state = estimated_next_state.unsqueeze(0).cuda()

            reward = share_simulator.get_reward()
            r_s.append(reward)
            print(
                f"Action is {action.item()} for {i} th state in the {episode} th episode.Profit is {share_simulator.total_money - 5000}. Share number is {share_simulator.share_number}")

            estimated_value = torch.tensor([reward]).cuda() + a2c_agent.get_value(estimated_next_state).squeeze(0)

            estimated_values.append(estimated_value)

        R = sum(r_s)
        total_R.append(R)

        Final_profit.append(share_simulator.total_money - 5000)

        print(f"Total reward in {episode} th is {R}")

        if R > max_R:
            max_R = R
            save_checkpoint({
                'episode': episode,
                'state_dict_actor': a2c_agent.actor.state_dict(),
                'state_dict_critic': a2c_agent.critic.state_dict(),
                'max_R_so_far': R,
            }, True, 'best_so_far-episode-%d.pth.tar' % episode)

            print(f'save checkpoint, episode = {episode}, max_R = {max_R}')

        if episode % 20 == 0:
            log_probs_t = torch.cat(log_probs)
            entropy_t = torch.cat(entropy)
            values_t = torch.cat(values)
            estimated_values_t = torch.cat(estimated_values)

            advantage = estimated_values_t - values_t

            actor_loss = (-(advantage.detach() * log_probs_t)).sum() / 20 - entropy_t.mean()
            critic_loss = advantage.pow(2).mean()

            actor_optimizer.zero_grad()

            actor_loss.backward()
            actor_optimizer.step()

            critic_optimizer.zero_grad()
            critic_loss.backward()
            critic_optimizer.step()

            log_probs = []
            entropy = []
            values = []
            estimated_values = []

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

    plt.savefig('train_result.png')


def test():
    a2c_agent = ActorCritic()
    a2c_agent = a2c_agent.cuda()
    share_simulator = Simulator()
    filename = 'best_so_far-episode-94.pth.tar'
    print('load previous model weight: {}'.format(filename))
    checkpoint = torch.load(filename)
    a2c_agent.actor.load_state_dict(checkpoint["state_dict_actor"])
    a2c_agent.critic.load_state_dict(checkpoint["state_dict_critic"])

    Final_profit = []
    for episode in range(1, 101):

        share_simulator.set_initial_state()

        for i in range(1, 201):
            current_state = share_simulator.current_state
            current_state = current_state.cuda()
            current_state = current_state.unsqueeze(0)
            action = a2c_agent.get_action_for_test(current_state)
            estimated_next_state = share_simulator.get_next_state(action, current_state.squeeze(0).to("cpu"))

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

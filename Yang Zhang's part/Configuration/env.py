from .utils import *
import random


def generate_orders(min_price, max_price):
    prices = random.sample(range(min_price, max_price), 4)
    for i in range(4):
        for j in range(3):
            if prices[j] > prices[j + 1]:
                temp = prices[j]
                prices[j] = prices[j + 1]
                prices[j + 1] = temp

    nums = [random.randint(1, 5) for _ in range(4)]

    orders = []
    for price, num in zip(prices, nums):
        orders.append(price)
        orders.append(num)
    return orders


def modify_state_market_helper(mode, order_num, start_index, end_index, processed_data):
    total_cost = torch.tensor([0]).float()

    if mode == "sell":
        while order_num != 0:

            if order_num >= processed_data[end_index]:

                total_cost += processed_data[end_index] * processed_data[end_index - 1]
                order_num -= processed_data[end_index]
                processed_data[end_index] = 0

            else:
                total_cost += order_num * processed_data[end_index - 1]
                processed_data[end_index] -= order_num
                order_num = 0

            end_index -= 2

    else:
        while order_num != 0:

            if order_num >= processed_data[start_index]:
                total_cost += processed_data[start_index] * processed_data[start_index - 1]
                order_num -= processed_data[start_index]
                processed_data[start_index] = 0

            else:
                total_cost += order_num * processed_data[start_index - 1]
                processed_data[start_index] -= order_num
                order_num = 0

            start_index += 2

    return processed_data, total_cost.item()


def modify_state_market_order(mode, order_num, processed_data):
    if mode == "sell":
        return modify_state_market_helper(mode, order_num, 3, 9, processed_data)
    else:
        return modify_state_market_helper(mode, order_num, 12, 18, processed_data)


def modify_state_from_action(action, pro_data):
    if action == 0:  # agent performs one market sell order
        return modify_state_market_order("sell", 1, pro_data)

    elif action == 1:  # agent performs two market sell orders
        return modify_state_market_order("sell", 2, pro_data)

    elif action == 2:  # agent performs three market sell orders
        return modify_state_market_order("sell", 3, pro_data)

    elif action == 3:  # agent performs four market sell orders
        return modify_state_market_order("sell", 4, pro_data)

    elif action == 4:  # agent performs five market sell orders
        return modify_state_market_order("sell", 5, pro_data)

    elif action == 5:  # agent performs one market buy order
        return modify_state_market_order("buy", 1, pro_data)

    elif action == 6:  # agent performs two market buy orders
        return modify_state_market_order("buy", 2, pro_data)

    elif action == 7:  # agent performs three market buy orders
        return modify_state_market_order("buy", 3, pro_data)

    elif action == 8:  # agent performs four market buy orders
        return modify_state_market_order("buy", 4, pro_data)

    elif action == 9:  # agent performs five market buy orders
        return modify_state_market_order("buy", 5, pro_data)

    elif action == 10:  # agent performs one limit sell order
        return modify_state_limit_order("sell", 1, pro_data)

    elif action == 11:  # agent performs two limit sell orders
        return modify_state_limit_order("sell", 2, pro_data)

    elif action == 12:  # agent performs three limit sell orders
        return modify_state_limit_order("sell", 3, pro_data)

    elif action == 13:  # agent performs four limit sell orders
        return modify_state_limit_order("sell", 4, pro_data)

    elif action == 14:  # agent performs five limit sell orders
        return modify_state_limit_order("sell", 5, pro_data)

    elif action == 15:  # agent performs one limit buy order
        return modify_state_limit_order("buy", 1, pro_data)

    elif action == 16:  # agent performs two limit buy orders
        return modify_state_limit_order("buy", 2, pro_data)

    elif action == 17:  # agent performs three limit buy orders
        return modify_state_limit_order("buy", 3, pro_data)

    elif action == 18:  # agent performs four limit buy orders
        return modify_state_limit_order("buy", 4, pro_data)

    elif action == 19:  # agent performs five limit buy orders
        return modify_state_limit_order("buy", 5, pro_data)

    else:
        return pro_data, 0, 0  # agent does nothing


def modify_state_limit_order(mode, order_num, processed_data):
    if mode == "sell":
        processed_data[12] += order_num
    else:
        processed_data[9] += order_num

    return processed_data, 0


def get_start_state():
    buy_orders = generate_orders(100, 300)
    sell_orders = generate_orders(400, 600)
    start_state = [0.1, 1] + buy_orders + [0] + sell_orders + [0, 0, 0, 1, 1, 1]
    start_state = torch.tensor(start_state)

    return start_state


def available_sum(start_index, end_index, pro_data):
    available_num = 0
    while start_index <= end_index:
        available_num += pro_data[start_index]
        start_index += 2
    return available_num


class Simulator:
    def __init__(self):
        self.current_state = None
        self.total_money = 5000
        self.share_number = 0

        self.limit_buy = 0
        self.limit_sell = 0

        self.delta_profit = 0

        self.delta_buy = 0
        self.delta_sell = 0

        self.reasonable1 = False
        self.reasonable2 = False
        self.reasonable3 = False

    def set_initial_state(self):
        self.current_state = get_start_state()
        self.total_money = 5000
        self.share_number = 0

        self.limit_buy = 0
        self.limit_sell = 0

    def triple_check(self, action, current_state):
        reasonable1 = True
        reasonable2 = True
        reasonable3 = True

        if 0 <= action <= 4:
            order_num = action + 1
            if self.share_number < order_num:
                order_num = self.share_number
                reasonable1 = False

                feasible = self.share_number - self.limit_sell
                if order_num > feasible:
                    reasonable3 = False
                    order_num = feasible

                    available_num = available_sum(3, 9, current_state)
                    if order_num > available_num:
                        order_num = available_num
                        reasonable2 = False
                else:
                    available_num = available_sum(3, 9, current_state)
                    if order_num > available_num:
                        order_num = available_num
                        reasonable2 = False

            else:
                feasible = self.share_number - self.limit_sell
                if order_num > feasible:
                    reasonable3 = False
                    order_num = feasible

                    available_num = available_sum(3, 9, current_state)
                    if order_num > available_num:
                        order_num = available_num
                        reasonable2 = False
                else:
                    available_num = available_sum(3, 9, current_state)
                    if order_num > available_num:
                        order_num = available_num
                        reasonable2 = False

        elif 5 <= action <= 9:
            order_num = action - 4
            available_num = available_sum(12, 18, current_state)
            if order_num > available_num:
                order_num = available_num
                reasonable2 = False

        elif 15 <= action <= 19:
            order_num = action - 14

        elif action == 20:
            order_num = 0
        else:
            order_num = action - 9
            if self.share_number < order_num:
                order_num = self.share_number
                reasonable1 = False
                feasible = self.share_number - self.limit_sell
                if order_num > feasible:
                    reasonable3 = False
                    order_num = feasible
            else:
                feasible = self.share_number - self.limit_sell
                if order_num > feasible:
                    reasonable3 = False
                    order_num = feasible

        return reasonable1, reasonable2, reasonable3, order_num

    def get_next_state(self, action, pro_data):

        reasonable1, reasonable2, reasonable3 , order_num = self.triple_check(action, pro_data)

        self.reasonable1 = reasonable1
        self.reasonable2 = reasonable2
        self.reasonable3 = reasonable3

        if 0 <= action <= 4:
            modified_state, total_cost = modify_state_market_order("sell", order_num, pro_data)
        elif 5 <= action <= 9:
            modified_state, total_cost = modify_state_market_order("buy", order_num, pro_data)
        elif 10 <= action <= 14:
            modified_state, total_cost = modify_state_limit_order("sell", order_num, pro_data)
        elif 15 <= action <= 19:
            modified_state, total_cost = modify_state_limit_order("buy", order_num, pro_data)
        else:
            modified_state, total_cost = pro_data, 0

        temp_money = self.total_money

        if 0 <= action <= 4:
            self.total_money += total_cost
            self.share_number -= order_num

            if self.limit_buy > 0:
                if order_num <= self.limit_buy:
                    self.total_money -= order_num * modified_state[8]
                    self.limit_buy -= order_num
                    self.delta_buy = -1 * order_num
                    self.share_number += order_num

                else:
                    self.total_money -= self.limit_buy * modified_state[8]
                    self.delta_buy = -1 * self.limit_buy
                    self.limit_buy = 0
                    self.share_number += self.limit_buy

        elif 5 <= action <= 9:
            self.total_money -= total_cost
            self.share_number += order_num

            if self.limit_sell > 0:
                if order_num <= self.limit_sell:
                    self.total_money += order_num * modified_state[11]
                    self.limit_sell -= order_num
                    self.delta_sell = -1 * order_num
                    self.share_number -= order_num

                else:
                    self.total_money += self.limit_buy * modified_state[11]
                    self.delta_sell = -1 * self.limit_sell
                    self.limit_sell = 0
                    self.share_number -= self.limit_sell

        elif 10 <= action <= 14:
            self.limit_sell += order_num
            self.delta_sell = order_num

        elif 15 <= action <= 19:
            self.limit_buy += order_num
            self.delta_buy = order_num

        # randomization as other people

        # direction of buying:
        num_zero_buy = 0
        start_end_index = 9
        while modified_state[start_end_index] == 0:
            num_zero_buy += 1
            start_end_index -= 2

        # other people perform limit buy orders
        if num_zero_buy > 0:
            if num_zero_buy == 4:
                prices = random.sample(range(100, 300), num_zero_buy)
            else:
                prices = random.sample(range(int(modified_state[start_end_index - 1].item() + 1), 300), num_zero_buy)
            nums = [random.randint(1, 5) for _ in range(num_zero_buy)]

            buy_dic = {price: num for price, num in zip(prices, nums)}

            while start_end_index >= 3:
                buy_dic[modified_state[start_end_index - 1].item()] = modified_state[start_end_index].item()
                start_end_index -= 2

            sorted_prices = sorted(buy_dic.keys())

            for j in range(2, 10, 2):
                modified_state[j] = sorted_prices[j // 2 - 1]
                modified_state[j + 1] = buy_dic[sorted_prices[j // 2 - 1]]

        # other people perform market sell orders or more limit buy orders
        else:
            random_number = random.randint(-5, 5)

            if random_number >= 0:
                modified_state[9] = modified_state[9] + random_number

            else:
                mso = -1 * random_number
                if mso >= modified_state[9].item():
                    modified_state[9] = 0
                    if self.limit_buy != 0:
                        self.total_money -= self.limit_buy * modified_state[8].item()
                        self.share_number += self.limit_buy
                        self.limit_buy = 0

                else:
                    modified_state[9] = modified_state[9] - mso

                    if mso >= self.limit_buy:
                        self.total_money -= self.limit_buy * modified_state[8].item()
                        self.share_number += self.limit_buy
                        self.limit_buy = 0
                    else:
                        self.total_money -= mso * modified_state[8].item()
                        self.share_number += mso
                        self.limit_buy -= mso

        # direction of selling:
        num_zero_sell = 0
        start_end_index1 = 12
        while start_end_index1 < 19 and modified_state[start_end_index1] == 0:
            num_zero_sell += 1
            start_end_index1 += 2

        # other people perform limit sell orders
        if num_zero_sell > 0:
            if num_zero_sell == 4:
                prices1 = random.sample(range(400, 600), num_zero_sell)
            else:
                prices1 = random.sample(range(400, int(modified_state[start_end_index1 - 1].item())), num_zero_sell)
            nums1 = [random.randint(1, 5) for _ in range(num_zero_sell)]

            sell_dic = {price: num for price, num in zip(prices1, nums1)}

            while start_end_index1 <= 18:
                sell_dic[modified_state[start_end_index1 - 1].item()] = modified_state[start_end_index1].item()
                start_end_index1 += 2

            sorted_prices1 = sorted(sell_dic.keys())

            for j in range(12, 20, 2):
                modified_state[j - 1] = sorted_prices1[j // 2 - 6]
                modified_state[j] = sell_dic[sorted_prices1[j // 2 - 6]]

        # other people perform market buy orders or more limit sell orders
        else:
            random_number1 = random.randint(-5, 5)

            if random_number1 >= 0:
                modified_state[12] = modified_state[12] + random_number1

            else:
                mbo = -1 * random_number1

                if mbo >= modified_state[12].item():
                    modified_state[12] = 0
                    if self.limit_sell != 0:
                        self.total_money += self.limit_sell * modified_state[11].item()
                        self.share_number -= self.limit_sell
                        self.limit_sell = 0

                else:
                    modified_state[12] = modified_state[12] - mbo

                    if mbo >= self.limit_sell:
                        self.total_money += self.limit_sell * modified_state[11].item()
                        self.share_number -= self.limit_sell
                        self.limit_sell = 0
                    else:
                        self.total_money += mbo * modified_state[11].item()
                        self.share_number -= mbo
                        self.limit_sell -= mbo

        modified_state[0] = modified_state[0] + 0.1
        modified_state[19] = self.share_number
        modified_state[20] = self.limit_sell
        modified_state[21] = self.limit_buy
        modified_state[22] = self.total_money / 5000

        self.delta_profit = self.total_money - temp_money

        if self.reasonable1:
            modified_state[23] = 1
        else:
            modified_state[23] = -1

        if self.reasonable2:
            modified_state[24] = 1
        else:
            modified_state[24] = -1

        self.current_state = modified_state

        return modified_state

    def get_reward(self):
        reward = 0
        if not self.reasonable1:
            reward -= 10

        if not self.reasonable2:
            reward -= 1.5

        if not self.reasonable3:
            reward -= 3.0

        profit = self.total_money - 5000

        setting = 0.05 * self.delta_buy + self.delta_sell + 0.001 * self.delta_profit + 0.0001 * profit

        reward += setting

        self.delta_sell = 0
        self.delta_buy = 0
        self.delta_profit = 0
        return reward

import re
import shutil
import numpy as np
import torch
import torch as t


def read_file(file_path):
    raw_datas = []
    with open(file_path, 'r') as f:
        for line in f:
            raw_datas.append(line)

    return raw_datas


def pre_process(raw_data):
    processed_data = raw_data.replace(" Exch0,", "")
    processed_data = re.sub(r'[\[\]"\',]', '', processed_data)
    processed_data = processed_data.replace("bid", "1")
    processed_data = processed_data.replace("ask", "0")
    processed_data = processed_data.replace("\n", "")
    processed_list = processed_data.split(" ")
    processed_list = [item for item in processed_list if item != '']
    processed_list = [float(item) for item in processed_list]
    if processed_list[0] == 0:
        processed_list[0] = 0.001
    padding_list = np.zeros(83)
    zero_index = -1

    buy_start_point = 2
    sell_start_point = 43

    for i in range(len(processed_list)):
        if processed_list[i] == 0:
            zero_index = i
            break

    copy_zero_index = zero_index

    while zero_index != 2:
        padding_list[buy_start_point] = processed_list[zero_index - 2]
        padding_list[buy_start_point + 1] = processed_list[zero_index - 1]
        zero_index -= 2
        buy_start_point += 2

    sell_order_end = len(processed_list)

    while sell_order_end != copy_zero_index + 1:
        padding_list[sell_start_point] = processed_list[sell_order_end - 2]
        padding_list[sell_start_point + 1] = processed_list[sell_order_end - 1]
        sell_order_end -= 2
        sell_start_point += 2

    padding_list[0] = processed_list[0]
    padding_list[1] = processed_list[1]

    return t.from_numpy(padding_list).float()


def save_checkpoint(state, is_best, filename='checkpoint.pth.tar'):
    """Save checkpoint model to disk

        state -- checkpoint state: model weight and other info
                 binding by user
        is_best -- if the checkpoint is the best. If it is, then
                   save as the best model
    """
    torch.save(state, filename)
    if is_best:
        shutil.copyfile(filename, 'model_best.pth.tar')



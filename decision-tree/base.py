import operator
from math import log


def is_all_sample_same(data_set):
    """
    检查data_set中的样本在lables上的取值都相同
    那如何比较连续特征的值呢
    :param data_set:
    :return:
    """
    for i in range(len(data_set) - 1):
        # 将sample中最后的分类结果去掉，只比较labels上的值是否完全一致
        sample1 = data_set[i][:-1]
        sample2 = data_set[i + 1][:-1]
        result = operator.eq(sample1, sample2)
        if result is False:
            return result
    return True


def get_most_common_class(data_set):
    """
    获取样本中个数最多的类
    这里的类指的是最后的分类结果，如好瓜、坏瓜
    :param data_set:
    :return:
    """
    class_counts = {}
    for sample in data_set:
        current_class = sample[-1]
        if current_class not in class_counts.keys():
            class_counts[current_class] = 0
        class_counts[current_class] += 1
    sorted_class_count = sorted(class_counts.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_class_count[0][0]


def split_data_set_by_operate(data_set, col, value, operate, delete_col):
    """
    按照data set中某一列的值，对数据进行划分，划分成几个子集
    :param data_set:
    :param col:
    :param value:
    :param operate:
    :param delete_col:
    :return:
    """
    new_data_set = []
    for sample in data_set:
        if delete_col is True:
            if operate(sample[col], value):
                new_sample = sample[:col]
                new_sample.extend(sample[col+1:])
                new_data_set.append(new_sample)
        else:
            if operate(sample[col], value):
                new_data_set.append(sample)
    return new_data_set


def calculate_gini(data_set):
    num_entries = len(data_set)
    class_count = {}
    for sample in data_set:
        current_class = sample[-1]
        if current_class not in class_count.keys():
            class_count[current_class] = 0
        class_count[current_class] += 1
    gini = 1.0
    for key in class_count:
        prob = float(class_count[key]/num_entries)
        gini -= prob*prob
    return gini


def calculate_information_entropy(data_set):
    """
    按照data_set中的结果分类来计算熵，如结果只有两类：好瓜与坏瓜
    :param data_set:
    :return:
    """
    num_entries = len(data_set)
    class_counts = {}
    # 先分别计算所有各个分类的个数
    for sample in data_set:
        current_class = sample[-1]
        if current_class not in class_counts.keys():
            class_counts[current_class] = 0
        class_counts[current_class] += 1
    entropy = 0.0
    # 根据个数，计算频率，得到熵
    for key in class_counts:
        prob = float(class_counts[key]) / num_entries
        entropy -= prob * log(prob, 2)
    return entropy
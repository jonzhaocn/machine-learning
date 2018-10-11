from math import log
import operator
import treePlotter

"""
周志华《机器学习》第四章中的习题4.3 code
实现基于信息熵进行划分选择的决策树算法
"""


def create_data_set():
    """
    色泽-》 0：青绿 | 1：乌黑 | 2：浅白
    根蒂-》 0：蜷缩 | 1：稍缩 | 2：硬挺
    敲声-》 0：浊响 | 1：沉闷 | 2：清脆
    纹理-》 0：清晰 | 1：稍糊 | 2：模糊
    脐部-》 0：凹陷 | 1：稍凹 | 2：平坦
    触感-》 0：硬滑 | 1：软粘
    密度-》 是一个连续值
    含糖量-》 是一个连续值

    结果-》 好瓜：Y | 坏瓜：N

    data_set = [[0, 0, 0, 0, 0, 0, 0.697, 0.460, 'Y'],
                [1, 0, 1, 0, 0, 0, 0.774, 0.376, 'Y'],
                [1, 0, 0, 0, 0, 0, 0.634, 0.264, 'Y'],
                [0, 0, 1, 0, 0, 0, 0.608, 0.318, 'Y'],
                [2, 0, 0, 0, 0, 0, 0.556, 0.215, 'Y'],
                [0, 1, 0, 0, 1, 1, 0.403, 0.237, 'Y'],
                [1, 1, 0, 1, 1, 1, 0.481, 0.149, 'Y'],
                [1, 1, 0, 0, 1, 0, 0.437, 0.211, 'Y'],
                [1, 1, 1, 1, 1, 0, 0.666, 0.091, 'N'],
                [0, 2, 2, 0, 2, 1, 0.243, 0.267, 'N'],
                [2, 2, 2, 2, 2, 0, 0.245, 0.057, 'N'],
                [2, 0, 0, 2, 2, 1, 0.343, 0.099, 'N'],
                [0, 1, 0, 1, 0, 0, 0.639, 0.161, 'N'],
                [2, 1, 1, 1, 0, 0, 0.657, 0.198, 'N'],
                [1, 1, 0, 0, 1, 1, 0.360, 0.370, 'N'],
                [2, 0, 0, 2, 2, 0, 0.593, 0.042, 'N'],
                [0, 0, 1, 1, 1, 0, 0.719, 0.103, 'N']]
    """
    data_set = [['青绿', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', 0.697, 0.460, '好瓜'],
                ['乌黑', '蜷缩', '沉闷', '清晰', '凹陷', '硬滑', 0.774, 0.376, '好瓜'],
                ['乌黑', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', 0.634, 0.264, '好瓜'],
                ['青绿', '蜷缩', '沉闷', '清晰', '凹陷', '硬滑', 0.608, 0.318, '好瓜'],
                ['浅白', '蜷缩', '浊响', '清晰', '凹陷', '硬滑', 0.556, 0.215, '好瓜'],
                ['青绿', '稍缩', '浊响', '清晰', '稍凹', '软粘', 0.403, 0.237, '好瓜'],
                ['乌黑', '稍缩', '浊响', '稍糊', '稍凹', '软粘', 0.481, 0.149, '好瓜'],
                ['乌黑', '稍缩', '浊响', '清晰', '稍凹', '硬滑', 0.437, 0.211, '好瓜'],
                ['乌黑', '稍缩', '沉闷', '稍糊', '稍凹', '硬滑', 0.666, 0.091, '坏瓜'],
                ['青绿', '硬挺', '清脆', '清晰', '平坦', '软粘', 0.243, 0.267, '坏瓜'],
                ['浅白', '硬挺', '清脆', '模糊', '平坦', '硬滑', 0.245, 0.057, '坏瓜'],
                ['浅白', '蜷缩', '浊响', '模糊', '平坦', '软粘', 0.343, 0.099, '坏瓜'],
                ['青绿', '稍缩', '浊响', '稍糊', '凹陷', '硬滑', 0.639, 0.161, '坏瓜'],
                ['浅白', '稍缩', '沉闷', '稍糊', '凹陷', '硬滑', 0.657, 0.198, '坏瓜'],
                ['乌黑', '稍缩', '浊响', '清晰', '稍凹', '软粘', 0.360, 0.370, '坏瓜'],
                ['浅白', '蜷缩', '浊响', '模糊', '平坦', '硬滑', 0.593, 0.042, '坏瓜'],
                ['青绿', '蜷缩', '沉闷', '稍糊', '稍凹', '硬滑', 0.719, 0.103, '坏瓜']]
    labels = ['色泽', '根蒂', '敲声', '纹理', '脐部', '触感', '密度', '含糖量']
    is_features_discrete = [1, 1, 1, 1, 1, 1, 0, 0]
    return data_set, labels, is_features_discrete


def is_all_sample_same(data_set):
    """
    检查data_set中的样本是否都同属于一类（如好瓜与坏瓜）
    :param data_set:
    :return:
    """
    for i in range(len(data_set) - 1):
        sample1 = data_set[i]
        sample2 = data_set[i + 1]
        result = operator.eq(sample1, sample2)
        if result is False:
            return result
    return True


def get_most_common_class(data_set):
    """
    获取样本中个数最多的类（如好瓜、坏瓜）
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
    return sorted_class_count[0]


def tree_generate(data_set, labels, is_features_discrete):
    # 检查样本是否已经同属于一类了
    class_list = [sample[-1] for sample in data_set]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]

    # 检查labels是否为空, dataSet在labels上的取值都一样（所有样本在所有属性上的取值一样）
    if len(labels) == 0 or is_all_sample_same(data_set):
        return get_most_common_class(data_set)

    # 从A中找出最优的属性值，进行划分
    best_feature_index, best_continuous_feature_value = get_best_feature_index(data_set, labels, is_features_discrete)
    best_feature_label = labels[best_feature_index]

    if is_features_discrete[best_feature_index] == 1:
        tree = {best_feature_label: {}}

        del(labels[best_feature_index])
        del(is_features_discrete[best_feature_index])

        sub_features_list = [sample[best_feature_index] for sample in data_set]
        unique_sub_features = set(sub_features_list)
        for value in unique_sub_features:
            # 往下继续生成树
            # 使用sub_labels来替代labels，传递到tree_generate函数，tree_generate会删除labels中的内容，
            # 如果一直传递同一个labels，会出现问题，sub_labels = labels[:]，相当于拷贝一个新的labels list
            sub_labels = labels[:]
            sub_is_feature_discrete = is_features_discrete[:]
            tree[best_feature_label][value] = tree_generate(split_data_set_by_operate(
                data_set, best_feature_index, value, operator.eq, delete_col=True), sub_labels, sub_is_feature_discrete)
    else:
        key = best_feature_label+'<='+str.format("%0.3f" % best_continuous_feature_value)
        tree = {key: {}}
        tree[key]['是'] = tree_generate(split_data_set_by_operate(
            data_set, best_feature_index, best_continuous_feature_value, operator.le, delete_col=False), labels, is_features_discrete)
        tree[key]['否'] = tree_generate(split_data_set_by_operate(
            data_set, best_feature_index, best_continuous_feature_value, operator.gt, delete_col=False), labels, is_features_discrete)
    return tree


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


def split_data_set_by_operate(data_set, col, value, operate, delete_col):
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


def get_best_feature_index(data_set, labels, is_features_discrete):
    """
    从lables中找出最优划分属性
    :param data_set:
    :param labels:
    :return:
    """
    feature_num = len(labels)
    base_entropy = calculate_information_entropy(data_set)
    best_gain = 0.0
    best_feature_index = -1
    best_continuous_feature_value = None
    for i in range(feature_num):
        # 处理离散型的特征
        if is_features_discrete[i] == 1:
            sub_features_list = [sample[i] for sample in data_set]
            unique_sub_features = set(sub_features_list)
            entropy = 0.0
            for value in unique_sub_features:
                sub_data_set = split_data_set_by_operate(data_set, i, value, operator.eq, delete_col=True)
                prob = float(len(sub_data_set)) / len(data_set)
                entropy += prob * calculate_information_entropy(sub_data_set)
            gain = base_entropy - entropy
            if gain > best_gain:
                best_gain = gain
                best_feature_index = i
        # 处理连续型的特征
        else:
            continuous_best_gain = 0.0
            continuous_best_feature_value = -1
            sub_features_list = [sample[i] for sample in data_set]
            unique_sub_features = set(sub_features_list)
            unique_sub_features = sorted(unique_sub_features, reverse=False)
            new_unique_sub_features = []
            for j in range(len(unique_sub_features)-1):
                new_unique_sub_features.append((unique_sub_features[j]+unique_sub_features[j+1])/2)
            for value in new_unique_sub_features:
                sub_data_set_le = split_data_set_by_operate(data_set, i, value, operator.le, delete_col=True)
                sub_data_set_gt = split_data_set_by_operate(data_set, i, value, operator.gt, delete_col=True)
                prob = float(len(sub_data_set_le)) / len(data_set)
                entropy = prob * calculate_information_entropy(sub_data_set_le) + (1-prob) * calculate_information_entropy(sub_data_set_gt)
                gain = base_entropy - entropy
                if gain > continuous_best_gain:
                    continuous_best_gain = gain
                    continuous_best_feature_value = value
            if continuous_best_gain > best_gain:
                best_gain = continuous_best_gain
                best_feature_index = i
                best_continuous_feature_value = continuous_best_feature_value

    return best_feature_index, best_continuous_feature_value


if __name__ == '__main__':
    data_set, labels, is_features_discrete = create_data_set()
    decision_tree = tree_generate(data_set, labels, is_features_discrete)
    treePlotter.createPlot(decision_tree)

from math import log
import operator
import treePlotter
from base import is_all_sample_same, get_most_common_class, split_data_set_by_operate, calculate_information_entropy

"""
周志华《机器学习》第四章中的习题4.3 code
实现基于信息熵进行划分选择的决策树算法
ID3基于信息增益，C4.5基于增益率
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
    """
    data_set = [[0, 0, 0, 0, 0, 0, 0.697, 0.460, '好瓜'],
                [1, 0, 1, 0, 0, 0, 0.774, 0.376, '好瓜'],
                [1, 0, 0, 0, 0, 0, 0.634, 0.264, '好瓜'],
                [0, 0, 1, 0, 0, 0, 0.608, 0.318, '好瓜'],
                [2, 0, 0, 0, 0, 0, 0.556, 0.215, '好瓜'],
                [0, 1, 0, 0, 1, 1, 0.403, 0.237, '好瓜'],
                [1, 1, 0, 1, 1, 1, 0.481, 0.149, '好瓜'],
                [1, 1, 0, 0, 1, 0, 0.437, 0.211, '好瓜'],
                [1, 1, 1, 1, 1, 0, 0.666, 0.091, '坏瓜'],
                [0, 2, 2, 0, 2, 1, 0.243, 0.267, '坏瓜'],
                [2, 2, 2, 2, 2, 0, 0.245, 0.057, '坏瓜'],
                [2, 0, 0, 2, 2, 1, 0.343, 0.099, '坏瓜'],
                [0, 1, 0, 1, 0, 0, 0.639, 0.161, '坏瓜'],
                [2, 1, 1, 1, 0, 0, 0.657, 0.198, '坏瓜'],
                [1, 1, 0, 0, 1, 1, 0.360, 0.370, '坏瓜'],
                [2, 0, 0, 2, 2, 0, 0.593, 0.042, '坏瓜'],
                [0, 0, 1, 1, 1, 0, 0.719, 0.103, '坏瓜']]
    labels_list = ['色泽', '根蒂', '敲声', '纹理', '脐部', '触感', '密度', '含糖量']
    labels_dict = {'色泽': {0: '青绿', 1: '乌黑', 2: '浅白'},
                   '根蒂': {0: '蜷缩', 1: '稍缩', 2: '硬挺'},
                   '敲声': {0: '浊响', 1: '沉闷', 2: '清脆'},
                   '纹理': {0: '清晰', 1: '稍糊', 2: '模糊'},
                   '脐部': {0: '凹陷', 1: '稍凹', 2: '平坦'},
                   '触感': {0: '硬滑', 1: '软粘'},
                   '密度': {},
                   '含糖量': {}}
    is_features_discrete = [1, 1, 1, 1, 1, 1, 0, 0]
    return data_set, labels_list, labels_dict, is_features_discrete


def tree_generate(data_set, labels_list, labels_dict, is_features_discrete, ID3_or_C45):
    # 检查样本是否已经同属于一类了
    class_list = [sample[-1] for sample in data_set]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]

    # 检查labels是否为空, dataSet在labels上的取值都一样（所有样本在所有属性上的取值一样）
    if len(labels_list) == 0 or is_all_sample_same(data_set):
        return get_most_common_class(data_set)

    # 从A中找出最优的属性值，进行划分
    best_feature_index, best_continuous_feature_value = get_best_feature(data_set, labels_list, is_features_discrete, ID3_or_C45)
    best_feature_label = labels_list[best_feature_index]
    # 如果该特征是离散型的，从数据中删除该特征
    if is_features_discrete[best_feature_index] == 1:
        tree = {best_feature_label: {}}

        del(is_features_discrete[best_feature_index])
        del (labels_list[best_feature_index])

        unique_sub_features = labels_dict[best_feature_label].keys()
        for value in unique_sub_features:
            # 往下继续生成树
            # 使用sub_labels来替代labels，传递到tree_generate函数，tree_generate会删除labels中的内容，
            # 如果一直传递同一个labels，会出现问题，sub_labels = labels[:]，相当于拷贝一个新的labels list
            sub_labels_list = labels_list[:]
            sub_is_feature_discrete = is_features_discrete[:]
            sub_data_set = split_data_set_by_operate(
                data_set, best_feature_index, value, operator.eq, delete_col=True)
            sub_feature_name = labels_dict[best_feature_label][value]
            # 如果划分出来的子属性集合为空，则将分支结点标记为叶节点，其分类标记为data_set中样本最多的类
            if len(sub_data_set) == 0:
                tree[best_feature_label][sub_feature_name] = get_most_common_class(data_set)
            # 如果划分出来的子属性集合不为空，则继续递归
            else:
                tree[best_feature_label][sub_feature_name] = tree_generate(sub_data_set,
                    sub_labels_list, labels_dict, sub_is_feature_discrete, ID3_or_C45)
    # 如果该特征是连续的，不需要从数据中删除该特征
    # 与离散属性不同，若当前结点划分属性为连续属性，该属性还可作为其后代结点的划分属性
    else:
        key = best_feature_label+'<='+str.format("%0.3f" % best_continuous_feature_value)
        tree = {key: {}}
        tree[key]['是'] = tree_generate(split_data_set_by_operate(
            data_set, best_feature_index, best_continuous_feature_value, operator.le, delete_col=False),
            labels_list, labels_dict, is_features_discrete, ID3_or_C45)
        tree[key]['否'] = tree_generate(split_data_set_by_operate(
            data_set, best_feature_index, best_continuous_feature_value, operator.gt, delete_col=False),
            labels_list, labels_dict, is_features_discrete, ID3_or_C45)
    return tree


def get_best_feature(data_set, labels, is_features_discrete, ID3_or_C45):
    """
    从lables中找出最优划分属性
    :param data_set:
    :param labels:
    :return:
    """
    feature_num = len(labels)
    base_entropy = calculate_information_entropy(data_set)
    gain_list = []
    gain_ratio_list = []
    continuous_feature_value_list = []
    epsilon = 1e-5
    for i in range(feature_num):
        # 处理离散型的特征，各个特征已经划分成特定的子集了，不需要再次进行划分
        if is_features_discrete[i] == 1:
            sub_features_list = [sample[i] for sample in data_set]
            unique_sub_features = set(sub_features_list)
            entropy = 0.0
            iv = 0.0
            for value in unique_sub_features:
                sub_data_set = split_data_set_by_operate(data_set, i, value, operator.eq, delete_col=True)
                prob = float(len(sub_data_set)) / len(data_set)
                entropy += prob * calculate_information_entropy(sub_data_set)
                iv += prob * log(prob, 2)
            gain = base_entropy - entropy
            gain_ratio = gain / (-iv+epsilon)
            gain_list.append(gain)
            gain_ratio_list.append(gain_ratio)
            continuous_feature_value_list.append(None)
        # 处理连续型的特征，需要手动进行划分，对特征中的各个值先从小排到大，再计算出连续两个值的中值，作为待定划分点
        # 找到一个让信息熵最大的划分点
        else:
            continuous_best_gain = 0.0
            continuous_best_feature_value = -1
            continuous_best_gain_ratio = 0.0

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
                iv = prob * log(prob, 2) + (1-prob) * log(1-prob, 2)
                gain_ratio = gain / (-iv)
                if gain > continuous_best_gain:
                    continuous_best_gain = gain
                    continuous_best_feature_value = value
                    continuous_best_gain_ratio = gain_ratio
            gain_list.append(continuous_best_gain)
            gain_ratio_list.append(continuous_best_gain_ratio)
            continuous_feature_value_list.append(continuous_best_feature_value)
    # ID3直接找信息增益最高的那一个
    if ID3_or_C45 == 0:
        max_gain_index = gain_list.index(max(gain_list))
        return max_gain_index, continuous_feature_value_list[max_gain_index]
    # C45先从候选划分属性中找出信息增益高于平均水平的属性，再从中选择增益率最高的
    elif ID3_or_C45 == 1:
        average_gain = 0.0
        for i in range(len(gain_list)):
            average_gain += gain_list[i]
        average_gain = average_gain / len(gain_list)
        max_gain_ratio = 0
        max_gain_ratio_index = -1
        for i in range(len(gain_list)):
            if gain_list[i] > average_gain and gain_ratio_list[i] > max_gain_ratio:
                max_gain_ratio = gain_ratio_list[i]
                max_gain_ratio_index = i
        return max_gain_ratio_index, continuous_feature_value_list[max_gain_ratio_index]
    else:
        raise NameError('ID3_or_C45 should be 0 or 1')


if __name__ == '__main__':
    ID3_or_C45 = 0
    data_set, labels_list, labels_dict, is_features_discrete = create_data_set()
    decision_tree = tree_generate(data_set, labels_list, labels_dict, is_features_discrete, ID3_or_C45)
    treePlotter.createPlot(decision_tree)

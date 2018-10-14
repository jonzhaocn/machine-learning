import operator
import treePlotter
from base import is_all_sample_same, get_most_common_class, split_data_set_by_operate, \
    calculate_gini, get_validation_error_count_by_major_class, get_validation_error_count_by_tree, get_keys_for_dict

"""
周志华《机器学习》第四章中的习题4.4 code
试编程实现基于基尼指数进行划分选择的决策树算法，为表4.2中数据生成预剪枝、后剪枝决策树，并与未剪枝决策树进行比较
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
    """
    data_set_train = [[0, 0, 0, 0, 0, 0, '好瓜'],
                      [1, 0, 1, 0, 0, 0, '好瓜'],
                      [1, 0, 0, 0, 0, 0, '好瓜'],
                      [0, 0, 1, 0, 0, 0, '好瓜'],
                      [0, 1, 0, 0, 1, 1, '好瓜'],
                      [1, 1, 0, 1, 1, 1, '好瓜'],
                      [0, 2, 2, 0, 2, 1, '坏瓜'],
                      [2, 1, 1, 1, 0, 0, '坏瓜'],
                      [1, 1, 0, 0, 1, 1, '坏瓜'],
                      [2, 0, 0, 2, 2, 0, '坏瓜'],
                      [0, 0, 1, 1, 1, 0, '坏瓜']]
    data_set_validate = [[2, 0, 0, 0, 0, 0, '好瓜'],
                         [1, 1, 0, 0, 1, 0, '好瓜'],
                         [1, 1, 1, 1, 1, 0, '坏瓜'],
                         [2, 2, 2, 2, 2, 0, '坏瓜'],
                         [2, 0, 0, 2, 2, 1, '坏瓜'],
                         [0, 1, 0, 1, 0, 0, '坏瓜']]
    labels_list = ['色泽', '根蒂', '敲声', '纹理', '脐部', '触感']
    labels_dict = {'色泽': {0: '青绿', 1: '乌黑', 2: '浅白'},
                   '根蒂': {0: '蜷缩', 1: '稍缩', 2: '硬挺'},
                   '敲声': {0: '浊响', 1: '沉闷', 2: '清脆'},
                   '纹理': {0: '清晰', 1: '稍糊', 2: '模糊'},
                   '脐部': {0: '凹陷', 1: '稍凹', 2: '平坦'},
                   '触感': {0: '硬滑', 1: '软粘'}}
    return data_set_train, data_set_validate, labels_list, labels_dict


def get_best_feature_gini(data_set, labels_list):
    best_gini_index = 100
    best_gini_index_index = -1
    for i in range(len(labels_list)):
        feature_values = [sample[i] for sample in data_set]
        feature_values = set(feature_values)
        gini_index = 0.0
        for value in feature_values:
            sub_data_set = split_data_set_by_operate(data_set, i, value, operator.eq, delete_col=False)
            prob = float(len(sub_data_set))/len(data_set)
            gini_index += prob * calculate_gini(sub_data_set)
        if gini_index < best_gini_index:
            best_gini_index = gini_index
            best_gini_index_index = i
    return best_gini_index_index


def tree_generate_without_pruning(data_set_train, labels_list, labels_dict):

    # 检查样本是否已经同属于一类了
    class_list = [sample[-1] for sample in data_set_train]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]

    # 检查labels是否为空, dataSet在labels上的取值都一样（所有样本在所有属性上的取值一样）
    if len(labels_list) == 0 or is_all_sample_same(data_set_train):
        return get_most_common_class(data_set_train)

    # 从A中找出最优的属性值，进行划分
    best_feature_index = get_best_feature_gini(data_set_train, labels_list)
    best_feature_label = labels_list[best_feature_index]

    del(labels_list[best_feature_index])

    tree = {best_feature_label: {}}
    sub_features_value_set = labels_dict[best_feature_label].keys()

    for sub_feature_value in sub_features_value_set:
        sub_labels_list = labels_list[:]
        sub_data_set_train = split_data_set_by_operate(data_set_train, best_feature_index, sub_feature_value,
                                                       operator.eq, delete_col=True)
        sub_feature_name = labels_dict[best_feature_label][sub_feature_value]
        # 如果划分出来的子属性集合为空，则将分支结点标记为叶节点，其分类标记为data_set中样本最多的类
        if len(sub_data_set_train) == 0:
            tree[best_feature_label][sub_feature_name] = get_most_common_class(data_set_train)
        # 如果划分出来的子属性集合不为空，则继续递归
        else:
            tree[best_feature_label][sub_feature_name] = tree_generate_without_pruning(sub_data_set_train,
                                                                                       sub_labels_list, labels_dict)
    return tree


def tree_generate_with_pre_pruning(data_set_train, data_set_validate, labels_list, labels_dict):
    # 检查样本是否已经同属于一类了
    class_list = [sample[-1] for sample in data_set_train]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]

    # 检查labels是否为空, dataSet在labels上的取值都一样（所有样本在所有属性上的取值一样）
    if len(labels_list) == 0 or is_all_sample_same(data_set_train):
        return get_most_common_class(data_set_train)

    # 从A中找出最优的属性值，进行划分
    best_feature_index = get_best_feature_gini(data_set_train, labels_list)
    best_feature_label = labels_list[best_feature_index]

    del (labels_list[best_feature_index])

    # 计算划分之前的准确率
    most_common_class = get_most_common_class(data_set_train)
    class_list = [sample[-1] for sample in data_set_validate]
    accuracy_rate_before_pruning = class_list.count(most_common_class) / float(len(class_list))
    # 计算划分之后的准确率
    accuracy_rate_after_pruning = 0.0
    sub_features_value_set = [sample[best_feature_index] for sample in data_set_train]
    sub_features_value_set = set(sub_features_value_set)

    for sub_feature_value in sub_features_value_set:
        sub_data_set_train = split_data_set_by_operate(data_set_train, best_feature_index, sub_feature_value,
                                                       operator.eq, delete_col=True)
        sub_data_set_validate = split_data_set_by_operate(data_set_validate, best_feature_index, sub_feature_value,
                                                          operator.eq, delete_col=True)
        if len(sub_data_set_validate) == 0:
            continue
        sub_most_common_class = get_most_common_class(sub_data_set_train)
        sub_class_list = [sample[-1] for sample in sub_data_set_validate]
        accuracy_rate_after_pruning += sub_class_list.count(sub_most_common_class) / float(len(sub_class_list)) \
                                       * (len(sub_class_list)/len(data_set_validate))
    # 划分之后的准确率没有超过划分之前的准确率，不再进行划分
    if accuracy_rate_before_pruning >= accuracy_rate_after_pruning:
        most_common_class = get_most_common_class(data_set_train)
        return most_common_class
    # 划分之后的准确率超过了划分之前的准确率，继续进行划分
    else:
        tree = {best_feature_label: {}}
        sub_features_value_set = [sample[best_feature_index] for sample in data_set_train]
        sub_features_value_set = set(sub_features_value_set)

        for sub_feature_value in sub_features_value_set:
            sub_labels_list = labels_list[:]
            sub_data_set_train = split_data_set_by_operate(data_set_train, best_feature_index, sub_feature_value,
                                                           operator.eq, delete_col=True)
            sub_data_set_validate = split_data_set_by_operate(data_set_validate, best_feature_index, sub_feature_value,
                                                              operator.eq, delete_col=True)
            sub_feature_name = labels_dict[best_feature_label][sub_feature_value]
            tree[best_feature_label][sub_feature_name] = \
                tree_generate_with_pre_pruning(sub_data_set_train, sub_data_set_validate, sub_labels_list, labels_dict)
        return tree


def tree_generator_with_post_pruning(input_tree, data_set_train, data_set_validate, labels_list, labels_dict):
    if type(input_tree).__name__ == 'str':
        return input_tree
    feature_name = list(input_tree.keys())[0]
    inferior_tree = input_tree[feature_name]
    feature_index = labels_list.index(feature_name)

    for value in inferior_tree:
        value_key = get_keys_for_dict(labels_dict[feature_name], value)[0]

        sub_labels_list = labels_list[:]
        del(sub_labels_list[feature_index])

        sub_data_set_train = split_data_set_by_operate(data_set_train, feature_index, value_key,
                                                       operator.eq, delete_col=True)
        sub_data_set_validate = split_data_set_by_operate(data_set_validate, feature_index, value_key,
                                                          operator.eq, delete_col=True)
        input_tree[feature_name][value] = tree_generator_with_post_pruning(
            inferior_tree[value], sub_data_set_train, sub_data_set_validate, sub_labels_list, labels_dict)
    # 到达某个结点之后，测试一下准确率，看看是否要剪枝
    # get_validation_error_count_by_major_class(major_class, data_set_validate)
    # get_validation_error_count_by_tree(input_tree, data_set_validate, labels_list)
    error_count_by_tree = get_validation_error_count_by_tree(input_tree, data_set_validate, labels_list, labels_dict)
    error_count_by_major_class = get_validation_error_count_by_major_class(get_most_common_class(data_set_train), data_set_validate)
    if error_count_by_tree <= error_count_by_major_class:
        return input_tree
    return get_most_common_class(data_set_train)


if __name__ == '__main__':
    data_set_train, data_set_validate, labels_list, labels_dict = create_data_set()
    tree_without_pruning = tree_generate_without_pruning(data_set_train, labels_list[:], labels_dict)
    tree_with_pre_pruning = tree_generate_with_pre_pruning(data_set_train, data_set_validate, labels_list[:], labels_dict)
    tree_with_post_pruning = tree_generator_with_post_pruning(tree_without_pruning, data_set_train, data_set_validate, labels_list[:], labels_dict)
    treePlotter.createPlot(tree_with_post_pruning)

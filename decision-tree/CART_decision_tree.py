import operator
import treePlotter
from base import is_all_sample_same, get_most_common_class, split_data_set_by_operate, \
    calculate_gini, get_validation_error_count_by_major_class, get_validation_error_count_by_tree, get_keys_for_dict, \
    get_validation_error_before_pruning, get_validation_error_after_pruning, create_data_set_two

"""
周志华《机器学习》第四章中的习题4.4 code
试编程实现基于基尼指数进行划分选择的决策树算法，为表4.2中数据生成预剪枝、后剪枝决策树，并与未剪枝决策树进行比较
"""


def get_best_feature_gini(data_set, features_list, is_features_discrete):
    best_gini_index = 100
    best_gini_index_index = -1
    continuous_feature_value = None
    for i in range(len(features_list)):
        # 处理离散型特征
        feature_values_list = [sample[i] for sample in data_set]
        feature_values_list = set(feature_values_list)
        if is_features_discrete[i] == 1:
            gini_index = 0.0
            # 在一个feature上根据feature的取值的不同，划分成不同的sub data set
            for value in feature_values_list:
                sub_data_set = split_data_set_by_operate(data_set, i, value, operator.eq, delete_col=False)
                prob = float(len(sub_data_set))/len(data_set)
                gini_index += prob * calculate_gini(sub_data_set)
            if gini_index < best_gini_index:
                best_gini_index = gini_index
                best_gini_index_index = i
        # 处理连续型特征
        else:
            continuous_best_gini_index = 100
            continuous_best_feature_value = -1
            feature_values_list = sorted(feature_values_list, reverse=False)
            feature_values_mid_value_list = []
            # 对于连续型特征，将其都有的取值进行排序，取连续两个取值的中值作为待测试划分
            for j in range(len(feature_values_list) - 1):
                feature_values_mid_value_list.append((feature_values_list[j] + feature_values_list[j + 1]) / 2)
            # 对于所有计算得到的中值，进行测试
            for value in feature_values_mid_value_list:
                # 一个中值可以将数据分为两部分
                sub_data_set_le = split_data_set_by_operate(data_set, i, value, operator.le, delete_col=True)
                sub_data_set_gt = split_data_set_by_operate(data_set, i, value, operator.gt, delete_col=True)
                prob = float(len(sub_data_set_le)) / len(data_set)
                gini_index = prob * calculate_gini(sub_data_set_le) + (1-prob) * calculate_gini(sub_data_set_gt)
                if gini_index < continuous_best_gini_index:
                    continuous_best_gini_index = gini_index
                    continuous_best_feature_value = value
            if continuous_best_gini_index < best_gini_index:
                best_gini_index = continuous_best_gini_index
                best_gini_index_index = i
                continuous_feature_value = continuous_best_feature_value
    return best_gini_index_index, continuous_feature_value


def tree_generate_without_pruning(data_set_train, features_list, features_dict, is_features_discrete):
    """
    树生成 不剪枝
    :param data_set_train:
    :param features_list:
    :param features_dict:
    :param is_features_discrete:
    :return:
    """
    # 检查样本是否已经同属于一类了
    class_list = [sample[-1] for sample in data_set_train]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]

    # 检查features_list是否为空, dataSet在feature上的取值都一样（所有样本在所有属性上的取值一样）
    if len(features_list) == 0 or is_all_sample_same(data_set_train):
        return get_most_common_class(data_set_train)

    # 从A中找出最优的属性值，进行划分
    best_feature_index, best_continuous_feature_value = get_best_feature_gini(data_set_train, features_list, is_features_discrete)
    best_feature_name = features_list[best_feature_index]

    if is_features_discrete[best_feature_index] == 1:
        # 如果该特征是离散型的，从数据中删除该特征
        del (features_list[best_feature_index])
        tree = {best_feature_name: {}}
        feature_values_list = features_dict[best_feature_name].keys()

        for feature_value in feature_values_list:
            new_features_list = features_list[:]
            sub_data_set_train = split_data_set_by_operate(data_set_train, best_feature_index, feature_value,
                                                           operator.eq, delete_col=True)
            feature_value_name = features_dict[best_feature_name][feature_value]
            # 如果划分出来的子属性集合为空，则将分支结点标记为叶节点，其分类标记为data_set中样本最多的类
            if len(sub_data_set_train) == 0:
                tree[best_feature_name][feature_value_name] = get_most_common_class(data_set_train)
            # 如果划分出来的子属性集合不为空，则继续递归
            else:
                tree[best_feature_name][feature_value_name] = tree_generate_without_pruning(sub_data_set_train,
                                                                                          new_features_list, features_dict,
                                                                                           is_features_discrete)
    else:
        # 如果该特征是连续的，不需要从数据中删除该特征
        # 与离散属性不同，若当前结点划分属性为连续属性，该属性还可作为其后代结点的划分属性
        key = best_feature_name + '<=' + str.format("%0.3f" % best_continuous_feature_value)
        tree = {key: {}}
        sub_data_set_le = split_data_set_by_operate(
            data_set_train, best_feature_index, best_continuous_feature_value, operator.le, delete_col=False)
        sub_data_set_gt = split_data_set_by_operate(
            data_set_train, best_feature_index, best_continuous_feature_value, operator.gt, delete_col=False)
        tree[key]['是'] = tree_generate_without_pruning(sub_data_set_le, features_list, features_dict, is_features_discrete)
        tree[key]['否'] = tree_generate_without_pruning(sub_data_set_gt, features_list, features_dict, is_features_discrete)
    return tree


def tree_generate_with_pre_pruning(data_set_train, data_set_validate, features_list, features_dict, is_features_discrete):
    """
    预剪枝 树生成
    :param data_set_train:
    :param data_set_validate:
    :param features_list:
    :param features_dict:
    :param is_features_discrete:
    :return:
    """
    # 检查样本是否已经同属于一类了
    class_list = [sample[-1] for sample in data_set_train]
    if class_list.count(class_list[0]) == len(class_list):
        return class_list[0]

    # 检查features_list是否为空, dataSet在feature上的取值都一样（所有样本在所有属性上的取值一样）
    if len(features_list) == 0 or is_all_sample_same(data_set_train):
        return get_most_common_class(data_set_train)

    # 从A中找出最优的属性值，进行划分
    best_feature_index, best_continuous_feature_value = get_best_feature_gini(data_set_train, features_list, is_features_discrete)
    best_feature_name = features_list[best_feature_index]

    # 特征值为离散值
    if is_features_discrete[best_feature_index] == 1:
        del (features_list[best_feature_index])
    accuracy_rate_before_pruning = get_validation_error_before_pruning(data_set_train, data_set_validate)
    accuracy_rate_after_pruning = get_validation_error_after_pruning(data_set_train, data_set_validate, best_feature_index,
                                                                     is_features_discrete[best_feature_index], best_continuous_feature_value)
    # 划分之后的准确率没有超过划分之前的准确率，不再进行划分
    if accuracy_rate_before_pruning >= accuracy_rate_after_pruning:
        most_common_class = get_most_common_class(data_set_train)
        return most_common_class
    # 划分之后的准确率超过了划分之前的准确率，继续进行划分
    else:
        if is_features_discrete[best_feature_index] == 1:
            tree = {best_feature_name: {}}
            feature_values_list = [sample[best_feature_index] for sample in data_set_train]
            feature_values_list = set(feature_values_list)

            for feature_value in feature_values_list:
                new_features_list = features_list[:]
                sub_data_set_train = split_data_set_by_operate(data_set_train, best_feature_index, feature_value,
                                                               operator.eq, delete_col=True)
                sub_data_set_validate = split_data_set_by_operate(data_set_validate, best_feature_index, feature_value,
                                                                  operator.eq, delete_col=True)
                feature_value_name = features_dict[best_feature_name][feature_value]
                tree[best_feature_name][feature_value_name] = \
                    tree_generate_with_pre_pruning(sub_data_set_train, sub_data_set_validate, new_features_list, features_dict, is_features_discrete)
        else:
            key = best_feature_name + '<=' + str.format("%0.3f" % best_continuous_feature_value)
            tree = {key: {}}
            # 划分数据集
            sub_data_set_train_le = split_data_set_by_operate(
                data_set_train, best_feature_index, best_continuous_feature_value, operator.le, delete_col=False)
            sub_data_set_validate_le = split_data_set_by_operate(
                data_set_validate, best_feature_index, best_continuous_feature_value, operator.le, delete_col=False)
            sub_data_set_train_gt = split_data_set_by_operate(
                data_set_train, best_feature_index, best_continuous_feature_value, operator.gt, delete_col=False)
            sub_data_set_validate_gt = split_data_set_by_operate(
                data_set_validate, best_feature_index, best_continuous_feature_value, operator.gt, delete_col=False)
            # 生成节点
            tree[key]['是'] = tree_generate_with_pre_pruning(sub_data_set_train_le, sub_data_set_validate_le, features_list, features_dict, is_features_discrete)
            tree[key]['否'] = tree_generate_with_pre_pruning(sub_data_set_train_gt, sub_data_set_validate_gt, features_list, features_dict, is_features_discrete)
        return tree


def tree_generator_with_post_pruning(input_tree, data_set_train, data_set_validate, features_list, features_dict):
    """
    后剪枝 树生成
    :param input_tree:
    :param data_set_train:
    :param data_set_validate:
    :param features_list:
    :param features_dict:
    :return:
    """
    if type(input_tree).__name__ == 'str':
        return input_tree
    feature_name = list(input_tree.keys())[0]
    inferior_tree = input_tree[feature_name]
    feature_index = features_list.index(feature_name)

    for value in inferior_tree:
        value_key = get_keys_for_dict(features_dict[feature_name], value)[0]

        new_features_list = features_list[:]
        del(new_features_list[feature_index])

        sub_data_set_train = split_data_set_by_operate(data_set_train, feature_index, value_key,
                                                       operator.eq, delete_col=True)
        sub_data_set_validate = split_data_set_by_operate(data_set_validate, feature_index, value_key,
                                                          operator.eq, delete_col=True)
        input_tree[feature_name][value] = tree_generator_with_post_pruning(
            inferior_tree[value], sub_data_set_train, sub_data_set_validate, new_features_list, features_dict)
    # 到达某个结点之后，测试一下准确率，看看是否要剪枝
    # get_validation_error_count_by_major_class(major_class, data_set_validate)
    # get_validation_error_count_by_tree(input_tree, data_set_validate, features_list)
    error_count_by_tree = get_validation_error_count_by_tree(input_tree, data_set_validate, features_list, features_dict)
    error_count_by_major_class = get_validation_error_count_by_major_class(get_most_common_class(data_set_train), data_set_validate)
    if error_count_by_tree <= error_count_by_major_class:
        return input_tree
    return get_most_common_class(data_set_train)


if __name__ == '__main__':
    data_set_train, data_set_validate, features_list, features_dict, is_features_discrete = create_data_set_two()
    tree_without_pruning = tree_generate_without_pruning(data_set_train, features_list[:], features_dict, is_features_discrete)
    tree_with_pre_pruning = tree_generate_with_pre_pruning(data_set_train, data_set_validate, features_list[:], features_dict, is_features_discrete)
    tree_with_post_pruning = tree_generator_with_post_pruning(tree_without_pruning, data_set_train, data_set_validate, features_list[:], features_dict)
    treePlotter.createPlot(tree_with_post_pruning)

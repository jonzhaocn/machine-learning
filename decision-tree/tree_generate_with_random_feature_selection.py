import operator
import treePlotter
import random
from base import is_all_sample_same, get_most_common_class, split_data_set_by_operate, create_data_set_one


def tree_generate_with_random_feature_selection(data_set, features_list, features_dict, is_features_discrete):
    """
    通过随机选择特征来生成决策树
    :param data_set:
    :param features_list:
    :param features_dict:
    :param is_features_discrete:
    :return:
    """
    # deep copy
    features_list = features_list[:]
    is_features_discrete = is_features_discrete[:]
    #
    samples_class = [sample[-1] for sample in data_set]
    if samples_class.count(samples_class[0]) == len(samples_class):
        return samples_class[0]
    if len(features_list) == 0 or is_all_sample_same(data_set):
        return get_most_common_class(data_set)
    best_feature_index = random.randint(0, len(features_list)-1)
    best_feature_name = features_list[best_feature_index]

    if is_features_discrete[best_feature_index] == 1:
        # 如果该特征是离散型的，从数据中删除该特征
        del(features_list[best_feature_index])
        del(is_features_discrete[best_feature_index])
        tree = {best_feature_name: {}}
        feature_value_set = features_dict[best_feature_name].keys()

        for feature_value in feature_value_set:
            # 如果没有重新拷贝一份，只要每往下一层，就会删除features_list中的一个数据，
            # 但是递归返回时的往另外一个分支走的时候就会出问题

            sub_data_set_train = split_data_set_by_operate(data_set, best_feature_index, feature_value,
                                                           operator.eq, delete_col=True)
            feature_value_name = features_dict[best_feature_name][feature_value]
            # 如果划分出来的子属性集合为空，则将分支结点标记为叶节点，其分类标记为data_set中样本最多的类
            if len(sub_data_set_train) == 0:
                tree[best_feature_name][feature_value_name] = get_most_common_class(data_set)
            # 如果划分出来的子属性集合不为空，则继续递归
            else:
                tree[best_feature_name][feature_value_name] = \
                    tree_generate_with_random_feature_selection(sub_data_set_train, features_list, features_dict,
                                                                is_features_discrete)
    else:
        # 如果该特征是连续的
        feature_values_mid_value_list = []
        feature_value_set = [sample[best_feature_index] for sample in data_set]
        feature_value_set = set(feature_value_set)
        feature_value_set = sorted(feature_value_set, reverse=False)
        for i in range(len(feature_value_set)-1):
            feature_values_mid_value_list.append((feature_value_set[i]+feature_value_set[i+1])/2)
        # 从中值中随机选择一个数作为best_continuous_feature_value
        best_continuous_feature_value = random.choice(feature_values_mid_value_list)
        key = best_feature_name + '<=' + str.format("%0.3f" % best_continuous_feature_value)
        tree = {key: {}}
        sub_data_set_le = split_data_set_by_operate(
            data_set, best_feature_index, best_continuous_feature_value, operator.le, delete_col=False)
        sub_data_set_gt = split_data_set_by_operate(
            data_set, best_feature_index, best_continuous_feature_value, operator.gt, delete_col=False)
        tree[key]['是'] = tree_generate_with_random_feature_selection(sub_data_set_le, features_list, features_dict,
                                                                     is_features_discrete)
        tree[key]['否'] = tree_generate_with_random_feature_selection(sub_data_set_gt, features_list, features_dict,
                                                                     is_features_discrete)
    return tree


if __name__ == '__main__':
    data_set, features_list, features_dict, is_features_discrete = create_data_set_one()
    decision_tree = tree_generate_with_random_feature_selection(data_set, features_list, features_dict,
                                                                is_features_discrete)
    treePlotter.createPlot(decision_tree)

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
    """
    计算gini
    :param data_set:
    :return:
    """
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


def classify_by_tree(input_tree, test_sample, lables_list, labels_dict):
    """
    按照树的结构对测试sample进行分类
    :param input_tree:
    :param test_sample:
    :param lables_list:
    :return:
    """
    feature_name = list(input_tree.keys())[0]
    inferior_tree = input_tree[feature_name]
    feature_index = lables_list.index(feature_name)
    for value in inferior_tree:
        current_sample_feature_key = test_sample[feature_index]
        if labels_dict[feature_name][current_sample_feature_key] == value:
            if type(inferior_tree[value]).__name__ == 'dict':
                return classify_by_tree(inferior_tree[value], test_sample, lables_list, labels_dict)
            else:
                return inferior_tree[value]


def get_validation_error_count_by_tree(input_tree, data_set_validate, labels_list, labels_dict):
    """
    根据决策树，获取验证集中分类错误的个数
    :param input_tree:
    :param data_set_validate:
    :param labels_list:
    :return:
    """
    num_sample = len(data_set_validate)
    error_count = 0
    for i in range(num_sample):
        classify_result = classify_by_tree(input_tree, data_set_validate[i], labels_list, labels_dict)
        if classify_result != data_set_validate[i][-1]:
            error_count += 1
    return error_count


def get_validation_error_count_by_major_class(major_class, data_set_validate):
    """
    根据major_class，获取验证集中分类错误的个数
    :param major_class:
    :param data_set_validate:
    :return:
    """
    num_sample = len(data_set_validate)
    error_count = 0
    for i in range(num_sample):
        if data_set_validate[i][-1] != major_class:
            error_count += 1
    return error_count


def get_validation_error_before_pruning(data_set_train, data_set_validate):
    # 计算划分之前的准确率
    most_common_class = get_most_common_class(data_set_train)
    # 没有划分就相当于将验证集中的所有数据分到 most_common_class 中
    class_list = [sample[-1] for sample in data_set_validate]
    accuracy_rate_before_pruning = class_list.count(most_common_class) / float(len(class_list))
    return accuracy_rate_before_pruning


def get_validation_error_after_pruning(data_set_train, data_set_validate, best_feature_index,
                                       is_feature_discrete, best_continuous_feature_value):
    # 计算划分之后的准确率
    accuracy_rate_after_pruning = 0.0
    if is_feature_discrete:
        sub_features_value_set = [sample[best_feature_index] for sample in data_set_train]
        sub_features_value_set = set(sub_features_value_set)
    else:
        sub_features_value_set = ['是', '否']

    for sub_feature_value in sub_features_value_set:
        # 离散特征值
        if is_feature_discrete:
            split_operate = operator.eq
            delete_col = True
        # 连续特征值
        else:
            sub_feature_value = best_continuous_feature_value
            delete_col = False
            if sub_feature_value == '是':
                split_operate = operator.le
            else:
                split_operate = operator.gt

        sub_data_set_train = split_data_set_by_operate(data_set_train, best_feature_index, sub_feature_value,
                                                       split_operate, delete_col=delete_col)
        sub_data_set_validate = split_data_set_by_operate(data_set_validate, best_feature_index, sub_feature_value,
                                                          split_operate, delete_col=delete_col)
        if len(sub_data_set_validate) == 0:
            continue
        sub_most_common_class = get_most_common_class(sub_data_set_train)
        # 按照feature的某个取值划分之后，该划分上的分类结果看成是 sub_most_common_class
        sub_class_list = [sample[-1] for sample in sub_data_set_validate]
        accuracy_rate_after_pruning += sub_class_list.count(sub_most_common_class) / float(len(sub_class_list)) \
                                       * (len(sub_class_list) / len(data_set_validate))
    return accuracy_rate_after_pruning


def get_keys_for_dict(dict, value):
    return [k for k, v in dict.items() if v == value]

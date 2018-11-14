import operator
from math import log


def create_data_set_one():
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
    features_list = ['色泽', '根蒂', '敲声', '纹理', '脐部', '触感', '密度', '含糖量']
    features_dict = {'色泽': {0: '青绿', 1: '乌黑', 2: '浅白'},
                     '根蒂': {0: '蜷缩', 1: '稍缩', 2: '硬挺'},
                     '敲声': {0: '浊响', 1: '沉闷', 2: '清脆'},
                     '纹理': {0: '清晰', 1: '稍糊', 2: '模糊'},
                     '脐部': {0: '凹陷', 1: '稍凹', 2: '平坦'},
                     '触感': {0: '硬滑', 1: '软粘'},
                     '密度': {},
                     '含糖量': {}}
    is_features_discrete = [1, 1, 1, 1, 1, 1, 0, 0]
    return data_set, features_list, features_dict, is_features_discrete


def create_data_set_two():
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
    features_list = ['色泽', '根蒂', '敲声', '纹理', '脐部', '触感']
    features_dict = {'色泽': {0: '青绿', 1: '乌黑', 2: '浅白'},
                     '根蒂': {0: '蜷缩', 1: '稍缩', 2: '硬挺'},
                     '敲声': {0: '浊响', 1: '沉闷', 2: '清脆'},
                     '纹理': {0: '清晰', 1: '稍糊', 2: '模糊'},
                     '脐部': {0: '凹陷', 1: '稍凹', 2: '平坦'},
                     '触感': {0: '硬滑', 1: '软粘'}}
    is_features_discrete = [1, 1, 1, 1, 1, 1]
    return data_set_train, data_set_validate, features_list, features_dict, is_features_discrete


def is_all_sample_same(data_set):
    """
    检查data_set中的样本在features上的取值都相同
    那如何比较连续特征的值呢
    :param data_set:
    :return:
    """
    for i in range(len(data_set) - 1):
        # 将sample中最后的分类结果去掉，只比较features上的值是否完全一致
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


def classify_by_tree(input_tree, test_sample, features_list, features_dict, is_features_discrete):
    """
    按照树的结构对测试sample进行分类
    :param input_tree:
    :param test_sample:
    :param features_list:
    :param features_dict:
    :param is_features_discrete:
    :return:
    """
    root_node_name = list(input_tree.keys())[0]
    sub_tree = input_tree[root_node_name]
    # split for the case that the feature is continual and it's node name contain "<="
    root_node_name_list = root_node_name.split("<=")
    root_node_name = root_node_name_list[0]
    feature_index = features_list.index(root_node_name)
    continual_feature_value = None
    if is_features_discrete[feature_index] == 0:
        continual_feature_value = float(root_node_name_list[1])

    for feature_value_name in sub_tree:
        sample_feature_value = test_sample[feature_index]
        if is_features_discrete[feature_index] == 1:
            if features_dict[root_node_name][sample_feature_value] == feature_value_name:
                if type(sub_tree[feature_value_name]).__name__ == 'dict':
                    return classify_by_tree(sub_tree[feature_value_name], test_sample, features_list,
                                            features_dict, is_features_discrete)
                else:
                    return sub_tree[feature_value_name]
        else:
            if (feature_value_name == '是' and sample_feature_value <= continual_feature_value) or \
                    (feature_value_name == '否' and sample_feature_value > continual_feature_value):
                if type(sub_tree[feature_value_name]).__name__ == 'dict':
                    return classify_by_tree(sub_tree[feature_value_name], test_sample, features_list,
                                            features_dict, is_features_discrete)
                else:
                    return sub_tree[feature_value_name]


def get_validation_error_count_by_tree(input_tree, data_set_validate, features_list, features_dict,
                                       is_features_discrete):
    """
    根据决策树，获取验证集中分类错误的个数
    :param input_tree:
    :param data_set_validate:
    :param features_list:
    :param features_dict:
    :param is_features_discrete:
    :return:
    """
    num_sample = len(data_set_validate)
    error_count = 0
    for i in range(num_sample):
        classify_result = classify_by_tree(input_tree, data_set_validate[i], features_list, features_dict,
                                           is_features_discrete)
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
        feature_values_list = [sample[best_feature_index] for sample in data_set_train]
        feature_values_list = set(feature_values_list)
    else:
        feature_values_list = ['是', '否']

    for feature_value in feature_values_list:
        # 离散特征值
        if is_feature_discrete:
            split_operate = operator.eq
            delete_col = True
        # 连续特征值
        else:
            feature_value = best_continuous_feature_value
            delete_col = False
            if feature_value == '是':
                split_operate = operator.le
            else:
                split_operate = operator.gt

        sub_data_set_train = split_data_set_by_operate(data_set_train, best_feature_index, feature_value,
                                                       split_operate, delete_col=delete_col)
        sub_data_set_validate = split_data_set_by_operate(data_set_validate, best_feature_index, feature_value,
                                                          split_operate, delete_col=delete_col)
        if len(sub_data_set_validate) == 0:
            continue
        sub_most_common_class = get_most_common_class(sub_data_set_train)
        # 按照feature的某个取值划分之后，该划分上的分类结果看成是 sub_most_common_class
        sub_class_list = [sample[-1] for sample in sub_data_set_validate]
        accuracy_rate_after_pruning += sub_class_list.count(sub_most_common_class) / float(len(sub_class_list)) \
                                       * (len(sub_class_list) / len(data_set_validate))
    return accuracy_rate_after_pruning


def get_keys_for_dict(my_dict, value):
    return [k for k, v in my_dict.items() if v == value]

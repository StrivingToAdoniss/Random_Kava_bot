from collections import Counter


def find_matches(arr1, arr2):
    set1 = set(arr1)
    set2 = set(arr2)
    matches = set1.intersection(set2)
    return len(list(matches))


class Classification:

    def __init__(self, ids, users, n_clusters):
        self.ids = [i for i in range(0, len(ids))]
        self.new_matrix = {}
        self.matrix1 = users
        for i in range(len(self.matrix1)):
            first_el = self.matrix1[i]
            for j in range(len(self.matrix1)):
                if i != j:
                    if not (i, j) or not (j, i) in self.new_matrix:
                        self.new_matrix[(i, j)] = find_matches(first_el, self.matrix1[j])

        self.n_clusters = n_clusters
        self.cluster_size = 4
        self.groups_dict = {}

    def classificate(self):
        self.init_groups()
        self.groups_distribution()

    def init_groups(self):
        sorted_by_value = sorted(self.new_matrix.items(), key=lambda x: x[1])
        cluster_num = 1
        while cluster_num <= self.n_clusters:
            for key, value in sorted_by_value:
                print(key, value)
                for i in key:
                    if len(self.groups_dict) == self.n_clusters:
                        print("groups", self.groups_dict)
                        return
                    if i not in self.groups_dict.keys():
                        self.groups_dict[i] = cluster_num
                        cluster_num += 1

    def groups_distribution(self):
        ids_elements_without = self.ids.copy()
        for group_id in list(self.groups_dict.keys()):
            ids_elements_without.remove(group_id)
        # print(ids_elements_without)
        start_dict_keys = self.groups_dict.copy()
        for id in ids_elements_without:
            list_keys = {}
            for element_key in self.new_matrix.keys():
                for key in start_dict_keys.keys():
                    if id in element_key and key in element_key:
                        list_keys[element_key] = dict(self.new_matrix)[element_key]
            sorted_list = dict(sorted(list_keys.items(), key=lambda x: x[1], reverse=True))
            print('sorted_list', sorted_list)
            ind = True
            el_idx = 0
            while ind:
                if not (len(self.matrix1) % 4 == 1 and ids_elements_without.index(id) == len(ids_elements_without) - 1):
                    res1 = list(sorted_list.keys())[el_idx]
                    print(self.groups_dict)
                    print(res1)
                    keys_list = [*res1]
                    keys_list.remove(id)
                    need_key = keys_list[0]
                    res = Counter(self.groups_dict.values())
                    group = self.groups_dict[need_key]
                    if res[group] < self.cluster_size:
                        self.groups_dict[id] = self.groups_dict[need_key]
                        ind = False
                    else:
                        el_idx += 1
                else:
                    res1 = list(sorted_list.keys())[0]
                    keys_list = [*res1]
                    keys_list.remove(id)
                    need_key = keys_list[0]
                    self.groups_dict[id] = self.groups_dict[need_key]
                    ind = False

    def get_groups(self):
        dict_keys = list(self.groups_dict.keys())
        dict_keys.sort()
        sorted_dict = {i: self.groups_dict[i] for i in dict_keys}
        return list(sorted_dict.values())

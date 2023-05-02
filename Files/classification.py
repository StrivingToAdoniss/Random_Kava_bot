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
        self.remainder = len(self.matrix1) % self.cluster_size

    def classificate(self):
        self.init_groups()
        self.groups_distribution()

    def init_groups(self):
        sorted_by_value = sorted(self.new_matrix.items(), key=lambda x: x[1])
        cluster_num = 1
        while cluster_num <= self.n_clusters:
            for key, value in sorted_by_value:
                # print(key, value)
                for i in key:
                    if len(self.groups_dict) == self.n_clusters:
                        # print("groups", self.groups_dict)
                        return
                    if i not in self.groups_dict.keys():
                        self.groups_dict[i] = cluster_num
                        cluster_num += 1

    def groups_distribution(self):
        ids_elements_without = self.ids.copy()
        for group_id in list(self.groups_dict.keys()):
            ids_elements_without.remove(group_id)
        start_dict_keys = self.groups_dict.copy()

        for id in ids_elements_without:
            list_keys = {}
            for element_key in self.new_matrix.keys():
                for key in start_dict_keys.keys():
                    if id in element_key and key in element_key:
                        list_keys[element_key] = dict(self.new_matrix)[element_key]
            sorted_list = dict(sorted(list_keys.items(), key=lambda x: x[1], reverse=True))
            ind = True
            el_idx = 0
            while ind:
                res1 = list(sorted_list.keys())[el_idx]
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
        print(self.groups_dict)

        if self.remainder != 0 and len(self.ids)>self.cluster_size:
            print("hereeeeeeeeeeeeee")
            lack_users = []
            res = Counter(self.groups_dict.values())
            print(res)

            for key, value in res.items():
                print("now here")
                if value <= 2:
                    print(key, value)
                    users = [i for i in self.groups_dict if self.groups_dict[i] == key][:self.cluster_size-1 - self.remainder]

                    for user in users:
                        reorganise_list = {}
                        if user not in lack_users:
                            lack_users.append(user)
                            for matrix_element in self.new_matrix.keys():
                                if user in matrix_element:
                                    reorganise_list[matrix_element] = dict(self.new_matrix)[matrix_element]

                        sorted_list = dict(sorted(reorganise_list.items(), key=lambda x: x[1], reverse=True))
                        print(sorted_list)
                        index = True
                        index_el = 0
                        while index:

                            print("index", index_el)
                            res1 = list(sorted_list.keys())[index_el]
                            keys_list = [*res1]
                            print("keys list", keys_list)

                            keys_list.remove(user)
                            need_key = keys_list[0]

                            group = self.groups_dict[need_key]
                            print("res group",res[group])
                            res = Counter(self.groups_dict.values())
                            if res[group] == self.cluster_size and self.groups_dict[user] != self.groups_dict[need_key]:
                                self.groups_dict[need_key] = key
                                print(Counter(self.groups_dict.values()))
                                index = False
                            else:
                                index_el += 1
                            res = Counter(self.groups_dict.values())
                            new_idx = False
                            for key_new, value_new in res.items():
                                print("now here")
                                if value_new <= 2:
                                    new_idx = True
                                    break
                            index = new_idx
                        print(self.groups_dict)


        print(self.groups_dict)


    def get_groups(self):
        dict_keys = list(self.groups_dict.keys())
        dict_keys.sort()
        sorted_dict = {i: self.groups_dict[i] for i in dict_keys}
        return list(sorted_dict.values())

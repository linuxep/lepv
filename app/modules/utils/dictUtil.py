
class DictUtil:

    '''
    compare two dicts.
    If the two dicts are equal, return 0;
    If the first one contains the second one ( first one is a superset of the second), return 1;
    If the second one contains the first one ( first one is a subset of the second ), return -1;
    Otherwise, return 2;
    '''
    @staticmethod
    def compare(dict_1, dict_2):
        # Store the keys of the dictionary in the collection,
        # if dict_1 is None, set(dict_1) will return empty collection.
        tdict_1 = set(dict_1)
        tdict_2 = set(dict_2)
    
        flag = 2
    
        # If the keys are exactly equal, and then judge whether
        # the value of the key corresponding to the equal.
        if tdict_1 == tdict_2:
            flag = 0
            for key in tdict_1:
                if dict_1[key] != dict_2[key]:
                    if isinstance(dict_1[key], dict):
                        flag = DictUtil.compare(dict_1[key], dict_2[key])
                    else:
                        return 2
            return flag
    
        # If the keys of dict_1 contains the keys of dict_2, and then
        # judge the value of the dict_2's key corresponding to the equal.
        elif tdict_1 > tdict_2:
            flag = 1
            for key in dict_2:
                if dict_1[key] != dict_2[key]:
                    if isinstance(dict_1[key], dict):
                        flag = DictUtil.compare(dict_1[key], dict_2[key])
                    else:
                        return 2
            return flag
    
        # If the keys of dict_2 contains the keys of dict_1, and then
        # judge the value of the dict_1's key corresponding to the equal.
        elif tdict_1 < tdict_2:
            flag = -1
            for key in dict_1:
                if dict_1[key] != dict_2[key]:
                    if isinstance(dict_1[key], dict):
                        flag = DictUtil.compare(dict_1[key], dict_2[key])
                    else:
                        return 2
        return flag
    

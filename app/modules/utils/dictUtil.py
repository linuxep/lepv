
class DictUtil:

    '''
    Compare two dicts.
    If the two dicts are equal, return 0;
    If the first one contains the second one ( first one is a superset of the second), return 1;
    If the second one contains the first one ( first one is a subset of the second ), return -1;
    Otherwise, return 2;
    '''
    @staticmethod
    def compare(dict_1, dict_2):
        return 0
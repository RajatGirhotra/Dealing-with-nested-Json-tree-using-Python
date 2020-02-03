import sys
import json
import collections
import itertools
from collections import Counter, defaultdict

try:
    with open(sys.argv[1], 'r') as jsonfile:
        data = json.load(jsonfile)
except IndexError:
    print ("Error ")


def findkeys(node, kv):
    if isinstance(node, list):
        for i in node:
            for x in findkeys(i, kv):
               yield x
    elif isinstance(node, dict):
        if kv in node:
            yield node[kv]
        for j in node.values():
            for x in findkeys(j, kv):
                yield x


def values(obj, key):
    #Pull all values of specified key from nested JSON.
    arr = []

    def extract(obj, arr, key):
        #Recursively search for values of key in JSON tree
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    for i in obj:
                        if i == 'size':
                            arr.append(v)
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    results = extract(obj, arr, key)
    return(arr)


def printing_values():
    '''Making two different array's containing all file name and file size respectively'''
    
    file_name = values(data, 'name')
    file_size = values(data, 'size')
    
    schema_dict = dict(zip(file_name, file_size))
    
    ''' Zipping two array's together into a dict to find key's with same value  '''
    val_map = collections.defaultdict(list)
    for k,v in schema_dict.items():
        val_map[v].append(k)
    
    print ('List with same value: ',val_map)

def main(argv1):
    counter = Counter(list(findkeys(data, 'type')))
    print('Total Count :', counter)
    print('Total size of Files : ', sum(list(findkeys(data, 'size'))))
    printing_values()

if __name__ == "__main__":
    try: 
        main(sys.argv[1])
    except IndexError:
        print ("Please specify the path for Json file... for example python3 taskPython.py '/xxx/xxx/xxx/xxx.json' ")
    





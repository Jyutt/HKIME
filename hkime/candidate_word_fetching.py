#Last Updated: 12/21/2019
# Not needed / used, deprecate?

from functools import reduce
import json

#Make sure there is an file already created
FILEPATH = './tree_dictionary.txt'

#add an element: root[path][key] = data
def add_element_to_path(root, path, key, data):
    if key == 'char': #dictionary['char'] is a list
        reduce(lambda x, y : x[y], path, root)[key].append(data)
    else:
        reduce(lambda x, y : x[y], path, root)[key] = data

#return value at path: return root[path]
def peek_path(root, path):
    return reduce(lambda x, y : x[y], path, root)

def python_dict_to_json(root, file_path):
    try:
        file_object = open(file_path, 'w')
        json.dump(root, file_object)
        print(file_path, "created.")
    except FileNotFoundError:
        print(file_path, "not found.")

#example dictionary tree structure
"""
{
    j : {
        next : {
            y : {
                next : dict()
                char : [(chinese characters for jy)]
            }
        }
        char : None
    }
    c : {
        next : dict()
        char : [(chinese characters for c)]
    }
}
"""
#Run file once to get json dictionary
def generate_json_tree():
    json_fetch_tree_root = dict()
    with open("JPTable-iso.txt", 'r') as f:
        file_content = f.read()
        for dict_entry in file_content.strip().split('\n'):
            try:
                #load values from single jyutping dictionary entry
                jyutping_entry = dict_entry.split()
                #possible multiple jyutpings for the same character
                id, chinese_char, jyutping_list = jyutping_entry[0], jyutping_entry[1], jyutping_entry[2:]
                for jyutping in jyutping_list:
                    path_stack = []
                    #loop through characters to build tree
                    for i in range(len(jyutping)):
                        letter = jyutping[i]
                        if letter in peek_path(json_fetch_tree_root, path_stack):
                            path_stack.append(letter)
                            if i == len(jyutping) - 1:
                                add_element_to_path(json_fetch_tree_root, path_stack,
                                                    "char", chinese_char)
                        else:
                            node = dict()
                            node["next"] = dict()
                            if i == len(jyutping) - 1:
                                node["char"] = [chinese_char]
                            else:
                                node["char"] = None
                            add_element_to_path(json_fetch_tree_root, path_stack, 
                                                letter, node)
                            path_stack.append(letter)
                        path_stack.append("next")
            except Exception as e:
                print("File entry wrong format, entry:", dict_entry.split())
                print(e)
        python_dict_to_json(json_fetch_tree_root, FILEPATH)

if __name__ == '__main__':
    generate_json_tree()

#Last Updated: 12/21/2019

from functools import reduce
import json

FILEPATH = './tree_dictionary.txt'

def peek_path(root, path):
    return reduce(lambda x, y : x[y], path, root)

def python_json_to_dict(file_path):
    try:
        with open(file_path, 'r') as f:
            dict_object = json.load(f)
    except FileNotFoundError:
        print(file_path, "not found.")
    return dict_object

def test_jyutping(root, jyutping):
    path_stack = []
    for letter in jyutping:
        path_stack.append(letter)
        path_stack.append('next')
    return peek_path(root, path_stack[:-1] + ['char'])

def test_word_fetch():
    root = python_json_to_dict(FILEPATH)
    assert('㹺' in test_jyutping(root, 'daat3'))
    assert('㺩' in test_jyutping(root, 'gau6'))
    assert('㺱' in test_jyutping(root, 'jing4'))
    #extra test cases

if __name__ == '__main__':
    test_word_fetch()
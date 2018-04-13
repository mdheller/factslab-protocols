from predpatt import load_conllu
from predpatt import PredPatt
import json
import os
import re


def replace_string(s):
    '''
    Make some changes to the input string to make it Turk readable
    '''

    # replace all single quotes by double quotes : except at the start/end of the list
    s = re.sub(r'([^\]])\"', r'\1""', s)

    # replace single quotes
    s = re.sub(r"\'\{", r"{", s)
    s = re.sub(r"\}\'", r"}", s)

    # replace two backslash to three
    s = re.sub(r"\\\\", r"\\\\\\", s)

    # remove spaces before and after span
    s = re.sub(r"> ", r">", s)
    s = re.sub(r" <", r"<", s)

    return s


id = 1
out_data = []
global_list = []
file = '/UD_English-r1.2/en-ud-dev.conllu'
path = os.getcwd() + file
with open(path, 'r') as infile:
    data = infile.read()
    parsed = [PredPatt(ud_parse) for sent_id, ud_parse in load_conllu(data)]
    # random.shuffle(parsed)
    for parse_sen in parsed:
        for predicate in parse_sen.instances:
            raw_sentence = [token.text for token in parse_sen.tokens]
            pred_token = predicate.root.position
            pred = predicate.root.text
            for argument in predicate.arguments:
                token_dict = {}
                noun = " ".join(token.text for token in argument.tokens)
                noun_token = raw_sentence.index(noun.split()[0])
                pred_sentence = raw_sentence.copy()
                noun_sentence = raw_sentence.copy()
                pred_sentence.insert(pred_token, '<span class=\"predicate\">')
                pred_sentence.insert(pred_token + 2, '</span>')
                noun_sentence.insert(noun_token, '<span class=\"noun\">')
                noun_sentence.insert(noun_token + 1 + len(noun.split()), '</span>')
                token_dict['raw_sentence'] = " ".join(raw_sentence)
                token_dict['id'] = id
                token_dict['pred'] = pred
                token_dict['pred_token'] = str(pred_token)
                token_dict['noun'] = noun
                token_dict['noun_token'] = str(noun_token)
                token_dict['pred_sentence'] = " ".join(pred_sentence)
                token_dict['noun_sentence'] = " ".join(noun_sentence)
                id += 1
                if id == 11:
                    id = 0
                if len(out_data) == 10:
                    global_list.append(out_data)
                    out_data = []
                    out_data.append(json.dumps(token_dict))
                else:
                    out_data.append(json.dumps(token_dict))

with open('dataset.csv', 'w+') as file_handler:
    file_handler.write("var_arrays\n")
    for item in global_list:
        local_str = "\"" + str(item) + "\"\n"
        file_handler.write(local_str)

with open('dataset.csv', 'r') as f_in:
    lines = f_in.readlines()
    with open('dataset_turk.csv', 'w+') as f_out:
        for item in lines:
            f_out.write(replace_string(item))

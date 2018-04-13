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
files = ['/UD_English-r1.2/en-ud-train.conllu', '/UD_English-r1.2/en-ud-dev.conllu', '/UD_English-r1.2/en-ud-test.conllu']
for file in files:
    path = os.getcwd() + file
    with open(path, 'r') as infile:
        data = infile.read()
        data = re.sub(r'\'', r'&#39;', data)
        data = re.sub(r'\"', r'&quot;', data)
        data = re.sub(r'\[', r'&lsqb;', data)
        data = re.sub(r'\]', r'&rsqb;', data)
        parsed = [PredPatt(ud_parse) for sent_id, ud_parse in load_conllu(data)]
        # random.shuffle(parsed)
        for parse_sen in parsed:
            for predicate in parse_sen.instances:
                raw_sentence = " ".join([token.text for token in parse_sen.tokens])
                pred_token = predicate.root.position
                pred = predicate.root.text
                for argument in predicate.arguments:
                    token_dict = {}
                    noun = argument.root.text
                    noun_token = raw_sentence.split().index(noun)
                    pred_sentence = raw_sentence.split().copy()
                    noun_sentence = raw_sentence.split().copy()
                    pred_sentence.insert(pred_token, '<span class=\"predicate\">')
                    pred_sentence.insert(pred_token + 2, '</span>')
                    noun_sentence.insert(noun_token, '<span class=\"noun\">')
                    noun_sentence.insert(noun_token + 1, '</span>')
                    token_dict['raw_sentence'] = raw_sentence
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

with open('bad_dataset.csv', 'w+') as file_handler:
    file_handler.write("var_arrays\n")
    for item in global_list:
        local_str = "\"" + str(item) + "\"\n"
        file_handler.write(local_str)

with open('bad_dataset.csv', 'r') as f_in:
    lines = f_in.readlines()
    with open('dataset.csv', 'w+') as f_out:
        for item in lines:
            f_out.write(replace_string(item))

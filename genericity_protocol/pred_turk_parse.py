from predpatt import load_conllu
from predpatt import PredPatt
import json
from os.path import expanduser
import re
import random


def html_ify(s):
    '''
        Takes care of &quot &lsqb &rsqb &#39
    '''

    html_string = re.sub(r'\'', r'&#39;', s)
    html_string = re.sub(r'\"', r'&quot;', html_string)
    html_string = re.sub(r'\[', r'&lsqb;', html_string)
    html_string = re.sub(r'\]', r'&rsqb;', html_string)
    return html_string


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
files = ['/UD_English-r1.2/en-ud-train.conllu', '/UD_English-r1.2/en-ud-dev.conllu', '/UD_English-r1.2/en-ud-test.conllu']
home = expanduser("~/Downloads/")
parsed = []
out_data = []

for file in files:
    path = home + file
    with open(path, 'r') as infile:
        data = infile.read()
        parsed += [(path[-17:] + " " + sent_id, PredPatt(ud_parse)) for
            sent_id, ud_parse in load_conllu(data)]

random.shuffle(parsed)

with open('pred_dataset.csv', 'w+') as outfile:
    outfile.write("var_arrays\n")
    for sent_id, parse_sen in parsed:
        raw_sentence = " ".join([token.text for token in parse_sen.tokens])
        raw_sentence = html_ify(raw_sentence)
        for predicate in parse_sen.instances:
            token_dict = {}
            pred_token = predicate.root.position
            pred = predicate.root.text
            pred_sentence = raw_sentence.split().copy()
            pred_sentence.insert(pred_token, ' <span class=\"predicate\">')
            pred_sentence.insert(pred_token + 2, '</span> ')
            token_dict['raw_sentence'] = raw_sentence
            token_dict['id'] = id
            token_dict['pred'] = pred
            token_dict['pred_token'] = str(pred_token)
            token_dict['pred_sentence'] = " ".join(pred_sentence)
            token_dict['sent_id'] = sent_id
            out_data.append(json.dumps(token_dict))
            id += 1
            if id == 11:
                id = 1
                outfile.write("\"" + replace_string(str(out_data)) + "\"\n")
                out_data = []
    outfile.write("\"" + replace_string(str(out_data)) + "\"\n")

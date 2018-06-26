from predpatt import load_conllu
from predpatt import PredPatt
from predpatt import PredPattOpts
import json
from os.path import expanduser
import re
import random
from pilot_ids import pilot_ids
import pdb

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


files = ['/UD_English-r1.2/en-ud-dev.conllu',
         '/UD_English-r1.2/en-ud-test.conllu']
home = expanduser("~/Downloads/")
parsed = {'train': [], 'devte': []}
out_data = []

options = PredPattOpts(resolve_relcl=True, borrow_arg_for_relcl=True, resolve_conj=False)  # Resolve relative clause

path = home + '/UD_English-r1.2/en-ud-train.conllu'
with open(path, 'r') as infile:
    data = infile.read()
    parsed['train'] += [('en-ud-train.conllu' + " " + sent_id, PredPatt(ud_parse, opts=options)) for sent_id, ud_parse in load_conllu(data)]

for file in files:
    path = home + file
    with open(path, 'r') as infile:
        data = infile.read()
        parsed['devte'] += [(file[17:] + " " + sent_id, PredPatt(ud_parse, opts=options)) for
            sent_id, ud_parse in load_conllu(data)]

c = {'train': 0, 'devte': 0}
ign = {'train': 0, 'devte': 0}
prons_incl = ["you", "they", "yourself", "themselves", "them", "themself",
              "theirself", "theirselves"]

for write_file in ['noun_train_data.csv', 'noun_devte_data.csv']:
    dat = write_file[5:10]
    with open(write_file, 'w+') as outfile:
        id = 1
        outfile.write("var_arrays\n")
        for sent_id, parse_sen in parsed[dat]:
            raw_sentence = " ".join([token.text for token in parse_sen.tokens])
            html_sentence = html_ify(raw_sentence)
            sent_args = []
            for predicate in parse_sen.instances:
                if predicate.root.tag in ["NOUN"]:
                    # Include noun predicates in arguments
                    all_args = predicate.arguments + [predicate]
                else:
                    all_args = predicate.arguments
                sent_check = [x.position for x in sent_args]
                for each_arg in all_args:
                    if each_arg.position not in sent_check:
                        sent_args.append(each_arg)

            for argument in sent_args:
                if argument.root.tag in ["DET", "NUM", "NOUN", "PROPN", "PRON"]:
                    if argument.root.tag == "PRON":
                        if argument.root.text.lower() not in prons_incl:
                            ign[dat] += 1
                            continue
                    c[dat] += 1
                    noun = argument.root.text
                    token_dict = {}
                    noun = html_ify(noun)
                    noun_token = argument.root.position
                    noun_sentence = html_sentence.split().copy()
                    noun_sentence.insert(noun_token, ' <span class=\"noun\">')
                    noun_sentence.insert(noun_token + 2, '</span> ')
                    token_dict['raw_sentence'] = html_sentence
                    token_dict['id'] = id
                    token_dict['noun'] = noun
                    token_dict['noun_token'] = html_ify(str(noun_token))
                    token_dict['noun_sentence'] = " ".join(noun_sentence)
                    token_dict['sent_id'] = html_ify(sent_id)
                    token_dict['predicate'] = html_ify(predicate.root.text)
                    token_dict['pred_token'] = html_ify(str(predicate.root.position))
                    out_data.append(json.dumps(token_dict))
                    id += 1
                    if id == 11:
                        id = 1
                        outfile.write("\"" + replace_string(str(out_data)) + "\"\n")
                        out_data = []
        outfile.write("\"" + replace_string(str(out_data)) + "\"\n")
        out_data = []
print("INCL", c, "IGN", ign)

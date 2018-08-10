from predpatt import load_conllu
from predpatt import PredPatt
import json
from os.path import expanduser
import re
import random
from pilot_ids import pilot_ids


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


copula_verbs = ['be', 'am', 'is', 'are', 'was', 'were', 'being', 'been']

id = 1
files = ['/UD_English-r1.2/en-ud-train.conllu', '/UD_English-r1.2/en-ud-dev.conllu']
home = expanduser("~/Downloads/")
parsed = []
out_data = []

for file in files:
    path = home + file
    with open(path, 'r') as infile:
        data = infile.read()
        parsed += [(file[17:] + " " + sent_id, PredPatt(ud_parse)) for
            sent_id, ud_parse in load_conllu(data)]

random.shuffle(parsed)
pilot_ids = pilot_ids()             # If you want to do pilot study
pilot_parsed = []

for sent_id in pilot_ids:
    for x, y in parsed:
        if x == sent_id:
            ud_parse = y
            break
    pilot_parsed.append((sent_id, ud_parse))

with open('noun_dataset.csv', 'w+') as outfile:
    outfile.write("var_arrays\n")
    # Replace parsed with pilot_parsed for pilot data
    for sent_id, parse_sen in parsed:
        raw_sentence = " ".join([token.text for token in parse_sen.tokens])
        raw_sentence = html_ify(raw_sentence)
        # if len(parse_sen.instances) == 1:
        for predicate in parse_sen.instances:
            # if predicate.root.tag == "NOUN":
                # pred = list(set(raw_sentence.split()) & set(copula_verbs))[0]
                # pred_pos = raw_sentence.split().index(pred)
            # else:
                # pred = predicate.root.text
                # pred_pos = predicate.root.position
            # for argument in (predicate.arguments + [predicate]):
            # if len(predicate.arguments) == 3:
            for argument in predicate.arguments:
                if argument.root.gov_rel in ['nsubj', 'dobj', 'obj', 'iobj', 'obl', 'vocative', 'expl', 'nmod', 'appos', 'nummod']:
                    noun = argument.root.text
                    token_dict = {}
                    noun = html_ify(noun)
                    noun_token = argument.root.position
                    noun_sentence = raw_sentence.split().copy()
                    noun_sentence.insert(noun_token, ' <span class=\"noun\">')
                    noun_sentence.insert(noun_token + 2, '</span> ')
                    token_dict['raw_sentence'] = raw_sentence
                    token_dict['id'] = id
                    token_dict['noun'] = noun
                    token_dict['noun_token'] = str(noun_token)
                    token_dict['noun_sentence'] = " ".join(noun_sentence)
                    token_dict['sent_id'] = sent_id
                    token_dict['predicate'] = predicate.root.text
                    token_dict['pred_token'] = predicate.root.position
                    out_data.append(json.dumps(token_dict))
                    # print(sent_id, " ".join(noun_sentence))

                    id += 1
                    if id == 11:
                        id = 1
                        outfile.write("\"" + replace_string(str(out_data)) + "\"\n")
                        out_data = []

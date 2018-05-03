from predpatt import load_conllu
from predpatt import PredPatt
import json
from os.path import expanduser
import re
import random
from pilot_ids import pilot_ids


def htmlify(s):
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


copula_verbs = ['be', 'am', 'is', 'are', 'was', 'were', 'being', 'been', 'r',
                '&#39;m', '&#39;s', 's']

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

# Create dictionary for each predicate token and write as json dump
# Create a new line after every 10 tokens - each HIT has 10 questions
with open('pilot_pred_dataset.csv', 'w+') as outfile:
    outfile.write("var_arrays\n")
    for sent_id, parse_sen in pilot_parsed:
        raw_sentence = " ".join([token.text for token in parse_sen.tokens])
        html_sentence = htmlify(raw_sentence)
        for predicate in parse_sen.instances:
            # print(raw_sentence, parse_sen.instances)
            if predicate.root.tag != "VERB":
                try:
                    pred = list(set(html_sentence.lower().split()) & set(copula_verbs))[0]
                    pred_token = html_sentence.split().index(pred)
                except IndexError:
                    pred = predicate.root.text
                    pred_token = predicate.root.position
                # print("PRED1:", pred)
            else:
                pred = predicate.root.text
                pred_token = predicate.root.position
                # print("PRED2:", pred, predicate.root.tag)
            token_dict = {}
            pred_sentence = html_sentence.split().copy()
            pred_sentence.insert(pred_token, ' <span class=\"predicate\">')
            pred_sentence.insert(pred_token + 2, '</span> ')
            token_dict['raw_sentence'] = html_sentence
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
    # outfile.write("\"" + replace_string(str(out_data)) + "\"\n")

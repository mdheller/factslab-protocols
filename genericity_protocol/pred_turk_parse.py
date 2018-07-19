from predpatt import load_conllu
from predpatt import PredPatt
from predpatt import PredPattOpts
from predpatt.filters import isNotCopula
import json
from os.path import expanduser
import re
import pdb


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


id = 1
files = ['/UD_English-r1.2/en-ud-dev.conllu',
         '/UD_English-r1.2/en-ud-test.conllu']
home = expanduser("~/Downloads/")
parsed = {'train': [], 'devte': []}
out_data = []

# Resolve relative clause
options = PredPattOpts(resolve_relcl=True, borrow_arg_for_relcl=True, resolve_conj=False)

path = home + '/UD_English-r1.2/en-ud-train.conllu'
with open(path, 'r') as infile:
    data = infile.read()
    parsed['train'] += [('en-ud-train.conllu' + " " + sent_id, PredPatt(ud_parse, opts=options)) for sent_id, ud_parse in load_conllu(data)]

for file in files:
    path = home + file
    with open(path, 'r') as infile:
        data = infile.read()
        parsed['devte'] += [(file[17:] + " " + sent_id, PredPatt(ud_parse, opts=options)) for sent_id, ud_parse in load_conllu(data)]
# random.shuffle(parsed['train'])
c = {'train': 0, 'devte': 0}
d = {'train': 0, 'dev': 0, 'test': 0}
copp = {'train': 0, 'devte': 0}
auxverb = {'train': 0, 'devte': 0}
ign = {'train': 0, 'devte': 0}

for write_file in ['pred_train_data.csv', 'pred_devte_data.csv']:
    dat = write_file[5:10]
    with open(write_file, 'w+') as outfile:
        id = 1
        outfile.write("var_arrays\n")
        for sent_id, parse_sen in parsed[dat]:
            raw_sentence = " ".join([token.text for token in parse_sen.tokens])
            html_sentence = htmlify(raw_sentence)
            sent_preds = []
            split = sent_id[6:11].strip('.c')
            for predicate in parse_sen.instances:
                sent_check = [pr.position for pr in sent_preds]
                if predicate.position not in sent_check:
                    sent_preds.append(predicate)

            for predicate in sent_preds:
                if predicate.root.tag not in ["ADJ", "NOUN", "NUM", "DET", "PROPN", "PRON", "VERB", "AUX"]:
                    ign[dat] += 1
                    continue
                if predicate.root.tag not in ["VERB", "AUX"]:
                    gov_rels = [tok.gov_rel for tok in predicate.tokens]
                    all_pred = [t for t in predicate.tokens]
                    if 'cop' in gov_rels:
                        # Highlight from cop to end of pred.text
                        copp[dat] += 1
                        cop_pos = gov_rels.index('cop')
                        pred = [x.text for x in all_pred[cop_pos:]]
                        pred_token = [x.position for x in all_pred[cop_pos:]]
                    else:
                        ign[dat] += 1
                        continue
                else:
                    # Just choose the verb or aux root as pred
                    auxverb[dat] += 1
                    pred = [predicate.root.text]
                    pred_token = [predicate.root.position]
                c[dat] += 1
                d[split] += 1
                token_dict = {}
                pred_sentence = html_sentence.split().copy()
                acc = 0
                for ins in pred_token:
                    pred_sentence.insert(ins + acc, ' <span class=\"predicate\">')
                    pred_sentence.insert(ins + acc + 2, '</span> ')
                    acc += 2
                token_dict['raw_sentence'] = html_sentence
                token_dict['id'] = id
                token_dict['predicate'] = htmlify(" ".join(pred))
                pred_token = ",".join(map(str, pred_token))
                token_dict['pred_token'] = htmlify(pred_token)
                token_dict['pred_sentence'] = " ".join(pred_sentence)
                token_dict['sent_id'] = sent_id
                token_dict['pred_root_pos'] = str(predicate.root.position)
                out_data.append(json.dumps(token_dict))
                id += 1
                if id == 11:
                    id = 1
                    outfile.write("\"" + replace_string(str(out_data)) + "\"\n")
                    out_data = []
        outfile.write("\"" + replace_string(str(out_data)) + "\"\n")
        out_data = []
print("INCL", c, "COP", copp, "VERB", auxverb, "IGN", ign)
print("SPLIT", d)

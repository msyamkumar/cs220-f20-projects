#!/usr/bin/python

import json
import os
import subprocess
import sys
import importlib
import inspect
import traceback
import re, ast, math
from collections import namedtuple, OrderedDict, defaultdict
from functools import wraps
from cleanMAC import clean

clean()

PASS = 'PASS'
FAIL_STDERR = 'Program produced an error - please scroll up for more details.'
FAIL_JSON = 'Expected program to print in json format. Make sure the only print statement is a print(json.dumps...)!'
EPSILON = 0.0001

obfuscate1 = "Tweet"
obfuscate2 = ['tweet_id', 'username', 'num_liked', 'length']
TEXT_FORMAT = "text"
PNG_FORMAT = "png"
Question = namedtuple("Question", ["number", "weight", "format"])
Tweet = namedtuple(obfuscate1, obfuscate2)

questions = [
    # stage 1
    Question(number=1, weight=1, format=TEXT_FORMAT),
    Question(number=2, weight=1, format=TEXT_FORMAT),
    Question(number=3, weight=1, format=TEXT_FORMAT),
    Question(number=4, weight=1, format=TEXT_FORMAT),
    Question(number=5, weight=1, format=TEXT_FORMAT),
    Question(number=6, weight=1, format=PNG_FORMAT),
    Question(number=7, weight=1, format=PNG_FORMAT),
    Question(number=8, weight=1, format=PNG_FORMAT),
    Question(number=9, weight=1, format=TEXT_FORMAT),
    Question(number=10, weight=1, format=TEXT_FORMAT),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1, format=PNG_FORMAT),
    Question(number=13, weight=1, format=PNG_FORMAT),
    Question(number=14, weight=1, format=TEXT_FORMAT),
    Question(number=15, weight=1, format=TEXT_FORMAT),
    Question(number=16, weight=1, format=TEXT_FORMAT),
    Question(number=17, weight=1, format=TEXT_FORMAT),
    Question(number=18, weight=1, format=TEXT_FORMAT),
    Question(number=19, weight=1, format=TEXT_FORMAT),
    Question(number=20, weight=1, format=TEXT_FORMAT),
]

question_nums = set([q.number for q in questions])

expected_json = {
    "1": 445,
    "2": {'USERID_1',
            'USERID_9',
            'USERID_4',
            'USERID_7',
            'USERID_6',
            'USERID_2',
            'USERID_10',
            'USERID_8',
            'USERID_3',
            'USERID_5'},
    "3": {'USERID_1': 52,
           'USERID_7': 55,
           'USERID_10': 45,
           'USERID_9': 44,
           'USERID_4': 35,
           'USERID_6': 51,
           'USERID_3': 39,
           'USERID_2': 47,
           'USERID_5': 46,
           'USERID_8': 31},
    "4": {'USERID_1': 9393,
           'USERID_7': 9851,
           'USERID_10': 9936,
           'USERID_9': 9728,
           'USERID_4': 9618,
           'USERID_6': 9149,
           'USERID_3': 9678,
           'USERID_2': 869000000,
           'USERID_5': 9608,
           'USERID_8': 915000},
    "5": {'USERID_1': 150,
           'USERID_7': 144,
           'USERID_10': 136,
           'USERID_9': 137,
           'USERID_4': 138,
           'USERID_6': 145,
           'USERID_3': 138,
           'USERID_2': 138,
           'USERID_5': 146,
           'USERID_8': 145},
    "9": 'USERID_2',
    "10": [Tweet(tweet_id='1467894593', username='USERID_2', num_liked='869M', length=136),
            Tweet(tweet_id='1467875163', username='USERID_2', num_liked=9891, length=69),
            Tweet(tweet_id='1467862806', username='USERID_2', num_liked=9465, length=68),
            Tweet(tweet_id='1467907751', username='USERID_2', num_liked=9048, length=110),
            Tweet(tweet_id='1467928764', username='USERID_2', num_liked=9026, length=41),
            Tweet(tweet_id='1467943007', username='USERID_2', num_liked=9000, length=130),
            Tweet(tweet_id='1467918682', username='USERID_2', num_liked=8884, length=102),
            Tweet(tweet_id='1467935121', username='USERID_2', num_liked=8740, length=37),
            Tweet(tweet_id='1467947913', username='USERID_2', num_liked=8578, length=36),
            Tweet(tweet_id='1467892667', username='USERID_2', num_liked=8270, length=20),
            Tweet(tweet_id='1467897316', username='USERID_2', num_liked=7890, length=64),
            Tweet(tweet_id='1467854917', username='USERID_2', num_liked=7741, length=30),
            Tweet(tweet_id='1467961106', username='USERID_2', num_liked=7552, length=65),
            Tweet(tweet_id='1467951252', username='USERID_2', num_liked=7515, length=48),
            Tweet(tweet_id='1467889988', username='USERID_2', num_liked=7394, length=51),
            Tweet(tweet_id='1467916959', username='USERID_2', num_liked=7081, length=69),
            Tweet(tweet_id='1467874916', username='USERID_2', num_liked=6935, length=23),
            Tweet(tweet_id='1467855981', username='USERID_2', num_liked=6455, length=92),
            Tweet(tweet_id='1467872247', username='USERID_2', num_liked=6316, length=137),
            Tweet(tweet_id='1467918850', username='USERID_2', num_liked=5383, length=103),
            Tweet(tweet_id='1467919055', username='USERID_2', num_liked=5370, length=68),
            Tweet(tweet_id='1467915670', username='USERID_2', num_liked=5287, length=138),
            Tweet(tweet_id='1467880442', username='USERID_2', num_liked=5125, length=96),
            Tweet(tweet_id='1467896253', username='USERID_2', num_liked=4906, length=91),
            Tweet(tweet_id='1467962897', username='USERID_2', num_liked=4898, length=98),
            Tweet(tweet_id='1467855812', username='USERID_2', num_liked=4806, length=28),
            Tweet(tweet_id='1467930220', username='USERID_2', num_liked=4770, length=94),
            Tweet(tweet_id='1467852031', username='USERID_2', num_liked=4565, length=63),
            Tweet(tweet_id='1467905378', username='USERID_2', num_liked=4420, length=111),
            Tweet(tweet_id='1467877833', username='USERID_2', num_liked=4270, length=89),
            Tweet(tweet_id='1467870866', username='USERID_2', num_liked=4166, length=82),
            Tweet(tweet_id='1467879984', username='USERID_2', num_liked=3694, length=69),
            Tweet(tweet_id='1467898511', username='USERID_2', num_liked=3477, length=99),
            Tweet(tweet_id='1467926632', username='USERID_2', num_liked=2602, length=98),
            Tweet(tweet_id='1467862213', username='USERID_2', num_liked=2455, length=138),
            Tweet(tweet_id='1467878633', username='USERID_2', num_liked=2351, length=33),
            Tweet(tweet_id='1467878971', username='USERID_2', num_liked=2238, length=27),
            Tweet(tweet_id='1467953090', username='USERID_2', num_liked=1896, length=64),
            Tweet(tweet_id='1467908798', username='USERID_2', num_liked=1659, length=51),
            Tweet(tweet_id='1467918015', username='USERID_2', num_liked=1508, length=97),
            Tweet(tweet_id='1467926444', username='USERID_2', num_liked=1394, length=61),
            Tweet(tweet_id='1467914499', username='USERID_2', num_liked=910, length=138),
            Tweet(tweet_id='1467968584', username='USERID_2', num_liked=777, length=132),
            Tweet(tweet_id='1467933102', username='USERID_2', num_liked=625, length=135),
            Tweet(tweet_id='1467953277', username='USERID_2', num_liked=494, length=31),
            Tweet(tweet_id='1467890222', username='USERID_2', num_liked=227, length=107),
            Tweet(tweet_id='1467871956', username='USERID_2', num_liked=110, length=68)],
    "11": 5003.565217391304,
    "14": [],
    "15": [os.path.join('play', 'ou', 'v'),
            os.path.join('play', 'ou', 'quap', 'uikwe'),
            os.path.join('play', 'ou', 'quap', 'qonxu.txt'),
            os.path.join('play', 'ou', 'quap', 'aoq', 'qsonj'),
            os.path.join('play', 'ou', 'quap', 'aoq', 'aqnsa'),
            os.path.join('play', 'ou', 'b'),
            os.path.join('play', 'ou', 'a')],
    "16": [os.path.join('play', 'rb', 'rb9', '89.csv'),
            os.path.join('play', 'rb', 'rb9', '12.xls'),
            os.path.join('play', 'rb', 'ppt.ppt'),
            os.path.join('play', 'ou', 'v'),
            os.path.join('play', 'ou', 'quap', 'uikwe'),
            os.path.join('play', 'ou', 'quap', 'qonxu.txt'),
            os.path.join('play', 'ou', 'quap', 'aoq', 'qsonj'),
            os.path.join('play', 'ou', 'quap', 'aoq', 'aqnsa'),
            os.path.join('play', 'ou', 'b'),
            os.path.join('play', 'ou', 'a'),
            os.path.join('play', 'ls', 'qwe', 'usun.pdf'),
            os.path.join('play', 'ls', 'qwe', 'iuqwe.json'),
            os.path.join('play', 'ls', 'mf.py'),
            os.path.join('play', 'ls', 'lu.txt')],
    "17": [os.path.join('recursive', 'others', 'USERID_9.json'),
            os.path.join('recursive', 'others', 'USERID_8.json'),
            os.path.join('recursive', 'others', 'USERID_7.json'),
            os.path.join('recursive', 'others', 'USERID_6.json'),
            os.path.join('recursive', 'others', 'USERID_5.json'),
            os.path.join('recursive', 'others', 'USERID_10.json')],
    "18": [os.path.join('recursive', 'others', 'USERID_9.json'),
            os.path.join('recursive', 'others', 'USERID_8.json'),
            os.path.join('recursive', 'others', 'USERID_7.json'),
            os.path.join('recursive', 'others', 'USERID_6.json'),
            os.path.join('recursive', 'others', 'USERID_5.json'),
            os.path.join('recursive', 'others', 'USERID_10.json'),
            os.path.join('recursive', 'USERID_4', 'true', 'tweets.json'),
            os.path.join('recursive', 'USERID_4', 'false', 'tweets.json'),
            os.path.join('recursive', 'USERID_3', 'tweets.json'),
            os.path.join('recursive', 'USERID_2', 'tweets.json'),
            os.path.join('recursive', 'USERID_1', 'tweets.json')],
    "19": 17,
    "20": 200,
}

# find a comment something like this: #q10
def extract_question_num(cell):
    for line in cell.get('source', []):
        line = line.strip().replace(' ', '').lower()
        m = re.match(r'\#q(\d+)', line)
        if m:
            return int(m.group(1))
    return None

# rerun notebook and return parsed JSON
def rerun_notebook(orig_notebook):
    new_notebook = 'cs-220-test.ipynb'

    # re-execute it from the beginning
    cmd = 'jupyter nbconvert --execute "{orig}" --to notebook --output="{new}" --ExecutePreprocessor.timeout=120'
    cmd = cmd.format(orig=os.path.abspath(orig_notebook), new=os.path.abspath(new_notebook))
    subprocess.check_output(cmd, shell=True)

    # parse notebook
    with open(new_notebook,encoding='utf-8') as f:
        nb = json.load(f)
    return nb

def normalize_json(orig):
    try:
        return json.dumps(json.loads(orig.strip("'")), indent=2, sort_keys=True)
    except:
        return 'not JSON'


def check_cell_text(qnum, cell):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = outputs[0].get('data', {}).get('text/plain', [])
    actual = ''.join(actual_lines)
    jbn = [10]
    if qnum in jbn:
        actual = (eval(compile(ast.parse(actual, mode='eval'), '', 'eval')))
    else:
        try:
            actual = ast.literal_eval(actual)
        except Exception as e:
            print("COULD NOT PARSE THIS CELL:")
            print(actual)
            raise e
    expected = expected_json[str(qnum)]

    expected_mismatch = False
    if type(expected) != type(actual):
        return "expected an answer of type %s but found one of type %s" % (type(expected), type(actual))
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=1e-06, abs_tol=1e-06):
            expected_mismatch = True
    elif type(expected) == list:
        try:
            extra = set(actual) - set(expected)
            missing = set(expected) - set(actual)
            if missing:
                return "missing %d entries list, such as: %s" % (len(missing), repr(list(missing)[0]))
            elif extra:
                return "found %d unexpected entries, such as: %s" % (len(extra), repr(list(extra)[0]))
            elif len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
            else:
                for i,(a,e) in enumerate(zip(actual, expected)):
                    if a != e:
                        return "found %s at position %d but expected %s" % (str(a), i, str(e))
        except TypeError:
            # this happens when the list contains dicts.  Just do a simple comparison
            if actual != expected:
                return "expected %s" % repr(expected)
    else:
        if expected != actual:
            expected_mismatch = True

    if expected_mismatch:
        return "found {} in cell {} but expected {}".format(actual, qnum, expected)

    return PASS


def check_cell_png(qnum, cell):
    for output in cell.get('outputs', []):
        if 'image/png' in output.get('data', {}):
            return PASS
    return 'no plot found'


def check_cell(question, cell):
    print('Checking question %d' % question.number)
    if question.format == TEXT_FORMAT:
        return check_cell_text(question.number, cell)
    elif question.format == PNG_FORMAT:
        return check_cell_png(question.number, cell)
    raise Exception("invalid question type")


def grade_answers(cells):
    results = {'score':0, 'tests': []}

    for question in questions:
        cell = cells.get(question.number, None)
        status = "not found"

        if question.number in cells:
            status = check_cell(question, cells[question.number])

        row = {"test": question.number, "result": status, "weight": question.weight}
        results['tests'].append(row)

    return results

def check_absolute(cell):
    for line in cell.get('source', []):
        line = line.strip().replace(' ', '').lower()   
        if ".csv" in line:
            word_double = re.findall("\"(.*?)\"",line)
            word_single = re.findall("\'(.*?)\'",line)
            if word_double:
                for word in word_double:
                    if ".csv" in word:	
                        return (os.path.isabs(word))

            if word_single:
                for word in word_single:
                    if ".csv" in word:
                        return (os.path.isabs(word))

    return False

def main():
    if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith("win"):
        import asyncio
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    # rerun everything
    orig_notebook = 'main.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py main.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]

    # make sure directories are properly setup
    assert(os.path.exists("sample_data"))
    assert(os.path.exists("full_data"))
    assert(os.path.exists("play"))
    assert(os.path.exists("recursive"))

    nb = rerun_notebook(orig_notebook)

    # check for absolute/relative path
    for cell in nb['cells']:
        is_absolute = check_absolute(cell)
        if is_absolute:
            print ("WARNING: REPLACE YOUR ABSOLUTE PATH WITH RELATIVE PATH!")
            print ("\nTOTAL SCORE: ", 0.0)
            return

    # extract cells that have answers
    answer_cells = {}
    for cell in nb['cells']:
        q = extract_question_num(cell)
        if q == None:
            continue
        if not q in question_nums:
            print('no question %d' % q)
            continue
        answer_cells[q] = cell

    # do grading on extracted answers and produce results.json
    results = grade_answers(answer_cells)
    passing = sum(t['weight'] for t in results['tests'] if t['result'] == PASS)
    total = sum(t['weight'] for t in results['tests'])
    results['score'] = 100.0 * passing / total

    print("\nSummary:")
    for test in results["tests"]:
        print("  Test %d: %s" % (test["test"], test["result"]))

    print('\nTOTAL SCORE: %.2f%%' % results['score'])
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()

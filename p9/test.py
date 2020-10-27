# -*- coding: utf-8 -*-
import os, sys, subprocess, json, re, collections, math, ast

# Aviod NotImplementError in Windows System
if (sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith("win")):
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

PASS = "PASS"
TEXT_FORMAT = "text"
PNG_FORMAT = "png"
Question = collections.namedtuple("Question", ["number", "weight", "format"])




questions = [
    # stage 1
    Question(number=1, weight=1, format=TEXT_FORMAT),
    Question(number=2, weight=1, format=TEXT_FORMAT),
    Question(number=3, weight=1, format=TEXT_FORMAT),
    Question(number=4, weight=1, format=PNG_FORMAT),
    Question(number=5, weight=1, format=PNG_FORMAT),
    Question(number=6, weight=1, format=PNG_FORMAT),
    Question(number=7, weight=1, format=PNG_FORMAT),
    Question(number=8, weight=1, format=PNG_FORMAT),
    Question(number=9, weight=1, format=TEXT_FORMAT),
    Question(number=10, weight=1, format=TEXT_FORMAT),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1, format=PNG_FORMAT),
    Question(number=13, weight=1, format=TEXT_FORMAT),
    Question(number=14, weight=1, format=TEXT_FORMAT),
    Question(number=15, weight=1, format=TEXT_FORMAT),
    Question(number=16, weight=1, format=TEXT_FORMAT),
    Question(number=17, weight=1, format=TEXT_FORMAT),
    Question(number=18, weight=1, format=TEXT_FORMAT),
    Question(number=19, weight=1, format=TEXT_FORMAT),
    Question(number=20, weight=1, format=TEXT_FORMAT),
]
question_nums = set([q.number for q in questions])


# JSON and plaintext values
expected_json = {
    "1": 6.380867346938772,
    "2": 6.742857142857143,
    "3": 6.413599999999994,
    "9":{'a': 6.413599999999994,
 'b': 6.312264150943395,
 'c': 6.337362637362637,
 'd': 6.297101449275363,
 'e': 6.128125000000001,
 'f': 6.375609756097562,
 'g': 6.443181818181819,
 'h': 6.476829268292684,
 'i': 6.714814814814817,
 'j': 6.375,
 'k': 6.316666666666666,
 'l': 6.172368421052631,
 'm': 6.650000000000002,
 'n': 6.348148148148147,
 'o': 6.5814814814814815,
 'p': 6.160377358490566,
 'q': 6.7,
 'r': 6.371052631578949,
 's': 6.216352201257862,
 't': 6.5432000000000015,
 'u': 6.15,
 'v': 6.1000000000000005,
 'w': 6.243076923076923,
 'y': 6.285714285714286,
 'z': 6.833333333333333},
    "10":{'Comedy': 6.3146391752577395,
 'Drama': 6.529707495429615,
 'Romance': 6.474147727272729,
 'History': 6.661643835616438,
 'Family': 6.512941176470589,
 'Mystery': 6.275206611570249,
 'Thriller': 5.981999999999998,
 'Action': 6.125752508361202,
 'Crime': 6.355182072829133,
 'Adventure': 6.612367491166079,
 'Western': 6.455309734513275,
 'Music': 6.3947368421052655,
 'Animation': 7.1533333333333315,
 'Sport': 6.527083333333334,
 'Fantasy': 6.405084745762712,
 'War': 6.771717171717175,
 'Sci-Fi': 6.104347826086958,
 'Horror': 5.724705882352941},
    "11":{'Comedy': 484,
 'Drama': 1085,
 'Romance': 352,
 'History': 73,
 'Family': 84,
 'Mystery': 117,
 'Thriller': 243,
 'Action': 289,
 'Crime': 351,
 'Adventure': 280,
 'Western': 226,
 'Music': 38,
 'Animation': 45,
 'Sport': 47,
 'Fantasy': 58,
 'War': 99,
 'Sci-Fi': 67,
 'Horror': 81},
    "13": [2015],
    "14": ['Music', 'Animation', 'Sport', 'Fantasy', 'Sci-Fi'],
    "15": ['Action', 'Romance', 'Crime', 'Comedy', 'Drama'],
    "16": ['Robert De Niro',
 'George Sanders',
 'Robert Mitchum',
 'Glenn Ford',
 'Randolph Scott',
 'Henry Fonda',
 'Anthony Quinn',
 'Mickey Rooney',
 'Eric Roberts',
 'John Wayne'],
    "17": 'John Wayne',
    "18": 1926,
    "19": ['The Godfather: Part II', 'The Dark Knight', 'The Godfather'],
    "20": ['Silk',
 'Stealing Las Vegas',
 'Singularity',
 'Body and Soul',
 'Garden of the Dead',
 'Beyond the Ring',
 "Hitman's Run",
 'Betrayal',
 "Jake's Road",
 'The Trouble with Spies',
 '2 Bedroom 1 Bath',
 'Victim of Desire',
 'Arsenal',
 'Woman of Desire',
 'Sweet Justice',
 'Falcon Beach',
 'The Flying Dutchman',
 'The Mark: Redemption',
 'The Steam Experiment'],
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
    new_notebook = 'cs-301-test.ipynb'

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
    actual = ast.literal_eval(actual)
    expected = expected_json[str(qnum)]

    expected_mismatch = False

    # TODO: remove this hack!!!
    if qnum == 34 or qnum == 35:
        # check they did some reasonable sorting
        for i in range(1, len(actual)):
            a = actual[i-1]["span"]
            b = actual[i]["span"]
            if a < b:
                return "bad sort: found a span of {} before a span of {}".format(a, b)
        expected = sorted(expected, key=lambda row: (-row["span"], row["name"]))
        actual = sorted(actual, key=lambda row: (-row["span"], row["name"]))

    # TODO: remove this hack!!!
    if 36 <= qnum <= 40:
        # check they did some reasonable sorting
        for i in range(1, len(actual)):
            a = actual[i-1]["rating"]
            b = actual[i]["rating"]
            if a < b:
                return "bad sort: found a rating of {} before a rating of {}".format(a, b)
        expected = sorted(expected, key=lambda row: (-row["rating"], row["category"]))
        actual = sorted(actual, key=lambda row: (-row["rating"], row["category"]))
        
    if type(expected) != type(actual):
        return "expected an answer of type %s but found one of type %s" % (type(expected), type(actual))
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=1e-06, abs_tol=1e-06):
            expected_mismatch = True
    elif type(expected) == list:
        try:
            extra = set(actual) - set(expected)
            missing = set(expected) - set(actual)
            if extra:
                return "found unexpected entry in list: %s" % repr(list(extra)[0])
            elif missing:
                return "missing %d entries list, such as: %s" % (len(missing), repr(list(missing)[0]))
            elif len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
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
    if qnum == 21:
        print('here')
        print(cell)
    for output in cell.get('outputs', []):
        if qnum == 21:
            print(output.get('data', {}).keys())
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
    # rerun everything
    orig_notebook = 'main.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py main.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]
    nb = rerun_notebook(orig_notebook)

    # check for absolute/relative path
    for cell in nb['cells']:
        is_absolute = check_absolute(cell)
        if (is_absolute):
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

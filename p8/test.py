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
    Question(number=4, weight=1, format=TEXT_FORMAT),
    Question(number=5, weight=1, format=TEXT_FORMAT),
    Question(number=6, weight=1, format=TEXT_FORMAT),
    Question(number=7, weight=1, format=TEXT_FORMAT),
    Question(number=8, weight=1, format=TEXT_FORMAT),
    Question(number=9, weight=1, format=TEXT_FORMAT),
    Question(number=10, weight=1, format=TEXT_FORMAT),
    Question(number=11, weight=1, format=TEXT_FORMAT),
    Question(number=12, weight=1, format=TEXT_FORMAT),
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
    "1": {'nm0000131': 'John Cusack',
 'nm0000154': 'Mel Gibson',
 'nm0000163': 'Dustin Hoffman',
 'nm0000418': 'Danny Glover',
 'nm0000432': 'Gene Hackman',
 'nm0000997': 'Gary Busey',
 'nm0001149': 'Richard Donner',
 'nm0001219': 'Gary Fleder',
 'nm0752751': 'Mitchell Ryan',
 'tt0093409': 'Lethal Weapon',
 'tt0313542': 'Runaway Jury'},
    "2": 'Gary Fleder',
    "3": ['John Cusack',
 'Mel Gibson',
 'Dustin Hoffman',
 'Danny Glover',
 'Gene Hackman',
 'Gary Busey',
 'Richard Donner',
 'Gary Fleder',
 'Mitchell Ryan'],
    "4": ['nm0000997', 'nm0001219'],
    "5":[{'actors': ['nm0000131', 'nm0000432', 'nm0000163'],
  'directors': ['nm0001219'],
  'genres': ['Crime', 'Drama', 'Thriller'],
  'rating': 7.1,
  'title': 'tt0313542',
  'year': 2003},
 {'actors': ['nm0000154', 'nm0000418', 'nm0000997', 'nm0752751'],
  'directors': ['nm0001149'],
  'genres': ['Action', 'Crime', 'Thriller'],
  'rating': 7.6,
  'title': 'tt0093409',
  'year': 1987}],
    "6":4,
    "7":'nm0000163',
    "8":[{'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
  'directors': ['Gary Fleder'],
  'genres': ['Crime', 'Drama', 'Thriller'],
  'rating': 7.1,
  'title': 'Runaway Jury',
  'year': 2003},
 {'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
  'directors': ['Richard Donner'],
  'genres': ['Action', 'Crime', 'Thriller'],
  'rating': 7.6,
  'title': 'Lethal Weapon',
  'year': 1987}],
    "9":'Lethal Weapon',
    "10":['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
    "11":['Richard Donner'],
    "12": [{'actors': ['John Wayne', 'Cedric Hardwicke'],
  'directors': ['Richard Wallace'],
  'genres': ['Adventure', 'Drama', 'Romance'],
  'rating': 6.3,
  'title': 'Tycoon',
  'year': 1947},
 {'actors': ['Randolph Scott', 'Jay C. Flippen', 'Frank Faylen'],
  'directors': ['Joseph H. Lewis'],
  'genres': ['Western'],
  'rating': 5.9,
  'title': '7th Cavalry',
  'year': 1956},
 {'actors': ['Randolph Scott', 'Lee Marvin', 'Walter Reed'],
  'directors': ['Budd Boetticher'],
  'genres': ['Action', 'Western'],
  'rating': 7.5,
  'title': '7 Men from Now',
  'year': 1956}],
    "13": [{'actors': ['Val Kilmer', 'Armand Assante', 'Eric Roberts'],
  'directors': ['Philippe Martinez'],
  'genres': ['Mystery', 'Thriller'],
  'rating': 4.0,
  'title': 'The Steam Experiment',
  'year': 2009},
 {'actors': ['Glenn Ford',
   'Bradford Dillman',
   'David Soul',
   'Robert F. Lyons'],
  'directors': ['Jud Taylor'],
  'genres': ['Drama', 'Mystery', 'Sci-Fi'],
  'rating': 4.8,
  'title': 'The Disappearance of Flight 412',
  'year': 1974},
 {'actors': ['Angelo Dundee', 'George Foreman', 'Freddie Roach'],
  'directors': ['Chris Tasara'],
  'genres': ['Sport'],
  'rating': 7.2,
  'title': 'Fortitude and Glory: Angelo Dundee and His Fighters',
  'year': 2012},
 {'actors': ['Robert Taylor', 'George Sanders'],
  'directors': ['Richard Thorpe'],
  'genres': ['Adventure', 'Drama', 'History'],
  'rating': 6.8,
  'title': 'Ivanhoe',
  'year': 1952},
 {'actors': ['Alan Ladd', 'Macdonald Carey'],
  'directors': ['Elliott Nugent'],
  'genres': ['Drama'],
  'rating': 6.6,
  'title': 'The Great Gatsby',
  'year': 1949}],
    "14": 22,
    "15": [{'actors': ['Fred Astaire', 'Mickey Rooney', 'Keenan Wynn', 'Paul Frees'],
  'directors': ['Jules Bass', 'Arthur Rankin Jr.'],
  'genres': ['Adventure', 'Animation', 'Comedy'],
  'rating': 7.8,
  'title': "Santa Claus Is Comin' to Town",
  'year': 1970},
 {'actors': ['Glenn Ford', 'Dean Jagger', 'Maurice Evans'],
  'directors': ['Paul Wendkos'],
  'genres': ['Drama', 'Thriller'],
  'rating': 7.3,
  'title': 'The Brotherhood of the Bell',
  'year': 1970}],
    "16": 18,
    "17": 2605,
    "18": 1247,
    "19": 6.401659528907912,
    "20": 'Dr. Strangelove or: How I Learned to Stop Worrying and Love the Bomb',
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

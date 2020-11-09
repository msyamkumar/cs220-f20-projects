# Project 10: Twitter Data

## Clarifications/Corrections

November 4th: modified the description of q4.

November 8th: added some hints to q10.

**Find any issues?** Report to us:  

- NEYANEL VASQUEZ-GARCIA vasquezgarci@wisc.edu
- SOURAV PAL <spal9@wisc.edu>
- SAYALI ANIL ALATKAR <alatkar@wisc.edu>

## Learning Objectives

In this project, you will

- gain more experience with reading and writing files;
- gain more experience with using dictionaries;
- practice handling errors;
- practice using namedtuples.

## Coding Style Requirements

Remember that coding style matters! **We might deduct points for bad coding style.** Here are a list of coding style requirements:

- Do not use meaningless names for variables or functions (e.g. uuu = "my name").
- Do not write the exact same code in multiple places. Instead, wrap this code into a function and call that function whenever the code should be used.
- Do not call unnecessary functions.
- Avoid using slow functions multiple times within a loop.
- Avoid inappropriate use of data structures.
- Don't name variables or functions as python keywords or built-in functions. Bad example: str = "23".
- Don't define multiple functions with the same name or define multiple versions of one function with different names. Just keep the best version.
- Put all `import` commands together at the second cell of `main.ipynb`, the first cell should be submission information (netid and etc).
- Think twice before creating a function without any parameters. Defining a new functions is unnecessary sometimes. The advantage of writing functions is that we can reuse the same code. If we only use this function once, there is no need to create a new function.
- Don't use absolute path such as `C://Desktop//220`. **You may only use relative path**. When we test your work on a different operating system, all of the test will fail and you will get a 0. Don't panic when you see this, please fix the error and resubmit your assignment.

## Setup

**Step 1:** Download [`tweets.zip`](https://github.com/msyamkumar/cs220-f20-projects/tree/master/p10/tweets.zip ) and extract it to a directory on your computer (using [Mac directions](http://osxdaily.com/2017/11/05/how-open-zip-file-mac/) or [Windows directions](https://support.microsoft.com/en-us/help/4028088/windows-zip-and-unzip-files)). 

**Step 2:** Download [`test.py`](https://github.com/msyamkumar/cs220-f20-projects/tree/master/p10/test.py)  to the directory from step 1 (`test.py` be next to the `sample_data` directory, for example)

**Step 3:** Create a `main.ipynb` in the same location.  Do all work for both stages there, and turn it in when complete.

**Mac User Only**: Download [`cleanMAC.py`](https://github.com/msyamkumar/cs220-f20-projects/tree/master/p10/cleanMAC.py) in the same location. Create a new cell in your `main.ipynb` and copy the following code 

```python
# import this module if and only if your laptop is mac
from cleanMAC import * 
# clean the .DS_Store file in MAC
clean()
```

to this cell. This is because MacOS will produce a file named `.DS_Store` automatically, which may make you fail to pass the tests.

Note: Make sure `full_data`, `sample_data`, `main.ipynb` and `test.py` are in same directory.

## Introduction

In this project, you'll be analyzing a collection of actual tweets.
This data is messy!  You'll face the following challenges:

* data is spread across multiple files
* some files will be CSVs, others JSONs
* the files may be missing values or may be too corrupt to parse.
* some integer values may be represented as strings with a suffix of "M", "K", or similar

In p10, you'll write code to cleanup the data, representing everything as Tweet objects (you'll create a new type for these).  In p11, you'll analyze your clean data.

For this project, you'll create a new `main.ipynb` and answer questions in the usual format. **Please go through the [lab-p10](https://github.com/msyamkumar/cs220-f20-projects/tree/master/lab-p10) before working on this project.** In the lab, you will make helper functions and learn some useful techniques related to this project.

## Questions

For the first 6 questions, we'll ask you to list files.  These
questions have a few things in common:

* any files with names beginning with "." should be excluded
* you must produce a list
* the list must be in reverse-alphabetical order

Some things will vary:

* which directory you'll look at
* whether the list contains simples file names, or paths
* sometimes you'll need to filter to only show files with certain extensions

You may consider writing a single function to answer several questions
(hint: things that change for different questions can often be
represented with parameters).

#### #Q1: What are the names of the files present in the `sample_data` directory?

Hint: Look into the `os.listdir` function. Produce a list of file names.

#### #Q2: What are the names of the files present in the `full_data` directory?

#### #Q3: What are the paths of all the files in the `sample_data` directory?

In order to achieve this, you need to use the `os.path.join()` function. Please do not hardcode "/" or "\\" because doing so will cause your function to fail on a computer that's not using the same operating system as yours. Again, remember to **use relative path instead of absolute path**.

#### #Q4: What are the paths of all the files in the `full_data` directory?

To clarify, this function must do everything you did for #Q2, as well as the additional step above. 

#### #Q5: What are the paths of the CSV files present in the `sample_data` directory?

#### #Q6: What are the paths of the CSV and INFO files present in the `full_data` directory?

----

For the following questions, you'll need to create a new Tweet type
(using namedtuple).  It will have the following attributes:

* tweet_id (string)
* username (string)
* num_liked (int)
* length (int)

Please ensure you define your namedtuple exactly according to the
specifications above, or you will be unable to pass the tests.  You
should be able to use your Tweet type to create new Tweet objects, like this:

```python
t = Tweet("id123", "user456", 100, 140)
t
```

Running the above in a cell should produce output like this:

```python
Tweet(tweet_id='id123', username='user456', num_liked=100, length=140)
```

Notice that we're ignoring a few fields from the CSV, such as `date`
and `is_retweet`.

----

#### #Q7: What are the tweets present in the CSV file `1.csv` in `sample_data`?

The expected output format is 

```python
[Tweet(tweet_id='1467811372', username='USERID_6', num_liked=5882, length=29),
 Tweet(tweet_id='1467811592', username='USERID_8', num_liked=2676, length=11),
 Tweet(tweet_id='1467811594', username='USERID_9', num_liked=2182, length=99),
 Tweet(tweet_id='1467811795', username='USERID_1', num_liked=7791, length=36),
 Tweet(tweet_id='1467812025', username='USERID_1', num_liked=8149, length=25)]
```

#### #Q8: What are the tweets present in the CSV file `1.csv` in `full_data`?

Same output format as q7 is expected here.

#### #Q9: What are the tweets present in the CSV file `2.csv` in `full_data`? 

Same output format as q7 is expected here.

If you just tried to run your code as-is on this file, chances are it
crashed, or you had some missing data. This is because some of the
rows in this file, are incomplete or inconsistent in some way. You
must now go back and modify your CSV parsing function to deal with
situations like this.

In short, whenever you see a row in the CSV file which does not have
all the fields present, just skip that row and move on to the next
one, parsing what remains.

#### #Q10: What are the tweets present in the JSON file `2.json` in `sample_data`?

Same output format as q7 is expected here.

Just like before with the CSV files, we're going to now parse a JSON
file and convert it to a list of Tweets, so that all of our data
from different files is going into one common format that's easy for
us to work with.

The JSON files have the data saved as one big dictionary. The keys in the dictionary are the tweet_id, and the values are a smaller dictionary, containing all the details of the tweet with that tweet_id. Feel free to open up a JSON file and take a look at it to get a sense of how it's structured (this is always a great first step when you're trying to parse data you're unfamiliar with).

Your task here is to convert each JSON file to a **list of Tweet
objects** (similar to what we did when parsing the CSVs).  Each
key-value pair in our big dictionary therefore corresponds to one
namedtuple in the list.

Here's the first tweet in the JSON file, `1.json` in `sample_data` 

```json
{
  "1467810369": {
    "date": "Mon Apr 06 22:19:45 PDT 2009",
    "username": "USERID_4",
    "tweet_text": "@switchfoot http://twitpic.com/2y1zl - Awww, that's a bummer.  You shoulda got David Carr of Third Day to do it. ;D",
    "is_retweet": false,
    "num_liked": 315
},
```

And here's the corresponding namedtuple:

`Tweet(tweet_id='1467810369', username='USERID_4', num_liked=315, length=115)`

Besides, if there are any tweets' `num_liked` is`unknown`, just treat it as 0. But if the `num_liked` is `8k` or `342m`, you should keep its original value. You can check `q20` for reference.

#### #Q11: What are the tweets present in the JSON file `1.json` in `sample_data`?

The expected output format is:

```python
[Tweet(tweet_id='1467810369', username='USERID_4', num_liked=315, length=115),
 Tweet(tweet_id='1467810672', username='USERID_8', num_liked=5298, length=111),
 Tweet(tweet_id='1467810917', username='USERID_8', num_liked=533, length=89),
 Tweet(tweet_id='1467811184', username='USERID_6', num_liked=2650, length=47),
 Tweet(tweet_id='1467811193', username='USERID_8', num_liked=2101, length=111)]
```

#### #Q12: What are the tweets present in the JSON file `5.json` in `full_data`?

Same format as q11 is expected.

#### #Q13: What are the tweets present in the JSON file `4.json` in `full_data`?

Same format as q11 is expected.

Create a function whose input is an integer textLength that returns a list containing all the tweets with a text less than textLength. Use this function in all of the remaining questions. It should read all the files in `full_data` and combine the tweets into one list. **When reading files, please read them in reverse alphabetical order (see your output of p2).** If the order of your output is not consistent with our expected output, you will fail to pass the tests.

```python
def tweetsLessThan(textLength):
  	#TODO: read all files in full_data and read them in an order of q2
```

#### #Q14: Return all the tweet objects with a length less than 50 in `full_data`.

Use the function you just created to answer this question. You may encounter a `JSONDecodeError`. This is because the `1.json` file is broken. Unfortunately, unlike CSV files, broken JSON files are much more complicated to fix, so we can't just skip over one tweet and salvage the rest.  Instead, your JSON parsing function should skip any file it cannot parse using `json.load` and just return an empty list. Modify your function with `try` and `except` to skip the broken file.

#### #Q15: Return a list of all the tweet objects with a length less than 30 in `full data`. 

#### #Q16: Return a list of all the tweet objects with a length less than 20 in `full data `.

#### #Q17: Which file in the directory `sample_data` contains the tweet with tweet_id '1467812784'?

Produce the **path to the file**. 

Hint: Use the functions you've written to help you accomplish this task, as it involves a combination of looking through all the files in a folder, parsing them, and then looking through the parsed list. 

#### #Q18: Which file in the directory `full_data` contains the tweet with tweet_id '1467944581'?

Produce the **path to the file**. 

#### #Q19: Which files in the directory `full_data` contain tweets by the user "USERID_1"?

Be sure to produce a **list of paths** (even if it's just 1 path) sorted in **reverse-alphabetical order**.

#### #Q20: What are the first 20 tweets present in all the files in the `full_data` directory, sorted by num_liked?

Produce a single **list of Tweets** of length 20 containing the first 20 tweets sorted in **descending order by num_liked**. Note, some Tweets has num_liked as String, e.g. Tweet(tweet_id='1467894593', username='USERID_2', num_liked='869M', length=136). And other have `num_liked` as an integer. Your code should be able to handle this kind of tweets.

The first 5 tweets of the expected output are:

```python
[Tweet(tweet_id='1467894593', username='USERID_2', num_liked='869M', length=136),
 Tweet(tweet_id='1467894600', username='USERID_8', num_liked='915k', length=67),
 Tweet(tweet_id='1467853431', username='USERID_10', num_liked=9936, length=30),
 Tweet(tweet_id='1467875163', username='USERID_2', num_liked=9891, length=69),
 Tweet(tweet_id='1467860904', username='USERID_7', num_liked=9851, length=30)]
```

That's it for p10. In the next project, we'll begin using the data structures we've set up to do some analysis that spans across multiple files!

### Please remember to Kernel->Restart and Run All to check for errors then run the test.py script one more time.

Cheers!

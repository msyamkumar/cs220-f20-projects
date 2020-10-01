# Project 5: Hurricane Study

## Corrections/Clarifications

October 1st: provide a frame of code for `#q19` and `#q20`.	

**Find any issues?** Report to us: VINAY SAHADEVAPPA BANAKAR <vin@cs.wisc.edu>, ZACHARY JOHN BAKLUND <baklund@wisc.edu>, LIANG SHANG <lshang6@wisc.edu>.

## Overview
This project will focus on **loops** and **strings**.

Hurricanes often count among the worst natural disasters, both in terms of
monetary costs and, more importantly, human life.  Data Science can
help us better understand these storms.  For example, take a quick
look at this FiveThirtyEight analysis by Maggie Koerth-Baker:
[Why We're Stuck With An Inadequate Hurricane Rating System](https://fivethirtyeight.com/features/why-were-stuck-with-an-inadequate-hurricane-rating-system/)
(you should all read FiveThirtyEight, btw!).

For this project, you'll be analyzing data in the `hurricanes.csv`
file.  We generated this data file by writing a Python program to
extract stats from this page:
https://en.wikipedia.org/wiki/List_of_United_States_hurricanes.  By
the end of this semester, we'll teach you to extract data from
websites like Wikipedia for yourself.

Before you start to work on p5, please complete [lab-p5](https://github.com/msyamkumar/cs220-f20-projects/tree/master/lab-p5) first.

 To start,
download `project.py`, `test.py` and `hurricanes.csv`.  You'll do your
work in Jupyter Notebooks this week, producing a `main.ipynb` file.
You'll test as usual by running `python test.py` to test a
`main.ipynb` file (or `python test.py other.ipynb` to test a notebook
with a different name). If needed, you may only use standard Python modules such as `math`. Please don't use `pip` to install any additional modules as these are not considered standard modules.

We won't explain how to use the `project` module here (the code in the
`project.py` file).  The lab this week is designed to teach you how it
works.

This project consists of writing code to answer 20 questions.  If
you're answering a particular question in a cell in your notebook, you
need to put a comment in the cell so we know what you're answering.
For example, if you're answering question 13, the first line of your
cell should contain `#q13`.

## Questions and Functions

For the first three questions, you don't have to define
any functions of your own. Instead you should just make use of the
functions provided in the file `project.py` by calling the corresponding
function that you need to solve a particular problem.

### Q1: How many records are in the dataset?

### Q2: What is the name of the hurricane at last but one index?

### Q3: How many deaths were caused by the hurricane at index 24?

### Q4: How many hurricanes named Florence are in the dataset?

Write your code such that it counts all the variants (e.g., "Florence",
"FLORENCE", "fLoReNce", etc.).

### Q5: What is the number of unique deaths in the dataset?

Pleas copy the following code to the `#q5`  cell and reaplce the `???` with your code to get the `number_of_death` of the ith record.		

```python
number_of_uniq_deaths = [] 
for i in range(project.count()):
# add this number to record if there is no duplicate
    if not project.get_deaths(i) in number_of_uniq_deaths: 
        number_of_uniq_deaths.append(???) # TODO: get the number_of_death of that hurricane
len(number_of_uniq_deaths)
```

You can also answer this question in your own way without using the code we provide.

### Q6: What is the name of the fastest hurricane?

### Q7: What is the average MPH achieved by all hurricanes?

### Q8: What is the average damage (in dollars) caused by all hurricanes?

You should answer this question with an integer. Therefore, you should use `int()` to convert your result to an integer. Be careful! In the data, the number was formatted with a suffix (like "K", "M" or "B"), but
you'll need to do some processing to convert it to this: `13500000` (an integer).

You need to write a general function that
handles "K", "M", and "B" suffixes (it will be handy later).
Remember that "K" stands for thousand, "M" stands for million, and "B"
stands for billion!
For e.g. your function should convert a string from "13.5M" to 13500000,
"6.9K" to 6900 and so on.

```python
def format_damage(damage):
  # TODO check the last character of the string
  # and then convert it to appropriate integer by slicing and type casting
  pass
```

<!-- ### Q9: How much faster was the fastest hurricane compared to the average speed of all the hurricanes in the dataset?

You need to calculate the average mph speed of all hurricanes and subtract it from fastest mph speed. -->


<!-- ### Q10: How much damage (in dollars) was done by the hurricane Sandy? -->

### Q9: How many deaths did hurricane 'Floyd' cause in total?

### Function Suggestion:

We suggest you complete a function something like the following to
answer the next several questions (this is not a requirement if you
prefer to solve the problem another way):

```python
# return index of deadliest hurricane over the given date range
def deadliest_in_range(year1, year2):
    worst_idx = None
    for i in range(project.count()):
        if ????:  # TODO: check if year is in range
            if worst_idx == None or ????:  # TODO: it is worse than previous?
                # TODO: finish this code!
    return worst_idx
```

Hint: You can copy the `get_month`, `get_day`, and `get_year`
functions you created in lab to your project notebook if you like.

### Q10: What is the deadliest hurricane between 2000 and 2020 (inclusive)?

For this and the following, count a hurricane as being in the year it
was formed (not dissipated).

### Q11: What is the deadliest hurricane ever recorded?

### Q12: In what year did the most deadly hurricane form in 20th century (1901, 2000, inclusive)?

### Q13: How much damage (in dollars) was done by the deadliest hurricane in the last decade (2000 ,2010, inclusive)?

### Q14: What is the total damage across all hurricanes that formed in the month of September, in dollars?

### Function Suggestion:

We suggest you complete a function something like the following to
answer the next several questions (this is not a requirement if you
prefer to solve the problem another way):

```python
# return number of huricanes formed in month mm
def hurricanes_in_month(mm):
    num_of_hurricanes = 0
    for i in range(project.count()):
        pass # TODO: finish this code!
    return num_of_hurricanes
```

### Q15: How many hurricanes were formed in the month of December?

### Q16: How many hurricanes formed between August and November (inclusive)?

### Q17: Which month experienced the formation of least number of hurricanes? 

Please answer with an integer. If there is a tie, answer with the smaller one. For example, if both January and March experienced the formation of least number of hurricanes, your answer should be `1`.

### Q18: How many hurricanes were formed in this decade 2010-2020 (inclusive)?

### Q19: How many years in the history experienced a hurricane that caused more than 1000 in deaths?

Pleas copy the following code to the `#q19` cell and reaplce the `???` with your code to answer this question.

```python
year_list = []
for i in range(project.count()):
    year = ??? # TODO: get the year this hurricane formed
    if ??? and (not year in year_list): # TODO: check whether this hurricane caused more than 1000 deaths
        year_list.append(year) 
len(year_list)
```

You can also answer this question in your own way without using the code we provide.

### Q20: How many years in the history experienced a hurricane that was faster than 150 mph?

Pleas copy the following code to the `#q20` cell and reaplce the `???` with your code to answer this question.

```python
year_list = []
for i in range(project.count()):
    year = ??? # TODO: get the year this hurricane formed
    if ??? and (not year in year_list): # TODO: check whether this hurricane is faster than 150 mph
        year_list.append(year)
len(year_list)
```

You can also answer this question in your own way without using the code we provide.

### Good luck with your hurricanes project! :)
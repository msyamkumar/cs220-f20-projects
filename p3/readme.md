# Project 3

<h2> Corrections/Clarifications

</h2>

* Sep 16: Modified q10's description, to make it clearer.

* Sep 16: Provided implementation for "Function 4". Just invoke the provided funciton to
          answer #q11 and #q12.

# Project 3

## Description

In this project, you'll analyze spending data from
2017 to 2020 for five agencies in Madison: governments, gyms, restaurants,
schools, and stores.  You'll get practice calling functions from a
`project` module, which we'll provide, and practice writing your own
functions.

Start by downloading `project.py`, `test.py` and `madison.csv`.
Double check that these files don't get renamed by your browser (by
running `ls` in the terminal from your `p3` project directory).
You'll do all your work in a new `main.ipynb` notebook that you'll
create and hand in when you're done (please do not write your
functions in a separate .py file).  You'll test as usual by running
`python test.py` (or similar, depending on your laptop setup).  Before
handing in, please put the project, submitter, and partner info in a
comment in the first cell, in the same format you used for previous
projects (please continue doing so for all projects this semester).

We won't explain how to use the `project` module here (the code is in the
`project.py` file).  Please read the code in the `project.py` and make use of them.

This project consists of writing code to answer 20 questions.  If
you're answering a particular question in a cell in your notebook, you
need to put a comment in the cell so we know what you're answering.
For example, if you're answering question 13, the first line of your
cell should contain `#q13`.

## Dataset

The data looks like this:

| agency_id | agency      | 2017                | 2018               | 2019               | 2020               |
| --------- | ----------- | ------------------- | ------------------ | ------------------ | ------------------ |
| 3         | schools     | 68.06346877         | 71.32575615000002  | 73.24794765999998  | 77.87553504        |
| 6         | gyms        | 49.73757877         | 51.96834048        | 53.14405332        | 55.215007260000014 |
| 7         | restaurants | 16.96543425         | 18.12552139        | 19.13634773        | 19.845065799999997 |
| 122       | stores      | 180.371421039999998 | 19.159243279999995 | 19.316837019999994 | 19.7607100000000   |
| 15        | governments | 25.368879940000006  | 28.2286218         | 26.655754419999994 | 27.798933740000003 |

The dataset is in the `madison.csv` file.  We'll learn about CSV files
later in the semester.  For now, you should know this about them:

* it's easy to create them by exporting from Excel
* it's easy to use them in Python programs
* we'll give you a `project.py` module to help you extract data from CSV files until we teach you to do it directly yourself

All the numbers in the dataset are in millions of dollars.  Answer
questions in millions of dollars unless we specify otherwise.

## Requirements

You may not hardcode agency IDs in your code.  For example, if we ask
how much was spent on stores in 2020, you could obtain the answer
with this code: `get_spending(get_id("stores"), 2020)`.  If you don't
use `get_id` and instead use `get_spending(122, 2015)`, we'll deduct
points.

For some of the questions, we'll ask you to write (then use) a
function to compute the answer.  If you compute the answer without
creating the function we ask you to, we'll manually deduct points from
the `test.py` score when recording your final grade, even if the way
you did it produced the correct answer.

## Questions and Functions

### Q1: What is the agency ID of the stores agency?


### Q2: How much did the agency with ID 3 spend in 2017?

It is OK to hardcode `3` in this case since we asked directly about
agency 3 (instead of about "schools").

### Q3: How much did "restaurants" spend in 2019?

Hint: instead of repeatedly calling `project.get_id("streets")` (or
similar) for each function, you may wish to make these calls once at
the beginning of your notebook and save the results in variables,
something like this:

```python
schools_id = project.get_id("schools")
gyms_id = project.get_id("gyms")
restaurants_id = project.get_id("restaurants")
...
```

### Function 1: `year_max(year)`

This function will compute the maximum spending of any one agency in a
given year.  We'll give this one to you directly (you'll have to write
the code for the subsequent functions yourself).  Copy/paste this into
a cell in your notebook:

```python
def year_max(year):
    # grab the spending by each agency in the given year
    governments_spending = project.get_spending(project.get_id("governments"), year)
    gyms_spending = project.get_spending(project.get_id("gyms"), year)
    restaurants_spending = project.get_spending(project.get_id("restaurants"), year)
    schools_spending = project.get_spending(project.get_id("schools"), year)
    stores_spending = project.get_spending(project.get_id("stores"), year)

    # use builtin max function to get the largest of the five values
    return max(governments_spending, gyms_spending, restaurants_spending, schools_spending, stores_spending)
```

### Q4: What was the most spent by a single agency in 2017?

Use `year_max` to answer this.

### Q5: What was the most spent by a single agency in 2020?

### Function 2: `agency_min(agency)`

We'll help you start this one, but you need to fill in the rest
yourself.

```python
def agency_min(agency):
    agency_id = project.get_id(agency)
    y17 = project.get_spending(agency_id, 2017)
    y18 = project.get_spending(agency_id, 2018)
    # grab the other years

    # use the min function (similar to the max function)
    # to get the minimum across the four years, and return
    # that value
```

This function will compute the minimum the given agency ever spent
over the course of a year.

### Q6: What was the least that gyms ever spent in a year?

Use your `agency_min` function.

### Q7: What was the least that stores ever spent in a year?


### Function 3: `agency_avg(agency)`

This function will compute the average (over the four datapoints) that
the given agency spends per year.

Hint: start by copy/pasting `agency_min` and renaming your copy to
`agency_avg`.  Instead of computing the minimum of `y17`, `y18`, etc.,
compute the average of these by adding, then dividing by 4.

### Q8: How much is spent per year on governments, on average?

Use your `agency_avg` function.

### Q9: How much is spent per year on restaurants, on average?

### Q10: How much did the gyms spend above their average in 2019?

You should answer by giving a **percentage** of the gyms spend above their average between 0 and 100, with no
percent sign.  In this case, your code should produce a number close
to `1.195455545247126 `.

### Function 4: `max_spending_agency(start_year, end_year)`

This function returns the agency that has the maximum overall spending over the period from `start_year` to `end_year`. **This function implementation is provided to you. You just need to figure out how to invoke the function.** The provided function uses the concepts of loop, lists, and tuples - none of those concepts are covered yet.

```python
def max_spending_agency(start_year=2018, end_year=2020):
    max_agency = (None, None)
    for agency in ["governments", "gyms", "restaurants", "schools", "stores"]:
        _sum = sum([project.get_spending(project.get_id(agency), year=year) for year in range(start_year, end_year+1)])
        max_agency = (agency, _sum) if (max_agency == (None, None) or max_agency[1] < _sum) else max_agency
    
    return max_agency[0]
```

Note the default arguments above.


### Q11: Which agency has the maximum overall spending from 2018 to 2020?

In this question, you just need to invoke the provided function `max_spending_agency(start_year, end_year)` function. Hint: Think about whether you need to pass arguments - read the above function definition line.

<!--In this question, feel free to manually code it without using the function `max_spending_agency(start_year, end_year)`. If you are not using the function, feel free to use print() or any method to see the values for each agency while finding the answer. However, please (1) **remove all the print() in the answer block** (2) **code the answer at the last line without printing them**.-->

### Q12: Which agency has the maximum overall spending from 2017 to 2019?

In this question, you just need to invoke the provided function `max_spending_agency(start_year, end_year)` function.
<!--In this question, feel free to manually code it without using the function `max_spending_agency(start_year, end_year)`. -->


### Function 5: `change_per_year(agency, start_year, end_year)`

This function returns the average increase in spending (could be
negative if there's a decrease) over the period from `start_year` to
`end_year` for the specified `agency`.

You can start from the following code:

```python
def change_per_year(agency, start_year=2017, end_year=2020):
     pass # TODO: replace this line with your code
```

Python requires all functions to have at least one line of code.  When
you don't have some code, yet, it's common for that line to be `pass`,
which does nothing.  Note the default arguments above.

We're not asking you to assume exponential growth or do anything fancy
here; you just need to compute the difference between spending in the
last year and the first year, then divide by the number of elapsed
years.

### Q13: how much has spending increased per year (on average) for stores from 2017 to 2020?

Use the default arguments (your call to `change_per_year` should only
pass one argument explicitly).

### Q14: how much has spending increased per year (on average) for stores from 2018 to 2020?


### Function 6: `extrapolate(agency, year1, year2, year3)`

This function should compute the average change per year from the data
from `year1` to `year2` for `agency`, using your previous function for
finding average change.  It then returns the predicted spending in
`year3` from `year2` (i.e. extrapolate `year3` from `year2`), assuming spending continues increasing (or decreasing) by the
same constant amount each year.  We don't have anything for you to
copy for this one (you need to write it from scratch).

As an example, suppose spending in 2018 (year1) is 100 and spending in
2020 (year2) is 120.  The average increase is 10 per year.  So we
would extrapolate to 130 for 2021, 140 for 2022, etc.  This kind of
prediction is a simple *linear extrapolation*.

### Q15: how much will governments spend in 2021?

Extrapolate to 2021 from the data between 2018 and 2019.

### Q16: how much will restaurants spend in 2100?

Extrapolate from the data between 2018 and 2020.

### Q17: how much will schools spend in 2300?

Extrapolate from the data between 2017 and 2020.

### Function 7: `extrapolate_error`

We can't know how well our simple extrapolations will perform in the
future (unless we wait 80 years), but we can do shorter extrapolations
to years for which we DO know the result.  For example, we can
extrapolate to 2020 from the 2017-to-2019 data, then compare our
extrapolation to the actual spending in 2020.

Write a function named `extrapolate_error` that does an extrapolation
using the `extrapolate` function and compares the extrapolation to the
actual result, returning the error (i.e., how much `extrapolate`
overestimated).  For example, if the extrapolation is 105 and the
actual is 110, then the function should return -5.

What parameters should `extrapolate_error` have?  That's your
decision!

### Q18: what is the error if we extrapolate to 2020 from the 2018-to-2019 data for gyms?

### Q19: what is the percent error if we extrapolate to 2020 from the 2017-to-2019 data for governments?

Percent error = extrapolate_error*100/actual_spending_of_the_agency_for_the_extrapolated_year

### Q20: what is the standard deviation for stores spending over the 4 years?

Compute the population standard deviation, as in [this example](https://en.wikipedia.org/wiki/Standard_deviation#Population_standard_deviation_of_grades_of_eight_students).

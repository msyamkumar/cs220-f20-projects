# Stage 2: Databases and Plotting

**Find any issues?** Report to us:  

- WINFRED LI <wli525@wisc.edu>
- SEAN CHUNG  <cchung49@wisc.edu>
- TARUN ANAND <tanand3@wisc.edu>

## Learning Objectives

In this project, you will:
- practice querying a database using SQL 
- reinforce your knowledge of working with dataframes and creating plots
- continue practicing good coding style 

## Coding Style Requirements

Remember that coding style matters! **We might deduct points for bad coding style.** Here are a list of coding style requirements:

- Do not use meaningless names for variables or functions (e.g. uuu = "my name").
- Do not write the exact same code in multiple places. Instead, wrap this code into a function and call that function whenever the code should be used.
- Do not call unnecessary functions.
- Avoid using slow functions multiple times within a loop.
- Avoid inappropriate use of data structures. A bad example: use for loop to search for a corresponding value in a dictionary with a given key instead of use `dictname[key]` directly.
- Don't name variables or functions as python keywords or built-in functions. Bad example: str = "23".
- Don't define multiple functions with the same name or define multiple versions of one function with different names. Just keep the best version.
- Put all `import` commands together at the second cell of `main.ipynb`, the first cell should be submission information (netid and etc).
- Think twice before creating a function without any parameters. Defining new functions is unnecessary sometimes. The advantage of writing functions is that we can reuse the same code. If we only use this function once, there is no need to create a new function.
- Don't use absolute path such as `C://Desktop//220`. **You may only use relative path**. When we test your work on a different operating system, all of the test will fail and you will get a 0. Don't panic when you see this, please fix the error and resubmit your assignment. Contact your TA if you need assistance with this task.


# Testing

For answers involving a DataFrame, `test.py` compares your tables to
those in `expected.html`, so take a moment to open that file in your
browser.

`test.py` doesn't care if you have extra rows or columns, and it
doesn't care about the order of the rows or columns.  However, you
must have the correct values at each index/column location shown in
`expected.html`.

For P13, `test.py` is pickier than it has been. In addition to
checking for incorrect answers, it will also check for a few common
kinds of bad coding style. You should look for linting messages at the bottom
of the output, for example:

```
Linting Summary:
  Warning Messages:
    cell: 1, line: 4 - Redefining built-in 'id'
    cell: 1, line: 3 - Reimport 'numpy' (imported line 2)
    cell: 1, line: 5 - Unnecessary pass statement
    cell: 1, line: 2 - Unused import numpy
```

In this case, `test.py` will deduct 1 point per linter message because of
bad style, and at most deduct 10 points. For more information about the linter
as well as how to run the full linter to see all of the automatically generated
advice and feedback, please check out the [linting README](../linter).

# Setup

Use the `download` function from [lab-p12](https://github.com/msyamkumar/cs220-f20-projects/blob/master/lab-p12) to pull the data from here (do not manually download): https://raw.githubusercontent.com/msyamkumar/cs220-f20-projects/master/p13/countries.json
and store it in `countries.json`. Once you have created the file, create a Dataframe `countries` from this file. 

**Warning**: 1. Make sure your `download` function does not download the file if it already exists. The TAs will manually deduct points otherwise. 2. Make sure you use `download` function to pull the data instead of manually download. Otherwise you may get a zero. 

*Hint*: `pd.read_json('countries.json')` will return a DataFrame by reading from
 the JSON file. If the file contains lists of dictionaries, each dictionary will be a row in the DataFrame.

# Introduction

For your final CS 220 project, you're going to continue analyzing the world using the same dataset from the last project.

In this project, you'll dump your DataFrames to a SQLite database.
You'll answer questions by doing queries on that database.  Often,
your answer will be in the form of a plot.  Check these carefully, as
the tests only verify a plot has been created, not that it looks
correct (TAs will manually deduct points for plotting mistakes).

Create your database by pasting the following cell to your notebook.

```python
import sqlite3
conn = sqlite3.connect('countries.db')
countries.to_sql("countries", conn, if_exists="replace", index=False)

# remember to do conn.close() at the end of your notebook
```

If you named your DataFrames something other than `countries`, tweak the above code to use your variable names.

### Disclaimer: 
This dataset has been taken from the source without any modifications. Any current information in world affairs, including political implications haven't been represented in this dataset accurately. Please consider this as a synthetic dataset and not a real-world representation of the country information.

# Questions

#### #Q1: In our dataset, how many countries are in each region?

Look at the `Question 1` table in `expected.html`.  Your answer
should be a DataFrame with the same rows and columns.  It should look
like this:

<img src="imgs/13-1.PNG" width="300">

Requirements:
* use a GROUP BY query in SQL
* sort by number of countries (most first)
* break ties alphabetically ("A" before "B", etc)
* the column names should be `region` and `number of countries`

Use backtics (`` ` ``) around column names with spaces to satisfy the
last requirement.  You should also use the backtics to deal with
column names containing other problematic characters as well (e.g.,
`-`).

#### #Q2: How many countries are in each region? (answer with a plot)

Answer with a **bar plot**. Put regions on the x-axis and number
of countries on the y-axis. The regions should be sorted along the
x-axis in descending order by the number of countries and then alphabetically by name.

**Expected output:**

<img src="imgs/13-2.PNG" width="350">

The color doesn't matter. Remember to remove the legend if you plot has.

#### #Q3: What is the total area of each region?

For this question, you should calculate the total area of every region
and display the `region` name and total area of the region (using a
column named `total area`). The results should be displayed in *descending* order of the
column `total area`.

**Expected output:**

<img src="imgs/13-3.PNG" width="250">

#### #Q4: What is the total area of each region? (answer with a plot)

Answer with a **bar plot**. Put regions on the x-axis and total
area on the y-axis.  The continents should be sorted along the
x-axis in *descending* order of the column `total area`.

**Expected output:**

<img src="imgs/13-4.PNG" width="350">

The color doesn't matter. Remember to remove the legend if you plot has.

#### #Q5: What is the area of each country in the Near East region?

You should display the `country` name and `area` of the countries. The results should be displayed in *descending* order of the column `area`.

**Expected output:**

<img src="imgs/13-5.PNG" width="250">

#### #Q6: What are the top 12 countries that have the largest real GDP?

You should display the `country` name and `real GDP (billion)` of the top 12 countries that have the largest real GDP. These top 12 countries should be
displayed in *descending* order of real GDP.

Hint: `real GDP = population * gdp-per-capita`

**Expected output:**

<img src="imgs/13-6.PNG" width="250">

#### #Q7: What are the top 12 countries that have the largest real GDP? (answer with a plot)

**Expected output:**

<img src="imgs/13-7.PNG" width="350">

The color doesn't matter. Remember to remove the legend if you plot has. Make sure to include the "other" category (add up the GDP of other countries).

#### #Q8: What is the relationship between GDP per capita and literacy?

Answer with a **scatter plot** with `gdp-per-capita` on the x-axis and `literacy` on the y-axis. You will have to convert the type of `literacy` to float.

Optional: Use [Series.apply()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.apply.html) to solve this question without using a for loop

**Expected output:**

<img src="imgs/13-8.PNG" width="350">

#### #Q9: What is the correlation between GDP per capita and literacy?
If you have a DataFrame `df`, then calling `df.corr()` will present a table showing the Pearson correlation between every pair of columns in df. A correlation of 1 is the max (so, for example, every column is correlated perfectly with itself). A high correlation between columns X and Y means that large X values tend to coincide with large Y values and small X values tend to coincide with small Y values. In some of the questions, you'll observe negative correlations (-1 being the smallest). This means that large X values tend to coincide with small Y values and vice versa.

**Expected output:**

`0.5154347345101354`

#### #Q10: What is the relationship between GDP per capita and phones?
Answer with a **scatter plot** with `gdp-per-capita` on the x-axis and `phones` on the y-axis. As in question 8 you will have to convert `phones` to float type. 

Optional: Use [Series.apply()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.Series.apply.html) to solve this question without using a for loop

**Expected output:**

<img src="imgs/13-10.PNG" width="400">

#### #Q11: What is the relationship between GDP per capita and infant-mortality?

Answer with a **scatter plot** with `gdp-per-capita` on the x-axis and `infant-mortality` on the y-axis.

**Expected output:**

<img src="imgs/13-11.PNG" width="400">

#### #Q12: What is the relationship between GDP per capita and inverse of infant-mortality?

Answer with a **scatter plot** with `gdp-per-capita` on the x-axis and `inverse infant-mortality` on the y-axis.

Hint: `inverse infant-mortality` is defined as `1 / infant-mortality`

**Expected output:**

<img src="imgs/13-12.PNG" width="400">

#### #Q13: fit a `y = m * x + n` line to the scatter plot in question 10 using the least-squares method; what are the coefficients m and n?

For the regression line, first try copy/pasting this code into a notebook cell and running it to see what happens:

```python
import numpy as np

df = DataFrame({
    "x": [1,2,3,4],
    "y": [2,5,6,5]
})
df["1"] = 1

res = np.linalg.lstsq(df[["x", "1"]], df["y"], rcond=None)

# res is a tuple: (COEFFICIENTS, VALUE, VALUE, VALUE)
coefficients = res[0] # coefficients is (m,n:
m = coefficients[0] # slope
n = coefficients[1] # intercept
ax = df.plot.scatter(x='x', y='y')

df["fit"] = df["x"] * m + n
df.plot.line(x='x', y='fit', c='red', ax=ax)
```

Then adapt the above code so that it uses your DataFrame (instead of
df) and replaces "x" with `gdp-per-capita` and "y" with `inverse infant-mortality`. Answer with a **tuple** for coefficients `(m, n)`.:

**Expected output:**

`(0.01808887883603978, 37.95908987837674)`

Don't worry if your result is slightly off. If your result is close enough to the expected output, you will pass the test.

#### #Q14: When `gdp-per-capita = 30000`, what is the expected value for `phones` according to the regression model between them?

**Expected output:**

`580.6254549595701`

Don't worry if your result is slightly off. If your result is close enough to the expected output, you will pass the test.

#### #Q15: plot the regression line to the scatter plot

To visualize how well the regression line fit the scatter points, draw a fit line over the **scatter plot**.

**Expected output:**

<img src="imgs/13-15.PNG" width="350">

The position of the legend doesn't matter. Make sure the fitted line is red.

#### #Q16: What are the top 15 countries that have the smallest gap between birth rate and death rate?

You should display the `country` name, `birth-rate`, and `death-rate` of the top 15 countries that have the smallest `birth-rate` - `death-rate`. These top 15 countries should be displayed in *ascending* order of the gap.

**Expected output:**

<img src="imgs/13-16.PNG" width="250">


#### #Q17: What are the top 15 countries that have the smallest gap between birth rate and death rate? (answer with a plot)

Answer with a **horizontal bar plot**. Put countries on the y-axis and `birth-rate` and `death-rate` on the x-axis. The countries should be sorted along the y-axis in *ascending* order of the gap from bottom to top.

**Expected output:**

<img src="imgs/13-17.PNG" width="400">

The position of the legend doesn't matter. Make sure the your x-axis ticks are exactly same with the expected output.

#### #Q18: What is the relationship between population and gdp-per-capita? (answer with a plot)

Answer with a **scatter plot** with `population` on the x-axis and `gdp-per-capita` on the y-axis. Do you observe a pattern between population and gdp-per-capita?

**Expected output:**

<img src="imgs/13-18.PNG" width="350">

#### #Q19: Did you notice the four outliers? Which countries are they?

These are the points:

<img src="imgs/13-19.PNG" width="350">

Write a query to grab rows corresponding roughly to that
rectangle to get the points.  In the output, `gdp-per-capita` should be
sorted low to high.

**Expected output:**

<img src="imgs/13-19-1.PNG" width="300">


#### #Q20: what are the top 12 countries that have the largest real GDP? (answer with a plot)

Make use of the output of q6. To make the problem more interesting, answer with a **pie chart**.

**Expected output:**

<img src="imgs/13-20.PNG" width="350">

The color doesn't matter. 

That's it for p13!

### After you add your name and the name of your partner to the notebook in the first cell, please remember to Kernel->Restart and Run All to check for errors then run the test.py script one more time before submission. To keep your code concise, please remove your own testing code that does not influence the correctness of answers.

Cheers!


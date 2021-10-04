# Project 7: Fédération Internationale de Football Association

# WARNING: Unless you took a time portal to become my student in the past, this is not the correct repository :) Please go to the correct github repository for the current semester. If you are a Fall'20 semester student though, you are in the right place.

## Corrections/ Clarifications

None yet.

**Find any issues?** Report to us, SAYALI ANIL ALATKAR <alatkar@wisc.edu>  LIANG SHANG <lshang6@wisc.edu>, ALVIN (YIFEI) MING <ming5@wisc.edu>.

<h2>Learing objectives </h2>

 In this project, you will

* learn how to use dictionaries to answer questions about provided data;
* gain more experience with using lists in Python;
* learn how to write programs to interpret data present in csv files;
* **develop good coding styling habits (points may be deducted for bad coding styles)**.


## Intro

Let's play Fifa20, Python style!  In this project, you will get more practice with lists and start using dictionaries.  Start by downloading `test.py` and `Fifa20.csv` (which was adapted from [this dataset](https://www.kaggle.com/stefanoleone992/fifa-20-complete-player-dataset#players_20.csv)). This dataset is too large to preview on GitHub (>18K rows), but you can view the [raw version](https://github.com/msyamkumar/cs220-f20-projects/blob/master/p7/Fifa20.csv) or using a program such as [Excel](https://github.com/msyamkumar/cs220-f20-projects/blob/master/p7/excel.md). You can also preview an example with 100 rows [here](https://github.com/msyamkumar/cs220-f20-projects/blob/master/p7/preview.csv). For this project, you'll create a new `main.ipynb` and answer questions in the usual format. **Please go through the [lab-p7](https://github.com/msyamkumar/cs220-f20-projects/tree/master/lab-p7) before working on this project.** The lab will help you to make helper functions and introduce some useful techniques related to this project.

<h2> Coding style requirements</h2>

* don't name the variables and functions as python keywords or built-in functions. Bad example: str = "23".
*  don't define functions with the same name or define one function multiple times. Just keep the best version.
*  put all `import` commands together at the second cell of `main.ipynb`, the first cell should be submission information (netid and etc).
* think twice before creating a function without any parameters. Defining a new functions is unnecessary sometimes. The advantage of writing functions is that we can reuse the same code. If we only use this function once, there is no need to create a new function.
* avoid redundant logic.

## The Data

Try to familiarize yourself with the data before starting the analysis. We have players belonging to a wide range of nationalities and clubs in Fifa20. As you can see the data includes their weekly wages, in Euros (yes, wages are per week!), net worth of the player (in Euros) and the performance rating (score out of 100). For instance, the player named "Neymar" is associated with Brazil, is signed up by club "Paris Saint-Germain", and is paid a weekly wage of 290000 Euros. 

To ingest the data to your notebook, paste the following in an early cell:

```python
import csv

fifa_file = open('Fifa20.csv', encoding='utf-8')
file_reader = csv.reader(fifa_file)
player_data = list(file_reader)
fifa_file.close()
header = player_data[0]
player_data = player_data[1:]
for row in player_data:
    for idx in [2,3,4,7,8,12]:
        row[idx] = int(row[idx])
```

Consider peeking at the first few rows:
```python
print(header)
for row in player_data[:5]:
    print(row)
```

It's up to you to write any functions that will make it more convenient to access this data. **Also, for questions asking you about average values, round to two decimal places (use built-in python function `round()`).  i.e. `round(3.14159, 2) -> 3.14`.**

## Let's Start!

#### Q1: What is the name of the oldest player?

If multiple players have the same age, break the tie in favor of whoever appears first in the dataset.

#### Q2: What is the name of the highest-paid player?

If multiple players are paid the same, break the tie in favor of whoever appears first in the dataset.

#### Q3: What is the name of the highest valued player?

#### Q4: What is the nationality of the highest valued player?

---

Complete the following function in your notebook:

```python
def get_column(col_name):
    pass # replace this
```

The function extracts an entire column from `player_data` to a list, which it returns.  For example, imagine `player_data` contained this:

```python
[
    ["a", "b", "c"],
    ["d", "e", "f"],
    ["g", "h", "i"]
]
```

And `header` contains this:

```python
["X", "Y", "Z"],
```

Then column "X" is `["a", "d", "g"]`, column "Y" is `["b", "e", "h"]`, and column "Z" is `["c", "f", "i"]`.  A call to `get_column("Y")` should therefore return `["b", "e", "h"]`, and so on.

----

#### Q5: What are the first five nationalities listed in the dataset?

Use `get_column`, then take a slice from the list that is returned to you.

#### Q6: Which five player names are alphabetically first in the dataset?

By alphabetically, we mean according to Python (e.g., it is true that `"B" < "a"`), so don't use the lower method.

Do not eliminate duplicate names in this output if multiple players have the same name.

#### Q7: What is the average Value?

#### Q8: What is the average Height of the players?

#### Q9: How many players play in the position 'CAM'?

#### Q10: How many players are there per nationality?

Answer in the form of a dictionary mapping the countries to the respective number of players. The form of the dictionary should look like (there should be more elements in your output):

```python
{'Argentina': 886,
 'Portugal': 344,
 'Brazil': 824,
 'Slovenia': 61,
 'Belgium': 268,
 'Germany': 1216
 }
```

Use the dictionary from Q10 to answer the next two questions.

#### Q11: Which nationality has the most players participating in FIFA20?

#### Q12: How many players have Argentina as their nationality?
----

Define a function `player_to_dict` that takes a parameter `player_id`, and returns a dict containing all the information about the player with that `player_id`. Find the player row by matching `player_id` to the `ID` column in the data.

---

#### Q13: what are the stats for the player with `ID` equal to '242444'?

Use your `player_to_dict` function.  The output should be a dictionary like this:

```python
{'ID': '242444',
 'Name': 'João Félix',
 'Age': 19,
 'Height(cm)': 181,
 'Weight(kg)': 70,
 'Nationality': 'Portugal',
 'Club': 'Atlético Madrid',
 'Value': 28000000,
 'Wage': 38000,
 'Player_Position': 'CF',
 'Preferred_Foot': 'Right',
 'Body_Type': 'Lean',
 'Stamina': 79}
```

#### Q14: What are the stats for the player with `ID` equal to '211300'?

#### Q15: What are the stats for the player with `ID` equal to '198717'?

#### Q16: What are the stats for the player with `ID` equal to '200536'?

#### Q17: How many players are there per body type (see column `Body_Type`)?
Answer in the form of a dictionary mapping body type to player count. Function `get_column` might be useful here.

#### Q18: How many players prefer the left foot (see column `Preferred_Foot`)?
Function `get_column` might be useful here.

#### Q19: What is the average stamina of the club 'FC Bayern München' (see column `Stamina`)?

#### Q20: What is the average wage per club?
Answer in the form of dictionary mapping club name to its average wage.

### Please remember to Kernel->Restart and Run All to check for errors then run the test.py script one more time.

Cheers!


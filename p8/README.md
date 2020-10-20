# Project 8: Going to the Movies

## Clarifications/Corrections

**Find any issues?** Report to us:  
- Yifei Ming [ming5@wisc.edu](mailto:ming5@wisc.edu)
- Changho Shin [cshin23@wisc.edu](mailto:cshin23@wisc.edu)
- Chengwei Lu [clu232@wisc.edu](mailto:clu232@wisc.edu)

## Learning Objectives

In this project, you will:
- integrate relevant information from various sources (e.g. multiple csv files)  
- reinforce your knowledge about dictionaries and lists
- use appropriate data structures for organized and informative presentation (e.g. list of dictionaries)
- continue practicing good coding style 

## Coding Style Requirements

Remember that coding style matters! **We may deduct points for bad coding style.** In addition to the [requirements from p7](https://github.com/msyamkumar/cs220-f20-projects/tree/master/p7), here are several other common bad coding habits to avoid:

- Do not use meaningless names for variables or functions (e.g. uuu = "my name").
- Do not write the exact same code in multiple places.  Instead, wrap this code into a function and call that function whenever the code should be used.
- Do not call unnecessary functions.
- Avoid using slow functions multiple times within a loop.  
- Avoid calling functions that iterate over the entire dataset within another loop. For example, do not call get_column(colname) within a loop; instead, call the function before the loop and store the result in a variable.

## Introduction

Having worked our way through soccer and hurricanes, we are now going to work on the IMDB Movies Dataset. A very exciting fortnight lies ahead where we find out some cool facts about our favorite movies, actors, and directors.

In this project, you will combine the data from the movie and mapping files into a more useful format. As usual, hand in the `main.ipynb` file (use the `#qN` format).  Start by downloading the following files: [`test.py`](https://github.com/msyamkumar/cs220-f20-projects/tree/master/p8/test.py), [`small_mapping.csv`](https://github.com/msyamkumar/cs220-f20-projects/tree/master/p8/small_mapping.csv), [`small_movies.csv`](https://github.com/msyamkumar/cs220-f20-projects/tree/master/p8/small_movies.csv), [`mapping.csv`](https://github.com/msyamkumar/cs220-f20-projects/tree/master/p8/mapping.csv), and [`movies.csv`](https://github.com/msyamkumar/cs220-f20-projects/tree/master/p8/movies.csv).

## The Data

The`small_movies.csv` and `small_mapping.csv` have been provided to help you get your core logic with
some simpler data. Note that in the next project (p9), you will be mostly working mainly with `movies.csv` and
`mapping.csv`. 

`small_movies.csv` and `movies.csv` have 6 columns: `title`, `year`, `rating`, `directors`, `actors`, and `genres`

Here are a few rows from `movies.csv`:
```
title,year,rating,directors,actors,genres
tt1931435,2013,5.6,nm0951698,nm0000134,"Comedy,Drama,Romance"
tt0242252,2001,6.1,nm0796124,"nm0048932,nm0000596,nm0004778","Drama,History,Romance"
tt0066811,1971,6.0,nm0125111,"nm0000621,nm0283499,nm0604702,nm0185281","Comedy,Family"
```

`small_mapping.csv` and `mapping.csv` have 2 columns: `id` and `name`

Here are a few rows from `mapping.csv`:

```
nm0000001,Fred Astaire
nm0000004,John Belushi
nm0000007,Humphrey Bogart
tt0110997,The River Wild
```

Each of those weird alphanumeric sequence is a unique identifier for either an actor or a director or a movie title.

If you are ready, let's get started with data plumbing!


# Data Plumbing

A lot of data science work often involves *plumbing*, the process of
getting messy data into a more useful format.  Data plumbing is the
focus of this project.  We'll develop and test three functions that will be
helpful in project 9:

1. `get_mapping(path)`: this loads a file that can be used to lookup names from IDs
2. `get_raw_movies(path)`: this loads movie data with info represented using IDs
3. `get_movies(movies_path, mapping_path)`: this uses the other two functions to load movie data, then replace IDs with names

---

Start by writing a function that starts like this:

```python
def get_mapping(path):
```

When called, the `path` should refer to one of the mapping files
(e.g., "small_mapping.csv").  The function should return a dictionary
that maps IDs (as keys) to names (as values), based on the file
referenced by `path`.  For example, this code:

```python
mapping = get_mapping("small_mapping.csv")
mapping
```

Should output this (order doesn't matter):

```python
{'nm0000131': 'John Cusack',
 'nm0000154': 'Mel Gibson',
 'nm0000163': 'Dustin Hoffman',
 'nm0000418': 'Danny Glover',
 'nm0000432': 'Gene Hackman',
 'nm0000997': 'Gary Busey',
 'nm0001149': 'Richard Donner',
 'nm0001219': 'Gary Fleder',
 'nm0752751': 'Mitchell Ryan',
 'tt0313542': 'Runaway Jury',
 'tt0093409': 'Lethal Weapon'}
```

Note that the mapping files DO NOT have a CSV header.

The following questions pertain to `small_mapping.csv` unless
otherwise specified.

---

#### Q1: What is returned by your `get_mapping("small_mapping.csv")` function?

Comments: You shouldn't be surprised to see the results are exactly the dictionary shown above if your function works correctly. Please (1) store the result in a variable for use in subsequent questions, and (2) display the result in the Out [N] area so the grading script can find your answer.

Hint: the `process_csv` function from the previous projects might come in handy.

#### Q2: What is the value associated with the key "nm0001219"?

Hint: use the dictionary returned earlier. 

#### Q3: What are the values in the mapping (dictionary) associated with keys that begin with "nm"?

Comments: the answer should be a Python list.

#### Q4: For people with "Gary" as their first name in the above mapping, which keys do they correspond to?

To be consistent, the values for directors, actors, and genres are always of type LIST, even if some of those lists only contain a single item.

---

Let's move on to read movie files! Build a function named `get_raw_movies` that takes the path to a
CSV file (e.g., "small_movies.csv" or "movies.csv") as the only parameter and
returns a list of dictionaries where each dictionary represents a
movie as follows:

```python
{ 
    "title": "movie-id",
    "year": <the year as an integer>,
    "rating": <the rating as a float>,
    "directors": ["director-id1", "director-id2", ...],
    "actors": ["actor-id1", "actor-id2", ....], 
    "genres": ["genre1", "genre2", ...]
}
```

Note that unlike small_mapping.csv, the movie files DO have a CSV header.

To be consistent, the values for `directors`, `actors`, and ```genres```
are always of type LIST, even if some lists might only contain a single item. 

---

#### Q5: What does `get_raw_movies("small_movies.csv")` return?

The result should be this:
```python
[{'title': 'tt0313542',
  'year': 2003,
  'rating': 7.1,
  'directors': ['nm0001219'],
  'actors': ['nm0000131', 'nm0000432', 'nm0000163'],
  'genres': ['Crime', 'Drama', 'Thriller']},
 {'title': 'tt0093409',
  'year': 1987,
  'rating': 7.6,
  'directors': ['nm0001149'],
  'actors': ['nm0000154', 'nm0000418', 'nm0000997', 'nm0752751'],
  'genres': ['Action', 'Crime', 'Thriller']}]
```

Comments: keep the result returned by `get_raw_movies` in a variable for use in answering future questions. Do not call get_raw_movies every time you need data from the movies file.  Remember to convert the type of items to match the above results.



#### Q6: How many actors does the movie at index 1 have?

Hint: use the dictionary from Q5.

#### Q7: What is the ID of the last actor listed for the movie at index 0?

Hint: use the dictionary from Q5 (all actors here are represented by IDs).

---
You may have noticed that `actors`, `directors`, and `title` are represented by IDs instead of actual names. Write a function named
`get_movies(movies_path, mapping_path)` that loads data from the
`movies_path` file using `get_raw_movies` and converts the IDs to
names using a mapping based on the `mapping_path` file, which you
should load using your `get_mapping` function.

Each dictionary in the list should look like this:

```python
{ 
    "title": "the movie name",
    "year": <the year as an integer>,
    "rating": <the rating as a float>,
    "directors": ["director-name1", "director-name2", ...],
    "actors": ["actor-name1", "actor-name2", ....], 
    "genres": ["genre1", "genre2", ...]
}
```

Notice the difference between the previous one and this (IDs are replaced by names). This list of dictionaries is essential for almost all of the following questions.

We recommend you break this down into several steps.  Start with the simple case the `title`: try to translate from the ID code to the name of the movie. Then work on translating for actors and directors after you get the title working. The `actors` and `directors` are more complicated because they are lists.

After you implement your function, call it and store the result as a variable named `small`:

```python
small = get_movies("small_movies.csv", "small_mapping.csv")
```

#### Q8: What is `small`?

The result should have the same format as :

```python
[{'title': 'Runaway Jury',
  'year': 2003,
  'rating': 7.1,
  'directors': ['Gary Fleder'],
  'actors': ['John Cusack', 'Gene Hackman', 'Dustin Hoffman'],
  'genres': ['Crime', 'Drama', 'Thriller']},
 {'title': 'Lethal Weapon',
  'year': 1987,
  'rating': 7.6,
  'directors': ['Richard Donner'],
  'actors': ['Mel Gibson', 'Danny Glover', 'Gary Busey', 'Mitchell Ryan'],
  'genres': ['Action', 'Crime', 'Thriller']}]
```

#### Q9: What is `small[1]["title"]`?

Comment: just paste `small[1]["title"]` into a cell and run it.  We're doing
this to check that the structures in `small` (as returned by
`get_movies` above) contain the correct data.

#### Q10: What is `small[1]["actors"]`?

#### Q11: What is `small[-1]["directors"]`?

---

If you've gotten this far, your functions must be working pretty well
with small datasets.  So let's try the full dataset!

```python
movies = get_movies("movies.csv", "mapping.csv")
```

You are not allowed to call `get_movies` more than once for the
"movies.csv" file in your notebook.  Reuse the `movies` variable
instead, which is more efficient. We will deduct points for bad coding style.

---

#### Q12: What are the 88th to 90th (inclusive) rows in movies?

Please return a list of dictionaries whose format is like this:

```python
[{'title': 'Fortitude and Glory: Angelo Dundee and His Fighters',
  'year': 2012,
  'rating': 7.2,
  'directors': ['Chris Tasara'],
  'actors': ['Angelo Dundee', 'George Foreman', 'Freddie Roach'],
  'genres': ['Sport']},
 {'title': 'Ivanhoe',
  'year': 1952,
  'rating': 6.8,
  'directors': ['Richard Thorpe'],
  'actors': ['Robert Taylor', 'George Sanders'],
  'genres': ['Adventure', 'Drama', 'History']},
 {'title': 'The Great Gatsby',
  'year': 1949,
  'rating': 6.6,
  'directors': ['Elliott Nugent'],
  'actors': ['Alan Ladd', 'Macdonald Carey'],
  'genres': ['Drama']}]
```

------



#### Q13: What are the last 5 rows in movies?

Please return a list of dictionaries whose format is like this:

```python
[{'title': 'Fortitude and Glory: Angelo Dundee and His Fighters',
  'year': 2012,
  'rating': 7.2,
  'directors': ['Chris Tasara'],
  'actors': ['Angelo Dundee', 'George Foreman', 'Freddie Roach'],
  'genres': ['Sport']},
 {'title': 'Ivanhoe',
  'year': 1952,
  'rating': 6.8,
  'directors': ['Richard Thorpe'],
  'actors': ['Robert Taylor', 'George Sanders'],
  'genres': ['Adventure', 'Drama', 'History']},
 {'title': 'The Great Gatsby',
  'year': 1949,
  'rating': 6.6,
  'directors': ['Elliott Nugent'],
  'actors': ['Alan Ladd', 'Macdonald Carey'],
  'genres': ['Drama']}]
```

------

Copy the following function to your notebook, but don't change it in any way.

```python
# you are not allowed to change this function
def filter_movies_by_year(movies, year):
    i = 0
    while i < len(movies):
        if movies[i]["year"] != year:
            movies.pop(i)
        else:
            i += 1
    return movies
```

The `movies` parameter is for a list of movie dictionaries (similar to what is retured by `get_movies`) and `year` is a year to filter on. The function returns the movies in `movies` that were in the given year.

------

#### 

#### Q14: What are the total number of movies from 1949?

Comments: the `filter_movies_by_year()` function has an **undesirable** side effect that we will fix in Q15 and you may need restart the kernel and run all.

Requirements:

1. answer using `filter_movies_by_year`

2. do NOT call `get_movies` on "movies.csv" more than once in your notebook



#### Q15: What are the movies from 1970 with ratings greater than 7.0?

**Hint:** we've set you up a bit to encounter a bug.  Review the copy functions in the `copy` module and see if you can use one of them to overcome the shortcomings of the `filter_movies_by_year` function we're forcing you to use.  You might need to go back and tweak your q14 answer and potentially do a "Restart & Run All" on your notebook after you've fixed the bug.

Return a list of movie dictionaries.

#### Q16: How many unique genres are there in the dataset?

Think about whether you can write a function that helps you with Q17 and Q18 at the same time.

#### Q17: How many unique actor names are there in the dataset?

#### Q18: How many unique director names are there in the dataset?

#### Q19: What is the average rating for all movies?

#### Q20: What is the longest movie title in the dataset ?

#### 

As before, please remember to **Kernel->Restart and Run All** to check for errors then run the test.py script one more time before submission.  To keep your code concise, please **remove our own test code that does not influence the correctness of answers**.

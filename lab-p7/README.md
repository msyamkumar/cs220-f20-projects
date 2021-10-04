# Lab 7: Dictionaries

# WARNING: Unless you took a time portal to become my student in the past, this is not the correct repository :) Please go to the correct github repository for the current semester. If you are a Fall'20 semester student though, you are in the right place.

In this lab, we'll practice problems that requires using dictionaries to help you get ready for P7. 
Start these exercises in a new Jupyter notebook.

## Exercises

### Counting Letters

Fill in the blanks so that `counts` becomes a dictionary where each
key is a character and the corresponding value is how many times it
appeared in the string `PI`.

```python
PI = "three, dot, one, four, one, five, nine, two, six, five, three, five, nine"
counts = {}
for char in ????:
    if not char in counts:
        counts[????] = ????
    else:
        ????[char] += ????
counts
```

If done correctly, your code output should be smilar to something like this:

```python
{'t': 4, 'h': 2, 'r': 3, 'e': 11, ',': 12, ' ': 12, 'd': 1, 'o': 5, 'n': 6, 'f': 4, 'u': 1, 'i': 6, 'v': 3, 'w': 1, 's': 1, 'x': 1}
```

### Counting Words

Fill in the blanks such that counts becomes a dictionary where each key is a word in a list generated from the string `PI` and the corresponding value is how many times it occured in `PI`.

```python
PI = "three, dot, one, four, one, five, nine, two, six, five, three, five, nine"
counts = {}
for word in PI.????(????):
    if ????:
        ????
    else:
        ????
counts
```

If done correctly, your code output should be smilar to something like this:

```python
{'three': 2, 'dot': 1, 'one': 2, 'four': 1, 'five': 3, 'nine': 2, 'two': 1, 'six': 1}
```

### Dictionary from Two Lists

Fill in the blanks to create a dictionary that maps the English words in list `keys` to their corresponding Spanish translations in list `vals`:

```python
keys = ["two", "zero"]
vals = ["dos", "cero"]
en2sp = ???? # empty dictionary
for i in range(len(????)):
    en2sp[keys[????]] = ????
en2sp
```

The resulting dictionary containing the mapping from English to Spanish
words, should look like this:

```python
{'two': 'dos', 'zero': 'cero'}
```

Now lets try using your `en2sp` dictionary to partially translate the following English sentence:

```python
words = "I love Comp Sci two two zero".split(" ")
for i in range(len(words)):
    default = words[i] # don't translate it
    words[i] = en2sp.get(words[i], default)
" ".join(words)
```

Not exactly a replacement for Google translate just yet!, but it's
a good start...

### Flipping Keys and Values

What if we want a dictionary to convert from Spanish back to English?
Complete the code:

```python
sp2en = {}
for en in en2sp:
    sp = ????
    sp2en[sp] = ????
sp2en
```

You should get this:

```python
{ 'dos': 'two', 'cero': 'zero'}
```

### Dictionary Division

What if we want to do multiple division operations, but we have all our
numerators in one dictionary and all our denominators in another. 
Can you fill in the missing code to help do these divisions correctly?

```python
numerators = {"A": 1, "B": 2, "C": 3}
denominators = {"A": 2, "B": 4, "C": 4}
result = {}
for key in ????:
    result[????] = ????[key] / ????[key]
result
````

If done correctly, you should get `{'A': 0.5, 'B': 0.5, 'C': 0.75}`.

### Ordered Print

Complete the code so it prints the incidents per year, with earliest
year first, like this:

```python
incidents = {2016: 14, 2019: 18, 2017: 13, 2018: 16, 2020: 25, 2015: 10}
keys = sorted(list(????.keys()))
for k in ????:
    print(k, incidents[????])
```

```
2015 10
2016 14
2017 13
2018 16
2019 18
2020 25
```

### Histogram

Modify the above code so it prints a yearly vaule histogram using the '*' character, like this:

```
2015 **********
2016 **************
2017 *************
2018 ****************
2019 ******************
2020 *************************
```

### Dictionary Max

Complete the following to find the year with the highest number of incidents:

```python
incidents = {2016: 14, 2019: 18, 2017: 13, 2018: 16, 2020: 25, 2015: 10}
best_key = None
for key in incidents:
    if best_key == None or incidents[????] > incidents[????]:
        best_key = ????
print("Year", best_key, "had", incidents[????], "incidents (the max)")
```

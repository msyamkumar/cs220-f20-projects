# Project 4: Pokémon Simulation

## Corrections/Clarifications
None yet.

**Find any issues?** Report to us: CHENG-WEI LU <clu232@wisc.edu>, TIMOTHY OSSOWSKI <ossowski@wisc.edu>, YUCHEN ZENG <yzeng58@wisc.edu>.

## Overview

For this project, you'll be using the data from `pokemon_stats.csv` to
simulate Pokémon battles. This data was gathered by the Python program
`gen_csv.ipynb` from the website https://www.pokemondb.net/.  This project will
focus on **conditional statements**. To start, download `project.py`,
`test.py` and `pokemon_stats.csv`. You'll do your work in a Jupyter Notebook,
producing a `main.ipynb` file. You'll test as usual by running `python test.py`
to test a `main.ipynb` file.

We won't explain how to use the `project` module here (the code in the
`project.py` file). The lab this week is designed to teach you how it
works. So, before starting P4, take a look at [Lab P4](https://github.com/msyamkumar/cs220-f20-projects/tree/master/lab-p4).

This project consists of writing code to answer 20 questions. If
you're answering a particular question in a cell in your notebook, you
need to put a comment in the cell so we know what you're answering.
For example, if you're answering question 13, the first line of your
cell should contain `#q13`.

## Questions and Functions

For the first few questions, we will try to simulate a very simple 'battle'.
Create a function `simple_battle(pkmn1, pkmn2)` which simply returns the name of
the Pokémon with the highest stat total.

**Hint: In Lab P4, you created a helper function which could be very useful here**
### Q1: What is the output of `simple_battle('Snorunt', 'Starly')`?

### Q2: What is the output of `simple_battle('Snorunt', 'Staravia')`?

---

While we are off to a good start, the function is not quite finished yet. For instance,
consider the Pokémon Charmander and Chimchar. Both of them have the same stat total
of 309. In such cases, we want our function to return the string `'Draw'` instead of
choosing between the two Pokémon.

### Q3: What is the output of `simple_battle('Chikorita', 'Turtwig')`?

---

Our function `simple_battle` is quite rudimentary. Sometimes, when two Pokémon meet in the wild,
the weaker one will run away if it senses it is outmatched. In this case, we want our function to return
a message saying the pokemon ran away. Modify `simple_battle` so that it returns `'<pkmn_name> ran away'` 
if `|stat total of pkmn1 - stat total of pkmn2| > 300`. Make sure the function says the Pokémon with the lower stat
total ran away!

### Q4: What is the output of `simple_battle('Caterpie', 'Melmetal')`?

### Q5: What is the output of `simple_battle('Dragonite', 'Snorunt')`?

---

Our function `simple_battle` is a good start, but we can make our battles a bit
more interesting. Let us set up some rules for our battles.

1. The Pokémon take turns attacking each other.
2. The Pokémon with the higher Speed stat attacks first.
3. On each turn, the attacking Pokémon can choose between two moves - Physical
or Special
4. Based on the move chosen by the attacking Pokémon, the defending Pokémon
receives damage to its HP.
5. If a Pokémon's HP drops to (or below) 0, it faints and therefore loses
the battle.

The damage caused by a Pokémon's Physical move is `10 * Attack stat of
Attacker / Defense stat of Defender`, and the damage caused by a Pokémon's
Special move is `10 * Sp. Atk. stat of Attacker / Sp. Def. stat of Defender`.

**If a Pokémon wants to win, it should always choose the move which will do
more damage.**

For example, let the attacker be Scraggy and the defender be Tranquill. Their
stats are as follows:
```python
>>> project.print_stats('Scraggy')
Name :  Scraggy
Region :  Unova
Type 1 :  Dark
Type 2 :  Fighting
HP :  50
Attack :  75
Defense :  70
Sp. Atk :  35
Sp. Def :  70
Speed :  48
>>> project.print_stats('Tranquill')
Name :  Tranquill
Region :  Unova
Type 1 :  Normal
Type 2 :  Flying
HP :  62
Attack :  77
Defense :  62
Sp. Atk :  50
Sp. Def :  42
Speed :  65
>>>
```
The damage caused by Scraggy's physical move will be `10*75/62`, which is `12.0967`,
while the damage caused by its special move will be `10*35/42`, which is `8.33`.
**So, in this case, when facing Tranquill, Scraggy would always choose its physical
move to do `12.0967` damage.**

Copy/paste the following code in a new cell of your notebook and fill in the details.

```python
def most_damage(attacker, defender):
    physical_damage = 10 * project.get_attack(attacker)/project.get_defense(defender)
    special_damage = ???
    if ???:
        return physical_damage
    else:
        ???
```

Verify that `most_damage('Scraggy', 'Tranquill')` returns `12.0967`.

For the following questions, assume the attacking pokemon chooses the move that does the most damage:

### Q6: How much damage does Dragonite do to Rockruff?

### Q7: How much damage does Quilava do to Grovyle?

### Q8: How much damage does Goomy do to Beedrill?

### Q9: How much damage does Tepig do to Charizard?

---

Now that we have a way of calculating the damage done by the Pokémon during
battle, we have to calculate how many hits each Pokémon can take before fainting.

Going back to our previous example, we saw that Scraggy does `12.0967` damage to
Tranquill, each turn. Since Tranquill has HP `62`, it can take a total of `62/12.0697
= 5.125` hits, which is rounded up to `6` hits. So, Tranquill
can take `6` hits from Scraggy before it faints.

Copy/paste the following code in a new cell of your notebook and fill in the details.

```python
def num_hits(attacker, defender):
    return math.ceil(project.get_hp(???)/???)
```

**Hint: You might want to use the method [math.ceil()](https://docs.python.org/3/library/math.html) here. First import the module math
and then look up the documentation of math.ceil to see how you could use it.**

### Q10: How many hits can Goomy take from Gible?

### Q11: How many hits can Donphan take from Aipom?

### Q12: How many hits can Aipom take from Donphan?

---

Since Donphan can take more hits from Aipom than Aipom can from Donphan, clearly
Donphan would win in a battle between the two. With the tools we have created
so far, we can now finally create a battle simulator. Copy/paste the following
code in a new cell of your notebook and fill in the details.


```python
def battle(pkmn1, pkmn2):
    #TODO: Return the name of the pkmn that can take more hits from the other
    # pkmn. If both pkmn faint within the same number of moves, return the
    # string 'Draw'
```

### Q13: What is the output of `battle('Scraggy', 'Krabby')`?

### Q14: What is the output of `battle('Charizard', 'Krabby')`?


---

You may have noticed that the function `battle` does not quite follow all the rules
that we laid out at the beginning. Look at the output of `battle('Swadloon', 'Palpitoad')`.
You will find that it is a draw, since they can both take 7 hits from the other Pokémon.
But since Palpitoad has a higher Speed, it attacks first, so it will land its
seventh hit on Swadloon, before Swadloon can hit Palpitoad. So, even though they
both go down in the same number of moves, Palpitoad should win the battle.

Go back and modify `battle()` so that if both Pokémon faint in the same number of
moves, the Pokémon with the higher Speed wins. If they both have the same Speed,
then the battle should be a `'Draw'`.

### Q15: What is the output of `battle('Treecko', 'Litten')`?

### Q16: What is the output of `battle('Treecko', 'Buizel')`?

---

One last rule we need to implement is the run away feature we coded in simple_battle(). 
It is more reasonable to compare the number of hits a Pokémon can take instead of total stats
in deciding whether it should run away. For example, consider
a battle between Pikachu and Incineroar. Since Incineroar can take 15 hits from Pikachu, 
but Pikachu can only take 2 hits from Incineroar, Pikachu should run away from this battle. 

Modify `battle()` so that if `|num_hits_pkmn1_can_take - num_hits_pkmn2_can_take| > 10`, the function
returns `<pkmn_name> ran away'`. Make sure the function says the Pokémon that can take 
less hits ran away!


### Q17: What is the output of `battle('Metapod', 'Talonflame')`?

### Q18: What is the output of `battle('Leavanny', 'Noibat')`?

---

Our function `battle` is now working just as intended. But let us build some checks
and balances into the function, to make it more reasonable. We will assume that
Pokémon from different regions cannot battle each other, since they can't both meet
each other.

Create a new function `final_battle(pkmn1, pkmn2)` so that if two Pokémon from
different regions try to fight each other, the function returns `'Cannot battle'`.
If both Pokémon are from the same region, the battle proceeds as before.

### Q19: What is the output of `final_battle('Grotle', 'Roggenrola')`?

---

This restriction however, is a little too harsh. We can assume that Pokémon whose
type (Type 1 or Type 2) is `Flying` can reach other regions by flying there.

Modify `final_battle` so that even if the two Pokémon are from different regions, if the
Type 1 **or** Type 2 of the Attacker is 'Flying', then the battle can
take place as before.

### Q20: What is the output of `final_battle('Starly', 'Goodra')`?

---


That will be all for now. If you are interested, you can make your `battle` functions
as complicated as you want. Good luck with your project!

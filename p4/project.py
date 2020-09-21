__pokemon__= {}

def __init__():
    """This function will read the data from 'pokemon_stats.csv' and store it in a dictionary of dictionaries"""
    import csv
    f = open('pokemon_stats.csv', encoding='utf-8')
    data = list(csv.reader(f))
    f.close()
    header = data[0]
    header.pop(0)
    data = data[1:]
    for pkmn_data in data:
        pkmn_data.pop(0)
        pkmn = {}
        for i in range(len(header)):
            pkmn[header[i]] = pkmn_data[i]
        for stat in pkmn:
            if stat in ['HP', 'Attack', 'Defense', 'Sp. Atk', 'Sp. Def', 'Speed']:
                pkmn[stat] = int(pkmn[stat])
        __pokemon__[pkmn["Name"]] = pkmn

def print_stats(pkmn):
    """print_stats(pkmn) prints all the statistics of the Pokémon with the name 'pkmn' """
    try:
        for stat in __pokemon__[pkmn]:
            if not (stat == 'Type 2' and __pokemon__[pkmn][stat] == "None"):
                print(stat, ": ", __pokemon__[pkmn][stat])
    except KeyError:
        print(pkmn, " not found in the file")

def get_region(pkmn):
    """get_region(pkmn) returns the region of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Region']

def get_type1(pkmn):
    """get_type1(pkmn) returns Type 1 of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Type 1']

def get_type2(pkmn):
    """get_type2(pkmn) returns Type 2 of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Type 2']

def get_hp(pkmn):
    """get_hp(pkmn) returns the HP of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['HP']

def get_attack(pkmn):
    """get_attack(pkmn) returns the Attack of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Attack']

def get_defense(pkmn):
    """get_defense(pkmn) returns the Defense of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Defense']

def get_sp_atk(pkmn):
    """get_sp_atk(pkmn) returns the Special Attack of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Sp. Atk']

def get_sp_def(pkmn):
    """get_sp_def(pkmn) returns the Special Defense of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Sp. Def']

def get_speed(pkmn):
    """get_speed(pkmn) returns the Speed of the Pokémon with the name 'pkmn' """
    return __pokemon__[pkmn]['Speed']

__init__()
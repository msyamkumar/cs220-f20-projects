#!/usr/bin/python

import json
import os
import subprocess
import sys
import importlib
import inspect
import traceback
import re, ast, math
from collections import namedtuple, OrderedDict, defaultdict
from functools import wraps
from cleanMAC import clean

clean()

PASS = 'PASS'
FAIL_STDERR = 'Program produced an error - please scroll up for more details.'
FAIL_JSON = 'Expected program to print in json format. Make sure the only print statement is a print(json.dumps...)!'
EPSILON = 0.0001

obfuscate1 = "Tweet"
obfuscate2 = ['tweet_id', 'username', 'num_liked', 'length']
TEXT_FORMAT = "text"
PNG_FORMAT = "png"
Question = namedtuple("Question", ["number", "weight", "format"])
Tweet = namedtuple(obfuscate1, obfuscate2)

questions = [
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
    Question(number=20, weight=1, format=TEXT_FORMAT)
]
question_nums = set([q.number for q in questions])

expected_json = {
    "1": sorted(['1.csv', '2.csv', '1.json', '2.json'], reverse=True),
    "2": ['meta.info', 'agency_info', '5.json', '5.csv', '4.json', '4.csv', '3.json', '3.csv',
         '2.json', '2.csv', '1.json', '1.csv'],
    "3": sorted([os.path.join('sample_data','1.csv'),
                 os.path.join('sample_data','1.json'),
                 os.path.join('sample_data','2.csv'),
                 os.path.join('sample_data','2.json')], reverse=True),
    "4": sorted([os.path.join('full_data','1.csv'),
             os.path.join('full_data','1.json'),
             os.path.join('full_data','2.csv'),
             os.path.join('full_data','2.json'),
             os.path.join('full_data','3.csv'),
             os.path.join('full_data','3.json'),
             os.path.join('full_data','4.csv'),
             os.path.join('full_data','4.json'),
             os.path.join('full_data','5.csv'),
             os.path.join('full_data','5.json'),
             os.path.join('full_data','agency_info'),
             os.path.join('full_data','meta.info')], reverse=True),
    "5": sorted([os.path.join('sample_data','1.csv'),
                 os.path.join('sample_data','2.csv')], reverse=True),
    "6": sorted([os.path.join('full_data','1.csv'),
             os.path.join('full_data','2.csv'),
             os.path.join('full_data','3.csv'),
             os.path.join('full_data','4.csv'),
             os.path.join('full_data','5.csv'),
             os.path.join('full_data','meta.info')], reverse=True),
    "7": [Tweet(tweet_id='1467811372', username='USERID_6', num_liked=5882, length=29),
            Tweet(tweet_id='1467811592', username='USERID_8', num_liked=2676, length=11),
            Tweet(tweet_id='1467811594', username='USERID_9', num_liked=2182, length=99),
            Tweet(tweet_id='1467811795', username='USERID_1', num_liked=7791, length=36),
            Tweet(tweet_id='1467812025', username='USERID_1', num_liked=8149, length=25)],
    "8": [Tweet(tweet_id='1467844540', username='USERID_9', num_liked=6366, length=49),
             Tweet(tweet_id='1467844907', username='USERID_3', num_liked=8770, length=42),
             Tweet(tweet_id='1467845095', username='USERID_4', num_liked=8567, length=126),
             Tweet(tweet_id='1467845157', username='USERID_8', num_liked=5761, length=17),
             Tweet(tweet_id='1467852031', username='USERID_2', num_liked=4565, length=63),
             Tweet(tweet_id='1467852067', username='USERID_4', num_liked=9594, length=34),
             Tweet(tweet_id='1467852789', username='USERID_10', num_liked=686, length=44),
             Tweet(tweet_id='1467853135', username='USERID_1', num_liked=6515, length=131),
             Tweet(tweet_id='1467853356', username='USERID_10', num_liked=3192, length=136),
             Tweet(tweet_id='1467853431', username='USERID_10', num_liked=9936, length=30),
             Tweet(tweet_id='1467853479', username='USERID_9', num_liked=4939, length=24),
             Tweet(tweet_id='1467854062', username='USERID_10', num_liked=9346, length=92),
             Tweet(tweet_id='1467854345', username='USERID_9', num_liked=7959, length=72),
             Tweet(tweet_id='1467854706', username='USERID_1', num_liked=8972, length=103),
             Tweet(tweet_id='1467854917', username='USERID_2', num_liked=7741, length=30),
             Tweet(tweet_id='1467855673', username='USERID_9', num_liked=9728, length=72),
             Tweet(tweet_id='1467855812', username='USERID_2', num_liked=4806, length=28),
             Tweet(tweet_id='1467855981', username='USERID_2', num_liked=6455, length=92),
             Tweet(tweet_id='1467856044', username='USERID_7', num_liked=1442, length=49),
             Tweet(tweet_id='1467856352', username='USERID_3', num_liked=523, length=20),
             Tweet(tweet_id='1467856426', username='USERID_6', num_liked=8675, length=99),
             Tweet(tweet_id='1467856497', username='USERID_7', num_liked=3105, length=79),
             Tweet(tweet_id='1467856632', username='USERID_1', num_liked=1724, length=43),
             Tweet(tweet_id='1467856821', username='USERID_6', num_liked=5145, length=80),
             Tweet(tweet_id='1467856919', username='USERID_4', num_liked=3887, length=61),
             Tweet(tweet_id='1467857221', username='USERID_5', num_liked=3589, length=102),
             Tweet(tweet_id='1467857297', username='USERID_1', num_liked=736, length=70),
             Tweet(tweet_id='1467857378', username='USERID_4', num_liked=9459, length=81),
             Tweet(tweet_id='1467857511', username='USERID_7', num_liked=3713, length=127),
             Tweet(tweet_id='1467857722', username='USERID_8', num_liked=9072, length=55),
             Tweet(tweet_id='1467857975', username='USERID_9', num_liked=4893, length=21),
             Tweet(tweet_id='1467858363', username='USERID_10', num_liked=4263, length=119),
             Tweet(tweet_id='1467858627', username='USERID_3', num_liked=8400, length=120),
             Tweet(tweet_id='1467858869', username='USERID_10', num_liked=1609, length=48),
             Tweet(tweet_id='1467859025', username='USERID_4', num_liked=5618, length=81),
             Tweet(tweet_id='1467859066', username='USERID_9', num_liked=99, length=53),
             Tweet(tweet_id='1467859408', username='USERID_5', num_liked=2878, length=128),
             Tweet(tweet_id='1467859436', username='USERID_7', num_liked=8001, length=67),
             Tweet(tweet_id='1467859558', username='USERID_1', num_liked=8732, length=136),
             Tweet(tweet_id='1467859666', username='USERID_9', num_liked=9158, length=16),
             Tweet(tweet_id='1467859820', username='USERID_10', num_liked=7921, length=27),
             Tweet(tweet_id='1467859922', username='USERID_6', num_liked=3955, length=120),
             Tweet(tweet_id='1467860895', username='USERID_1', num_liked=2055, length=18),
             Tweet(tweet_id='1467860904', username='USERID_7', num_liked=9851, length=30),
             Tweet(tweet_id='1467861095', username='USERID_10', num_liked=7191, length=38),
             Tweet(tweet_id='1467861522', username='USERID_1', num_liked=2742, length=70),
             Tweet(tweet_id='1467861571', username='USERID_1', num_liked=7095, length=84),
             Tweet(tweet_id='1467862213', username='USERID_2', num_liked=2455, length=138),
             Tweet(tweet_id='1467862313', username='USERID_10', num_liked=3256, length=127),
             Tweet(tweet_id='1467862355', username='USERID_3', num_liked=4110, length=53)],
    "9": [Tweet(tweet_id='1467876711', username='USERID_10', num_liked=1117, length=84),
           Tweet(tweet_id='1467877496', username='USERID_1', num_liked=2062, length=106),
           Tweet(tweet_id='1467877833', username='USERID_2', num_liked=4270, length=89),
           Tweet(tweet_id='1467877865', username='USERID_1', num_liked=5899, length=30),
           Tweet(tweet_id='1467878057', username='USERID_6', num_liked=703, length=42),
           Tweet(tweet_id='1467878557', username='USERID_6', num_liked=5814, length=61),
           Tweet(tweet_id='1467878633', username='USERID_2', num_liked=2351, length=33),
           Tweet(tweet_id='1467878971', username='USERID_2', num_liked=2238, length=27),
           Tweet(tweet_id='1467878983', username='USERID_8', num_liked=4860, length=61),
           Tweet(tweet_id='1467879480', username='USERID_4', num_liked=1345, length=97),
           Tweet(tweet_id='1467879984', username='USERID_2', num_liked=3694, length=69),
           Tweet(tweet_id='1467880085', username='USERID_4', num_liked=2478, length=120),
           Tweet(tweet_id='1467880431', username='USERID_3', num_liked=9407, length=85),
           Tweet(tweet_id='1467880442', username='USERID_2', num_liked=5125, length=96),
           Tweet(tweet_id='1467880463', username='USERID_9', num_liked=1226, length=29),
           Tweet(tweet_id='1467880692', username='USERID_6', num_liked=4989, length=49),
           Tweet(tweet_id='1467881131', username='USERID_10', num_liked=732, length=107),
           Tweet(tweet_id='1467881373', username='USERID_6', num_liked=8615, length=145),
           Tweet(tweet_id='1467881376', username='USERID_4', num_liked=4378, length=49),
           Tweet(tweet_id='1467881457', username='USERID_7', num_liked=119, length=27),
           Tweet(tweet_id='1467881686', username='USERID_5', num_liked=8136, length=46),
           Tweet(tweet_id='1467881809', username='USERID_4', num_liked=1797, length=138),
           Tweet(tweet_id='1467881897', username='USERID_5', num_liked=2314, length=76),
           Tweet(tweet_id='1467881920', username='USERID_3', num_liked=4101, length=112),
           Tweet(tweet_id='1467882140', username='USERID_8', num_liked=5320, length=137),
           Tweet(tweet_id='1467882491', username='USERID_10', num_liked=3512, length=55),
           Tweet(tweet_id='1467882592', username='USERID_10', num_liked=1887, length=67),
           Tweet(tweet_id='1467882902', username='USERID_3', num_liked=4646, length=48),
           Tweet(tweet_id='1467888679', username='USERID_8', num_liked=3089, length=27),
           Tweet(tweet_id='1467888732', username='USERID_7', num_liked=2800, length=48),
           Tweet(tweet_id='1467888953', username='USERID_3', num_liked=3951, length=46),
           Tweet(tweet_id='1467889231', username='USERID_5', num_liked=1320, length=79),
           Tweet(tweet_id='1467889334', username='USERID_5', num_liked=8495, length=42),
           Tweet(tweet_id='1467889574', username='USERID_1', num_liked=4696, length=123),
           Tweet(tweet_id='1467889791', username='USERID_5', num_liked=4027, length=132),
           Tweet(tweet_id='1467889988', username='USERID_2', num_liked=7394, length=51),
           Tweet(tweet_id='1467890079', username='USERID_8', num_liked=2556, length=38),
           Tweet(tweet_id='1467890222', username='USERID_2', num_liked=227, length=107),
           Tweet(tweet_id='1467890723', username='USERID_1', num_liked=96, length=134),
           Tweet(tweet_id='1467891826', username='USERID_9', num_liked=2021, length=113),
           Tweet(tweet_id='1467891880', username='USERID_7', num_liked=6847, length=96),
           Tweet(tweet_id='1467892075', username='USERID_6', num_liked=2816, length=124),
           Tweet(tweet_id='1467892515', username='USERID_5', num_liked=917, length=39),
           Tweet(tweet_id='1467892667', username='USERID_2', num_liked=8270, length=20),
           Tweet(tweet_id='1467892720', username='USERID_3', num_liked=3227, length=128)],
    "10": [Tweet(tweet_id='1467812416', username='USERID_9', num_liked=5278, length=43),
            Tweet(tweet_id='1467812579', username='USERID_1', num_liked=9700, length=26),
            Tweet(tweet_id='1467812723', username='USERID_3', num_liked=5414, length=94),
            Tweet(tweet_id='1467812771', username='USERID_8', num_liked=2190, length=77),
            Tweet(tweet_id='1467812784', username='USERID_10', num_liked=2667, length=117)],
    "11": [Tweet(tweet_id='1467810369', username='USERID_4', num_liked=315, length=115),
        Tweet(tweet_id='1467810672', username='USERID_8', num_liked=5298, length=111),
        Tweet(tweet_id='1467810917', username='USERID_8', num_liked=533, length=89),
        Tweet(tweet_id='1467811184', username='USERID_6', num_liked=2650, length=47),
        Tweet(tweet_id='1467811193', username='USERID_8', num_liked=2101, length=111)],
    "12":[Tweet(tweet_id='1467944581', username='USERID_1', num_liked=7216, length=131),
           Tweet(tweet_id='1467944654', username='USERID_7', num_liked=2838, length=59),
           Tweet(tweet_id='1467944871', username='USERID_1', num_liked=9393, length=51),
           Tweet(tweet_id='1467945476', username='USERID_10', num_liked=9246, length=33),
           Tweet(tweet_id='1467945704', username='USERID_1', num_liked=526, length=62),
           Tweet(tweet_id='1467945787', username='USERID_9', num_liked=8850, length=81),
           Tweet(tweet_id='1467945885', username='USERID_4', num_liked=9403, length=67),
           Tweet(tweet_id='1467946026', username='USERID_1', num_liked=2861, length=69),
           Tweet(tweet_id='1467946137', username='USERID_1', num_liked=5470, length=135),
           Tweet(tweet_id='1467946559', username='USERID_6', num_liked=987, length=116),
           Tweet(tweet_id='1467946592', username='USERID_3', num_liked=9085, length=137),
           Tweet(tweet_id='1467946749', username='USERID_4', num_liked=3381, length=42),
           Tweet(tweet_id='1467946810', username='USERID_4', num_liked=5338, length=62),
           Tweet(tweet_id='1467947005', username='USERID_7', num_liked=6974, length=53),
           Tweet(tweet_id='1467947104', username='USERID_6', num_liked=5847, length=24),
           Tweet(tweet_id='1467947557', username='USERID_9', num_liked=8449, length=110),
           Tweet(tweet_id='1467947713', username='USERID_7', num_liked=7444, length=140),
           Tweet(tweet_id='1467947913', username='USERID_2', num_liked=8578, length=36),
           Tweet(tweet_id='1467948169', username='USERID_1', num_liked=4545, length=33),
           Tweet(tweet_id='1467948434', username='USERID_9', num_liked=770, length=53),
           Tweet(tweet_id='1467948521', username='USERID_4', num_liked=8276, length=100),
           Tweet(tweet_id='1467948526', username='USERID_3', num_liked=7010, length=64),
           Tweet(tweet_id='1467948979', username='USERID_10', num_liked=9209, length=93),
           Tweet(tweet_id='1467949047', username='USERID_3', num_liked=7231, length=30),
           Tweet(tweet_id='1467949516', username='USERID_3', num_liked=4787, length=104),
           Tweet(tweet_id='1467949681', username='USERID_5', num_liked=5318, length=36),
           Tweet(tweet_id='1467949746', username='USERID_8', num_liked=4383, length=8),
           Tweet(tweet_id='1467949969', username='USERID_3', num_liked=1177, length=80),
           Tweet(tweet_id='1467950027', username='USERID_10', num_liked=8575, length=26),
           Tweet(tweet_id='1467950029', username='USERID_1', num_liked=7362, length=119),
           Tweet(tweet_id='1467950217', username='USERID_7', num_liked=1241, length=63),
           Tweet(tweet_id='1467950510', username='USERID_7', num_liked=5002, length=34),
           Tweet(tweet_id='1467950588', username='USERID_4', num_liked=589, length=63),
           Tweet(tweet_id='1467950600', username='USERID_3', num_liked=5951, length=71),
           Tweet(tweet_id='1467950649', username='USERID_7', num_liked=9449, length=46),
           Tweet(tweet_id='1467950687', username='USERID_3', num_liked=3464, length=70),
           Tweet(tweet_id='1467950866', username='USERID_4', num_liked=122, length=27),
           Tweet(tweet_id='1467950975', username='USERID_3', num_liked=6793, length=74),
           Tweet(tweet_id='1467951016', username='USERID_5', num_liked=7795, length=80),
           Tweet(tweet_id='1467951035', username='USERID_9', num_liked=3477, length=114),
           Tweet(tweet_id='1467951252', username='USERID_2', num_liked=7515, length=48),
           Tweet(tweet_id='1467951422', username='USERID_6', num_liked=2520, length=98),
           Tweet(tweet_id='1467951568', username='USERID_8', num_liked=39, length=98),
           Tweet(tweet_id='1467951850', username='USERID_8', num_liked=1170, length=29),
           Tweet(tweet_id='1467951931', username='USERID_4', num_liked=5320, length=81),
           Tweet(tweet_id='1467952069', username='USERID_7', num_liked=399, length=24),
           Tweet(tweet_id='1467952100', username='USERID_1', num_liked=2754, length=69),
           Tweet(tweet_id='1467952123', username='USERID_9', num_liked=9222, length=137),
           Tweet(tweet_id='1467952985', username='USERID_4', num_liked=6256, length=118),
           Tweet(tweet_id='1467953090', username='USERID_2', num_liked=1896, length=64)],
    "13": [Tweet(tweet_id='1467916851', username='USERID_3', num_liked=559, length=58),
             Tweet(tweet_id='1467916959', username='USERID_2', num_liked=7081, length=69),
             Tweet(tweet_id='1467917177', username='USERID_3', num_liked=9678, length=105),
             Tweet(tweet_id='1467917302', username='USERID_5', num_liked=1624, length=35),
             Tweet(tweet_id='1467917484', username='USERID_1', num_liked=4679, length=94),
             Tweet(tweet_id='1467917499', username='USERID_4', num_liked=2851, length=51),
             Tweet(tweet_id='1467917718', username='USERID_1', num_liked=1344, length=84),
             Tweet(tweet_id='1467917800', username='USERID_6', num_liked=7810, length=55),
             Tweet(tweet_id='1467918015', username='USERID_2', num_liked=1508, length=97),
             Tweet(tweet_id='1467918552', username='USERID_3', num_liked=8973, length=44),
             Tweet(tweet_id='1467918560', username='USERID_6', num_liked=6796, length=131),
             Tweet(tweet_id='1467918682', username='USERID_2', num_liked=8884, length=102),
             Tweet(tweet_id='1467918728', username='USERID_6', num_liked=903, length=58),
             Tweet(tweet_id='1467918812', username='USERID_3', num_liked=2835, length=99),
             Tweet(tweet_id='1467918850', username='USERID_2', num_liked=5383, length=103),
             Tweet(tweet_id='1467919055', username='USERID_2', num_liked=5370, length=68),
             Tweet(tweet_id='1467919452', username='USERID_5', num_liked=2839, length=10),
             Tweet(tweet_id='1467919538', username='USERID_10', num_liked=406, length=83),
             Tweet(tweet_id='1467919762', username='USERID_5', num_liked=4035, length=139),
             Tweet(tweet_id='1467919765', username='USERID_7', num_liked=5237, length=124),
             Tweet(tweet_id='1467922983', username='USERID_3', num_liked=8024, length=94),
             Tweet(tweet_id='1467923235', username='USERID_9', num_liked=9662, length=134),
             Tweet(tweet_id='1467923247', username='USERID_1', num_liked=1211, length=44),
             Tweet(tweet_id='1467923370', username='USERID_5', num_liked=2601, length=117),
             Tweet(tweet_id='1467923445', username='USERID_4', num_liked=3462, length=52),
             Tweet(tweet_id='1467923775', username='USERID_9', num_liked=4869, length=33),
             Tweet(tweet_id='1467924273', username='USERID_3', num_liked=825, length=35),
             Tweet(tweet_id='1467924690', username='USERID_9', num_liked=2250, length=41),
             Tweet(tweet_id='1467924823', username='USERID_6', num_liked=7229, length=59),
             Tweet(tweet_id='1467925327', username='USERID_9', num_liked=8401, length=99),
             Tweet(tweet_id='1467925657', username='USERID_5', num_liked=7082, length=69),
             Tweet(tweet_id='1467926153', username='USERID_5', num_liked=2376, length=56),
             Tweet(tweet_id='1467926444', username='USERID_2', num_liked=1394, length=61),
             Tweet(tweet_id='1467926632', username='USERID_2', num_liked=2602, length=98),
             Tweet(tweet_id='1467927016', username='USERID_6', num_liked=48, length=87),
             Tweet(tweet_id='1467927126', username='USERID_5', num_liked=468, length=126),
             Tweet(tweet_id='1467927987', username='USERID_3', num_liked=4156, length=39),
             Tweet(tweet_id='1467928014', username='USERID_7', num_liked=9830, length=18),
             Tweet(tweet_id='1467928037', username='USERID_3', num_liked=4319, length=138),
             Tweet(tweet_id='1467928300', username='USERID_9', num_liked=9681, length=79),
             Tweet(tweet_id='1467928490', username='USERID_7', num_liked=1065, length=57),
             Tweet(tweet_id='1467928676', username='USERID_10', num_liked=9187, length=84),
             Tweet(tweet_id='1467928749', username='USERID_10', num_liked=7504, length=99),
             Tweet(tweet_id='1467928764', username='USERID_2', num_liked=9026, length=41),
             Tweet(tweet_id='1467929184', username='USERID_4', num_liked=1977, length=21),
             Tweet(tweet_id='1467929230', username='USERID_6', num_liked=3724, length=47),
             Tweet(tweet_id='1467929248', username='USERID_7', num_liked=4986, length=66),
             Tweet(tweet_id='1467929601', username='USERID_9', num_liked=366, length=99),
             Tweet(tweet_id='1467929915', username='USERID_5', num_liked=4550, length=146),
             Tweet(tweet_id='1467930017', username='USERID_7', num_liked=2627, length=14)],
    "14": [Tweet(tweet_id='1467945476', username='USERID_10', num_liked=9246, length=33),
             Tweet(tweet_id='1467946749', username='USERID_4', num_liked=3381, length=42),
             Tweet(tweet_id='1467947104', username='USERID_6', num_liked=5847, length=24),
             Tweet(tweet_id='1467947913', username='USERID_2', num_liked=8578, length=36),
             Tweet(tweet_id='1467948169', username='USERID_1', num_liked=4545, length=33),
             Tweet(tweet_id='1467949047', username='USERID_3', num_liked=7231, length=30),
             Tweet(tweet_id='1467949681', username='USERID_5', num_liked=5318, length=36),
             Tweet(tweet_id='1467949746', username='USERID_8', num_liked=4383, length=8),
             Tweet(tweet_id='1467950027', username='USERID_10', num_liked=8575, length=26),
             Tweet(tweet_id='1467950510', username='USERID_7', num_liked=5002, length=34),
             Tweet(tweet_id='1467950649', username='USERID_7', num_liked=9449, length=46),
             Tweet(tweet_id='1467950866', username='USERID_4', num_liked=122, length=27),
             Tweet(tweet_id='1467951252', username='USERID_2', num_liked=7515, length=48),
             Tweet(tweet_id='1467951850', username='USERID_8', num_liked=1170, length=29),
             Tweet(tweet_id='1467952069', username='USERID_7', num_liked=399, length=24),
             Tweet(tweet_id='1467953277', username='USERID_2', num_liked=494, length=31),
             Tweet(tweet_id='1467953367', username='USERID_6', num_liked=552, length=40),
             Tweet(tweet_id='1467953738', username='USERID_1', num_liked=1544, length=46),
             Tweet(tweet_id='1467959908', username='USERID_1', num_liked=2241, length=8),
             Tweet(tweet_id='1467960066', username='USERID_8', num_liked=8350, length=28),
             Tweet(tweet_id='1467961091', username='USERID_10', num_liked=9184, length=38),
             Tweet(tweet_id='1467961817', username='USERID_4', num_liked=3179, length=27),
             Tweet(tweet_id='1467962502', username='USERID_5', num_liked=7788, length=32),
             Tweet(tweet_id='1467962938', username='USERID_3', num_liked=8703, length=42),
             Tweet(tweet_id='1467963477', username='USERID_6', num_liked=5004, length=47),
             Tweet(tweet_id='1467965949', username='USERID_9', num_liked=8308, length=29),
             Tweet(tweet_id='1467966187', username='USERID_7', num_liked=7995, length=39),
             Tweet(tweet_id='1467966260', username='USERID_4', num_liked=6040, length=25),
             Tweet(tweet_id='1467966271', username='USERID_1', num_liked=4664, length=38),
             Tweet(tweet_id='1467966560', username='USERID_5', num_liked=767, length=43),
             Tweet(tweet_id='1467966646', username='USERID_7', num_liked=9821, length=47),
             Tweet(tweet_id='1467967089', username='USERID_6', num_liked=7597, length=19),
             Tweet(tweet_id='1467917302', username='USERID_5', num_liked=1624, length=35),
             Tweet(tweet_id='1467918552', username='USERID_3', num_liked=8973, length=44),
             Tweet(tweet_id='1467919452', username='USERID_5', num_liked=2839, length=10),
             Tweet(tweet_id='1467923247', username='USERID_1', num_liked=1211, length=44),
             Tweet(tweet_id='1467923775', username='USERID_9', num_liked=4869, length=33),
             Tweet(tweet_id='1467924273', username='USERID_3', num_liked=825, length=35),
             Tweet(tweet_id='1467924690', username='USERID_9', num_liked=2250, length=41),
             Tweet(tweet_id='1467927987', username='USERID_3', num_liked=4156, length=39),
             Tweet(tweet_id='1467928014', username='USERID_7', num_liked=9830, length=18),
             Tweet(tweet_id='1467928764', username='USERID_2', num_liked=9026, length=41),
             Tweet(tweet_id='1467929184', username='USERID_4', num_liked=1977, length=21),
             Tweet(tweet_id='1467929230', username='USERID_6', num_liked=3724, length=47),
             Tweet(tweet_id='1467930017', username='USERID_7', num_liked=2627, length=14),
             Tweet(tweet_id='1467930083', username='USERID_6', num_liked=6650, length=48),
             Tweet(tweet_id='1467931027', username='USERID_5', num_liked=1699, length=26),
             Tweet(tweet_id='1467933295', username='USERID_1', num_liked=6234, length=14),
             Tweet(tweet_id='1467933662', username='USERID_5', num_liked=5510, length=39),
             Tweet(tweet_id='1467933685', username='USERID_6', num_liked=8653, length=39),
             Tweet(tweet_id='1467934184', username='USERID_9', num_liked=8463, length=31),
             Tweet(tweet_id='1467934606', username='USERID_10', num_liked=7842, length=31),
             Tweet(tweet_id='1467935121', username='USERID_2', num_liked=8740, length=37),
             Tweet(tweet_id='1467935345', username='USERID_9', num_liked=2980, length=45),
             Tweet(tweet_id='1467936498', username='USERID_5', num_liked=313, length=16),
             Tweet(tweet_id='1467936541', username='USERID_5', num_liked=2821, length=47),
             Tweet(tweet_id='1467936901', username='USERID_5', num_liked=9181, length=24),
             Tweet(tweet_id='1467937038', username='USERID_3', num_liked=5684, length=21),
             Tweet(tweet_id='1467937250', username='USERID_3', num_liked=4415, length=15),
             Tweet(tweet_id='1467943851', username='USERID_6', num_liked=1658, length=42),
             Tweet(tweet_id='1467944261', username='USERID_1', num_liked=7023, length=40),
             Tweet(tweet_id='1467892945', username='USERID_4', num_liked=8101, length=43),
             Tweet(tweet_id='1467893504', username='USERID_9', num_liked=4940, length=25),
             Tweet(tweet_id='1467894749', username='USERID_5', num_liked=6311, length=40),
             Tweet(tweet_id='1467894750', username='USERID_6', num_liked=1046, length=46),
             Tweet(tweet_id='1467895424', username='USERID_10', num_liked=3423, length=41),
             Tweet(tweet_id='1467895481', username='USERID_5', num_liked=6120, length=49),
             Tweet(tweet_id='1467896211', username='USERID_6', num_liked=3966, length=31),
             Tweet(tweet_id='1467899753', username='USERID_10', num_liked=675, length=32),
             Tweet(tweet_id='1467900033', username='USERID_10', num_liked=9041, length=36),
             Tweet(tweet_id='1467900244', username='USERID_10', num_liked=1618, length=45),
             Tweet(tweet_id='1467900431', username='USERID_9', num_liked=3306, length=34),
             Tweet(tweet_id='1467900545', username='USERID_7', num_liked=148, length=13),
             Tweet(tweet_id='1467901500', username='USERID_7', num_liked=7376, length=13),
             Tweet(tweet_id='1467905125', username='USERID_7', num_liked=1738, length=27),
             Tweet(tweet_id='1467906151', username='USERID_8', num_liked=6711, length=45),
             Tweet(tweet_id='1467906345', username='USERID_3', num_liked=8279, length=46),
             Tweet(tweet_id='1467906723', username='USERID_6', num_liked=7222, length=28),
             Tweet(tweet_id='1467908672', username='USERID_10', num_liked=1692, length=48),
             Tweet(tweet_id='1467909292', username='USERID_10', num_liked=5179, length=45),
             Tweet(tweet_id='1467910531', username='USERID_7', num_liked=6172, length=34),
             Tweet(tweet_id='1467910689', username='USERID_3', num_liked=1529, length=37),
             Tweet(tweet_id='1467912333', username='USERID_7', num_liked=3345, length=49),
             Tweet(tweet_id='1467912842', username='USERID_4', num_liked=496, length=14),
             Tweet(tweet_id='1467914434', username='USERID_1', num_liked=1269, length=49),
             Tweet(tweet_id='1467915140', username='USERID_7', num_liked=1996, length=22),
             Tweet(tweet_id='1467915612', username='USERID_6', num_liked=4014, length=41),
             Tweet(tweet_id='1467862411', username='USERID_10', num_liked=5740, length=34),
             Tweet(tweet_id='1467863072', username='USERID_5', num_liked=2574, length=10),
             Tweet(tweet_id='1467863716', username='USERID_7', num_liked=6088, length=48),
             Tweet(tweet_id='1467871917', username='USERID_9', num_liked=6516, length=48),
             Tweet(tweet_id='1467872175', username='USERID_1', num_liked=1418, length=28),
             Tweet(tweet_id='1467872218', username='USERID_5', num_liked=3366, length=37),
             Tweet(tweet_id='1467872594', username='USERID_6', num_liked=3097, length=37),
             Tweet(tweet_id='1467872759', username='USERID_1', num_liked=6966, length=49),
             Tweet(tweet_id='1467872940', username='USERID_8', num_liked=5494, length=30),
             Tweet(tweet_id='1467873828', username='USERID_6', num_liked=520, length=34),
             Tweet(tweet_id='1467874569', username='USERID_3', num_liked=3439, length=12),
             Tweet(tweet_id='1467874916', username='USERID_2', num_liked=6935, length=23),
             Tweet(tweet_id='1467876133', username='USERID_1', num_liked=2748, length=44),
             Tweet(tweet_id='1467877865', username='USERID_1', num_liked=5899, length=30),
             Tweet(tweet_id='1467878057', username='USERID_6', num_liked=703, length=42),
             Tweet(tweet_id='1467878633', username='USERID_2', num_liked=2351, length=33),
             Tweet(tweet_id='1467878971', username='USERID_2', num_liked=2238, length=27),
             Tweet(tweet_id='1467880463', username='USERID_9', num_liked=1226, length=29),
             Tweet(tweet_id='1467880692', username='USERID_6', num_liked=4989, length=49),
             Tweet(tweet_id='1467881376', username='USERID_4', num_liked=4378, length=49),
             Tweet(tweet_id='1467881457', username='USERID_7', num_liked=119, length=27),
             Tweet(tweet_id='1467881686', username='USERID_5', num_liked=8136, length=46),
             Tweet(tweet_id='1467882902', username='USERID_3', num_liked=4646, length=48),
             Tweet(tweet_id='1467888679', username='USERID_8', num_liked=3089, length=27),
             Tweet(tweet_id='1467888732', username='USERID_7', num_liked=2800, length=48),
             Tweet(tweet_id='1467888953', username='USERID_3', num_liked=3951, length=46),
             Tweet(tweet_id='1467889334', username='USERID_5', num_liked=8495, length=42),
             Tweet(tweet_id='1467890079', username='USERID_8', num_liked=2556, length=38),
             Tweet(tweet_id='1467892515', username='USERID_5', num_liked=917, length=39),
             Tweet(tweet_id='1467892667', username='USERID_2', num_liked=8270, length=20),
             Tweet(tweet_id='1467844540', username='USERID_9', num_liked=6366, length=49),
             Tweet(tweet_id='1467844907', username='USERID_3', num_liked=8770, length=42),
             Tweet(tweet_id='1467845157', username='USERID_8', num_liked=5761, length=17),
             Tweet(tweet_id='1467852067', username='USERID_4', num_liked=9594, length=34),
             Tweet(tweet_id='1467852789', username='USERID_10', num_liked=686, length=44),
             Tweet(tweet_id='1467853431', username='USERID_10', num_liked=9936, length=30),
             Tweet(tweet_id='1467853479', username='USERID_9', num_liked=4939, length=24),
             Tweet(tweet_id='1467854917', username='USERID_2', num_liked=7741, length=30),
             Tweet(tweet_id='1467855812', username='USERID_2', num_liked=4806, length=28),
             Tweet(tweet_id='1467856044', username='USERID_7', num_liked=1442, length=49),
             Tweet(tweet_id='1467856352', username='USERID_3', num_liked=523, length=20),
             Tweet(tweet_id='1467856632', username='USERID_1', num_liked=1724, length=43),
             Tweet(tweet_id='1467857975', username='USERID_9', num_liked=4893, length=21),
             Tweet(tweet_id='1467858869', username='USERID_10', num_liked=1609, length=48),
             Tweet(tweet_id='1467859666', username='USERID_9', num_liked=9158, length=16),
             Tweet(tweet_id='1467859820', username='USERID_10', num_liked=7921, length=27),
             Tweet(tweet_id='1467860895', username='USERID_1', num_liked=2055, length=18),
             Tweet(tweet_id='1467860904', username='USERID_7', num_liked=9851, length=30),
             Tweet(tweet_id='1467861095', username='USERID_10', num_liked=7191, length=38)],
    "15": [Tweet(tweet_id='1467947104', username='USERID_6', num_liked=5847, length=24),
             Tweet(tweet_id='1467949746', username='USERID_8', num_liked=4383, length=8),
             Tweet(tweet_id='1467950027', username='USERID_10', num_liked=8575, length=26),
             Tweet(tweet_id='1467950866', username='USERID_4', num_liked=122, length=27),
             Tweet(tweet_id='1467951850', username='USERID_8', num_liked=1170, length=29),
             Tweet(tweet_id='1467952069', username='USERID_7', num_liked=399, length=24),
             Tweet(tweet_id='1467959908', username='USERID_1', num_liked=2241, length=8),
             Tweet(tweet_id='1467960066', username='USERID_8', num_liked=8350, length=28),
             Tweet(tweet_id='1467961817', username='USERID_4', num_liked=3179, length=27),
             Tweet(tweet_id='1467965949', username='USERID_9', num_liked=8308, length=29),
             Tweet(tweet_id='1467966260', username='USERID_4', num_liked=6040, length=25),
             Tweet(tweet_id='1467967089', username='USERID_6', num_liked=7597, length=19),
             Tweet(tweet_id='1467919452', username='USERID_5', num_liked=2839, length=10),
             Tweet(tweet_id='1467928014', username='USERID_7', num_liked=9830, length=18),
             Tweet(tweet_id='1467929184', username='USERID_4', num_liked=1977, length=21),
             Tweet(tweet_id='1467930017', username='USERID_7', num_liked=2627, length=14),
             Tweet(tweet_id='1467931027', username='USERID_5', num_liked=1699, length=26),
             Tweet(tweet_id='1467933295', username='USERID_1', num_liked=6234, length=14),
             Tweet(tweet_id='1467936498', username='USERID_5', num_liked=313, length=16),
             Tweet(tweet_id='1467936901', username='USERID_5', num_liked=9181, length=24),
             Tweet(tweet_id='1467937038', username='USERID_3', num_liked=5684, length=21),
             Tweet(tweet_id='1467937250', username='USERID_3', num_liked=4415, length=15),
             Tweet(tweet_id='1467893504', username='USERID_9', num_liked=4940, length=25),
             Tweet(tweet_id='1467900545', username='USERID_7', num_liked=148, length=13),
             Tweet(tweet_id='1467901500', username='USERID_7', num_liked=7376, length=13),
             Tweet(tweet_id='1467905125', username='USERID_7', num_liked=1738, length=27),
             Tweet(tweet_id='1467906723', username='USERID_6', num_liked=7222, length=28),
             Tweet(tweet_id='1467912842', username='USERID_4', num_liked=496, length=14),
             Tweet(tweet_id='1467915140', username='USERID_7', num_liked=1996, length=22),
             Tweet(tweet_id='1467863072', username='USERID_5', num_liked=2574, length=10),
             Tweet(tweet_id='1467872175', username='USERID_1', num_liked=1418, length=28),
             Tweet(tweet_id='1467874569', username='USERID_3', num_liked=3439, length=12),
             Tweet(tweet_id='1467874916', username='USERID_2', num_liked=6935, length=23),
             Tweet(tweet_id='1467878971', username='USERID_2', num_liked=2238, length=27),
             Tweet(tweet_id='1467880463', username='USERID_9', num_liked=1226, length=29),
             Tweet(tweet_id='1467881457', username='USERID_7', num_liked=119, length=27),
             Tweet(tweet_id='1467888679', username='USERID_8', num_liked=3089, length=27),
             Tweet(tweet_id='1467892667', username='USERID_2', num_liked=8270, length=20),
             Tweet(tweet_id='1467845157', username='USERID_8', num_liked=5761, length=17),
             Tweet(tweet_id='1467853479', username='USERID_9', num_liked=4939, length=24),
             Tweet(tweet_id='1467855812', username='USERID_2', num_liked=4806, length=28),
             Tweet(tweet_id='1467856352', username='USERID_3', num_liked=523, length=20),
             Tweet(tweet_id='1467857975', username='USERID_9', num_liked=4893, length=21),
             Tweet(tweet_id='1467859666', username='USERID_9', num_liked=9158, length=16),
             Tweet(tweet_id='1467859820', username='USERID_10', num_liked=7921, length=27),
             Tweet(tweet_id='1467860895', username='USERID_1', num_liked=2055, length=18)],
    "16": [Tweet(tweet_id='1467949746', username='USERID_8', num_liked=4383, length=8),
             Tweet(tweet_id='1467959908', username='USERID_1', num_liked=2241, length=8),
             Tweet(tweet_id='1467967089', username='USERID_6', num_liked=7597, length=19),
             Tweet(tweet_id='1467919452', username='USERID_5', num_liked=2839, length=10),
             Tweet(tweet_id='1467928014', username='USERID_7', num_liked=9830, length=18),
             Tweet(tweet_id='1467930017', username='USERID_7', num_liked=2627, length=14),
             Tweet(tweet_id='1467933295', username='USERID_1', num_liked=6234, length=14),
             Tweet(tweet_id='1467936498', username='USERID_5', num_liked=313, length=16),
             Tweet(tweet_id='1467937250', username='USERID_3', num_liked=4415, length=15),
             Tweet(tweet_id='1467900545', username='USERID_7', num_liked=148, length=13),
             Tweet(tweet_id='1467901500', username='USERID_7', num_liked=7376, length=13),
             Tweet(tweet_id='1467912842', username='USERID_4', num_liked=496, length=14),
             Tweet(tweet_id='1467863072', username='USERID_5', num_liked=2574, length=10),
             Tweet(tweet_id='1467874569', username='USERID_3', num_liked=3439, length=12),
             Tweet(tweet_id='1467845157', username='USERID_8', num_liked=5761, length=17),
             Tweet(tweet_id='1467859666', username='USERID_9', num_liked=9158, length=16),
             Tweet(tweet_id='1467860895', username='USERID_1', num_liked=2055, length=18)],
    "17": os.path.join('sample_data', '2.json'),
    "18": os.path.join('full_data', '5.json'),
    "19": [os.path.join('full_data', '5.json'),
             os.path.join('full_data', '5.csv'),
             os.path.join('full_data', '4.json'),
             os.path.join('full_data', '4.csv'),
             os.path.join('full_data', '3.json'),
             os.path.join('full_data', '3.csv'),
             os.path.join('full_data', '2.json'),
             os.path.join('full_data', '2.csv'),
             os.path.join('full_data', '1.csv')],
    "20": [Tweet(tweet_id='1467894593', username='USERID_2', num_liked='869M', length=136),
             Tweet(tweet_id='1467894600', username='USERID_8', num_liked='915k', length=67),
             Tweet(tweet_id='1467853431', username='USERID_10', num_liked=9936, length=30),
             Tweet(tweet_id='1467875163', username='USERID_2', num_liked=9891, length=69),
             Tweet(tweet_id='1467860904', username='USERID_7', num_liked=9851, length=30),
             Tweet(tweet_id='1467928014', username='USERID_7', num_liked=9830, length=18),
             Tweet(tweet_id='1467895048', username='USERID_10', num_liked=9822, length=136),
             Tweet(tweet_id='1467966646', username='USERID_7', num_liked=9821, length=47),
             Tweet(tweet_id='1467855673', username='USERID_9', num_liked=9728, length=72),
             Tweet(tweet_id='1467898078', username='USERID_10', num_liked=9705, length=104),
             Tweet(tweet_id='1467928300', username='USERID_9', num_liked=9681, length=79),
             Tweet(tweet_id='1467917177', username='USERID_3', num_liked=9678, length=105),
             Tweet(tweet_id='1467923235', username='USERID_9', num_liked=9662, length=134),
             Tweet(tweet_id='1467964211', username='USERID_4', num_liked=9618, length=79),
             Tweet(tweet_id='1467873980', username='USERID_5', num_liked=9608, length=88),
             Tweet(tweet_id='1467852067', username='USERID_4', num_liked=9594, length=34),
             Tweet(tweet_id='1467863633', username='USERID_9', num_liked=9549, length=95),
             Tweet(tweet_id='1467953733', username='USERID_4', num_liked=9526, length=67),
             Tweet(tweet_id='1467862806', username='USERID_2', num_liked=9465, length=68),
             Tweet(tweet_id='1467954070', username='USERID_8', num_liked=9462, length=64)]
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
    new_notebook = 'cs-220-test.ipynb'

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
    jbn = [7,8,9,10,11,12,13,14,15,16,20]
    if qnum in jbn:
        actual = (eval(compile(ast.parse(actual, mode='eval'), '', 'eval')))
    else:
        try:
            actual = ast.literal_eval(actual)
        except Exception as e:
            print("COULD NOT PARSE THIS CELL:")
            print(actual)
            raise e
    expected = expected_json[str(qnum)]

    expected_mismatch = False

    if type(expected) != type(actual):
        return "expected an answer of type %s but found one of type %s" % (type(expected), type(actual))
    elif type(expected) == float:
        if not math.isclose(actual, expected, rel_tol=1e-06, abs_tol=1e-06):
            expected_mismatch = True
    elif type(expected) == list:
        try:
            extra = set(actual) - set(expected)
            missing = set(expected) - set(actual)
            if missing:
                return "missing %d entries list, such as: %s" % (len(missing), repr(list(missing)[0]))
            elif extra:
                return "found %d unexpected entries, such as: %s" % (len(extra), repr(list(extra)[0]))
            elif len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
            else:
                for i,(a,e) in enumerate(zip(actual, expected)):
                    if a != e:
                        return "found %s at position %d but expected %s" % (str(a), i, str(e))
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


def main():
    # rerun everything
    orig_notebook = 'main.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py main.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]

    # make sure directories are properly setup
    assert(os.path.exists("sample_data"))
    assert(os.path.exists("full_data"))

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

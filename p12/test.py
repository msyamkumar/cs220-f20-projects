#!/usr/bin/python

import json
import os
import sys
import re, ast, math
from collections import namedtuple, OrderedDict, defaultdict
from bs4 import BeautifulSoup
from datetime import datetime
import nbconvert
import nbformat

# Avoid NotImplementError in Windows System
if (sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith("win")):
    import asyncio
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

try:
    from lint import lint
except ImportError:
    err_msg = """Please download lint.py and place it in this directory for
    the tests to run correctly. If you haven't yet looked at the linting module,
    it is designed to help you improve your code so take a look at:
    https://github.com/msyamkumar/cs220-projects/tree/master/linter"""
    raise FileNotFoundError(err_msg)

ALLOWED_LINT_ERRS = {
  "W0703": "broad-except",
  "R1716": "chained-comparison",
  "E0601": "used-before-assignment",
  "W0105": "pointless-string-statement",
  "E1135": "unsupported-membership-test",
  "R1711": "useless-return",
  "W0143": "comparison-with-callable",
  "E1102": "not-callable",
  "W0107": "unnecessary-pass",
  "W0301": "unnecessary-semicolon",
  "W0404": "reimported",
  "W0101": "unreachable",
  "R1714": "consider-using-in",
  "W0311": "bad-indentation",
  "E0102": "function-redefined",
  "E0602": "undefined-variable",
  "W0104": "pointless-statement",
  "W0622": "redefined-builtin",
  "W0702": "bare-except",
  "R1703": "simplifiable-if-statement",
  "W0631": "undefined-loop-variable",
}

PASS = 'PASS'
FAIL_STDERR = 'Program produced an error - please scroll up for more details.'
FAIL_JSON = 'Expected program to print in json format. Make sure the only print statement is a print(json.dumps...)!'
EPSILON = 0.0001


TEXT_FORMAT = "text"
PNG_FORMAT = "png"
HTML_FORMAT = "html"
Question = namedtuple("Question", ["number", "weight", "format"])

questions = [
    # stage 1
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
    Question(number=13, weight=1, format=HTML_FORMAT),
    Question(number=14, weight=1, format=HTML_FORMAT),
    Question(number=15, weight=1, format=TEXT_FORMAT),
    Question(number=16, weight=1, format=TEXT_FORMAT),
    Question(number=17, weight=1, format=HTML_FORMAT),
    Question(number=18, weight=1, format=HTML_FORMAT),
    Question(number=19, weight=1, format=HTML_FORMAT),
    Question(number=20, weight=1, format=TEXT_FORMAT)
]
question_nums = set([q.number for q in questions])

expected_json = {
    "1": 174,
    "2": 6261901793,
    "3": ['Abu Dhabi',
         'Abuja',
         'Accra',
         'Addis Ababa',
         'Algiers',
         'Amman',
         'Amsterdam',
         'Ankara',
         'Antananarivo',
         'Apia',
         'Ashgabat',
         'Asmara',
         'Astana',
         'Asuncion',
         'Athens',
         'Baghdad',
         'Baku',
         'Bamako',
         'Bangkok',
         'Beijing',
         'Beirut',
         'Belmopan',
         'Berlin',
         'Bern',
         'Bishkek',
         'Bissau',
         'Bogota',
         'Brasilia',
         'Bridgetown',
         'Brussels',
         'Bucharest',
         'Budapest',
         'Buenos Aires',
         'Bujumbura',
         'Cairo',
         'Canberra',
         'Caracas',
         'Castries',
         'Chisinau',
         'Colombo',
         'Conakry',
         'Copenhagen',
         'Dakar',
         'Damascus',
         'Dar es Salaam',
         'Dhaka',
         'Djibouti',
         'Doha',
         'Dublin',
         'Dushanbe',
         'Freetown',
         'Gaborone',
         'George Town',
         'Georgetown',
         'Guatemala City',
         'Hagatna',
         'Hamilton',
         'Hanoi',
         'Harare',
         'Havana',
         'Helsinki',
         'Islamabad',
         'Jakarta',
         'Jamestown',
         'Jerusalem',
         'Kabul',
         'Kampala',
         'Kathmandu',
         'Khartoum',
         'Kigali',
         'Kingston',
         'Kingstown',
         'Kuala Lumpur',
         'Kuwait City',
         'Kyiv',
         'La Paz',
         'Libreville',
         'Lilongwe',
         'Lima',
         'Lisbon',
         'Ljubljana',
         'Lome',
         'London',
         'Lusaka',
         'Luxembourg',
         'Madrid',
         'Majuro',
         'Malabo',
         'Male',
         'Managua',
         'Manama',
         'Manila',
         'Maputo',
         'Maseru',
         'Mbabane',
         'Melekeok',
         'Mexico City',
         'Minsk',
         'Mogadishu',
         'Monaco',
         'Monrovia',
         'Montevideo',
         'Moroni',
         'Moscow',
         'Muscat',
         'Nairobi',
         'New Delhi',
         'Niamey',
         'Nouakchott',
         'Noumea',
         'Nuku’alofa',
         'N’Djamena',
         'Oranjestad',
         'Oslo',
         'Ottawa',
         'Ouagadougou',
         'Panama City',
         'Papeete',
         'Paramaribo',
         'Paris',
         'Phnom Penh',
         'Port Louis',
         'Port Moresby',
         'Port-Vila',
         'Port-au-Prince',
         'Porto-Novo',
         'Prague',
         'Praia',
         'Pretoria',
         'Quito',
         'Rabat',
         'Reykjavik',
         'Riga',
         'Riyadh',
         'Rome',
         'Roseau',
         'Saint George’s',
         'San Jose',
         'San Juan',
         'San Marino',
         'San Salvador',
         'Sanaa',
         'Santiago',
         'Santo Domingo',
         'Singapore',
         'Sofia',
         'Stockholm',
         'Suva',
         'Taipei',
         'Tallinn',
         'Tashkent',
         'Tbilisi',
         'Tegucigalpa',
         'Tehran',
         'The Valley',
         'Thimphu',
         'Tirana',
         'Tokyo',
         'Tripoli',
         'Tunis',
         'Ulaanbaatar',
         'Vaduz',
         'Valletta',
         'Victoria',
         'Vienna',
         'Vientiane',
         'Vilnius',
         'Warsaw',
         'Washington, D.C.',
         'Wellington',
         'Windhoek',
         'Yaounde',
         'Yerevan',
         'Zagreb'],
    "4": "Rome",
    "5": 'Belgium',
    "6": ['New Zealand',
         'Australia',
         'Uruguay',
         'Argentina',
         'Chile',
         'Lesotho',
         'Swaziland'],
    "7": ['Iceland',
         'Finland',
         'Norway',
         'Estonia',
         'Sweden',
         'Latvia',
         'Russia',
         'Denmark',
         'Lithuania',
         'Belarus'],
    "8": 'Bhutan',
    "9": 'China',
    "10": 'Suriname',
    "11": 1.433899492072933,
    "12": 520.8581822565817,
    "15": 'Jamaica',
    "16": 'Canada',
    "20": ('[{"country": "Afghanistan", "capital": "Kabul", "latitude": 34.51666667, "longitude": 69.183333}, {"country": "Albania", "capital": "Tirana", "latitude": 41.31666667, "longitude": 19.816667}, {"country": "Algeria", "capital": "Algiers", "latitude": 36.75, "longitude": 3.05}, {"country": "Anguilla", "capital": "The Valley", "latitude": 18.21666667, "longitude": -63.05}, {"country": "Argentina", "capital": "Buenos Aires", "latitude": -34.58333333, "longitude": -58.666667}, {"country": "Armenia", "capital": "Yerevan", "latitude": 40.16666667, "longitude": 44.5}, {"country": "Aruba", "capital": "Oranjestad", "latitude": 12.51666667, "longitude": -70.033333}, {"country": "Australia", "capital": "Canberra", "latitude": -35.26666667, "longitude": 149.133333}, {"country": "Austria", "capital": "Vienna", "latitude": 48.2, "longitude": 16.366667}, {"country": "Azerbaijan", "capital": "Baku", "latitude": 40.38333333, "longitude": 49.866667}, {"country": "Bahrain", "capital": "Manama", "latitude": 26.23333333, "longitude": 50.566667}, {"country": "Bangladesh", "capital": "Dhaka", "latitude": 23.71666667, "longitude": 90.4}, {"country": "Barbados", "capital": "Bridgetown", "latitude": 13.1, "longitude": -59.616667}, {"country": "Belarus", "capital": "Minsk", "latitude": 53.9, "longitude": 27.566667}, {"country": "Belgium", "capital": "Brussels", "latitude": 50.83333333, "longitude": 4.333333}, {"country": "Belize", "capital": "Belmopan", "latitude": 17.25, "longitude": -88.766667}, {"country": "Benin", "capital": "Porto-Novo", "latitude": 6.483333333, "longitude": 2.616667}, {"country": "Bermuda", "capital": "Hamilton", "latitude": 32.28333333, "longitude": -64.783333}, {"country": "Bhutan", "capital": "Thimphu", "latitude": 27.46666667, "longitude": 89.633333}, {"country": "Bolivia", "capital": "La Paz", "latitude": -16.5, "longitude": -68.15}, {"country": "Botswana", "capital": "Gaborone", "latitude": -24.63333333, "longitude": 25.9}, {"country": "Brazil", "capital": "Brasilia", "latitude": -15.78333333, "longitude": -47.916667}, {"country": "Bulgaria", "capital": "Sofia", "latitude": 42.68333333, "longitude": 23.316667}, {"country": "Burkina Faso", "capital": "Ouagadougou", "latitude": 12.36666667, "longitude": -1.516667}, {"country": "Burundi", "capital": "Bujumbura", "latitude": -3.366666667, "longitude": 29.35}, {"country": "Cambodia", "capital": "Phnom Penh", "latitude": 11.55, "longitude": 104.916667}, '
    '{"country": "Cameroon", "capital": "Yaounde", "latitude": 3.866666667, "longitude": 11.516667}, {"country": "Canada", "capital": "Ottawa", "latitude": 45.41666667, "longitude": -75.7}, {"country": "Cape Verde", "capital": "Praia", "latitude": 14.91666667, "longitude": -23.516667}, {"country": "Cayman Islands", "capital": "George Town", "latitude": 19.3, "longitude": -81.383333}, {"country": "Chad", "capital": "N\\u2019Djamena", "latitude": 12.1, "longitude": 15.033333}, {"country": "Chile", "capital": "Santiago", "latitude": -33.45, "longitude": -70.666667}, {"country": "China", "capital": "Beijing", "latitude": 39.91666667, "longitude": 116.383333}, {"country": "Colombia", "capital": "Bogota", "latitude": 4.6, "longitude": -74.083333}, {"country": "Comoros", "capital": "Moroni", "latitude": -11.7, "longitude": 43.233333}, {"country": "Costa Rica", "capital": "San Jose", "latitude": 9.933333333, "longitude": -84.083333}, {"country": "Croatia", "capital": "Zagreb", "latitude": 45.8, "longitude": 16.0}, {"country": "Cuba", "capital": "Havana", "latitude": 23.11666667, "longitude": -82.35}, {"country": "Czech Republic", "capital": "Prague", "latitude": 50.08333333, "longitude": 14.466667}, {"country": "Denmark", "capital": "Copenhagen", "latitude": 55.66666667, "longitude": 12.583333}, {"country": "Djibouti", "capital": "Djibouti", "latitude": 11.58333333, "longitude": 43.15}, {"country": "Dominica", "capital": "Roseau", "latitude": 15.3, "longitude": -61.4}, {"country": "Dominican Republic", "capital": "Santo Domingo", "latitude": 18.46666667, "longitude": -69.9}, {"country": "Ecuador", "capital": "Quito", "latitude": -0.216666667, "longitude": -78.5}, {"country": "Egypt", "capital": "Cairo", "latitude": 30.05, "longitude": 31.25}, {"country": "El Salvador", "capital": "San Salvador", "latitude": 13.7, "longitude": -89.2}, {"country": "Equatorial Guinea", "capital": "Malabo", "latitude": 3.75, "longitude": 8.783333}, {"country": "Eritrea", "capital": "Asmara", "latitude": 15.33333333, "longitude": 38.933333}, {"country": "Estonia", "capital": "Tallinn", "latitude": 59.43333333, "longitude": 24.716667}, {"country": "Ethiopia", "capital": "Addis Ababa", "latitude": 9.033333333, "longitude": 38.7}, {"country": "Fiji", "capital": "Suva", "latitude": -18.13333333, "longitude": 178.416667}, {"country": "Finland", "capital": "Helsinki", "latitude": 60.16666667, "longitude": 24.933333}, '
    '{"country": "France", "capital": "Paris", "latitude": 48.86666667, "longitude": 2.333333}, {"country": "French Polynesia", "capital": "Papeete", "latitude": -17.53333333, "longitude": -149.566667}, {"country": "Gabon", "capital": "Libreville", "latitude": 0.383333333, "longitude": 9.45}, {"country": "Georgia", "capital": "Tbilisi", "latitude": 41.68333333, "longitude": 44.833333}, {"country": "Germany", "capital": "Berlin", "latitude": 52.51666667, "longitude": 13.4}, {"country": "Ghana", "capital": "Accra", "latitude": 5.55, "longitude": -0.216667}, {"country": "Greece", "capital": "Athens", "latitude": 37.98333333, "longitude": 23.733333}, {"country": "Grenada", "capital": "Saint George\\u2019s", "latitude": 12.05, "longitude": -61.75}, {"country": "Guam", "capital": "Hagatna", "latitude": 13.46666667, "longitude": 144.733333}, {"country": "Guatemala", "capital": "Guatemala City", "latitude": 14.61666667, "longitude": -90.516667}, {"country": "Guinea", "capital": "Conakry", "latitude": 9.5, "longitude": -13.7}, {"country": "Guinea-Bissau", "capital": "Bissau", "latitude": 11.85, "longitude": -15.583333}, {"country": "Guyana", "capital": "Georgetown", "latitude": 6.8, "longitude": -58.15}, {"country": "Haiti", "capital": "Port-au-Prince", "latitude": 18.53333333, "longitude": -72.333333}, {"country": "Honduras", "capital": "Tegucigalpa", "latitude": 14.1, "longitude": -87.216667}, {"country": "Hungary", "capital": "Budapest", "latitude": 47.5, "longitude": 19.083333}, {"country": "Iceland", "capital": "Reykjavik", "latitude": 64.15, "longitude": -21.95}, {"country": "India", "capital": "New Delhi", "latitude": 28.6, "longitude": 77.2}, {"country": "Indonesia", "capital": "Jakarta", "latitude": -6.166666667, "longitude": 106.816667}, {"country": "Iran", "capital": "Tehran", "latitude": 35.7, "longitude": 51.416667}, {"country": "Iraq", "capital": "Baghdad", "latitude": 33.33333333, "longitude": 44.4}, {"country": "Ireland", "capital": "Dublin", "latitude": 53.31666667, "longitude": -6.233333}, {"country": "Israel", "capital": "Jerusalem", "latitude": 31.76666667, "longitude": 35.233333}, {"country": "Italy", "capital": "Rome", "latitude": 41.9, "longitude": 12.483333}, {"country": "Jamaica", "capital": "Kingston", "latitude": 18.0, "longitude": -76.8}, {"country": "Japan", "capital": "Tokyo", "latitude": 35.68333333, "longitude": 139.75}, {"country": "Jordan", "capital": "Amman", "latitude": 31.95, "longitude": 35.933333}, '
    '{"country": "Kazakhstan", "capital": "Astana", "latitude": 51.16666667, "longitude": 71.416667}, {"country": "Kenya", "capital": "Nairobi", "latitude": -1.283333333, "longitude": 36.816667}, {"country": "Kuwait", "capital": "Kuwait City", "latitude": 29.36666667, "longitude": 47.966667}, {"country": "Kyrgyzstan", "capital": "Bishkek", "latitude": 42.86666667, "longitude": 74.6}, {"country": "Laos", "capital": "Vientiane", "latitude": 17.96666667, "longitude": 102.6}, {"country": "Latvia", "capital": "Riga", "latitude": 56.95, "longitude": 24.1}, {"country": "Lebanon", "capital": "Beirut", "latitude": 33.86666667, "longitude": 35.5}, {"country": "Lesotho", "capital": "Maseru", "latitude": -29.31666667, "longitude": 27.483333}, {"country": "Liberia", "capital": "Monrovia", "latitude": 6.3, "longitude": -10.8}, {"country": "Libya", "capital": "Tripoli", "latitude": 32.88333333, "longitude": 13.166667}, {"country": "Liechtenstein", "capital": "Vaduz", "latitude": 47.13333333, "longitude": 9.516667}, {"country": "Lithuania", "capital": "Vilnius", "latitude": 54.68333333, "longitude": 25.316667}, {"country": "Luxembourg", "capital": "Luxembourg", "latitude": 49.6, "longitude": 6.116667}, {"country": "Madagascar", "capital": "Antananarivo", "latitude": -18.91666667, "longitude": 47.516667}, {"country": "Malawi", "capital": "Lilongwe", "latitude": -13.96666667, "longitude": 33.783333}, {"country": "Malaysia", "capital": "Kuala Lumpur", "latitude": 3.166666667, "longitude": 101.7}, {"country": "Maldives", "capital": "Male", "latitude": 4.166666667, "longitude": 73.5}, {"country": "Mali", "capital": "Bamako", "latitude": 12.65, "longitude": -8.0}, {"country": "Malta", "capital": "Valletta", "latitude": 35.88333333, "longitude": 14.5}, {"country": "Marshall Islands", "capital": "Majuro", "latitude": 7.1, "longitude": 171.383333}, {"country": "Mauritania", "capital": "Nouakchott", "latitude": 18.06666667, "longitude": -15.966667}, {"country": "Mauritius", "capital": "Port Louis", "latitude": -20.15, "longitude": 57.483333}, {"country": "Mexico", "capital": "Mexico City", "latitude": 19.43333333, "longitude": -99.133333}, {"country": "Moldova", "capital": "Chisinau", "latitude": 47.0, "longitude": 28.85}, {"country": "Monaco", "capital": "Monaco", "latitude": 43.73333333, "longitude": 7.416667}, {"country": "Mongolia", "capital": "Ulaanbaatar", "latitude": 47.91666667, "longitude": 106.916667}, '
    '{"country": "Morocco", "capital": "Rabat", "latitude": 34.01666667, "longitude": -6.816667}, {"country": "Mozambique", "capital": "Maputo", "latitude": -25.95, "longitude": 32.583333}, {"country": "Namibia", "capital": "Windhoek", "latitude": -22.56666667, "longitude": 17.083333}, {"country": "Nepal", "capital": "Kathmandu", "latitude": 27.71666667, "longitude": 85.316667}, {"country": "Netherlands", "capital": "Amsterdam", "latitude": 52.35, "longitude": 4.916667}, {"country": "New Caledonia", "capital": "Noumea", "latitude": -22.26666667, "longitude": 166.45}, {"country": "New Zealand", "capital": "Wellington", "latitude": -41.3, "longitude": 174.783333}, {"country": "Nicaragua", "capital": "Managua", "latitude": 12.13333333, "longitude": -86.25}, {"country": "Niger", "capital": "Niamey", "latitude": 13.51666667, "longitude": 2.116667}, {"country": "Nigeria", "capital": "Abuja", "latitude": 9.083333333, "longitude": 7.533333}, {"country": "Norway", "capital": "Oslo", "latitude": 59.91666667, "longitude": 10.75}, {"country": "Oman", "capital": "Muscat", "latitude": 23.61666667, "longitude": 58.583333}, {"country": "Pakistan", "capital": "Islamabad", "latitude": 33.68333333, "longitude": 73.05}, {"country": "Palau", "capital": "Melekeok", "latitude": 7.483333333, "longitude": 134.633333}, {"country": "Panama", "capital": "Panama City", "latitude": 8.966666667, "longitude": -79.533333}, {"country": "Papua New Guinea", "capital": "Port Moresby", "latitude": -9.45, "longitude": 147.183333}, {"country": "Paraguay", "capital": "Asuncion", "latitude": -25.26666667, "longitude": -57.666667}, {"country": "Peru", "capital": "Lima", "latitude": -12.05, "longitude": -77.05}, {"country": "Philippines", "capital": "Manila", "latitude": 14.6, "longitude": 120.966667}, {"country": "Poland", "capital": "Warsaw", "latitude": 52.25, "longitude": 21.0}, {"country": "Portugal", "capital": "Lisbon", "latitude": 38.71666667, "longitude": -9.133333}, {"country": "Puerto Rico", "capital": "San Juan", "latitude": 18.46666667, "longitude": -66.116667}, {"country": "Qatar", "capital": "Doha", "latitude": 25.28333333, "longitude": 51.533333}, {"country": "Romania", "capital": "Bucharest", "latitude": 44.43333333, "longitude": 26.1}, {"country": "Russia", "capital": "Moscow", "latitude": 55.75, "longitude": 37.6}, {"country": "Rwanda", "capital": "Kigali", "latitude": -1.95, "longitude": 30.05}, '
    '{"country": "Saint Helena", "capital": "Jamestown", "latitude": -15.93333333, "longitude": -5.716667}, {"country": "Saint Lucia", "capital": "Castries", "latitude": 14.0, "longitude": -61.0}, {"country": "Saint Vincent and the Grenadines", "capital": "Kingstown", "latitude": 13.13333333, "longitude": -61.216667}, {"country": "Samoa", "capital": "Apia", "latitude": -13.81666667, "longitude": -171.766667}, {"country": "San Marino", "capital": "San Marino", "latitude": 43.93333333, "longitude": 12.416667}, {"country": "Saudi Arabia", "capital": "Riyadh", "latitude": 24.65, "longitude": 46.7}, {"country": "Senegal", "capital": "Dakar", "latitude": 14.73333333, "longitude": -17.633333}, {"country": "Seychelles", "capital": "Victoria", "latitude": -4.616666667, "longitude": 55.45}, {"country": "Sierra Leone", "capital": "Freetown", "latitude": 8.483333333, "longitude": -13.233333}, {"country": "Singapore", "capital": "Singapore", "latitude": 1.283333333, "longitude": 103.85}, {"country": "Slovenia", "capital": "Ljubljana", "latitude": 46.05, "longitude": 14.516667}, {"country": "Somalia", "capital": "Mogadishu", "latitude": 2.066666667, "longitude": 45.333333}, {"country": "South Africa", "capital": "Pretoria", "latitude": -25.7, "longitude": 28.216667}, {"country": "Spain", "capital": "Madrid", "latitude": 40.4, "longitude": -3.683333}, {"country": "Sri Lanka", "capital": "Colombo", "latitude": 6.916666667, "longitude": 79.833333}, {"country": "Sudan", "capital": "Khartoum", "latitude": 15.6, "longitude": 32.533333}, {"country": "Suriname", "capital": "Paramaribo", "latitude": 5.833333333, "longitude": -55.166667}, {"country": "Swaziland", "capital": "Mbabane", "latitude": -26.31666667, "longitude": 31.133333}, {"country": "Sweden", "capital": "Stockholm", "latitude": 59.33333333, "longitude": 18.05}, {"country": "Switzerland", "capital": "Bern", "latitude": 46.91666667, "longitude": 7.466667}, {"country": "Syria", "capital": "Damascus", "latitude": 33.5, "longitude": 36.3}, {"country": "Taiwan", "capital": "Taipei", "latitude": 25.03333333, "longitude": 121.516667}, {"country": "Tajikistan", "capital": "Dushanbe", "latitude": 38.55, "longitude": 68.766667}, {"country": "Tanzania", "capital": "Dar es Salaam", "latitude": -6.8, "longitude": 39.283333}, {"country": "Thailand", "capital": "Bangkok", "latitude": 13.75, "longitude": 100.516667}, '
    '{"country": "Togo", "capital": "Lome", "latitude": 6.116666667, "longitude": 1.216667}, {"country": "Tonga", "capital": "Nuku\\u2019alofa", "latitude": -21.13333333, "longitude": -175.2}, {"country": "Tunisia", "capital": "Tunis", "latitude": 36.8, "longitude": 10.183333}, {"country": "Turkey", "capital": "Ankara", "latitude": 39.93333333, "longitude": 32.866667}, {"country": "Turkmenistan", "capital": "Ashgabat", "latitude": 37.95, "longitude": 58.383333}, {"country": "Uganda", "capital": "Kampala", "latitude": 0.316666667, "longitude": 32.55}, {"country": "Ukraine", "capital": "Kyiv", "latitude": 50.43333333, "longitude": 30.516667}, {"country": "United Arab Emirates", "capital": "Abu Dhabi", "latitude": 24.46666667, "longitude": 54.366667}, {"country": "United Kingdom", "capital": "London", "latitude": 51.5, "longitude": -0.083333}, {"country": "United States", "capital": "Washington, D.C.", "latitude": 38.883333, "longitude": -77.0}, {"country": "Uruguay", "capital": "Montevideo", "latitude": -34.85, "longitude": -56.166667}, {"country": "Uzbekistan", "capital": "Tashkent", "latitude": 41.31666667, "longitude": 69.25}, {"country": "Vanuatu", "capital": "Port-Vila", "latitude": -17.73333333, "longitude": 168.316667}, {"country": "Venezuela", "capital": "Caracas", "latitude": 10.48333333, "longitude": -66.866667}, {"country": "Vietnam", "capital": "Hanoi", "latitude": 21.03333333, "longitude": 105.85}, {"country": "Yemen", "capital": "Sanaa", "latitude": 15.35, "longitude": 44.2}, {"country": "Zambia", "capital": "Lusaka", "latitude": -15.41666667, "longitude": 28.283333}, {"country": "Zimbabwe", "capital": "Harare", "latitude": -17.81666667, "longitude": 31.033333}]')

}

def parse_df_html_table(html, question=None):
    soup = BeautifulSoup(html, 'html.parser')

    if question == None:
        tables = soup.find_all('table')
        assert(len(tables) == 1)
        table = tables[0]
    else:
        # find a table that looks like this:
        # <table data-question="6"> ...
        table = soup.find('table', {"data-question": str(question)})

    rows = []
    for tr in table.find_all('tr'):
        rows.append([])
        for cell in tr.find_all(['td', 'th']):
            rows[-1].append(cell.get_text())

    cells = {}
    for r in range(1, len(rows)):
        for c in range(1, len(rows[0])):
            rname = rows[r][0]
            cname = rows[0][c]
            cells[(rname,cname)] = rows[r][c]
    return cells

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
    with open(orig_notebook, encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=nbformat.NO_CONVERT)
    ep = nbconvert.preprocessors.ExecutePreprocessor(timeout=120, kernel_name='python3')
    try:
        out = ep.preprocess(nb, {'metadata': {'path': os.getcwd()}})
    except nbconvert.preprocessors.CellExecutionError:
        out = None
        msg = 'Error executing the notebook "%s".\n\n' % orig_notebook
        msg += 'See notebook "%s" for the traceback.' % new_notebook
        print(msg)
        raise
    finally:
        with open(new_notebook, mode='w', encoding='utf-8') as f:
            nbformat.write(nb, f)

    # Note: Here we are saving and reloading, this isn't needed but can help student's debug

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
    jbn = [6,7,8,9,10,11,12,18,19,20,30]
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
        if not math.isclose(actual, expected, rel_tol=1e-02, abs_tol=1e-02):
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
            if len(actual) != len(expected):
                return "expected %d entries in the list but found %d" % (len(expected), len(actual))
            for i,(a,e) in enumerate(zip(actual, expected)):
                if a != e:
                    return "found %s at position %d but expected %s" % (str(a), i, str(e))            # this happens when the list contains dicts.  Just do a simple comparison
    elif type(expected) == tuple:
        if len(expected) != len(actual):
            expected_mismatch = True
        try:
            for idx in range(len(expected)):
                if not math.isclose(actual[idx], expected[idx], rel_tol=1e-02, abs_tol=1e-02):
                    expected_mismatch = True
        except:
            expected_mismatch = True

    else:
        if expected != actual:
            expected_mismatch = True

    if expected_mismatch:
        return "found {} in cell {} but expected {}".format(actual, qnum, expected)

    return PASS

def diff_df_cells(actual_cells, expected_cells):
    for location, expected in expected_cells.items():
        location_name = "column {} at index {}".format(location[1], location[0])
        actual = actual_cells.get(location, None)
        if actual == None:
            return 'value missing for ' + location_name
        try:
            actual_float = float(actual)
            expected_float = float(expected)
            if math.isnan(actual_float) and math.isnan(expected_float):
                return PASS
            if not math.isclose(actual_float, expected_float, rel_tol=1e-02, abs_tol=1e-02):
                print(type(actual_float), actual_float)
                return "found {} in {} but it was not close to expected {}".format(actual, location_name, expected)
        except Exception as e:
            if actual != expected:
                return "found '{}' in {} but expected '{}'".format(actual, location_name, expected)
    return PASS

def check_cell_html(qnum, cell):
    outputs = cell.get('outputs', [])
    if len(outputs) == 0:
        return 'no outputs in an Out[N] cell'
    actual_lines = outputs[0].get('data', {}).get('text/html', [])
    try:
        actual_cells = parse_df_html_table(''.join(actual_lines))
    except Exception as e:
        print("ERROR!  Could not find table in notebook")
        raise e

    try:
        with open('expected.html') as f:
            expected_cells = parse_df_html_table(f.read(), qnum)
    except Exception as e:
        print("ERROR!  Could not find table in expected.html")
        raise e

    return diff_df_cells(actual_cells, expected_cells)

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


def check_cell(question, cell):
    print('Checking question %d' % question.number)
    if question.format == TEXT_FORMAT:
        return check_cell_text(question.number, cell)
    elif question.format == PNG_FORMAT:
        return check_cell_png(question.number, cell)
    elif question.format == HTML_FORMAT:
        return check_cell_html(question.number,cell)
    raise Exception("invalid question type")


def grade_answers(cells):
    results = {'score':0, 'tests': [], 'lint': [], "date":datetime.now().strftime("%m/%d/%Y")}

    for question in questions:
        cell = cells.get(question.number, None)
        status = "not found"

        if question.number in cells:
            # does it match the expected output?
            status = check_cell(question, cells[question.number])

        row = {"test": question.number, "result": status, "weight": question.weight}
        results['tests'].append(row)

    return results

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


def main():
    # rerun everything
    orig_notebook = 'main.ipynb'
    if len(sys.argv) > 2:
        print("Usage: test.py main.ipynb")
        return
    elif len(sys.argv) == 2:
        orig_notebook = sys.argv[1]

    # make sure directories are properly setup
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

    lint_msgs = lint(orig_notebook, verbose=1, show=False)
    lint_msgs = filter(lambda msg: msg.msg_id in ALLOWED_LINT_ERRS, lint_msgs)
    lint_msgs = list(lint_msgs)
    results["lint"] = [str(l) for l in lint_msgs]

    functionality_score = 100.0 * passing / total
    linting_score = min(10.0, len(lint_msgs))
    results['score'] = max(functionality_score - linting_score, 0.0)

    print("\nSummary:")
    for test in results["tests"]:
        print("  Question %d: %s" % (test["test"], test["result"]))

    if len(lint_msgs) > 0:
        msg_types = defaultdict(list)
        for msg in lint_msgs:
            msg_types[msg.category].append(msg)
        print("\nLinting Summary:")
        for msg_type, msgs in msg_types.items():
            print('  ' + msg_type.title() + ' Messages:')
            for msg in msgs:
                print('    ' + str(msg))

    print('\nTOTAL SCORE: %.1f/100.0' % results['score'])
    with open('result.json', 'w') as f:
        f.write(json.dumps(results, indent=2))


if __name__ == '__main__':
    main()

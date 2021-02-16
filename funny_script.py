import os
import json

import mariadb
import sys

# Connect to MariaDB Platform
try:
    conn = mariadb.connect(
        user="root",
        password="",
        host="localhost",
        port=3306,
        database="semrep"

    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)


# Get Cursor
cur = conn.cursor()

l1_words = ["say","know","think","want","don't want","feel","see","hear","do","happen","move","be","is","live","die","touch","can"]

#cur.execute("DROP TABLE Primes_EN")

cur.execute("CREATE TABLE Primes_EN (PrimeIndex int PRIMARY KEY, Prime_EN NVARCHAR(100) NOT NULL)")

for l1_word in l1_words:
    cur.execute("INSERT INTO Primes_EN (PrimeIndex, Prime_EN) VALUES (?,?)", (l1_words.index(l1_word), l1_word))
    print("Added " + l1_word + " to Primes_EN")
    conn.commit()

conn.commit()

def import_into_db(filename, l1, l2):

    #cur.execute("DROP TABLE Europarl_" + l1.upper() + "_" + l2.upper())
    cur.execute("CREATE TABLE Europarl_" + l1.upper() + "_" + l2.upper() + "(LineIndex int, Line_" + l1.upper() + " nvarchar(5000), Prime_" + l1.upper() +" int, Line_" + l2.upper() + " nvarchar(5000))")
    conn.commit()

    with open(filename + "." + l1) as input_l1:
        with open(filename + "." + l2) as input_l2:

            l2_lines = input_l2.readlines()
            
            l1_words_dict = {}

            for l1_word in l1_words:
                l1_words_dict[l1_word] = []

            for line_index, l1_line in enumerate(input_l1):
                for l1_word in l1_words_dict.keys():
                    if l1_word in l1_line.lower():
                        l2_line = l2_lines[line_index]
                        l1_word_index = l1_words.index(l1_word)
                        l1_words_dict[l1_word].append((line_index, l1_line, l1_word_index ,l2_line))
                if line_index % 10000 == 0: 
                    print("Looking up all mentions of primes. " + str(line_index) + " done.") # str(len(input_l1))

            print("Looking up all mentions of primes. Done.")

            for l1_word in l1_words_dict.keys():
                print(str(len(l1_words_dict[l1_word])) + " sentences containing " + l1_word + " were found.")

            insert_string = "INSERT INTO Europarl_" + l1.upper() + "_" + l2.upper() + "(LineIndex, Line_" + l1.upper() + ", Prime_" + l1.upper() +", Line_" + l2.upper() + ") VALUES (?,?,?,?)"
            print(insert_string)


            for l1_word in l1_words_dict:
                cur.executemany(insert_string, l1_words_dict[l1_word])
                print("Added all sentences containing " + l1_word + ". (prime index =" + str(l1_words.index(l1_word)) + ", len = " + str(len(l1_words_dict[l1_word])))
                conn.commit()

import_into_db("europarl-v7.es-en", "en", "es")
import_into_db("europarl-v7.de-en", "en", "de")
conn.close()
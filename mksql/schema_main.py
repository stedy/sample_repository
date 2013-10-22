import csv
import sqlite3

connection = sqlite3.connect('../tsadb.db')
connection.text_factory = str
cursor = connection.cursor()

cursor.execute('DROP table IF EXISTS main')
cursor.execute("""CREATE table main (urid text, ptdon text, resclin text,
	                sample_type text, sourcecoll text, accession_number text, 
                    coll_date date) """)

connection.commit()

csvre = csv.reader(open("../original/repo_main.csv", 'rb'), delimiter
					= ",", quotechar='"')

t = (csvre,)
csvre.next()
for t in csvre:
	cursor.execute('INSERT INTO	main VALUES (?,?,?,?,?,?,?)', t)
connection.commit()


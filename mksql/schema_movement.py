import csv
import sqlite3

connection = sqlite3.connect('../sample_repo.db')
connection.text_factory = str
cursor = connection.cursor()

cursor.execute('DROP table IF EXISTS sample_location')
cursor.execute("""CREATE table sample_location (irs_id text, proj_id text,
                    proj_tube_no text, proj_cell text, date_moved date,
                    location text) """)

connection.commit()

csvre = csv.reader(open("../test_sampleFlow.csv", 'rb'), delimiter
					= ",", quotechar='"')

t = (csvre,)
csvre.next()
for t in csvre:
	cursor.execute('INSERT INTO	sample_location VALUES (?,?,?,?,?,?)', t)
    #print len(t)
connection.commit()


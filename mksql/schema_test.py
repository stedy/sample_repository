import csv
import sqlite3

connection = sqlite3.connect('../tsadb.db')
connection.text_factory = str
cursor = connection.cursor()

cursor.execute('DROP table IF EXISTS test_movement')
cursor.execute("""CREATE table test_movement (irs_id text, datestamp date, 
                    sent_from text, site text) """)

connection.commit()

csvre = csv.reader(open("../original/test_movement.csv", 'rb'), delimiter
					= ",", quotechar='"')

t = (csvre,)
csvre.next()
for t in csvre:
	cursor.execute('INSERT INTO	test_movement VALUES (?,?,?,?)', t)
    #print len(t)
connection.commit()


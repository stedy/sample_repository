import csv
import sqlite3

connection = sqlite3.connect('../tsadb.db')
connection.text_factory = str
cursor = connection.cursor()

cursor.execute('DROP table IF EXISTS sample_movement')
cursor.execute("""CREATE table sample_movement (irs_id text, proj_id text,
                    proj_tube_no text, proj_cell text, date_out date,
                    shipped_to text, sent_to text, received_date date) """)

connection.commit()

csvre = csv.reader(open("../test_sampleFlow.csv", 'rb'), delimiter
					= ",", quotechar='"')

t = (csvre,)
csvre.next()
for t in csvre:
	cursor.execute('INSERT INTO	sample_movement VALUES (?,?,?,?,?,?,?,?)', t)
    #print len(t)
connection.commit()


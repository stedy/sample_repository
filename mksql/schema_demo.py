import csv
import sqlite3

connection = sqlite3.connect('../sample_repo.db')
connection.text_factory = str
cursor = connection.cursor()

cursor.execute('DROP table IF EXISTS demo')
cursor.execute("""CREATE table demo (irs_id text, ptdon text, sample_res text, sample_type
                    text, sourcecoll text, sample_acc text,
                    coldate date, pt_name text, txdate date,
                    donor_names text, signed9 text) """)

connection.commit()

csvre = csv.reader(open("../test_patientInfo.csv", 'rb'), delimiter
					= ",", quotechar='"')

t = (csvre,)
csvre.next()
for t in csvre:
	cursor.execute('INSERT INTO	demo VALUES (?,?,?,?,?,?,?,?,?,?,?)', t)
connection.commit()


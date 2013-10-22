import csv
import sqlite3

connection = sqlite3.connect('../sample_repo.db')
connection.text_factory = str
cursor = connection.cursor()

cursor.execute('DROP table IF EXISTS repo_location')
cursor.execute("""CREATE table repo_location (urid text, freezer text, mainbox text,
	                main_cell text, label_info text, comments text,
                    current_location_freezer text,
                    current_location_box text, current_location_cell text) """)

connection.commit()

csvre = csv.reader(open("../original/repo_location.csv", 'rb'), delimiter
					= ",", quotechar='"')

t = (csvre,)
csvre.next()
for t in csvre:
	cursor.execute('INSERT INTO	repo_location VALUES (?,?,?,?,?,?,?,?,?)', t)
    #print len(t)
connection.commit()


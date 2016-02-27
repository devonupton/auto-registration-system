import cx_Oracle
import sys
import getpass

user = input( "Oracle username: " ) 
pw = getpass.getpass()
con_string = user + "/" + pw + "@gwynne.cs.ualberta.ca:1521/CRS"
con = cx_Oracle.connect( con_string )
con.autocommit = 1
curs = con.cursor()

statement =  ("CREATE TABLE Movie ( \
	     title	VARCHAR(20),  \
	     movie_number INTEGER, \
	     PRIMARY KEY( movie_number ) )")

curs.execute( statement )

statement = "INSERT INTO Movie VALUES ( 'Chicago', 1 )"  

curs.execute( statement )

query = "SELECT * FROM Movie"

curs.execute(query)
rows = curs.fetchall()

for row in rows:
	print(row)

statement = "DROP TABLE Movie"

curs.execute( statement )

# If we actually want to commit everytime, look into autocommit??

con.close()
try:
	con.close()
except:
	print( "con.close() successful...")
import cx_Oracle
import sys
import getpass

user = input( "Oracle username: " ) 
pw = getpass.getpass()
con_string = user + "/" + pw + "@gwynne.cs.ualberta.ca:1521/CRS"
con = cx_Oracle.connect( con_string )

con.close()
try:
	con.cursor()
except:
	print("con.close() successful...")
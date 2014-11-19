

from pyramid.config import Configurator

from dummy_data import getUsers
from dummy_data import userExists
from dummy_data import addUser

import psycopg2

if __name__ == '__main__':
	#print(getUsers())
	
	#print(userExists("jon@gfb.com"))
	
	print(addUser(1, "Nic@gfb.com", "password", "Nic", "Durish", "555-555-5555", None))
	

def Example():

	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")

	cur = conn.cursor()

	cur.execute("SELECT first_name from public.\"Users\"")

	rows = cur.fetchall()

	print ("\nShow me some stuff:\n")
	for row in rows:
		print ("   ", row)
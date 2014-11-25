

from pyramid.config import Configurator

from dummy_data import *

import psycopg2

if __name__ == '__main__':
	
	#print(userExists("jon@gfb.com"))
	
	#print(addUser(1, "example@gfb.com", "password", "Example", "Dude", "000-000-0000", None))
	
	#print(updateUser("jon@gfb.com", "jon@gfb.com", "password", "Jon", "Bourdeau", "111-111-1111", "1"))
	
	#print(authUser("jon@gfb.com", "password"))
	
	#print(getUsers())
	
	print(getUser("jon@gfb.com"))
	
	#print(addHostSite("Example Host Site 3", "", "", "", ""))
	
	#print(addCoordToHostSite("3","2"))
	
	#print(removeCoordFromHostSite("3","2"))
	
	#print(getHostSiteList("3"))
	
	#print(getHostSites())
	
	#print(getHostSite("1"))
	
	#print(addOrder("Bob", "Nopants", "bob@email.com", "123-456-7890", "1", "2", "30", "65", "1"))

	#print(updateOrder("1", "Bob", "Nopants", "bob@email.com", "123-456-7890", "1", "2", "30", "65", "2"))
	
	#print(getOrders("2"))
	
def Example():

	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")

	cur = conn.cursor()

	cur.execute("SELECT first_name from public.\"Users\"")

	rows = cur.fetchall()

	print ("\nShow me some stuff:\n")
	for row in rows:
		print ("   ", row)
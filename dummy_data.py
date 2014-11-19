
from pyramid.config import Configurator

import psycopg2


conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")

cur = conn.cursor()

cur.execute("SELECT * from public.\"Things\"")

rows = cur.fetchall()


COMPANY = "Garden Fresh Box"

def GetUsers():
	returnVal = []
	
	conn = psycopg2.connect("dbname='postgres' user='postgres' password='password'")
	cur = conn.cursor()
	cur.execute("SELECT first_name from public.\"Users\"")
	rows = cur.fetchall()

	for row in rows:
		user = {'first_name': row[0]}
		returnVal.append(user);
	
	return returnVal

SITE_MENU = [
        {'href': '', 'title': 'Home'},
        {'href': 'contact', 'title': COMPANY},
]
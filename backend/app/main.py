from flask import Flask
from flask_cors import CORS
import psycopg2

from flask import send_file
from flask import jsonify

import json
import shlex

app = Flask(__name__)
CORS(app)

app.config.from_pyfile('.env.py') # Load config/env vars

PUBLIC_DIR = f'{app.root_path}/../public'

JSON_FULLQUERY_PATH = f'arduino_hardver_query_json.sql'
CSV_FULLQUERY_PATH = f'arduino_hardver_query_csv.sql'

JSON_FILE_OUT = f'{PUBLIC_DIR}/arduino_hardver_auto.json'
CSV_FILE_OUT = f'{PUBLIC_DIR}/arduino_hardver_auto.csv'

SCHEMA_FILE = f'{PUBLIC_DIR}/schema.json'


def connect_to_db():
	""" """
	conn = psycopg2.connect(database	= app.config["POSTGRES_DBNAME"],
							host		= app.config["POSTGRES_HOST"],
							user		= app.config["POSTGRES_USER"],
							password	= app.config["POSTGRES_PASS"])
	return conn

dbase = connect_to_db() ###

def query(qu, params=None):
	""" """
	cur = dbase.cursor()
	if not qu.endswith(';'): qu += ';'
	cur.execute(qu, params)
	try:
		return cur.fetchall(), 0
	except psycopg2.ProgrammingError:
		return None, 0

cleanup = lambda ss: ss.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')

def logg(ss, *args, **kwargs):
	""" """
	print(f'{ss}', *args, **kwargs)


def db_generate_json():
	""" """
	with open(JSON_FULLQUERY_PATH) as fp:
		q = cleanup(fp.read())
	dbresp = query(q)

	if dbresp[1] == 0:
		jsn = (dbresp[0])[0][0]
		logg(f"Generated json data")
		return jsn, 0
	else:
		logg(f"Unable to generate json data")
		return [], 1


def save_json_public(dat):
	""" """
	with open(JSON_FILE_OUT, 'w') as fp:
		fp.write(json.dumps(dat, indent=4)) # fp.write(dat)
	logg(f"Saved json data at {JSON_FILE_OUT}")


def db_generate_csv():
	""" """
	with open(CSV_FULLQUERY_PATH) as fp:
		q = cleanup(fp.read())
	dbresp = query(q)

	if dbresp[1] == 0:
		formatted = []
		with open(SCHEMA_FILE) as fp:
			sch = json.loads(fp.read())
		formatted += [','.join(sch["items"]["required"])]

		for row in dbresp[0]:
			ss = ""
			ss += str(row[0])
			for col in row[1:]:
				if col is None:
					ss += ','
				elif type(col) == list:

					ss += ',"{'
					ss += f'{",".join(col)}'
					ss += '}"'
				else:
					ss += f',{str(col)}'
			formatted += [ss]

		logg(f"Generated csv data")
		return formatted, 0

	else:
		logg(f"Unable to generate csv data")
		return [], 1


def save_csv_public(dat):
	""" """
	with open(CSV_FILE_OUT, 'w') as fp:
		fp.write('\n'.join(dat))
	logg(f"Saved csv data at {CSV_FILE_OUT}")


@app.route("/")
def index():
	""" """
	return {'site': 'index'}, 200


@app.route("/get-schema")
def get_schema():
	""" """
	# return {'data': }, 200
	return send_file(SCHEMA_FILE, as_attachment=True)

@app.route("/get-full-json")
def get_full_json():
	""" """
	try:
		dat, stat = db_generate_json()
		if stat == 0: # Ok
			return {'data': dat}, 200
		else:
			return {'msg': 'Cannot generate JSON at this time'}, 503 

	except Exception as ex:
		logg(f'{ex}')

@app.route("/get-full-csv")
def get_full_csv():
	""" """
	try:
		dat, stat = db_generate_csv()
		if stat == 0: # Ok
			return {'data': dat}, 200
		else:
			return {'msg': 'Cannot generate CSV at this time'}, 503 

	except Exception as ex:
		logg(f'{ex}')

@app.route("/download-json")
def download_json():
	""" """
	try:
		dat, stat = db_generate_json()
		if stat == 0: # Ok
			save_json_public(dat)
			return send_file(JSON_FILE_OUT, as_attachment=True)
		else:
			return {'msg': 'Cannot generate JSON at this time'}, 503 

	except Exception as ex:
		logg(f'{ex}')


@app.route("/download-csv")
def download_csv():
	""" """
	try:
		dat, stat = db_generate_csv()
		if stat == 0: # Ok
			save_csv_public(dat)
			return send_file(CSV_FILE_OUT, as_attachment=True)
		else:
			return {'msg': 'Cannot generate JSON at this time'}, 503 

	except Exception as ex:
		logg(f'{ex}')

#####
# On load
##### 
jsns, _ = db_generate_json()
csvs, _ = db_generate_csv()

save_json_public(jsns)
save_csv_public(csvs)


### DEBUG MAIN ###
if __name__ == "__main__":
	app.run(port='5002', debug=True)

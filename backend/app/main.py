from flask import Flask, request
from flask_cors import CORS
import psycopg2

from flask import send_file
from flask import jsonify

import json
import shlex

from query_builder import make_query_json, make_query_csv

app = Flask(__name__)
CORS(app)

app.config.from_pyfile('.env.py') # Load config/env vars

PUBLIC_DIR = f'{app.root_path}/../public'

JSON_FULLQUERY_PATH = f'arduino_hardver_query_json.sql'
CSV_FULLQUERY_PATH = f'arduino_hardver_query_csv.sql'

JSON_TEMPLATE_PATH = f'arduino_hardver_query_json_template.sql'
CSV_TEMPLATE_PATH = f'arduino_hardver_query_csv_template.sql'

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

def query(qu, *params):
	""" """
	cur = dbase.cursor()
	if not qu.endswith(';'): qu += ';'
	logg(f"QUERY: {cur.mogrify(qu, params)}")

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


@app.route("/filter-download-json", methods=['POST'])
def filter_download_json():
	""" """
	data = request.json
	logg(f"\nReceived data:\n", data)

	with open(JSON_TEMPLATE_PATH) as fp:
		q = cleanup(fp.read())

	field = data['fltBy']
	value = data['fltTxt']

	fld = field
	if field == 'pins': fld = ""

	whole_cond, whole_params, pins_cond, pins_params = make_query_json(fld, value)
	q = q.replace('__INSERT_PIN_COND__', pins_cond)
	q = q.replace('__INSERT_WHOLE_COND__', whole_cond)
	tup = tuple(pins_params + whole_params)
	dbresp = query(q, *tup)

	if dbresp[1] == 0:
		jsn = (dbresp[0])[0][0]

		newjsn = []
		if field == 'pins':
			for obj in jsn:
				for o in obj['pins']:
					v = [o['pin_type'], o['pin_count'], *o['pin_list']]
					if value in v:
						newjsn += [obj]
		else:
			for row in jsn:
				if row['pins'] is not None:
					newjsn += [row]

		logg(f"Generated filtered json")
		save_json_public(newjsn)
		return send_file(JSON_FILE_OUT, as_attachment=True)
	else:
		logg(f"Unable to generate json data")
		return {'msg': 'Cannot filter at this time'}, 503


@app.route("/filter-download-csv", methods=['POST'])
def filter_download_csv():
	""" """
	data = request.json
	print(f"\nReceived data:\n", data)

	with open(CSV_TEMPLATE_PATH) as fp:
		q = cleanup(fp.read())

	field = data['fltBy']
	value = data['fltTxt']

	fld = field
	if field == 'pins': fld = ""

	whole_cond, whole_params = make_query_csv(fld, value)
	q = q.replace('__INSERT_WHOLE_COND__', whole_cond)
	dbresp = query(q, *tuple(whole_params))

	if dbresp[1] == 0:
		csv = dbresp[0]

		newcsv = []
		if field == 'pins':
			for row in csv:
				v = [row[12], row[13], *(row[14] if row[14] is not None else [])]
				if value in v:
					newcsv += [row]
		else:
			newcsv = csv

		logg(f"Generated filtered csv")
		with open(SCHEMA_FILE) as fp:
			sch = json.loads(fp.read())

		formatted = format_csv_resp(sch, newcsv)
		save_csv_public(formatted)

		logg(f"Saved csv data at {CSV_FILE_OUT}")
		return send_file(CSV_FILE_OUT, as_attachment=True)
	else:
		logg(f"Unable to generate csv data")
		return {'msg': 'Cannot filter at this time'}, 503


def save_json_public(dat):
	""" """
	with open(JSON_FILE_OUT, 'w') as fp:
		fp.write(json.dumps(dat, indent=4)) # fp.write(dat)
	logg(f"Saved json data at {JSON_FILE_OUT}")


def format_csv_resp(sch, rows):
	""" """
	props = sch["items"]["properties"]
	formatted = []
	names = f"{list(props.keys())[0]}"

	for prop in list(props.keys())[1:]:
		if prop == 'microcontroller':
			names += ','+','.join(props[prop]['properties'].keys())
		elif prop == 'pins':
			names += ','+','.join(props[prop]['items']['properties'].keys())
		else:
			names += ','+prop
	formatted += [names]

	for row in rows:
		ss = str(row[0])
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

	return formatted

def db_generate_csv():
	""" """
	with open(CSV_FULLQUERY_PATH) as fp:
		q = cleanup(fp.read())
	dbresp = query(q)

	if dbresp[1] == 0:
		formatted = []
		with open(SCHEMA_FILE) as fp:
			sch = json.loads(fp.read())

		formatted = format_csv_resp(sch, dbresp[0])

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
# On load pregen some
##### 
jsns, _ = db_generate_json()
csvs, _ = db_generate_csv()

save_json_public(jsns)
save_csv_public(csvs)


### DEBUG MAIN ###
if __name__ == "__main__":
	app.run(port='5002', debug=True)

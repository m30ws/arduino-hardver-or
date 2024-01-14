from flask import Flask, request
from flask_cors import CORS
from werkzeug.http import HTTP_STATUS_CODES
import psycopg2

from flask import send_file
from flask import jsonify

import json
import shlex
from functools import wraps

from query_builder import make_query_json, make_query_csv

import os
# from dotenv import load_dotenv
# load_dotenv()

from urllib.request import urlopen
from authlib.oauth2.rfc7523 import JWTBearerTokenValidator
from authlib.jose.rfc7517.jwk import JsonWebKey
from authlib.integrations.flask_oauth2 import ResourceProtector

class Auth0JWTBearerTokenValidator(JWTBearerTokenValidator):
	""" """
	def __init__(self, domain, audience):
		""" """
		issuer = f"https://{domain}/"
		jsonurl = urlopen(f"{issuer}.well-known/jwks.json")
		public_key = JsonWebKey.import_key_set(
			json.loads(jsonurl.read())
		)
		super(Auth0JWTBearerTokenValidator, self).__init__(
			public_key
		)
		self.claims_options = {
			"exp": {"essential": True},
			"aud": {"essential": True, "value": audience},
			"iss": {"essential": True, "value": issuer},
		}

require_auth = ResourceProtector()
validator = Auth0JWTBearerTokenValidator(
	f"{os.getenv('AUTH0_DOMAIN')}",
	f"{os.getenv('AUTH0_AUDIENCE')}"
)

require_auth.register_token_validator(validator)


app = Flask(__name__)#, static_folder=None)

STATIC_DIR = f'{app.root_path}/../static'

JSON_FULLQUERY_PATH = f'arduino_hardver_query_json.sql'
CSV_FULLQUERY_PATH = f'arduino_hardver_query_csv.sql'

JSON_TEMPLATE_PATH = f'arduino_hardver_query_json_template.sql'
CSV_TEMPLATE_PATH = f'arduino_hardver_query_csv_template.sql'

JSON_STATIC = f'{STATIC_DIR}/arduino_hardver.json'
CSV_STATIC = f'{STATIC_DIR}/arduino_hardver.csv'

OPENAPI_STATIC = f'{STATIC_DIR}/openapi.json'
SCHEMA_FILE = f'{STATIC_DIR}/schema.json'

GENERATED_DIR = f'{app.root_path}/../generated_files'

JSON_FILE_OUT = f'{GENERATED_DIR}/arduino_hardver_auto.json'
CSV_FILE_OUT = f'{GENERATED_DIR}/arduino_hardver_auto.csv'


CORS(app)


# =========== UTILITY ========== #


def connect_to_db():
	""" """
	conn = psycopg2.connect(database	= os.getenv("POSTGRES_DBNAME", ""),
							host		= os.getenv("POSTGRES_HOST", ""),
							user		= os.getenv("POSTGRES_USER", ""),
							password	= os.getenv("POSTGRES_PASS", ""))
	return conn

dbase = connect_to_db() ###


def query(qu, *params):
	""" """
	global dbase

	def query_(qu_, *params_):
		cur = dbase.cursor()
		if not qu_.endswith(';'): qu_ += ';'

		mogr = cur.mogrify(qu_, params_).replace(b'\t', b' ').replace(b'\n', b' ').strip()
		logg(f"Query: {mogr}")

		cur.execute(qu_, params_)
		try:
			return cur.fetchall(), 0
		except psycopg2.ProgrammingError:
			return None, 1
		finally:
			try:
				dbase.commit()
			except Exception as ex:
				logg(f"Warning :: {ex}")

	try:
		return query_(qu, *params)
	except (psycopg2.OperationalError, psycopg2.InterfaceError):
		logg(f"Restarting database connection...")
		dbase = connect_to_db()
		return query_(qu, *params)


# cleanup = lambda ss: ss.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
def cleanup(ss):
	""" """
	return ss.replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')


def logg(ss, *args, **kwargs):
	""" """
	print(f'{ss}', *args, **kwargs)


# Json_get
json_get = lambda: {} if request.data == b'' else request.json



# ========== API ========== #


def fmt_response(code=None, status=None, msg=None, resp=None):
	""" """
	if code is None:
		code = 200

	if status is None:
		try:
			status = HTTP_STATUS_CODES[code]
		except:
			status = "OK"

	if msg is None:
		msg = "Operation successful"

	if resp is None:
		resp = {}

	return {
		"status": status,
		"message": msg,
		"response": resp
	}, code


@app.errorhandler(400)
def handle_400(err):
	""" """
	logg(f"[!] Generic 400 encountered: {err}")

	return fmt_response(400, # "Bad Request",
		msg="Malformed input")


@app.errorhandler(404)
def handle_404(err):
	""" """
	logg(f"[!] Generic 404 encountered: {err} {request}")

	return fmt_response(404, # "Not Found",
		msg="Requested resource doesn't exist")


@app.errorhandler(405)
def handle_405(err):
	""" """
	logg(f"[!] Generic 405 encountered: {err}")

	return fmt_response(405, # "Method Not Allowed",
		msg="Requested method not allowed for requested resource")


@app.errorhandler(500)
def handle_generic_error(err):
	""" """
	logg(f"[!] Generic 50X encountered: {err}")

	# Convert 500 -> 503
	return fmt_response(503, # "Service Unavailable",
		msg="Requested service is temporarily unavailable")


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


# @app.route("/filter-download-json", methods=['POST'])
@app.route("/boards/filtered/json", methods=['POST'])
@app.route("/boards/filtered", methods=['POST'])
def filter_download_json():
	""" """

	data = json_get()

	logg(f"\nReceived data:\n", data)

	with open(JSON_TEMPLATE_PATH) as fp:
		q = cleanup(fp.read())

	if 'fltBy' not in data:
		#=[Response]=
		return fmt_response(400, # "Bad Request",
			msg="Filter field (fltBy) not specified")

	if 'fltTxt' not in data:
		#=[Response]=
		return fmt_response(400, # "Bad Request",
			msg="Filter expression (fltTxt) not specified") 

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

		logg(jsn, dbresp)

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
		#=[Response]=
		return fmt_response(503, # "Service Unavailable",
			msg="Cannot filter at this time")


# @app.route("/filter-download-csv", methods=['POST'])
@app.route("/boards/filtered/csv", methods=['POST'])
def filter_download_csv():
	""" """
	data = json_get() # request.json
	logg(f"\nReceived data:\n", data)

	with open(CSV_TEMPLATE_PATH) as fp:
		q = cleanup(fp.read())

	if 'fltBy' not in data:
		#=[Response]=
		return fmt_response(400, # "Bad Request",
			msg="Filter field (fltBy) not specified")
	if 'fltTxt' not in data:
		#=[Response]=
		return fmt_response(400, # "Bad Request",
			msg="Filter expression (fltTxt) not specified") 

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
		#=[Response]=
		return fmt_response(503, # "Service Unavailable",
			msg="Cannot filter at this time")


def save_json_public(dat):
	""" """
	# with open(JSON_FILE_OUT, 'w') as fp:
	# 	fp.write(json.dumps(dat, indent=4)) # fp.write(dat)
	# logg(f"Saved json data at {JSON_FILE_OUT}")
	with open(JSON_STATIC, 'w') as fp:
		fp.write(json.dumps(dat, indent=4)) # fp.write(dat)
	logg(f"Saved json data at {JSON_STATIC}")


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
	# with open(CSV_FILE_OUT, 'w') as fp:
	# 	fp.write('\n'.join(dat))
	# logg(f"Saved csv data at {CSV_FILE_OUT}")
	with open(CSV_STATIC, 'w') as fp:
		fp.write('\n'.join(dat))
	logg(f"Saved csv data at {CSV_STATIC}")


@app.route("/")
def index():
	""" """
	return {'site': 'index'}, 200


@app.route("/get-schema")
def get_schema():
	""" """
	try:
		return send_file(SCHEMA_FILE, as_attachment=True)
	except Exception as ex:
		logg(f'{ex}')
		return fmt_response(503,
			msg="Cannot fetch schema at this time")


@app.route("/openapi")
def get_openapi():
	""" """
	try:
		return send_file(OPENAPI_STATIC, as_attachment=True)

	except Exception as ex:
		logg(f'{ex}')
		return fmt_response(503,
			msg="Cannot fetch openapi docs at this time")


# @app.route("/get-full-json")
# def get_full_json():
# 	""" """
# 	try:
# 		dat, stat = db_generate_json()
# 		if stat == 0: # Ok
# 			return {'data': dat}, 200
# 		else:
# 			return {'msg': 'Cannot generate JSON at this time'}, 503 

# 	except Exception as ex:
# 		logg(f'{ex}')

# @app.route("/get-full-csv")
# def get_full_csv():
# 	""" """
# 	try:
# 		dat, stat = db_generate_csv()
# 		if stat == 0: # Ok
# 			return {'data': dat}, 200
# 		else:
# 			return {'msg': 'Cannot generate CSV at this time'}, 503 

# 	except Exception as ex:
# 		logg(f'{ex}')


@app.route("/snapshot-database", methods=['GET'])
@require_auth("update:snapshot_database")
def snapshot_db():
	""" """
	try:
		dat, stat = db_generate_json()
		if stat == 0: # Ok
			save_json_public(dat)
		else:
			return fmt_response(503,
				msg="Unable to generate snapshot at this time")

		dat, stat = db_generate_csv()
		if stat == 0: # Ok
			save_csv_public(dat)
		else:
			return fmt_response(503,
				msg="Unable to generate snapshot at this time")

		return fmt_response(200,
			msg="Generated snapshots")

	except Exception as ex:
		logg(f'{ex}')
		return fmt_response(503,
			msg="Unable to generate snapshot at this time")


# @app.route("/download-json", methods=['GET'])
@app.route("/boards/json", methods=['GET'])
@app.route("/boards", methods=['GET'])
def download_json():
	""" """
	try:
		# dat, stat = db_generate_json()
		# if stat == 0: # Ok
		# 	save_json_public(dat)
		# 	return send_file(JSON_FILE_OUT, as_attachment=True)
		# else:
		# 	return {'msg': 'Cannot generate JSON at this time'}, 503
		
		return send_file(JSON_STATIC, as_attachment=True)

	except Exception as ex:
		logg(f'{ex}')
		return fmt_response(503,
			msg="Cannot fetch json data at this time")


# @app.route("/download-csv", methods=['GET'])
@app.route("/boards/csv", methods=['GET'])
def download_csv():
	""" """
	try:
		# dat, stat = db_generate_csv()
		# if stat == 0: # Ok
		# 	save_csv_public(dat)
		# 	return send_file(CSV_FILE_OUT, as_attachment=True)
		# else:
		# 	return {'msg': 'Cannot generate JSON at this time'}, 503
		return send_file(CSV_STATIC, as_attachment=True)

	except Exception as ex:
		logg(f'{ex}')
		return fmt_response(503,
			msg="Cannot fetch csv data at this time")


@app.route("/microcontrollers/<microcontroller_name>", methods=['GET'])
@app.route("/microcontrollers", methods=['GET'])
def get_microcontroller(microcontroller_name=None):
	""" """
	q = """
			SELECT json_agg(
				json_build_object(
					'microcontroller_name', microcontroller_name,
					'low_power', 			low_power::bool,
					'i2c', 					i2c,
					'spi', 					spi,
					'microcontroller_id', 	microcontroller_id
				)
			)
			from public.microcontroller
		"""
	params = tuple()

	if microcontroller_name is not None:
		q += f" where microcontroller_name = %s "
		params = (microcontroller_name,)

	dbresp = query(q, *params)

	# DB error
	if dbresp[1] != 0:
		return fmt_response(503,
			msg="Cannot fetch microcontroller(s) at this time")

	dbresp = dbresp[0][0][0]

	# No entries
	if dbresp is None:
		return fmt_response(404,
			msg="Microcontroller name doesn't exist")

	# logg(f"\nmicrocontroller resp:\n{dbresp}")

	# OK
	return fmt_response(200, resp=dbresp)


# PUT
@app.route("/microcontrollers/<int:microcontroller_id>", methods=['PUT'])
@app.route("/microcontrollers/<microcontroller_name>", methods=['PUT'])
def microcontroller_put(microcontroller_id=None, microcontroller_name=None):
	""" """
	if microcontroller_name is None and microcontroller_id is None:
		#=[Response]=
		return fmt_response(400,
			msg="Invalid data provided")

	data = json_get() or dict(request.form)

	logg(microcontroller_name, microcontroller_id)
	logg(f"data: {data}")


	q = """
		UPDATE microcontroller SET 
	"""
	fields = []
	params = []

	if 'low_power' in data:
		fields += ['low_power']
		params += [data['low_power']]

	if 'i2c' in data:
		fields += ['i2c']
		params += [data['i2c']]

	if 'spi' in data:
		fields += ['spi']
		params += [data['spi']]

	if 'microcontroller_name' in data:
		fields += ['microcontroller_name']
		params += [data['microcontroller_name']]

	if len(fields) == 0:
		#=[Response]=
		return fmt_response(400,
			msg="Invalid data provided")

	for i, f in enumerate(fields):
		q += f" {f} = %s"
		if i < len(fields) - 1:
			q += ","

	def build_distinct_cond(lst, paramsRef):
		""" Builds DISTINCT list and updates params list ! """
		ss = " ( "
		for i, f in enumerate(lst):
			ss += f" microcontroller.{f} IS DISTINCT FROM %s "
			paramsRef += [ data[f] ]
			if i < len(lst) - 1:
				ss += " OR "
		return f"{ss} ) "


	if microcontroller_id is not None:
		q += " WHERE microcontroller_id = %s "
		params += [microcontroller_id]

	elif microcontroller_name is not None:
		q += " WHERE microcontroller_name = %s "
		params += [microcontroller_name]


	dist = build_distinct_cond(fields, params)
	q += f" AND {dist} "

	q += " RETURNING microcontroller.* "
	params = tuple(params)

	logg(q, params)

	dbresp = query(q, *params)

	logg(f"dbresp: {dbresp}")

	if dbresp[1] != 0:
		return fmt_response(503,
			msg="Cannot PUT microcontroller at this time")

	elif len(dbresp[0]) > 0:
		return fmt_response(200,
			msg="Resource updated")

	else:
		return fmt_response(204,
			msg="Resource unchanged")


@app.route("/pins/<sku>", methods=['GET'])
@app.route("/pins", methods=['GET'])
def get_pins(sku=None):
	""" """
	q = """
			SELECT json_agg(
				json_build_object(
					'sku', 			public.pins.sku,
					'pin_type', 	public.pins.type,
					'pin_count', 	public.pins.count,
					'pin_list', 	COALESCE(public.pins.pin_list, '{}')
				))
			from public.pins
		"""
	params = tuple()

	if sku is not None:
		q += f" where sku = %s "
		params = (sku, )

	dbresp = query(q, *params)

	# DB error
	if dbresp[1] != 0:
		return fmt_response(503,
			msg="Cannot fetch pins at this time")

	dbresp = dbresp[0][0][0]

	# No entries
	if dbresp is None:
		return fmt_response(404,
			msg="Sku doesn't exist")

	# logg(f"\nsku resp:\n{dbresp}")

	# OK
	return fmt_response(200, resp=dbresp)


# POST
@app.route("/families", methods=['POST'])
def family_create():
	""" """
	data = json_get() or dict(request.form)
	
	if not data:
		#=[Response]=
		return fmt_response(400,
			msg="Invalid data provided")

	if 'family_name' not in data or data['family_name'] == '':
		#=[Response]=
		return fmt_response(400,
			msg="Invalid data provided")

	logg(f"family create: {data}")

	q = """
		INSERT INTO public.family
			(family_name) VALUES (%s)
		RETURNING family_id
	"""
	params = (data['family_name'],)

	dbresp = query(q, *params)
	if dbresp[1] != 0:
		#=[Response]=
		return fmt_response(400,
			msg="Invalid data provided")

	generated_family_id = dbresp[0][0][0]

	return fmt_response(201,
		msg="Resource created", resp={
			"family_id": generated_family_id
		})


@app.route("/families", methods=['GET']) ###
def family_get():
	dbresp = query(""" select json_agg(json_build_object('family_id', family_id, 'family_name', family_name)) from family """)
	return fmt_response(200, resp=dbresp[0][0][0])

# DELETE
@app.route("/families/<int:family_id>", methods=['DELETE'])
@app.route("/families/<family_name>", methods=['DELETE'])
def family_delete(family_name=None, family_id=None):
	""" """
	q = """
		DELETE FROM family
	"""
	params = tuple()

	if family_name is not None:
		logg(f"family_name: {family_name}")
		q += f" WHERE family_name = %s "
		params = (family_name,)

	elif family_id is not None:
		logg(f"family_id: {family_id}")
		q += f" WHERE family_id = %s "
		params = (family_id,)

	else:
		#=[Response]=
		return fmt_response(400,
			msg="Invalid data provided")

	q += " RETURNING family.family_id "

	logg(f"family delete: {q} , {params}")

	dbresp = query(q, *params)
	logg(f"dbresp {dbresp}")
	if dbresp[1] != 0:
		#=[Response]=
		return fmt_response(400,
			msg="Unable to delete selected resource")

	return fmt_response(200,
		msg="Resource deleted")


#####
# On load pregen some
##### 
# jsns, _ = db_generate_json()
# csvs, _ = db_generate_csv()
# save_json_public(jsns)
# save_csv_public(csvs)


### DEBUG MAIN ###
if __name__ == "__main__":
	app.run(port='5002', debug=True)

def make_query_json(field, value):
	""" """
	# field -> 'fltBy'
	# value ->'fltTxt'

	whole_params = []
	pins_params = []

	whole_cond = ""
	pins_cond = ""

	if field == f'model':
		whole_params += [f"%{value}%"]
		whole_cond += f""" model ILIKE %s """

	elif field == f'family_name':
		whole_params += [f"%{value}%"]
		whole_cond += r" family_name ILIKE %s "

	elif field == f'sku':
		whole_params += [f"%{value}%"]
		whole_cond += r" sku ILIKE %s "

	elif field == f'microcontroller':
		whole_params += 4 * [f"%{value}%"]
		whole_cond += r" microcontroller_name ILIKE %s OR low_power::text ILIKE %s::text OR i2c::text ILIKE %s::text OR spi::text ILIKE %s::text "

	elif field == f'clock_speed':
		whole_params += [int(value)]
		whole_cond += r" clock_speed = %s "

	elif field == f'flash_memory':
		whole_params += [int(value)]
		whole_cond += r" flash_memory = %s "

	elif field == f'sram':
		whole_params += [float(value)]
		whole_cond += r" sram = %s "

	elif field == f'operating_voltage':
		whole_params += [float(value)]
		whole_cond += r" operating_voltage = %s "

	elif field == f'input_voltage':
		whole_params += [f"%{value}%"]
		whole_cond += r" input_voltage ILIKE %s "

	elif field == f'pins':
		pins_params += [f"%{value}%", f"%{value}%", f"{value}"]
		pins_cond += r" type ILIKE %s OR count::text ILIKE %s::text or %s ILIKE ANY(pin_list) "

	elif field == f'length':
		whole_params += [float(value)]
		whole_cond += r" length = %s "

	elif field == f'width':
		whole_params += [float(value)]
		whole_cond += r" width = %s "

	elif field == f'weight':
		whole_params += [float(value)]
		whole_cond += r" weight = %s "


	if whole_cond != "": whole_cond = f"WHERE {whole_cond}"
	if pins_cond != "": pins_cond = f"AND {pins_cond}"
	
	return whole_cond, whole_params, pins_cond, pins_params


def make_query_csv(field, value):
	""" """
	# field -> 'fltBy'
	# value ->'fltTxt'

	whole_params = []

	whole_cond = ""
	pins_cond = ""

	if field == f'model':
		whole_params += [f"%{value}%"]
		whole_cond += f""" model ILIKE %s """

	elif field == f'family_name':
		whole_params += [f"%{value}%"]
		whole_cond += r" family_name ILIKE %s "

	elif field == f'sku':
		whole_params += [f"%{value}%"]
		whole_cond += r" sku ILIKE %s "

	elif field == f'microcontroller':
		whole_params += 4 * [f"%{value}%"]
		whole_cond += r" microcontroller_name ILIKE %s OR low_power::text ILIKE %s::text OR i2c::text ILIKE %s::text OR spi::text ILIKE %s::text "

	elif field == f'clock_speed':
		whole_params += [int(value)]
		whole_cond += r" clock_speed = %s "

	elif field == f'flash_memory':
		whole_params += [int(value)]
		whole_cond += r" flash_memory = %s "

	elif field == f'sram':
		whole_params += [float(value)]
		whole_cond += r" sram = %s "

	elif field == f'operating_voltage':
		whole_params += [float(value)]
		whole_cond += r" operating_voltage = %s "

	elif field == f'input_voltage':
		whole_params += [f"%{value}%"]
		whole_cond += r" input_voltage ILIKE %s "

	elif field == f'pins':
		whole_params += [f"%{value}%", f"%{value}%", f"{value}"]
		whole_cond += r" type ILIKE %s OR count::text ILIKE %s::text or %s ILIKE ANY(pin_list) "

	elif field == f'length':
		whole_params += [float(value)]
		whole_cond += r" length = %s "

	elif field == f'width':
		whole_params += [float(value)]
		whole_cond += r" width = %s "

	elif field == f'weight':
		whole_params += [float(value)]
		whole_cond += r" weight = %s "


	if whole_cond != "": whole_cond = f"WHERE {whole_cond}"

	print(f"{whole_cond} || {whole_params}")
	
	return whole_cond, whole_params
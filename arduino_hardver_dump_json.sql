copy (
	select json_agg(
		json_build_object(
			'model', model,
			'family_name', family_name,
			'sku', public.board.sku,
			'microcontroller', json_build_object(
				'microcontroller_name', microcontroller_name,
				'low_power', 			low_power::bool,
				'i2c', 					i2c,
				'spi', 					spi
			),
			'clock_speed', 			clock_speed,
			'flash_memory', 		flash_memory,
			'sram', 				sram,
			'operating_voltage', 	operating_voltage,
			'input_voltage', 		input_voltage,
			
			'pins', (
				SELECT
					json_agg(json_build_object(
						'pin_type', 	public.pins.type,
						'pin_count', 	public.pins.count,
						'pin_list', 	COALESCE(public.pins.pin_list, '{}')
				))
				from public.pins
				where public.pins.sku = public.board.sku
			),
			'length', 				length,
			'width', 				width,
			'weight', 				weight
		))
	from public.board
		join public.family 
			using(family_id)
		join public.microcontroller
			using(microcontroller_id)
	)
to 'C:/arduino_hardver.json'
;
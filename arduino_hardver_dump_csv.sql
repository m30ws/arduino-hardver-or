copy (
	select model, family_name, sku, microcontroller_name, low_power::text, i2c, spi, clock_speed,
		flash_memory, sram,operating_voltage, input_voltage, digital_pins,
		pwm_pins, analog_in_pins, analog_out_pins, length, width, weight
	from public.board
			join public.family 
				using(family_id)
			join public.microcontroller
				using(microcontroller_id)
	)
to 'C:/arduino_hardver.csv'
delimiter ','
csv header
;
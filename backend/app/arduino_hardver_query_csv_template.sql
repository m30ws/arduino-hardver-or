select model, family_name, public.board.sku, microcontroller_name, low_power::text, i2c, spi, clock_speed,
	flash_memory, sram,operating_voltage, input_voltage,
	public.pins.type as pin_type, public.pins.count as pin_count, public.pins.pin_list,
	length, width, weight
from public.board
		join public.family 
			using(family_id)
		join public.microcontroller
			using(microcontroller_id)
		left join public.pins
			using (sku)

__INSERT_WHOLE_COND__
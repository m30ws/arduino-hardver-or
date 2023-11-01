# Otvoreni podaci o Arduino razvojnim pločicama

Repozitorij sadrži otvoreni skup podataka o dijelu Arduino razvojnih pločica te nekim njihovim tehničkim karakteristikama i mogućnostima.

## Licenca
Shield: [![CC BY 4.0][cc-by-shield]][cc-by]

This work is licensed under a
[Creative Commons Attribution 4.0 International License][cc-by].

[![CC BY 4.0][cc-by-image]][cc-by]

[cc-by]: http://creativecommons.org/licenses/by/4.0/
[cc-by-image]: https://i.creativecommons.org/l/by/4.0/88x31.png
[cc-by-shield]: https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg

[comment]: # (https://github.com/santisoler/cc-licenses#cc-attribution-40-international)

## Općenite informacije

**Autor:** Fran Tomljenović

**Verzija:** 1.0

**Jezik:** Engleski

## Atributi

### Board
| Property | Data type | Description |
|----------|-----------|-------------|
| model | varijabilni tekst (64) | Ime modela pločice |
| family | cijeli broj | Obitelj pločica |
| sku | varijabilni tekst (32) | ID proizvoda |
| clock_speed | cijeli broj | Radni takt (MHz) |
| flash_memory | cijeli broj | Veličina memorije (KB) |
| sram | decimalni broj | Veličina radne memorije (KB) |
| operating_voltage | decimalni broj | Napon komponenti (V) |
| input_voltage | varijabilni tekst (5) | Raspon ulaznog napona u pločicu (V) |
| digital_pins | cijeli broj | Broj digitalnih pinova |
| pwm_pins | cijeli broj | Broj PWM pinova |
| analog_in_pins | cijeli broj | Broj ulaznih analognih pinova |
| analog_out_pins | cijeli broj | Broj izlaznih analognih pinova |
| length | decimalni broj | Duljina pločice (mm) |
| width | decimalni broj | Širina pločice (mm) |
| weight | cijeli broj | Masa pločice (g) |

### Family
| Property | Data type | Description |
|----------|-----------|-------------|
| family_name | varijabilni tekst (64) | Naziv obitelji pločica |

### Microcontroller
| Property | Data type | Description |
|----------|-----------|-------------|
| microcontroller_name | varijabilni tekst (64) | Naziv modela mikrokontrolera |
| low_power | boolean | Dostupan low-power mod? |
| i2c | cijeli broj | Broj dostupnih I2C sučelja |
| spi | cijeli broj | Broj dostupnih SPI sučelja |

## CSV i JSON

Exportanje podataka iz baze u navedene oblike izvodi se pokretanjem odgovarajuće *.sql* skripte koja će zatim generirane podatke smjestiti u datoteku na disku čija je pretpostavljena vrijednost `C:\arduino_hardver.csv` odnosno `C:\arduino_hardver.json`. Za pisanja na navedena mjesta potrebno je imati odgovarajuće sigurnosne dozvole, a ona se mogu promijeniti u samoj skripti.

[comment]: # (Alternativno može se pozvati direktno alat *psql* s odgovarajućim parametrima za spajanje i autentikaciju )

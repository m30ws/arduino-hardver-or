--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

-- Started on 2023-11-01 02:32:46

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- TOC entry 200 (class 1259 OID 18704)
-- Name: board; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.board (
    model character varying(64) NOT NULL,
    family_id integer NOT NULL,
    sku character varying(32) NOT NULL,
    microcontroller_id integer NOT NULL,
    clock_speed integer NOT NULL,
    flash_memory integer NOT NULL,
    sram real NOT NULL,
    operating_voltage real NOT NULL,
    input_voltage character varying(5) NOT NULL,
    digital_pins integer NOT NULL,
    pwm_pins integer,
    analog_in_pins integer,
    analog_out_pins integer,
    length real NOT NULL,
    width real NOT NULL,
    weight integer NOT NULL
);


ALTER TABLE public.board OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 18707)
-- Name: family; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.family (
    family_id integer NOT NULL,
    family_name character varying(64) NOT NULL
);


ALTER TABLE public.family OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 18710)
-- Name: microcontroller; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.microcontroller (
    microcontroller_id integer NOT NULL,
    microcontroller_name character varying(64) NOT NULL,
    low_power boolean,
    i2c integer,
    spi integer
);


ALTER TABLE public.microcontroller OWNER TO postgres;

--
-- TOC entry 2992 (class 0 OID 18704)
-- Dependencies: 200
-- Data for Name: board; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.board (model, family_id, sku, microcontroller_id, clock_speed, flash_memory, sram, operating_voltage, input_voltage, digital_pins, pwm_pins, analog_in_pins, analog_out_pins, length, width, weight) FROM stdin;
Arduino Nano	0	A000005	0	16	32	2	5	7-12	22	6	8	0	45	18	7
Arduino Nano 33 IoT	0	ABX00027	1	48	256	32	3.3	21	14	11	8	1	45	18	5
Arduino Nano 33 BLE	0	ABX00030	2	64	1000	256	3.3	21	14	14	8	0	45	18	5
Arduino MKR WiFi 1010	1	ABX00023	1	48	256	32	3.3	5	8	13	7	1	61.5	25	32
Arduino MKR Zero	1	ABX00012	1	48	256	32	3.3	5	22	12	7	1	61.5	25	32
Arduino MKR GSM 1400	1	MKRGSM1400WANT	1	48	256	32	3.3	5	8	13	7	1	67.64	25	32
Arduino UNO WiFi Rev2	2	ABX00021	3	16	48	6	5	6-20	14	5	6	0	68.6	53.4	25
Arduino UNO R3	2	A000066	4	16	32	2	5	7-12	14	6	6	0	68.6	53.4	25
Arduino Leonardo	2	A000057	5	16	32	2.5	5	7-12	20	7	12	0	68.6	53.3	20
Arduino Mega 2560 Rev3	3	A000067	6	16	256	8	5	7-12	54	15	16	0	101.52	53.3	37
Arduino Due	3	A000062	7	84	512	96	3.3	7-12	54	12	12	2	101.52	53.3	36
\.


--
-- TOC entry 2993 (class 0 OID 18707)
-- Dependencies: 201
-- Data for Name: family; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.family (family_id, family_name) FROM stdin;
0	Nano Family
1	MKR Family
2	Classic Family
3	Mega Family
\.


--
-- TOC entry 2994 (class 0 OID 18710)
-- Dependencies: 202
-- Data for Name: microcontroller; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.microcontroller (microcontroller_id, microcontroller_name, low_power, i2c, spi) FROM stdin;
0	ATmega328	f	1	2
1	SAMD21 Cortex-M0+ 32bit low power ARM MCU	t	6	6
2	nRF52840	t	2	4
3	ATmega4809	t	1	1
4	ATmega328P	t	1	2
5	ATmega32u4	f	1	2
6	ATmega2560	f	1	5
7	AT91SAM3X8E	t	2	6
\.


--
-- TOC entry 2857 (class 2606 OID 18714)
-- Name: family family_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.family
    ADD CONSTRAINT family_pkey PRIMARY KEY (family_id);


--
-- TOC entry 2859 (class 2606 OID 18716)
-- Name: microcontroller microcontroller_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.microcontroller
    ADD CONSTRAINT microcontroller_pkey PRIMARY KEY (microcontroller_id);


--
-- TOC entry 2860 (class 2606 OID 18717)
-- Name: board family_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.board
    ADD CONSTRAINT family_id FOREIGN KEY (family_id) REFERENCES public.family(family_id) NOT VALID;


--
-- TOC entry 2861 (class 2606 OID 18722)
-- Name: board microcontroller_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.board
    ADD CONSTRAINT microcontroller_id FOREIGN KEY (microcontroller_id) REFERENCES public.microcontroller(microcontroller_id) NOT VALID;


-- Completed on 2023-11-01 02:32:47

--
-- PostgreSQL database dump complete
--


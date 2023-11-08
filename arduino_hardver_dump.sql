--
-- PostgreSQL database dump
--

-- Dumped from database version 13.2
-- Dumped by pg_dump version 13.2

-- Started on 2023-11-08 18:34:37

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
-- TOC entry 200 (class 1259 OID 18728)
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
    length real NOT NULL,
    width real NOT NULL,
    weight integer NOT NULL
);


ALTER TABLE public.board OWNER TO postgres;

--
-- TOC entry 201 (class 1259 OID 18731)
-- Name: family; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.family (
    family_id integer NOT NULL,
    family_name character varying(64) NOT NULL
);


ALTER TABLE public.family OWNER TO postgres;

--
-- TOC entry 202 (class 1259 OID 18734)
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
-- TOC entry 203 (class 1259 OID 18771)
-- Name: pins; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pins (
    sku character varying(32) NOT NULL,
    type character varying(16) NOT NULL,
    count integer,
    pin_list character varying(8)[]
);


ALTER TABLE public.pins OWNER TO postgres;

--
-- TOC entry 2999 (class 0 OID 18728)
-- Dependencies: 200
-- Data for Name: board; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.board (model, family_id, sku, microcontroller_id, clock_speed, flash_memory, sram, operating_voltage, input_voltage, length, width, weight) FROM stdin;
Arduino Nano	0	A000005	0	16	32	2	5	7-12	45	18	7
Arduino Nano 33 IoT	0	ABX00027	1	48	256	32	3.3	21	45	18	5
Arduino Nano 33 BLE	0	ABX00030	2	64	1000	256	3.3	21	45	18	5
Arduino MKR WiFi 1010	1	ABX00023	1	48	256	32	3.3	5	61.5	25	32
Arduino MKR Zero	1	ABX00012	1	48	256	32	3.3	5	61.5	25	32
Arduino MKR GSM 1400	1	MKRGSM1400WANT	1	48	256	32	3.3	5	67.64	25	32
Arduino UNO WiFi Rev2	2	ABX00021	3	16	48	6	5	6-20	68.6	53.4	25
Arduino UNO R3	2	A000066	4	16	32	2	5	7-12	68.6	53.4	25
Arduino Leonardo	2	A000057	5	16	32	2.5	5	7-12	68.6	53.3	20
Arduino Mega 2560 Rev3	3	A000067	6	16	256	8	5	7-12	101.52	53.3	37
Arduino Due	3	A000062	7	84	512	96	3.3	7-12	101.52	53.3	36
\.


--
-- TOC entry 3000 (class 0 OID 18731)
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
-- TOC entry 3001 (class 0 OID 18734)
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
-- TOC entry 3002 (class 0 OID 18771)
-- Dependencies: 203
-- Data for Name: pins; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.pins (sku, type, count, pin_list) FROM stdin;
A000005	digital	22	\N
A000005	pwm	6	{3,5,6,9,10,11}
A000005	analogin	8	\N
A000005	analogout	0	\N
ABX00027	digital	14	\N
ABX00027	pwm	11	{2,3,5,6,9,10,11,12,16,17,19}
ABX00027	analogin	8	\N
ABX00027	analogout	1	{A0}
ABX00030	digital	14	\N
ABX00030	pwm	14	\N
ABX00030	analogin	8	\N
ABX00030	analogout	0	\N
ABX00023	digital	8	\N
ABX00023	pwm	13	{0,1,2,3,4,5,6,7,8,10,12,18,19}
ABX00023	analogin	7	\N
ABX00023	analogout	1	{A0}
ABX00012	digital	22	\N
ABX00012	pwm	12	{0,1,2,3,4,5,6,7,8,10,18,19}
ABX00012	analogin	7	\N
ABX00012	analogout	1	{A0}
MKRGSM1400WANT	digital	8	\N
MKRGSM1400WANT	pwm	13	{0,1,2,3,4,5,6,7,8,10,12,18,19}
MKRGSM1400WANT	analogin	7	\N
MKRGSM1400WANT	analogout	1	{A0}
ABX00021	digital	14	\N
ABX00021	pwm	5	{3,5,6,9,10}
ABX00021	analogin	6	\N
ABX00021	analogout	0	\N
A000066	digital	14	\N
A000066	pwm	6	{3,5,6,9,10,11}
A000066	analogin	6	\N
A000066	analogout	0	\N
A000057	digital	20	\N
A000057	pwm	7	{3,5,6,9,10,11,13}
A000057	analogin	12	\N
A000057	analogout	0	\N
A000067	digital	54	\N
A000067	pwm	15	{2,3,4,5,6,7,8,9,10,11,12,13,44,45,46}
A000067	analogin	16	\N
A000067	analogout	0	\N
A000062	digital	54	\N
A000062	pwm	12	{2,3,4,5,6,7,8,9,10,11,12,13}
A000062	analogin	12	\N
A000062	analogout	2	{A0,A1}
\.


--
-- TOC entry 2862 (class 2606 OID 18738)
-- Name: family family_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.family
    ADD CONSTRAINT family_pkey PRIMARY KEY (family_id);


--
-- TOC entry 2864 (class 2606 OID 18740)
-- Name: microcontroller microcontroller_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.microcontroller
    ADD CONSTRAINT microcontroller_pkey PRIMARY KEY (microcontroller_id);


--
-- TOC entry 2866 (class 2606 OID 18778)
-- Name: pins pins_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pins
    ADD CONSTRAINT pins_pkey PRIMARY KEY (sku, type);


--
-- TOC entry 2867 (class 2606 OID 18741)
-- Name: board family_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.board
    ADD CONSTRAINT family_id FOREIGN KEY (family_id) REFERENCES public.family(family_id) NOT VALID;


--
-- TOC entry 2868 (class 2606 OID 18746)
-- Name: board microcontroller_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.board
    ADD CONSTRAINT microcontroller_id FOREIGN KEY (microcontroller_id) REFERENCES public.microcontroller(microcontroller_id) NOT VALID;


-- Completed on 2023-11-08 18:34:37

--
-- PostgreSQL database dump complete
--


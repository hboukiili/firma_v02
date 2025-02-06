--
-- PostgreSQL database dump
--

-- Dumped from database version 16.4 (Debian 16.4-1.pgdg110+2)
-- Dumped by pg_dump version 16.4 (Debian 16.4-1.pgdg110+2)

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

--
-- Data for Name: models_only_farmer; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_farmer (id, first_name, last_name, email, password) FROM stdin;
1	admin	firma	h@g.com	pbkdf2_sha256$390000$Jx81CYWF3ZNdOlQQVST0M4$nqkFbBc0Y6Fs5/kyYhodVnrdv9GRKo5v4x5Hmct5LgI=
2	string	string	user@example.com	pbkdf2_sha256$390000$TeD68MMdlKXaKHBwjp8RBh$josUWE29yQK0gcIsYp57YISp63vyhTIA7CXSyUq6oyE=
3	string	string	user1@example.com	pbkdf2_sha256$390000$ya9FEHdAHzm7OEz7bmg2Pt$LVmQfDbfOsh9YhJE4a2F9SFRtQbGUjtyY8J5qRSvxNU=
4	a	b	farmer@g.com	pbkdf2_sha256$390000$7TxCfagkbkRRkMUFC9VIGi$TztqejAzwom1PQ671Y1w+GNlNmuLRMrDZ6KiksWragE=
5	hamza	boukili	f@g.com	pbkdf2_sha256$390000$yfyJf3sMZemSI0OuCv3vDl$68WhKjer/WoerMh2IDU2Z4WW2lrljTsCbq2oOgDJw/M=
6	tst	tst	t@g.com	pbkdf2_sha256$390000$YtU6XnZZv3s6FupwRXIztd$ojuWs3RdQG/XDv2Yqz8BqYEBPK1VPmr9MJXiFcxeRa0=
\.


--
-- Data for Name: models_only_field; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_field (id, name, boundaries, user_id_id) FROM stdin;
32	E3P2	0103000020E610000001000000060000001EFF058200B91EC0DFE00B93A9AA3F4052D4997B48B81EC019ABCDFFABAA3F40EC6CC83F33B81EC0F1457BBC90AA3F409015FC36C4B81EC0151C5E1091AA3F40DFA5D425E3B81EC04E9B711AA2AA3F401EFF058200B91EC0DFE00B93A9AA3F40	1
34	E3P1	0103000020E61000000100000007000000B344679945B81EC09C89E942ACAA3F403753211E89B71EC0F6D4EAABABAA3F40AE9AE7887CB71EC02D95B7239CAA3F402BA4FCA4DAB71EC0F3CAF5B699AA3F404D4C1762F5B71EC01F2E39EE94AA3F401955867137B81EC0D2C43BC093AA3F40B344679945B81EC09C89E942ACAA3F40	1
35	E3P4	0103000020E61000000100000005000000419DF2E846B81EC0F6D4EAABABAA3F40014EEFE2FDB81EC0382C0DFCA8AA3F40560F98874CB91EC073309B00C3AA3F40A704C4245CB81EC03DBB7CEBC3AA3F40419DF2E846B81EC0F6D4EAABABAA3F40	1
36	E3P3	0103000020E61000000100000005000000488AC8B08AB71EC0F6D4EAABABAA3F40E02C25CB49B81EC0C05FCC96ACAA3F40A704C4245CB81EC096067E54C3AA3F40FE2AC0779BB71EC077853E58C6AA3F40488AC8B08AB71EC0F6D4EAABABAA3F40	1
37	E3P6	0103000020E61000000100000005000000C8B60C384BB91EC0BADC60A8C3AA3F407DE882FA96B91EC013622EA9DAAA3F40B2BD16F4DEB81EC0D00A0C59DDAA3F404B5645B8C9B81EC060915F3FC4AA3F40C8B60C384BB91EC0BADC60A8C3AA3F40	1
38	E3P8	0103000020E610000001000000070000004016A243E0B81EC02A560DC2DCAA3F40D46531B1F9B81EC00A0F9A5DF7AA3F4083F755B950B91EC017F19D98F5AA3F405B971AA19FB91EC0BEA59C2FF6AA3F404451A04FE4B91EC0B493C151F2AA3F408E1F2A8D98B91EC013622EA9DAAA3F404016A243E0B81EC02A560DC2DCAA3F40	1
39	E3P7	0103000020E61000000100000008000000D46531B1F9B81EC088307E1AF7AA3F40B2BD16F4DEB81EC07B4E7ADFF8AA3F40F7949C137BB81EC07B4E7ADFF8AA3F40C9ACDEE176B81EC06FB72407ECAA3F40FDA36FD234B81EC0166C239EECAA3F40302C7FBE2DB81EC0F4E0EEACDDAA3F40CE6E2D93E1B81EC04D2CF015DDAA3F40D46531B1F9B81EC088307E1AF7AA3F40	1
40	E3P5	0103000020E61000000100000005000000BE840A0E2FB81EC0BE6BD097DEAA3F40DBFB54151AB81EC006465ED6C4AA3F40EBE5779ACCB81EC060915F3FC4AA3F404016A243E0B81EC02A560DC2DCAA3F40BE840A0E2FB81EC0BE6BD097DEAA3F40	1
41	E2P6	0103000020E61000000100000007000000EC6CC83F33B81EC0166C239EECAA3F408BFCFA2136B81EC0F86F5E9CF8AA3F40D50451F701B81EC0F86F5E9CF8AA3F407BA35698BEB71EC038F7578FFBAA3F4086E3F90CA8B71EC00BD5CDC5DFAA3F40BE840A0E2FB81EC09A95ED43DEAA3F40EC6CC83F33B81EC0166C239EECAA3F40	1
42	E2P5	0103000020E6100000010000000500000009FCE1E7BFB71EC00F643DB5FAAA3F40DCF126BF45B71EC0E200FA7DFFAA3F401BBAD91F28B71EC0A4A7C821E2AA3F4026732CEFAAB71EC00BD5CDC5DFAA3F4009FCE1E7BFB71EC00F643DB5FAAA3F40	1
43	E2P7	0103000020E6100000010000000500000086E3F90CA8B71EC0E7FEEA71DFAA3F402B137EA99FB71EC01D3A3DEFC6AA3F40DBFB54151AB81EC006465ED6C4AA3F40CFBBB1A030B81EC077BF0AF0DDAA3F4086E3F90CA8B71EC0E7FEEA71DFAA3F40	1
44	E2P4	0103000020E6100000010000000500000026732CEFAAB71EC0E7FEEA71DFAA3F40A912656F29B71EC0FEF2C98AE1AA3F405A828C800AB71EC077853E58C6AA3F40BA6B09F9A0B71EC0A0185932C7AA3F4026732CEFAAB71EC0E7FEEA71DFAA3F40	1
45	E2P3	0103000020E610000001000000050000009DBAF2599EB71EC077853E58C6AA3F40D6E253008CB71EC073F6CE68ABAA3F40EE409DF2E8B61EC073F6CE68ABAA3F405A828C800AB71EC077853E58C6AA3F409DBAF2599EB71EC077853E58C6AA3F40	1
46	E2P2	0103000020E61000000100000005000000D6E253008CB71EC073F6CE68ABAA3F4020425C397BB71EC0DCD6169E97AA3F4088D9CBB6D3B61EC0A661F88898AA3F407C992842EAB61EC04F20EC14ABAA3F40D6E253008CB71EC073F6CE68ABAA3F40	1
47	E2P1	0103000020E6100000010000000600000020425C397BB71EC059F8FA5A97AA3F404293C49272B71EC04A0C022B87AA3F402C9ACE4E06B71EC0994528B682AA3F4093196F2BBDB61EC04DDC2A8881AA3F4088D9CBB6D3B61EC02383DC4598AA3F4020425C397BB71EC059F8FA5A97AA3F40	1
\.


--
-- Data for Name: models_only_aquacrop_output; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_aquacrop_output (id, date, "IrrDay", "Tr", "DeepPerc", "Es", "Th1", "Th2", th3, gdd_cum, canopy_cover, biomass, z_root, "DryYield", "FreshYield", harvest_index, "ET", field_id_id) FROM stdin;
\.


--
-- Data for Name: models_only_crop; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_crop (id, "Crop", "Crop_planting_date", "Tree", "Tree_planting_date", field_id_id) FROM stdin;
\.


--
-- Data for Name: models_only_irrigation_system; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_irrigation_system (id, irrigation_type, instalation_date, field_id_id) FROM stdin;
46	Drip	\N	32
52	Drip	\N	47
53	Drip	\N	47
54	Drip	\N	46
55	Drip	\N	45
56	Drip	\N	44
57	Drip	\N	43
58	Drip	\N	42
59	Drip	\N	41
60	Drip	\N	40
61	Drip	\N	39
62	Drip	\N	38
63	Drip	\N	37
64	Drip	\N	36
65	Drip	\N	35
66	Drip	\N	34
\.


--
-- Data for Name: models_only_drip_irrigation; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_drip_irrigation (irrigation_system_ptr_id, "Crop_Tubes_distance", "Crop_Drippers_distance", "Crop_outflow_rate", "Tree_row_distance", "Tree_distance", "Tubes_number_by_tree", drippers_number_by_tree, "Tree_outflow_rate") FROM stdin;
46	\N	\N	\N	\N	\N	\N	\N	\N
52	\N	\N	\N	\N	\N	\N	\N	\N
53	\N	\N	\N	\N	\N	\N	\N	\N
54	\N	\N	\N	\N	\N	\N	\N	\N
55	\N	\N	\N	\N	\N	\N	\N	\N
56	\N	\N	\N	\N	\N	\N	\N	\N
57	\N	\N	\N	\N	\N	\N	\N	\N
58	\N	\N	\N	\N	\N	\N	\N	\N
59	\N	\N	\N	\N	\N	\N	\N	\N
60	\N	\N	\N	\N	\N	\N	\N	\N
61	\N	\N	\N	\N	\N	\N	\N	\N
62	\N	\N	\N	\N	\N	\N	\N	\N
63	\N	\N	\N	\N	\N	\N	\N	\N
64	\N	\N	\N	\N	\N	\N	\N	\N
65	\N	\N	\N	\N	\N	\N	\N	\N
66	\N	\N	\N	\N	\N	\N	\N	\N
\.


--
-- Data for Name: models_only_drone; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_drone (id, datetime, field_id_id) FROM stdin;
\.


--
-- Data for Name: models_only_fao_crop_parametre; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_fao_crop_parametre (id, crop, "Kcbini", "Kcbmid", "Kcbend", "Lini", "Ldev", "Lmid", "Lend", "Zrini", zrmax, pbase, "Ze") FROM stdin;
1	Broccoli	0.15	0.95	0.85	35	45	40	15	0.05	0.6	0.45	0.1
2	Cabbage	0.15	0.95	0.85	40	60	50	15	0.05	0.8	0.45	0.1
3	Carrots	0.15	0.95	0.85	30	40	60	20	0.05	1	0.35	0.1
4	Cauliflower	0.15	0.95	0.85	35	50	40	15	0.05	0.7	0.45	0.1
5	Celery	0.15	0.95	0.9	25	40	45	14	0.05	0.5	0.2	0.1
6	Lettuce	0.15	0.9	0.9	20	30	15	10	0.05	0.5	0.3	0.1
7	Dry onions	0.15	0.95	0.65	15	25	70	40	0.05	0.6	0.3	0.1
9	Seed onions	0.15	1.05	0.7	20	45	165	45	0.05	0.6	0.35	0.1
10	Spinach	0.15	0.9	0.85	20	20	25	5	0.05	0.5	0.2	0.1
11	Radishes	0.15	0.85	0.75	5	10	15	5	0.05	0.5	0.3	0.1
12	EggPlant	0.15	1	0.8	30	45	40	25	0.05	1.2	0.45	0.1
13	Sweet Peppers	0.15	1	0.8	30	35	40	20	0.05	1	0.3	0.1
14	Tomato	0.15	1.1	0.8	30	40	45	30	0.05	1.5	0.4	0.1
15	Cantaloupe	0.15	0.75	0.5	30	45	35	10	0.05	1.5	0.45	0.1
16	Cucumber	0.15	0.95	0.7	20	30	40	14	0.05	1.2	0.5	0.1
17	Pumpkin	0.15	0.95	0.7	20	30	40	15	0.05	1.5	0.35	0.1
18	Sweet Melons	0.15	1	0.7	25	35	40	20	0.05	1.5	0.4	0.1
19	Watermelon	0.15	0.95	0.7	20	30	30	30	0.05	1.5	40	0.1
20	Beets	0.15	0.95	0.85	15	25	20	10	0.05	1	0.5	0.1
21	Potato	0.15	0.95	0.85	30	35	50	30	0.05	0.6	0.35	0.1
22	Sweet Potato	0.15	1.1	0.55	20	30	60	40	0.05	1.5	0.65	0.1
23	Sugar Beet	0.15	1.15	0.5	25	35	50	50	0.05	1.2	0.55	0.1
8	green Onions	0.15	0.9	0.9	25	30	10	5	0.05	0.6	0.3	0.1
24	Green Beans	0.15	1	0.8	20	30	30	10	0.05	0.7	0.45	0.1
25	Dry Beans	0.15	1	0.8	20	30	40	20	0.05	0.9	0.45	0.1
26	Faba Bean	0.15	1.1	1.05	90	45	40	0	0.05	0.7	0.45	0.1
27	Green Gram	0.15	1	0.55	20	30	30	20	0.05	1	0.45	0.1
28	Cowpeas	0.15	1	0.55	20	30	30	20	0.05	1	0.45	0.1
29	Groundnut	0.15	1.1	0.5	35	45	35	25	0.05	1	0.5	0.1
30	Lentil	0.15	1.05	0.2	20	30	60	40	0.05	0.8	0.5	0.1
31	Peas	0.15	1.1	1.05	20	30	35	15	0.05	1	0.4	0.1
32	Soybeans	0.15	1.1	0.3	20	35	60	25	0.05	1.3	0.5	0.1
33	Artichokes	0.15	0.95	0.9	40	40	250	30	0.05	0.9	0.45	0.1
34	Asparagus	0.15	0.95	0.9	90	30	200	45	0.05	1.8	0.45	0.1
35	Cotton	0.15	1.15	0.4	30	50	60	55	0.05	1.7	0.65	0.1
36	Flax	0.15	1.05	0.2	30	50	60	55	0.05	1.7	0.65	0.1
37	Sunflower	0.15	0.95	0.25	25	35	45	25	0.05	1.5	0.45	0.1
38	Barley	0.15	1.1	0.15	15	30	65	40	0.05	1.5	0.55	0.1
39	Oats	0.15	1.1	0.15	15	30	65	40	0.05	1.5	0.55	0.1
40	Spring Wheat	0.15	1.1	0.15	15	30	65	40	0.05	1.5	0.55	0.1
41	Winter Wheat	0.15	1.1	0.15	30	140	40	30	0.05	1.8	0.55	0.1
42	Field Corn	0.15	1.15	0.5	30	50	60	40	0.05	1.7	0.55	0.1
43	Sweet Corn	0.15	1.1	1	20	25	25	10	0.05	1.2	0.5	0.1
44	Millet	0.15	0.95	0.2	20	30	55	35	0.05	2	0.55	0.1
45	Rice	1	1.15	0.45	30	30	60	30	0.05	1	0.2	0.1
46	Alfalfa Hay	0.3	0.45	0.45	5	20	10	10	0.05	2	0.6	0.1
47	Bermuda Hay	0.5	0.95	0.8	10	15	75	35	0.05	1	0.6	0.1
48	Banana first year	0.15	1.05	0.9	120	90	120	60	0.05	0.9	0.35	0.1
49	Banana second year	0.6	1.1	1.05	120	60	180	5	0.05	0.9	0.35	0.1
50	Pineapple	0.15	0.25	0.25	60	120	600	10	0.05	0.6	0.5	0.1
51	Berries	0.2	1	0.4	20	40	120	60	0.05	1.2	0.5	0.1
52	Grapes	0.15	0.8	0.4	20	40	120	60	0.05	2	0.35	0.1
53	olivies	0.55	0.65	0.65	30	90	60	90	0.05	1.7	0.65	0.1
54	Pistachios	0.2	1.05	0.4	20	60	30	40	0.05	1.5	0.4	0.1
\.


--
-- Data for Name: models_only_fao_output; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_fao_output (id, date, field_id) FROM stdin;
\.


--
-- Data for Name: models_only_forcast_weather_date; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_forcast_weather_date (id, "Date", "T2m", "Ws", "Et0", "Rain", "Rh", "D2m", "Field_id_id") FROM stdin;
\.


--
-- Data for Name: models_only_irrigation_amount; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_irrigation_amount (id, amount, date, irrigation_system_id_id) FROM stdin;
3	0	2024-12-16	46
4	0	2024-12-17	46
5	0	2024-12-18	46
6	0	2024-12-19	46
7	22.10251597	2024-12-20	46
8	0	2024-12-21	46
9	0	2024-12-22	46
10	17.68372754	2024-12-23	46
11	0	2024-12-24	46
12	0	2024-12-25	46
13	0	2024-12-26	46
14	0	2024-12-27	46
15	0	2024-12-28	46
16	0	2024-12-29	46
17	0	2024-12-30	46
18	0	2024-12-31	46
19	0	2025-01-01	46
20	0	2025-01-02	46
21	0	2025-01-03	46
22	1.494152744	2025-01-04	46
23	6.17857993	2025-01-05	46
24	0	2025-01-06	46
25	0	2025-01-07	46
26	0	2025-01-08	46
27	0	2025-01-09	46
28	0	2025-01-10	46
29	0	2025-01-11	46
30	0	2025-01-12	46
31	0	2025-01-13	46
32	0	2025-01-14	46
33	0	2025-01-15	46
34	0	2025-01-16	46
35	0	2025-01-17	46
36	7.328736828	2025-01-18	46
37	0	2025-01-19	46
38	0	2025-01-20	46
39	0	2025-01-21	46
40	0	2025-01-22	46
41	0	2025-01-23	46
\.


--
-- Data for Name: models_only_lidar; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_lidar (id, datetime, field_id_id) FROM stdin;
\.


--
-- Data for Name: models_only_maitenance_dates; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_maitenance_dates (id, date, irrigation_system_id_id) FROM stdin;
\.


--
-- Data for Name: models_only_ogimet_stations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_ogimet_stations (id, station_id, lat, long, location_name) FROM stdin;
1	60060	29.366666666666667	-10.183055555555555	Sidi ifni
2	60101	35.726111111111116	-5.905277777777778	Tanger Aerodrome
3	60106	35.17222222222222	-5.313055555555556	Chefchaouen
4	60115	34.783055555555556	-1.9330555555555553	Oujda
5	60120	34.30027777777777	-6.594444444444444	Kenitra
6	60128	34.39666666666667	-2.8980555555555556	Taourirt
7	60135	34.045833333333334	-6.757777777777778	Rabat-Sale
8	60141	33.9325	-4.974722222222223	Fes-Sais
9	60144	34.22944444444445	-3.943611111111111	Taza Hammou Meftah
10	60150	33.88194444444444	-5.522777777777778	Meknes
11	60155	33.56666666666667	-7.666666666666667	Casablanca
12	60156	33.36666666666667	-7.583055555555555	Nouasseur
13	60158	33.645833333333336	-7.214166666666667	Benslimane
14	60160	33.5	-5.166666666666667	Ifrane
15	60165	33.23305555555556	-8.516666666666667	El Jadida
16	60178	32.86666666666667	-6.966666666666667	Khouribga
17	60185	32.283055555555556	-9.233055555555556	Safi
18	60195	32.683055555555555	-4.733055555555556	Midelt
19	60200	32.56638888888889	-1.7833333333333332	Bouarfa
20	60210	31.93305555555556	-4.4	Errachidia
21	60230	31.616388888888892	-8.033055555555556	Marrakech
22	60253	30.5	-8.816666666666666	Taroudant
23	60265	30.93305555555556	-6.9	Ouarzazate
24	60270	29.68305555555556	-9.733055555555556	Tiznit
25	60280	29.016666666666666	-10.05	Guelmin
26	60285	28.445833333333333	-11.158055555555556	Tan-Tan
27	60340	34.98305555555556	-3.0166666666666666	Nador-Aroui
\.


--
-- Data for Name: models_only_policymaker; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_policymaker (id, first_name, last_name, email, password) FROM stdin;
\.


--
-- Data for Name: models_only_remote_sensing; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_remote_sensing (id, datetime, path, "RS_type", source, field_id_id) FROM stdin;
\.


--
-- Data for Name: models_only_searcher; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_searcher (id, first_name, last_name, email, password) FROM stdin;
\.


--
-- Data for Name: models_only_sentinel2; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_sentinel2 (id, path, date) FROM stdin;
\.


--
-- Data for Name: models_only_soil; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_soil (id, soil_input_method, soil_type, sand_percentage, silt_percentage, clay_percentage, field_id_id) FROM stdin;
\.


--
-- Data for Name: models_only_soil_analysis; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_soil_analysis (id, "PH_eau", "EC_ms_cm", "EC_ms_cm_pate_saturée", "Argile", "Limon", "Sable", "MO", "Nt", "P205", "K20", "Na20", "Na", "Cao", "Ca", "MGo", "Mg", "SAR", "Cu", "Mn", "Fe", "Zn", "NNH4", "NO3", "CI", "BORE", "Caco3", "Caco3_actif_AXB", soil_id_id) FROM stdin;
\.


--
-- Data for Name: models_only_sol_fao_parametre; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_sol_fao_parametre (id, sol, "REW_min", "REW_max", "thetaFC_min", "thetaFC_max", "thetaWP_min", "thetaWP_max") FROM stdin;
1	Sand	2	7	0.07	0.17	0.02	0.07
2	Loamy sand	4	8	0.11	0.17	0.03	0.1
3	Sandy loam	6	10	0.18	0.28	0.06	0.16
4	Loam	8	10	0.2	0.3	0.07	0.17
5	Silt loam	8	11	0.22	0.36	0.09	0.21
6	Silt	8	11	0.28	0.36	0.12	0.22
7	Silt clay loam	8	11	0.3	0.37	0.17	0.24
8	Silty clay	8	12	0.3	0.42	0.17	0.29
9	Clay	8	12	0.32	0.4	0.2	0.24
\.


--
-- Data for Name: models_only_sprinkler_irrigation; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_sprinkler_irrigation (irrigation_system_ptr_id, coverage_area, outflow_rate, number_of_sprinklers) FROM stdin;
\.


--
-- Data for Name: models_only_station; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_station (id, datetime, coordinates, station_type, sensor_type, mesur, field_id_id) FROM stdin;
\.


--
-- Data for Name: models_only_surface_irrigation; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_surface_irrigation (irrigation_system_ptr_id) FROM stdin;
\.


--
-- Data for Name: models_only_weather_date; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_weather_date (id, "Date", "T2m", "Ws", "Et0", "Rain", "Rh", "D2m", "Field_id_id") FROM stdin;
\.


--
-- Name: models_only_aquacrop_output_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_aquacrop_output_id_seq', 1, false);


--
-- Name: models_only_crop_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_crop_id_seq', 29, true);


--
-- Name: models_only_drone_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_drone_id_seq', 1, false);


--
-- Name: models_only_fao_crop_parametre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_fao_crop_parametre_id_seq', 1, false);


--
-- Name: models_only_fao_output_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_fao_output_id_seq', 1, false);


--
-- Name: models_only_farmer_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_farmer_id_seq', 1, true);


--
-- Name: models_only_field_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_field_id_seq', 31, true);


--
-- Name: models_only_forcast_weather_date_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_forcast_weather_date_id_seq', 1, false);


--
-- Name: models_only_irrigation_amount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_irrigation_amount_id_seq', 41, true);


--
-- Name: models_only_irrigation_system_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_irrigation_system_id_seq', 68, true);


--
-- Name: models_only_lidar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_lidar_id_seq', 1, false);


--
-- Name: models_only_maitenance_dates_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_maitenance_dates_id_seq', 1, false);


--
-- Name: models_only_ogimet_stations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_ogimet_stations_id_seq', 1, false);


--
-- Name: models_only_policymaker_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_policymaker_id_seq', 1, false);


--
-- Name: models_only_remote_sensing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_remote_sensing_id_seq', 1, false);


--
-- Name: models_only_searcher_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_searcher_id_seq', 1, false);


--
-- Name: models_only_sentinel2_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_sentinel2_id_seq', 1, false);


--
-- Name: models_only_soil_analysis_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_soil_analysis_id_seq', 1, false);


--
-- Name: models_only_soil_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_soil_id_seq', 30, true);


--
-- Name: models_only_sol_fao_parametre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_sol_fao_parametre_id_seq', 1, false);


--
-- Name: models_only_station_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_station_id_seq', 1, false);


--
-- Name: models_only_weather_date_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_weather_date_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--


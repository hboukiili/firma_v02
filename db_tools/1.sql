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
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group (id, name) FROM stdin;
1	admin
2	farmer
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	contenttypes	contenttype
5	sessions	session
6	models_only	fao_crop_parametre
7	models_only	field
8	models_only	irrigation_system
9	models_only	ogimet_stations
10	models_only	sentinel2
11	models_only	soil
12	models_only	sol_fao_parametre
13	models_only	drip_irrigation
14	models_only	sprinkler_irrigation
15	models_only	surface_irrigation
16	models_only	weather_date
17	models_only	user
18	models_only	station
19	models_only	soil_analysis
20	models_only	remote_sensing
21	models_only	maitenance_dates
22	models_only	lidar
23	models_only	irrigation_amount
24	models_only	forcast_weather_date
25	models_only	fao_output
26	models_only	drone
27	models_only	crop
28	models_only	aquacrop_output
29	django_celery_beat	crontabschedule
30	django_celery_beat	intervalschedule
31	django_celery_beat	periodictask
32	django_celery_beat	periodictasks
33	django_celery_beat	solarschedule
34	django_celery_beat	clockedschedule
35	django_celery_results	taskresult
36	django_celery_results	chordcounter
37	django_celery_results	groupresult
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add content type	4	add_contenttype
14	Can change content type	4	change_contenttype
15	Can delete content type	4	delete_contenttype
16	Can view content type	4	view_contenttype
17	Can add session	5	add_session
18	Can change session	5	change_session
19	Can delete session	5	delete_session
20	Can view session	5	view_session
21	Can add fao_ crop_ parametre	6	add_fao_crop_parametre
22	Can change fao_ crop_ parametre	6	change_fao_crop_parametre
23	Can delete fao_ crop_ parametre	6	delete_fao_crop_parametre
24	Can view fao_ crop_ parametre	6	view_fao_crop_parametre
25	Can add field	7	add_field
26	Can change field	7	change_field
27	Can delete field	7	delete_field
28	Can view field	7	view_field
29	Can add irrigation_system	8	add_irrigation_system
30	Can change irrigation_system	8	change_irrigation_system
31	Can delete irrigation_system	8	delete_irrigation_system
32	Can view irrigation_system	8	view_irrigation_system
33	Can add ogimet_stations	9	add_ogimet_stations
34	Can change ogimet_stations	9	change_ogimet_stations
35	Can delete ogimet_stations	9	delete_ogimet_stations
36	Can view ogimet_stations	9	view_ogimet_stations
37	Can add sentinel2	10	add_sentinel2
38	Can change sentinel2	10	change_sentinel2
39	Can delete sentinel2	10	delete_sentinel2
40	Can view sentinel2	10	view_sentinel2
41	Can add soil	11	add_soil
42	Can change soil	11	change_soil
43	Can delete soil	11	delete_soil
44	Can view soil	11	view_soil
45	Can add sol_ fao_ parametre	12	add_sol_fao_parametre
46	Can change sol_ fao_ parametre	12	change_sol_fao_parametre
47	Can delete sol_ fao_ parametre	12	delete_sol_fao_parametre
48	Can view sol_ fao_ parametre	12	view_sol_fao_parametre
49	Can add drip_ irrigation	13	add_drip_irrigation
50	Can change drip_ irrigation	13	change_drip_irrigation
51	Can delete drip_ irrigation	13	delete_drip_irrigation
52	Can view drip_ irrigation	13	view_drip_irrigation
53	Can add sprinkler_irrigation	14	add_sprinkler_irrigation
54	Can change sprinkler_irrigation	14	change_sprinkler_irrigation
55	Can delete sprinkler_irrigation	14	delete_sprinkler_irrigation
56	Can view sprinkler_irrigation	14	view_sprinkler_irrigation
57	Can add surface_irrigation	15	add_surface_irrigation
58	Can change surface_irrigation	15	change_surface_irrigation
59	Can delete surface_irrigation	15	delete_surface_irrigation
60	Can view surface_irrigation	15	view_surface_irrigation
61	Can add weather_date	16	add_weather_date
62	Can change weather_date	16	change_weather_date
63	Can delete weather_date	16	delete_weather_date
64	Can view weather_date	16	view_weather_date
65	Can add user	17	add_user
66	Can change user	17	change_user
67	Can delete user	17	delete_user
68	Can view user	17	view_user
69	Can add station	18	add_station
70	Can change station	18	change_station
71	Can delete station	18	delete_station
72	Can view station	18	view_station
73	Can add soil_analysis	19	add_soil_analysis
74	Can change soil_analysis	19	change_soil_analysis
75	Can delete soil_analysis	19	delete_soil_analysis
76	Can view soil_analysis	19	view_soil_analysis
77	Can add remote_sensing	20	add_remote_sensing
78	Can change remote_sensing	20	change_remote_sensing
79	Can delete remote_sensing	20	delete_remote_sensing
80	Can view remote_sensing	20	view_remote_sensing
81	Can add maitenance_dates	21	add_maitenance_dates
82	Can change maitenance_dates	21	change_maitenance_dates
83	Can delete maitenance_dates	21	delete_maitenance_dates
84	Can view maitenance_dates	21	view_maitenance_dates
85	Can add lidar	22	add_lidar
86	Can change lidar	22	change_lidar
87	Can delete lidar	22	delete_lidar
88	Can view lidar	22	view_lidar
89	Can add irrigation_amount	23	add_irrigation_amount
90	Can change irrigation_amount	23	change_irrigation_amount
91	Can delete irrigation_amount	23	delete_irrigation_amount
92	Can view irrigation_amount	23	view_irrigation_amount
93	Can add forcast_ weather_date	24	add_forcast_weather_date
94	Can change forcast_ weather_date	24	change_forcast_weather_date
95	Can delete forcast_ weather_date	24	delete_forcast_weather_date
96	Can view forcast_ weather_date	24	view_forcast_weather_date
97	Can add fao_output	25	add_fao_output
98	Can change fao_output	25	change_fao_output
99	Can delete fao_output	25	delete_fao_output
100	Can view fao_output	25	view_fao_output
101	Can add drone	26	add_drone
102	Can change drone	26	change_drone
103	Can delete drone	26	delete_drone
104	Can view drone	26	view_drone
105	Can add crop	27	add_crop
106	Can change crop	27	change_crop
107	Can delete crop	27	delete_crop
108	Can view crop	27	view_crop
109	Can add aquacrop_output	28	add_aquacrop_output
110	Can change aquacrop_output	28	change_aquacrop_output
111	Can delete aquacrop_output	28	delete_aquacrop_output
112	Can view aquacrop_output	28	view_aquacrop_output
113	Can add crontab	29	add_crontabschedule
114	Can change crontab	29	change_crontabschedule
115	Can delete crontab	29	delete_crontabschedule
116	Can view crontab	29	view_crontabschedule
117	Can add interval	30	add_intervalschedule
118	Can change interval	30	change_intervalschedule
119	Can delete interval	30	delete_intervalschedule
120	Can view interval	30	view_intervalschedule
121	Can add periodic task	31	add_periodictask
122	Can change periodic task	31	change_periodictask
123	Can delete periodic task	31	delete_periodictask
124	Can view periodic task	31	view_periodictask
125	Can add periodic task track	32	add_periodictasks
126	Can change periodic task track	32	change_periodictasks
127	Can delete periodic task track	32	delete_periodictasks
128	Can view periodic task track	32	view_periodictasks
129	Can add solar event	33	add_solarschedule
130	Can change solar event	33	change_solarschedule
131	Can delete solar event	33	delete_solarschedule
132	Can view solar event	33	view_solarschedule
133	Can add clocked	34	add_clockedschedule
134	Can change clocked	34	change_clockedschedule
135	Can delete clocked	34	delete_clockedschedule
136	Can view clocked	34	view_clockedschedule
137	Can add task result	35	add_taskresult
138	Can change task result	35	change_taskresult
139	Can delete task result	35	delete_taskresult
140	Can view task result	35	view_taskresult
141	Can add chord counter	36	add_chordcounter
142	Can change chord counter	36	change_chordcounter
143	Can delete chord counter	36	delete_chordcounter
144	Can view chord counter	36	view_chordcounter
145	Can add group result	37	add_groupresult
146	Can change group result	37	change_groupresult
147	Can delete group result	37	delete_groupresult
148	Can view group result	37	view_groupresult
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public."user" (id, password, last_login, is_superuser, email, first_name, last_name, role, is_staff, is_active, date_joined) FROM stdin;
2	pbkdf2_sha256$390000$x7WrXbLNHbSHCBBj3O43fZ$fNrbmDgOy6/H7VOyXFUfec0xo4jKE2tJkhoeNh76Tf0=	2025-02-26 19:47:23.5892+00	t	h@g.com			admin	t	t	2025-02-26 19:47:09.993204+00
3	pbkdf2_sha256$390000$TU465P2blcOA11DxqG4oq3$R5qU0VBN9uwaC1UjclnUl59YV7xCqJo/Rz2xVheVi44=	\N	f	farmer@g.com	farmer	farmer	farmer	f	t	2025-02-26 20:43:50.039523+00
\.


--
-- Data for Name: field; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.field (id, name, boundaries, user_id) FROM stdin;
1	E3P2	0103000020E610000001000000060000001EFF058200B91EC0DFE00B93A9AA3F4052D4997B48B81EC019ABCDFFABAA3F40EC6CC83F33B81EC0F1457BBC90AA3F409015FC36C4B81EC0151C5E1091AA3F40DFA5D425E3B81EC04E9B711AA2AA3F401EFF058200B91EC0DFE00B93A9AA3F40	3
2	E3P1	0103000020E61000000100000007000000B344679945B81EC09C89E942ACAA3F403753211E89B71EC0F6D4EAABABAA3F40AE9AE7887CB71EC02D95B7239CAA3F402BA4FCA4DAB71EC0F3CAF5B699AA3F404D4C1762F5B71EC01F2E39EE94AA3F401955867137B81EC0D2C43BC093AA3F40B344679945B81EC09C89E942ACAA3F40	3
3	E3P4	0103000020E61000000100000005000000419DF2E846B81EC0F6D4EAABABAA3F40014EEFE2FDB81EC0382C0DFCA8AA3F40560F98874CB91EC073309B00C3AA3F40A704C4245CB81EC03DBB7CEBC3AA3F40419DF2E846B81EC0F6D4EAABABAA3F40	3
4	E3P3	0103000020E61000000100000005000000488AC8B08AB71EC0F6D4EAABABAA3F40E02C25CB49B81EC0C05FCC96ACAA3F40A704C4245CB81EC096067E54C3AA3F40FE2AC0779BB71EC077853E58C6AA3F40488AC8B08AB71EC0F6D4EAABABAA3F40	3
5	E3P6	0103000020E61000000100000005000000C8B60C384BB91EC0BADC60A8C3AA3F407DE882FA96B91EC013622EA9DAAA3F40B2BD16F4DEB81EC0D00A0C59DDAA3F404B5645B8C9B81EC060915F3FC4AA3F40C8B60C384BB91EC0BADC60A8C3AA3F40	3
6	E3P8	0103000020E610000001000000070000004016A243E0B81EC02A560DC2DCAA3F40D46531B1F9B81EC00A0F9A5DF7AA3F4083F755B950B91EC017F19D98F5AA3F405B971AA19FB91EC0BEA59C2FF6AA3F404451A04FE4B91EC0B493C151F2AA3F408E1F2A8D98B91EC013622EA9DAAA3F404016A243E0B81EC02A560DC2DCAA3F40	3
7	E3P7	0103000020E61000000100000008000000D46531B1F9B81EC088307E1AF7AA3F40B2BD16F4DEB81EC07B4E7ADFF8AA3F40F7949C137BB81EC07B4E7ADFF8AA3F40C9ACDEE176B81EC06FB72407ECAA3F40FDA36FD234B81EC0166C239EECAA3F40302C7FBE2DB81EC0F4E0EEACDDAA3F40CE6E2D93E1B81EC04D2CF015DDAA3F40D46531B1F9B81EC088307E1AF7AA3F40	3
8	E3P5	0103000020E61000000100000005000000BE840A0E2FB81EC0BE6BD097DEAA3F40DBFB54151AB81EC006465ED6C4AA3F40EBE5779ACCB81EC060915F3FC4AA3F404016A243E0B81EC02A560DC2DCAA3F40BE840A0E2FB81EC0BE6BD097DEAA3F40	3
9	E2P6	0103000020E61000000100000007000000EC6CC83F33B81EC0166C239EECAA3F408BFCFA2136B81EC0F86F5E9CF8AA3F40D50451F701B81EC0F86F5E9CF8AA3F407BA35698BEB71EC038F7578FFBAA3F4086E3F90CA8B71EC00BD5CDC5DFAA3F40BE840A0E2FB81EC09A95ED43DEAA3F40EC6CC83F33B81EC0166C239EECAA3F40	3
10	E2P5	0103000020E6100000010000000500000009FCE1E7BFB71EC00F643DB5FAAA3F40DCF126BF45B71EC0E200FA7DFFAA3F401BBAD91F28B71EC0A4A7C821E2AA3F4026732CEFAAB71EC00BD5CDC5DFAA3F4009FCE1E7BFB71EC00F643DB5FAAA3F40	3
11	E2P7	0103000020E6100000010000000500000086E3F90CA8B71EC0E7FEEA71DFAA3F402B137EA99FB71EC01D3A3DEFC6AA3F40DBFB54151AB81EC006465ED6C4AA3F40CFBBB1A030B81EC077BF0AF0DDAA3F4086E3F90CA8B71EC0E7FEEA71DFAA3F40	3
12	E2P4	0103000020E6100000010000000500000026732CEFAAB71EC0E7FEEA71DFAA3F40A912656F29B71EC0FEF2C98AE1AA3F405A828C800AB71EC077853E58C6AA3F40BA6B09F9A0B71EC0A0185932C7AA3F4026732CEFAAB71EC0E7FEEA71DFAA3F40	3
13	E2P3	0103000020E610000001000000050000009DBAF2599EB71EC077853E58C6AA3F40D6E253008CB71EC073F6CE68ABAA3F40EE409DF2E8B61EC073F6CE68ABAA3F405A828C800AB71EC077853E58C6AA3F409DBAF2599EB71EC077853E58C6AA3F40	3
14	E2P2	0103000020E61000000100000005000000D6E253008CB71EC073F6CE68ABAA3F4020425C397BB71EC0DCD6169E97AA3F4088D9CBB6D3B61EC0A661F88898AA3F407C992842EAB61EC04F20EC14ABAA3F40D6E253008CB71EC073F6CE68ABAA3F40	3
15	E2P1	0103000020E6100000010000000600000020425C397BB71EC059F8FA5A97AA3F404293C49272B71EC04A0C022B87AA3F402C9ACE4E06B71EC0994528B682AA3F4093196F2BBDB61EC04DDC2A8881AA3F4088D9CBB6D3B61EC02383DC4598AA3F4020425C397BB71EC059F8FA5A97AA3F40	3
\.


--
-- Data for Name: crop; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.crop (id, "Crop", "Crop_planting_date", "Tree", "Tree_planting_date", field_id_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
2	2025-02-26 21:23:49.188026+00	1	Field object (1)	2	[{"changed": {"fields": ["User"]}}]	7	2
3	2025-02-26 21:24:07.6412+00	15	Field object (15)	3		7	2
4	2025-02-26 21:24:07.642728+00	14	Field object (14)	3		7	2
5	2025-02-26 21:24:07.643764+00	13	Field object (13)	3		7	2
6	2025-02-26 21:24:07.644832+00	12	Field object (12)	3		7	2
7	2025-02-26 21:24:07.645515+00	11	Field object (11)	3		7	2
8	2025-02-26 21:24:07.64625+00	10	Field object (10)	3		7	2
9	2025-02-26 21:24:07.646964+00	9	Field object (9)	3		7	2
10	2025-02-26 21:24:07.647707+00	8	Field object (8)	3		7	2
11	2025-02-26 21:24:07.648383+00	7	Field object (7)	3		7	2
12	2025-02-26 21:24:07.649062+00	6	Field object (6)	3		7	2
13	2025-02-26 21:24:07.649705+00	5	Field object (5)	3		7	2
14	2025-02-26 21:24:07.650385+00	4	Field object (4)	3		7	2
15	2025-02-26 21:24:07.651073+00	3	Field object (3)	3		7	2
16	2025-02-26 21:24:07.651713+00	2	Field object (2)	3		7	2
17	2025-02-26 21:24:07.652373+00	1	Field object (1)	3		7	2
\.


--
-- Data for Name: django_celery_beat_clockedschedule; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_celery_beat_clockedschedule (id, clocked_time) FROM stdin;
\.


--
-- Data for Name: django_celery_beat_crontabschedule; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_celery_beat_crontabschedule (id, minute, hour, day_of_week, day_of_month, month_of_year, timezone) FROM stdin;
\.


--
-- Data for Name: django_celery_beat_intervalschedule; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_celery_beat_intervalschedule (id, every, period) FROM stdin;
\.


--
-- Data for Name: django_celery_beat_solarschedule; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_celery_beat_solarschedule (id, event, latitude, longitude) FROM stdin;
\.


--
-- Data for Name: django_celery_beat_periodictask; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_celery_beat_periodictask (id, name, task, args, kwargs, queue, exchange, routing_key, expires, enabled, last_run_at, total_run_count, date_changed, description, crontab_id, interval_id, solar_id, one_off, start_time, priority, headers, clocked_id, expire_seconds) FROM stdin;
\.


--
-- Data for Name: django_celery_beat_periodictasks; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_celery_beat_periodictasks (ident, last_update) FROM stdin;
\.


--
-- Data for Name: django_celery_results_chordcounter; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_celery_results_chordcounter (id, group_id, sub_tasks, count) FROM stdin;
\.


--
-- Data for Name: django_celery_results_groupresult; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_celery_results_groupresult (id, group_id, date_created, date_done, content_type, content_encoding, result) FROM stdin;
\.


--
-- Data for Name: django_celery_results_taskresult; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_celery_results_taskresult (id, task_id, status, content_type, content_encoding, result, date_done, traceback, meta, task_args, task_kwargs, task_name, worker, date_created, periodic_task_name) FROM stdin;
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2025-02-26 19:45:19.968772+00
2	contenttypes	0002_remove_content_type_name	2025-02-26 19:45:19.972815+00
3	auth	0001_initial	2025-02-26 19:45:19.99577+00
4	auth	0002_alter_permission_name_max_length	2025-02-26 19:45:19.999503+00
5	auth	0003_alter_user_email_max_length	2025-02-26 19:45:20.003476+00
6	auth	0004_alter_user_username_opts	2025-02-26 19:45:20.006455+00
7	auth	0005_alter_user_last_login_null	2025-02-26 19:45:20.009841+00
8	auth	0006_require_contenttypes_0002	2025-02-26 19:45:20.012365+00
9	auth	0007_alter_validators_add_error_messages	2025-02-26 19:45:20.016972+00
10	auth	0008_alter_user_username_max_length	2025-02-26 19:45:20.021158+00
11	auth	0009_alter_user_last_name_max_length	2025-02-26 19:45:20.025454+00
12	auth	0010_alter_group_name_max_length	2025-02-26 19:45:20.029858+00
13	auth	0011_update_proxy_permissions	2025-02-26 19:45:20.035599+00
14	auth	0012_alter_user_first_name_max_length	2025-02-26 19:45:20.039621+00
15	models_only	0001_initial	2025-02-26 19:45:20.324176+00
16	admin	0001_initial	2025-02-26 19:45:20.341337+00
17	admin	0002_logentry_remove_auto_add	2025-02-26 19:45:20.345709+00
18	admin	0003_logentry_add_action_flag_choices	2025-02-26 19:45:20.35264+00
19	django_celery_beat	0001_initial	2025-02-26 19:45:20.37772+00
20	django_celery_beat	0002_auto_20161118_0346	2025-02-26 19:45:20.387985+00
21	django_celery_beat	0003_auto_20161209_0049	2025-02-26 19:45:20.393703+00
22	django_celery_beat	0004_auto_20170221_0000	2025-02-26 19:45:20.396858+00
23	django_celery_beat	0005_add_solarschedule_events_choices	2025-02-26 19:45:20.401113+00
24	django_celery_beat	0006_auto_20180322_0932	2025-02-26 19:45:20.416529+00
25	django_celery_beat	0007_auto_20180521_0826	2025-02-26 19:45:20.424691+00
26	django_celery_beat	0008_auto_20180914_1922	2025-02-26 19:45:20.438174+00
27	django_celery_beat	0006_auto_20180210_1226	2025-02-26 19:45:20.447368+00
28	django_celery_beat	0006_periodictask_priority	2025-02-26 19:45:20.454166+00
29	django_celery_beat	0009_periodictask_headers	2025-02-26 19:45:20.460445+00
30	django_celery_beat	0010_auto_20190429_0326	2025-02-26 19:45:20.536557+00
31	django_celery_beat	0011_auto_20190508_0153	2025-02-26 19:45:20.551506+00
32	django_celery_beat	0012_periodictask_expire_seconds	2025-02-26 19:45:20.558598+00
33	django_celery_beat	0013_auto_20200609_0727	2025-02-26 19:45:20.564198+00
34	django_celery_beat	0014_remove_clockedschedule_enabled	2025-02-26 19:45:20.569452+00
35	django_celery_beat	0015_edit_solarschedule_events_choices	2025-02-26 19:45:20.573175+00
36	django_celery_beat	0016_alter_crontabschedule_timezone	2025-02-26 19:45:20.578231+00
37	django_celery_beat	0017_alter_crontabschedule_month_of_year	2025-02-26 19:45:20.583259+00
38	django_celery_beat	0018_improve_crontab_helptext	2025-02-26 19:45:20.588419+00
39	django_celery_beat	0019_alter_periodictasks_options	2025-02-26 19:45:20.591451+00
40	django_celery_results	0001_initial	2025-02-26 19:45:20.604218+00
41	django_celery_results	0002_add_task_name_args_kwargs	2025-02-26 19:45:20.610722+00
42	django_celery_results	0003_auto_20181106_1101	2025-02-26 19:45:20.613606+00
43	django_celery_results	0004_auto_20190516_0412	2025-02-26 19:45:20.642682+00
44	django_celery_results	0005_taskresult_worker	2025-02-26 19:45:20.650014+00
45	django_celery_results	0006_taskresult_date_created	2025-02-26 19:45:20.668266+00
46	django_celery_results	0007_remove_taskresult_hidden	2025-02-26 19:45:20.671366+00
47	django_celery_results	0008_chordcounter	2025-02-26 19:45:20.6794+00
48	django_celery_results	0009_groupresult	2025-02-26 19:45:20.732736+00
49	django_celery_results	0010_remove_duplicate_indices	2025-02-26 19:45:20.73729+00
50	django_celery_results	0011_taskresult_periodic_task_name	2025-02-26 19:45:20.739478+00
51	models_only	0002_alter_field_table_alter_user_table	2025-02-26 19:45:20.752072+00
52	models_only	0003_alter_crop_table	2025-02-26 19:45:20.762481+00
53	sessions	0001_initial	2025-02-26 19:45:20.773259+00
54	models_only	0004_rename_user_id_field_user	2025-02-26 21:04:09.560449+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.django_session (session_key, session_data, expire_date) FROM stdin;
ctmzkhxtm3jlmjeaca10xsgz2ps470lo	.eJxVjDsOwjAQBe_iGln-xD9Kes5g7XptHEC2FCcV4u4QKQW0b2bei0XY1hq3kZc4EzszxU6_G0J65LYDukO7dZ56W5cZ-a7wgw5-7ZSfl8P9O6gw6re2XtmsEIWSxSfwQYAmmYrTqGGaIBhNBoyjIgORcs4WSNLIYrPNQiN7fwDmqTgr:1tnNNL:eEnRiCPp5BNiwcIO1hCtKDKNjklwFJxAKcUXoCByuo8	2025-03-12 19:47:23.591503+00
\.


--
-- Data for Name: models_only_aquacrop_output; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_aquacrop_output (id, date, "IrrDay", "Tr", "DeepPerc", "Es", "Th1", "Th2", th3, gdd_cum, canopy_cover, biomass, z_root, "DryYield", "FreshYield", harvest_index, "ET", field_id_id) FROM stdin;
\.


--
-- Data for Name: models_only_irrigation_system; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_irrigation_system (id, irrigation_type, instalation_date, field_id_id) FROM stdin;
46	Drip	\N	1
52	Drip	\N	15
54	Drip	\N	14
55	Drip	\N	13
56	Drip	\N	12
57	Drip	\N	11
58	Drip	\N	10
59	Drip	\N	9
60	Drip	\N	8
61	Drip	\N	7
62	Drip	\N	6
63	Drip	\N	5
64	Drip	\N	4
65	Drip	\N	3
66	Drip	\N	2
\.


--
-- Data for Name: models_only_drip_irrigation; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_drip_irrigation (irrigation_system_ptr_id, "Crop_Tubes_distance", "Crop_Drippers_distance", "Crop_outflow_rate", "Tree_row_distance", "Tree_distance", "Tubes_number_by_tree", drippers_number_by_tree, "Tree_outflow_rate") FROM stdin;
46	0.6	0.4	2	\N	\N	\N	\N	\N
52	0.55	0.2	2	\N	\N	\N	\N	\N
54	0.6	0.4	2	\N	\N	\N	\N	\N
55	0.55	0.2	2	\N	\N	\N	\N	\N
56	0.6	0.4	2	\N	\N	\N	\N	\N
57	0.6	0.4	2	\N	\N	\N	\N	\N
58	0.6	0.4	2	\N	\N	\N	\N	\N
59	0.6	0.4	2	\N	\N	\N	\N	\N
60	0.6	0.4	2	\N	\N	\N	\N	\N
61	0.6	0.4	2	\N	\N	\N	\N	\N
62	0.6	0.4	2	\N	\N	\N	\N	\N
63	0.6	0.4	2	\N	\N	\N	\N	\N
64	0.6	0.4	2	\N	\N	\N	\N	\N
65	0.6	0.4	2	\N	\N	\N	\N	\N
66	0.6	0.4	2	\N	\N	\N	\N	\N
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

COPY public.models_only_irrigation_amount (id, amount, date, amount_type, irrigation_system_id_id) FROM stdin;
2450	0	2024-12-17	m³	64
2460	0	2024-12-27	m³	64
2470	0.416413547	2025-01-06	m³	64
2480	0	2025-01-16	m³	64
2490	0	2025-01-26	m³	64
2500	0	2025-02-05	m³	64
2510	0	2025-02-15	m³	64
2520	0	2024-12-25	m³	65
2530	0	2025-01-04	m³	65
1113	0	2024-12-16	m³	65
2540	0	2025-01-14	m³	65
2550	0	2025-01-24	m³	65
2560	0	2025-02-03	m³	65
2570	0	2025-02-13	m³	65
2580	14.66826516	2024-12-23	m³	60
2590	0	2025-01-02	m³	60
2600	0	2025-01-12	m³	60
2610	0	2025-01-22	m³	60
2620	0	2025-02-01	m³	60
2630	7.366728726	2025-02-11	m³	60
2640	0	2024-12-21	m³	46
2650	0	2024-12-31	m³	46
2660	0	2025-01-10	m³	46
2670	0	2025-01-20	m³	46
2680	0	2025-01-30	m³	46
2690	0	2025-02-09	m³	46
2700	0	2024-12-19	m³	66
2710	0	2024-12-29	m³	66
2720	0	2025-01-08	m³	66
2730	5.015526832	2025-01-18	m³	66
2740	9.103749711	2025-01-28	m³	66
2750	0	2025-02-07	m³	66
2760	0	2024-12-17	m³	63
2770	0	2024-12-27	m³	63
2780	0	2025-01-06	m³	63
2790	0	2025-01-16	m³	63
2800	14.26548966	2025-01-26	m³	63
2810	0	2025-02-05	m³	63
2820	0	2025-02-15	m³	63
2830	22.25614736	2024-12-25	m³	61
2840	10.38029471	2025-01-04	m³	61
2850	0	2025-01-14	m³	61
2860	0	2025-01-24	m³	61
2870	0	2025-02-03	m³	61
2880	0	2025-02-13	m³	61
2890	0	2024-12-23	m³	62
2900	0	2025-01-02	m³	62
2910	0	2025-01-12	m³	62
2920	0	2025-01-22	m³	62
2930	0	2025-02-01	m³	62
2940	0	2025-02-11	m³	62
2950	0	2024-12-21	m³	56
2960	0	2024-12-31	m³	56
2970	0	2025-01-10	m³	56
2980	0	2025-01-20	m³	56
2990	0	2025-01-30	m³	56
3000	4.756886228	2025-02-09	m³	56
3010	0	2024-12-19	m³	58
3020	0.03697281	2024-12-29	m³	58
3030	0	2025-01-08	m³	58
3040	0	2025-01-18	m³	58
3050	0	2025-01-28	m³	58
1269	0	2024-12-16	m³	63
3060	0	2025-02-07	m³	58
3070	0	2024-12-17	m³	57
3080	14.21862887	2024-12-27	m³	57
3090	0.774577155	2025-01-06	m³	57
3100	3.978409483	2025-01-16	m³	57
3110	7.862206743	2025-01-26	m³	57
3120	0	2025-02-05	m³	57
3130	0	2025-02-15	m³	57
3140	6.927204775	2024-12-25	m³	59
3150	0	2025-01-04	m³	59
3160	0	2025-01-14	m³	59
3170	0	2025-01-24	m³	59
3180	0	2025-02-03	m³	59
3190	6.368923049	2025-02-13	m³	59
3200	0	2024-12-23	m³	52
3210	0	2025-01-02	m³	52
3220	0	2025-01-12	m³	52
3230	0	2025-01-22	m³	52
3240	0	2025-02-01	m³	52
3250	0	2025-02-11	m³	52
3260	0	2024-12-21	m³	54
3270	0	2024-12-31	m³	54
3280	0	2025-01-10	m³	54
3290	0	2025-01-20	m³	54
3300	0	2025-01-30	m³	54
3310	10.38	2025-02-09	m³	54
3320	0	2024-12-19	m³	55
3330	0	2024-12-29	m³	55
3340	0	2025-01-08	m³	55
3350	0	2025-01-18	m³	55
3360	0	2025-01-28	m³	55
3370	0	2025-02-07	m³	55
1074	0	2024-12-16	m³	64
2451	0	2024-12-18	m³	64
2461	0	2024-12-28	m³	64
2471	0	2025-01-07	m³	64
2481	0	2025-01-17	m³	64
2491	0	2025-01-27	m³	64
2501	0	2025-02-06	m³	64
2511	0	2025-02-16	m³	64
2521	0	2024-12-26	m³	65
2531	5.703798882	2025-01-05	m³	65
2541	0	2025-01-15	m³	65
2551	0	2025-01-25	m³	65
2561	0	2025-02-04	m³	65
2571	0	2025-02-14	m³	65
2581	19.73268744	2024-12-24	m³	60
2591	0	2025-01-03	m³	60
2601	0	2025-01-13	m³	60
2611	0	2025-01-23	m³	60
2621	0	2025-02-02	m³	60
2631	0	2025-02-12	m³	60
2641	0	2024-12-22	m³	46
2651	0	2025-01-01	m³	46
2661	0	2025-01-11	m³	46
2671	0	2025-01-21	m³	46
2681	0	2025-01-31	m³	46
2691	5.411187375	2025-02-10	m³	46
2701	0	2024-12-20	m³	66
2711	0	2024-12-30	m³	66
2721	0	2025-01-09	m³	66
2731	0	2025-01-19	m³	66
2741	0	2025-01-29	m³	66
2751	0	2025-02-08	m³	66
2761	0	2024-12-18	m³	63
2771	1.507221185	2024-12-28	m³	63
2781	0	2025-01-07	m³	63
2791	10.51035573	2025-01-17	m³	63
2801	0	2025-01-27	m³	63
2811	0	2025-02-06	m³	63
2821	0	2025-02-16	m³	63
1230	0	2024-12-16	m³	66
2831	0	2024-12-26	m³	61
2841	0	2025-01-05	m³	61
2851	0	2025-01-15	m³	61
2861	0	2025-01-25	m³	61
2871	0	2025-02-04	m³	61
2881	0	2025-02-14	m³	61
2891	0	2024-12-24	m³	62
2901	0	2025-01-03	m³	62
2911	0	2025-01-13	m³	62
2921	0	2025-01-23	m³	62
2931	0	2025-02-02	m³	62
2941	11.25120536	2025-02-12	m³	62
2951	0	2024-12-22	m³	56
2961	0	2025-01-01	m³	56
2971	0	2025-01-11	m³	56
2981	0	2025-01-21	m³	56
2991	0	2025-01-31	m³	56
3001	0	2025-02-10	m³	56
3011	0	2024-12-20	m³	58
3021	0	2024-12-30	m³	58
3031	0	2025-01-09	m³	58
3041	0	2025-01-19	m³	58
3051	0	2025-01-29	m³	58
3061	0	2025-02-08	m³	58
3071	0	2024-12-18	m³	57
3081	0	2024-12-28	m³	57
3091	0	2025-01-07	m³	57
3101	0	2025-01-17	m³	57
3111	0	2025-01-27	m³	57
3121	0	2025-02-06	m³	57
3131	0	2025-02-16	m³	57
3141	8.535507283	2024-12-26	m³	59
3151	2.604750802	2025-01-05	m³	59
3161	0	2025-01-15	m³	59
3171	0	2025-01-25	m³	59
3181	0	2025-02-04	m³	59
3191	0	2025-02-14	m³	59
3201	0	2024-12-24	m³	52
1386	0	2024-12-16	m³	56
3211	0	2025-01-03	m³	52
3221	0	2025-01-13	m³	52
3231	0	2025-01-23	m³	52
3241	0	2025-02-02	m³	52
3251	24.04743601	2025-02-12	m³	52
3261	0	2024-12-22	m³	54
3271	0	2025-01-01	m³	54
3281	0	2025-01-11	m³	54
3291	0	2025-01-21	m³	54
3301	0	2025-01-31	m³	54
3311	0	2025-02-10	m³	54
3321	0	2024-12-20	m³	55
3331	0	2024-12-30	m³	55
3341	0	2025-01-09	m³	55
3351	0	2025-01-19	m³	55
3361	0	2025-01-29	m³	55
3371	0	2025-02-08	m³	55
2452	0	2024-12-19	m³	64
2462	0	2024-12-29	m³	64
2472	0	2025-01-08	m³	64
2482	12.84728805	2025-01-18	m³	64
2492	9.619009834	2025-01-28	m³	64
2502	0	2025-02-07	m³	64
2512	0	2024-12-17	m³	65
2522	14.4445449	2024-12-27	m³	65
2532	0	2025-01-06	m³	65
2542	0	2025-01-16	m³	65
2552	0	2025-01-26	m³	65
2562	0	2025-02-05	m³	65
2572	0	2025-02-15	m³	65
2582	0.081422453	2024-12-25	m³	60
2592	0	2025-01-04	m³	60
2602	0	2025-01-14	m³	60
2612	0	2025-01-24	m³	60
2622	0	2025-02-03	m³	60
2632	0	2025-02-13	m³	60
2642	17.68372754	2024-12-23	m³	46
2652	0	2025-01-02	m³	46
2662	0	2025-01-12	m³	46
2672	0	2025-01-22	m³	46
2682	0	2025-02-01	m³	46
2692	9.41030684	2025-02-11	m³	46
2702	0	2024-12-21	m³	66
2712	0	2024-12-31	m³	66
2722	0	2025-01-10	m³	66
2732	0	2025-01-20	m³	66
1191	0	2024-12-16	m³	46
2742	0	2025-01-30	m³	66
2752	0	2025-02-09	m³	66
2762	0	2024-12-19	m³	63
2772	0	2024-12-29	m³	63
2782	0	2025-01-08	m³	63
2792	1.620621636	2025-01-18	m³	63
2802	0	2025-01-28	m³	63
2812	0	2025-02-07	m³	63
2822	0	2024-12-17	m³	61
2832	0	2024-12-27	m³	61
2842	0	2025-01-06	m³	61
2852	0	2025-01-16	m³	61
2862	8.136518831	2025-01-26	m³	61
2872	0	2025-02-05	m³	61
2882	0	2025-02-15	m³	61
2892	32.6012182	2024-12-25	m³	62
2902	13.357467	2025-01-04	m³	62
2912	0	2025-01-14	m³	62
2922	0	2025-01-24	m³	62
2932	0	2025-02-03	m³	62
2942	0	2025-02-13	m³	62
2952	0	2024-12-23	m³	56
2962	0	2025-01-02	m³	56
2972	0	2025-01-12	m³	56
2982	0	2025-01-22	m³	56
2992	0	2025-02-01	m³	56
3002	0	2025-02-11	m³	56
3012	0	2024-12-21	m³	58
3022	0	2024-12-31	m³	58
3032	0	2025-01-10	m³	58
3042	0	2025-01-20	m³	58
3052	0	2025-01-30	m³	58
3062	4.503904485	2025-02-09	m³	58
3072	0	2024-12-19	m³	57
3082	0	2024-12-29	m³	57
3092	0	2025-01-08	m³	57
3102	0	2025-01-18	m³	57
3112	0	2025-01-28	m³	57
1347	0	2024-12-16	m³	62
3122	0	2025-02-07	m³	57
3132	0	2024-12-17	m³	59
3142	14.5130692	2024-12-27	m³	59
3152	0.790617152	2025-01-06	m³	59
3162	4.060794658	2025-01-16	m³	59
3172	8.025017857	2025-01-26	m³	59
3182	0	2025-02-05	m³	59
3192	0	2025-02-15	m³	59
3202	0	2024-12-25	m³	52
3212	19.67517491	2025-01-04	m³	52
3222	0	2025-01-14	m³	52
3232	0	2025-01-24	m³	52
3242	0	2025-02-03	m³	52
3252	0	2025-02-13	m³	52
3262	0	2024-12-23	m³	54
3272	0	2025-01-02	m³	54
3282	0	2025-01-12	m³	54
3292	0	2025-01-22	m³	54
3302	0	2025-02-01	m³	54
3312	0	2025-02-11	m³	54
3322	0	2024-12-21	m³	55
3332	0	2024-12-31	m³	55
3342	0	2025-01-10	m³	55
3352	0	2025-01-20	m³	55
3362	0	2025-01-30	m³	55
3372	13.09	2025-02-09	m³	55
2453	0	2024-12-20	m³	64
2463	0	2024-12-30	m³	64
2473	0	2025-01-09	m³	64
2483	0	2025-01-19	m³	64
2493	0	2025-01-29	m³	64
2503	0	2025-02-08	m³	64
2513	0	2024-12-18	m³	65
2523	0	2024-12-28	m³	65
2533	0	2025-01-07	m³	65
2543	0	2025-01-17	m³	65
2553	0	2025-01-27	m³	65
2563	0	2025-02-06	m³	65
2573	0	2025-02-16	m³	65
2583	0	2024-12-26	m³	60
2593	12.03381758	2025-01-05	m³	60
2603	0	2025-01-15	m³	60
2613	0	2025-01-25	m³	60
2623	0	2025-02-04	m³	60
2633	0	2025-02-14	m³	60
2643	0	2024-12-24	m³	46
2653	0	2025-01-03	m³	46
2663	0	2025-01-13	m³	46
2673	0	2025-01-23	m³	46
2683	0	2025-02-02	m³	46
1152	0	2024-12-16	m³	60
2693	0	2025-02-12	m³	46
2703	4.131177013	2024-12-22	m³	66
2713	0	2025-01-01	m³	66
2723	0	2025-01-11	m³	66
2733	0	2025-01-21	m³	66
2743	0	2025-01-31	m³	66
2753	4.549348142	2025-02-10	m³	66
2763	0	2024-12-20	m³	63
2773	0	2024-12-30	m³	63
2783	0	2025-01-09	m³	63
2793	0	2025-01-19	m³	63
2803	0	2025-01-29	m³	63
2813	0	2025-02-08	m³	63
2823	0	2024-12-18	m³	61
2833	1.668039035	2024-12-28	m³	61
2843	0.070233223	2025-01-07	m³	61
2853	5.324848821	2025-01-17	m³	61
2863	0	2025-01-27	m³	61
2873	0	2025-02-06	m³	61
2883	0	2025-02-16	m³	61
2893	0	2024-12-26	m³	62
2903	0	2025-01-05	m³	62
2913	0	2025-01-15	m³	62
2923	0	2025-01-25	m³	62
2933	0	2025-02-04	m³	62
2943	0	2025-02-14	m³	62
2953	0	2024-12-24	m³	56
2963	0	2025-01-03	m³	56
2973	0	2025-01-13	m³	56
2983	0	2025-01-23	m³	56
2993	0	2025-02-02	m³	56
3003	17.81375468	2025-02-12	m³	56
3013	0	2024-12-22	m³	58
3023	0	2025-01-01	m³	58
3033	0	2025-01-11	m³	58
3043	0	2025-01-21	m³	58
3053	0	2025-01-31	m³	58
3063	0	2025-02-10	m³	58
1308	0	2024-12-16	m³	61
3073	0	2024-12-20	m³	57
3083	0	2024-12-30	m³	57
3093	0	2025-01-09	m³	57
3103	0	2025-01-19	m³	57
3113	0	2025-01-29	m³	57
3123	0	2025-02-08	m³	57
3133	0	2024-12-18	m³	59
3143	0	2024-12-28	m³	59
3153	0	2025-01-07	m³	59
3163	0	2025-01-17	m³	59
3173	0	2025-01-27	m³	59
3183	0	2025-02-06	m³	59
3193	0	2025-02-16	m³	59
3203	0	2024-12-26	m³	52
3213	0	2025-01-05	m³	52
3223	0	2025-01-15	m³	52
3233	26.23356655	2025-01-25	m³	52
3243	0	2025-02-04	m³	52
3253	0	2025-02-14	m³	52
3263	0	2024-12-24	m³	54
3273	0	2025-01-03	m³	54
3283	0	2025-01-13	m³	54
3293	0	2025-01-23	m³	54
3303	0	2025-02-02	m³	54
3313	43.25	2025-02-12	m³	54
3323	0	2024-12-22	m³	55
3333	0	2025-01-01	m³	55
3343	0	2025-01-11	m³	55
3353	0	2025-01-21	m³	55
3363	0	2025-01-31	m³	55
3373	0	2025-02-10	m³	55
2454	0	2024-12-21	m³	64
2464	0	2024-12-31	m³	64
2474	0	2025-01-10	m³	64
2484	0	2025-01-20	m³	64
2494	0	2025-01-30	m³	64
2504	0	2025-02-09	m³	64
2514	0	2024-12-19	m³	65
2524	0	2024-12-29	m³	65
2534	0	2025-01-08	m³	65
2544	6.364654144	2025-01-18	m³	65
2554	13.42948875	2025-01-28	m³	65
2564	0	2025-02-07	m³	65
2574	0	2024-12-17	m³	60
2584	0	2024-12-27	m³	60
2594	0	2025-01-06	m³	60
2604	0	2025-01-16	m³	60
2614	0	2025-01-26	m³	60
2624	0	2025-02-05	m³	60
2634	0	2025-02-15	m³	60
2644	0	2024-12-25	m³	46
2654	1.494152744	2025-01-04	m³	46
2664	0	2025-01-14	m³	46
2674	0	2025-01-24	m³	46
2684	0	2025-02-03	m³	46
2694	0	2025-02-13	m³	46
2704	22.29951237	2024-12-23	m³	66
2714	0	2025-01-02	m³	66
2724	0	2025-01-12	m³	66
2734	0	2025-01-22	m³	66
2744	0	2025-02-01	m³	66
2754	8.152441978	2025-02-11	m³	66
2764	0	2024-12-21	m³	63
2774	0	2024-12-31	m³	63
2784	0	2025-01-10	m³	63
2794	0	2025-01-20	m³	63
2804	0.086126925	2025-01-30	m³	63
2814	0	2025-02-09	m³	63
2824	0	2024-12-19	m³	61
2834	0.456515946	2024-12-29	m³	61
2844	0	2025-01-08	m³	61
2854	0	2025-01-18	m³	61
2864	0	2025-01-28	m³	61
2874	0	2025-02-07	m³	61
2884	0	2024-12-17	m³	62
2894	0	2024-12-27	m³	62
2904	0	2025-01-06	m³	62
2914	0	2025-01-16	m³	62
2924	10.21775923	2025-01-26	m³	62
2934	0	2025-02-05	m³	62
2944	0	2025-02-15	m³	62
2954	0.039049552	2024-12-25	m³	56
2964	0	2025-01-04	m³	56
2974	0	2025-01-14	m³	56
2984	0	2025-01-24	m³	56
2994	0	2025-02-03	m³	56
3004	0	2025-02-13	m³	56
3014	0	2024-12-23	m³	58
3024	0	2025-01-02	m³	58
3034	0	2025-01-12	m³	58
3044	0	2025-01-22	m³	58
3054	0	2025-02-01	m³	58
3064	0	2025-02-11	m³	58
3074	0	2024-12-21	m³	57
3084	0	2024-12-31	m³	57
3094	0	2025-01-10	m³	57
3104	0	2025-01-20	m³	57
3114	0	2025-01-30	m³	57
3124	3.954100357	2025-02-09	m³	57
3134	0	2024-12-19	m³	59
3144	0	2024-12-29	m³	59
3154	0	2025-01-08	m³	59
3164	0	2025-01-18	m³	59
3174	0	2025-01-28	m³	59
3184	0	2025-02-07	m³	59
3194	0	2024-12-17	m³	52
3204	0	2024-12-27	m³	52
3214	0	2025-01-06	m³	52
3224	13.11678328	2025-01-16	m³	52
3234	0	2025-01-26	m³	52
3244	0	2025-02-05	m³	52
3254	0	2025-02-15	m³	52
3264	0	2024-12-25	m³	54
3274	15.57	2025-01-04	m³	54
3284	0	2025-01-14	m³	54
3294	0	2025-01-24	m³	54
3304	0	2025-02-03	m³	54
3314	0	2025-02-13	m³	54
3324	0	2024-12-23	m³	55
3334	0	2025-01-02	m³	55
3344	0	2025-01-12	m³	55
3354	0	2025-01-22	m³	55
3364	0	2025-02-01	m³	55
3374	0	2025-02-11	m³	55
2455	10.11985087	2024-12-22	m³	64
2465	0	2025-01-01	m³	64
2475	0	2025-01-11	m³	64
2485	0	2025-01-21	m³	64
2495	0	2025-01-31	m³	64
2505	5.16295559	2025-02-10	m³	64
2515	0	2024-12-20	m³	65
2525	0	2024-12-30	m³	65
2535	0	2025-01-09	m³	65
2545	0	2025-01-19	m³	65
2555	0	2025-01-29	m³	65
2565	0	2025-02-08	m³	65
2575	0	2024-12-18	m³	60
2585	1.211490048	2024-12-28	m³	60
2595	0.081490362	2025-01-07	m³	60
2605	20.02625647	2025-01-17	m³	60
2615	0	2025-01-27	m³	60
2625	0	2025-02-06	m³	60
2635	0	2025-02-16	m³	60
2645	0	2024-12-26	m³	46
2655	6.17857993	2025-01-05	m³	46
2665	0	2025-01-15	m³	46
2675	0	2025-01-25	m³	46
2685	0	2025-02-04	m³	46
2695	0	2025-02-14	m³	46
2705	0	2024-12-24	m³	66
2715	0	2025-01-03	m³	66
2725	0.075801413	2025-01-13	m³	66
2735	0	2025-01-23	m³	66
2745	0	2025-02-02	m³	66
2755	0	2025-02-12	m³	66
2765	0	2024-12-22	m³	63
2775	0	2025-01-01	m³	63
2785	0	2025-01-11	m³	63
2795	0	2025-01-21	m³	63
2805	0	2025-01-31	m³	63
2815	5.30828947	2025-02-10	m³	63
2825	0	2024-12-20	m³	61
2835	0.888450265	2024-12-30	m³	61
2845	13.84296816	2025-01-09	m³	61
2855	0	2025-01-19	m³	61
2865	0	2025-01-29	m³	61
2875	0	2025-02-08	m³	61
2885	0	2024-12-18	m³	62
2895	1.476351615	2024-12-28	m³	62
2905	0	2025-01-07	m³	62
2915	12.23122163	2025-01-17	m³	62
2925	0	2025-01-27	m³	62
2935	0	2025-02-06	m³	62
2945	0	2025-02-16	m³	62
2955	11.23650851	2024-12-26	m³	56
2965	4.979468673	2025-01-05	m³	56
2975	0	2025-01-15	m³	56
2985	11.21685357	2025-01-25	m³	56
2995	0	2025-02-04	m³	56
3005	0	2025-02-14	m³	56
3015	0	2024-12-24	m³	58
3025	0	2025-01-03	m³	58
3035	0	2025-01-13	m³	58
3045	0	2025-01-23	m³	58
3055	0	2025-02-02	m³	58
3065	16.86637976	2025-02-12	m³	58
3075	0	2024-12-22	m³	57
3085	0	2025-01-01	m³	57
3095	0	2025-01-11	m³	57
3105	0	2025-01-21	m³	57
3115	0	2025-01-31	m³	57
3125	0	2025-02-10	m³	57
3135	0	2024-12-20	m³	59
3145	0	2024-12-30	m³	59
3155	0	2025-01-09	m³	59
3165	0	2025-01-19	m³	59
3175	0	2025-01-29	m³	59
3185	0	2025-02-08	m³	59
3195	0	2024-12-18	m³	52
3205	19.67517491	2024-12-28	m³	52
3215	0	2025-01-07	m³	52
3225	0	2025-01-17	m³	52
3235	0	2025-01-27	m³	52
3245	0	2025-02-06	m³	52
3255	0	2025-02-16	m³	52
3265	0	2024-12-26	m³	54
3275	0	2025-01-05	m³	54
3285	0	2025-01-15	m³	54
3295	20.76	2025-01-25	m³	54
3305	0	2025-02-04	m³	54
3315	0	2025-02-14	m³	54
3325	0	2024-12-24	m³	55
3335	0	2025-01-03	m³	55
3345	0	2025-01-13	m³	55
3355	0	2025-01-23	m³	55
3365	0	2025-02-02	m³	55
3375	36.652	2025-02-12	m³	55
2456	25.94499662	2024-12-23	m³	64
2466	0	2025-01-02	m³	64
2476	0	2025-01-12	m³	64
2486	0	2025-01-22	m³	64
2496	0	2025-02-01	m³	64
2506	5.23164236	2025-02-11	m³	64
2516	0	2024-12-21	m³	65
2526	0	2024-12-31	m³	65
2536	0	2025-01-10	m³	65
2546	0	2025-01-20	m³	65
2556	0	2025-01-30	m³	65
2566	0	2025-02-09	m³	65
2576	0	2024-12-19	m³	60
2586	0	2024-12-29	m³	60
2596	0	2025-01-08	m³	60
2606	0	2025-01-18	m³	60
2616	10.92921572	2025-01-28	m³	60
2626	0	2025-02-07	m³	60
2636	0	2024-12-17	m³	46
2646	0	2024-12-27	m³	46
2656	0	2025-01-06	m³	46
2666	0	2025-01-16	m³	46
2676	0	2025-01-26	m³	46
2686	0	2025-02-05	m³	46
2696	0	2025-02-15	m³	46
2706	0	2024-12-25	m³	66
2716	0.105679804	2025-01-04	m³	66
2726	0.075801413	2025-01-14	m³	66
2736	0	2025-01-24	m³	66
2746	0	2025-02-03	m³	66
2756	0	2025-02-13	m³	66
2766	15.50284648	2024-12-23	m³	63
2776	0	2025-01-02	m³	63
2786	0	2025-01-12	m³	63
2796	0	2025-01-22	m³	63
2806	0	2025-02-01	m³	63
2816	4.834591382	2025-02-11	m³	63
2826	0	2024-12-21	m³	61
2836	0	2024-12-31	m³	61
2846	0	2025-01-10	m³	61
2856	0	2025-01-20	m³	61
2866	0.070233223	2025-01-30	m³	61
2876	7.863779816	2025-02-09	m³	61
2886	0	2024-12-19	m³	62
2896	0	2024-12-29	m³	62
2906	0	2025-01-08	m³	62
2916	0	2025-01-18	m³	62
2926	0	2025-01-28	m³	62
2936	0	2025-02-07	m³	62
2946	0	2024-12-17	m³	56
2956	16.76267091	2024-12-27	m³	56
2966	0	2025-01-06	m³	56
2976	6.696347298	2025-01-16	m³	56
2986	0.418220699	2025-01-26	m³	56
2996	0	2025-02-05	m³	56
3006	0	2025-02-15	m³	56
3016	0.03697281	2024-12-25	m³	58
3026	0	2025-01-04	m³	58
3036	0	2025-01-14	m³	58
3046	0	2025-01-24	m³	58
3056	0	2025-02-03	m³	58
3066	0	2025-02-13	m³	58
3076	0	2024-12-23	m³	57
3086	0	2025-01-02	m³	57
3096	0	2025-01-12	m³	57
3106	0	2025-01-22	m³	57
3116	0	2025-02-01	m³	57
3126	0	2025-02-11	m³	57
3136	0	2024-12-21	m³	59
3146	0	2024-12-31	m³	59
3156	0	2025-01-10	m³	59
3166	0	2025-01-20	m³	59
3176	0	2025-01-30	m³	59
3186	4.035982137	2025-02-09	m³	59
3196	0	2024-12-19	m³	52
3206	0	2024-12-29	m³	52
3216	0	2025-01-08	m³	52
3226	0	2025-01-18	m³	52
3236	0	2025-01-28	m³	52
3246	0	2025-02-07	m³	52
3256	0	2024-12-17	m³	54
3266	0	2024-12-27	m³	54
3276	0	2025-01-06	m³	54
3286	10.38	2025-01-16	m³	54
3296	0	2025-01-26	m³	54
3306	0	2025-02-05	m³	54
3316	0	2025-02-15	m³	54
3326	0	2024-12-25	m³	55
3336	19.635	2025-01-04	m³	55
3346	0	2025-01-14	m³	55
3356	0	2025-01-24	m³	55
3366	0	2025-02-03	m³	55
3376	0	2025-02-13	m³	55
2457	18.92012871	2024-12-24	m³	64
2467	0	2025-01-03	m³	64
2477	0	2025-01-13	m³	64
2487	0	2025-01-23	m³	64
2497	0	2025-02-02	m³	64
2507	0	2025-02-12	m³	64
2517	0	2024-12-22	m³	65
2527	0	2025-01-01	m³	65
2537	0	2025-01-11	m³	65
2547	0	2025-01-21	m³	65
2557	0	2025-01-31	m³	65
2567	4.91085478	2025-02-10	m³	65
2577	0	2024-12-20	m³	60
2587	0	2024-12-30	m³	60
2597	0	2025-01-09	m³	60
1425	0	2024-12-16	m³	58
2607	0	2025-01-19	m³	60
2617	0	2025-01-29	m³	60
2627	0	2025-02-08	m³	60
2637	0	2024-12-18	m³	46
2647	0	2024-12-28	m³	46
2657	0	2025-01-07	m³	46
2667	0	2025-01-17	m³	46
2677	0	2025-01-27	m³	46
2687	0	2025-02-06	m³	46
2697	0	2025-02-16	m³	46
2707	0	2024-12-26	m³	66
2717	7.991553478	2025-01-05	m³	66
2727	0	2025-01-15	m³	66
2737	0	2025-01-25	m³	66
2747	0	2025-02-04	m³	66
2757	0	2025-02-14	m³	66
2767	25.83807746	2024-12-24	m³	63
2777	0	2025-01-03	m³	63
2787	0	2025-01-13	m³	63
2797	0	2025-01-23	m³	63
2807	0	2025-02-02	m³	63
2817	5.404464536	2025-02-12	m³	63
2827	0	2024-12-22	m³	61
2837	0	2025-01-01	m³	61
2847	0	2025-01-11	m³	61
2857	0	2025-01-21	m³	61
2867	0	2025-01-31	m³	61
2877	0.03160495	2025-02-10	m³	61
2887	0	2024-12-20	m³	62
2897	0	2024-12-30	m³	62
2907	9.433183801	2025-01-09	m³	62
2917	0	2025-01-19	m³	62
2927	0	2025-01-29	m³	62
2937	0	2025-02-08	m³	62
2947	0	2024-12-18	m³	56
2957	0	2024-12-28	m³	56
2967	0	2025-01-07	m³	56
2977	0	2025-01-17	m³	56
1464	0	2024-12-16	m³	57
2987	0	2025-01-27	m³	56
2997	0	2025-02-06	m³	56
3007	0	2025-02-16	m³	56
3017	10.63892611	2024-12-26	m³	58
3027	4.714649502	2025-01-05	m³	58
3037	0	2025-01-15	m³	58
3047	10.62031646	2025-01-25	m³	58
3057	0	2025-02-04	m³	58
3067	0	2025-02-14	m³	58
3077	0	2024-12-24	m³	57
3087	0	2025-01-03	m³	57
3097	0	2025-01-13	m³	57
3107	0	2025-01-23	m³	57
3117	0	2025-02-02	m³	57
3127	0.056905454	2025-02-12	m³	57
3137	0	2024-12-22	m³	59
3147	0	2025-01-01	m³	59
3157	0	2025-01-11	m³	59
3167	0	2025-01-21	m³	59
3177	0	2025-01-31	m³	59
3187	0	2025-02-10	m³	59
3197	0	2024-12-20	m³	52
3207	0	2024-12-30	m³	52
3217	0	2025-01-09	m³	52
3227	0	2025-01-19	m³	52
3237	0	2025-01-29	m³	52
3247	0	2025-02-08	m³	52
3257	0	2024-12-18	m³	54
3267	15.57	2024-12-28	m³	54
3277	0	2025-01-07	m³	54
3287	0	2025-01-17	m³	54
3297	0	2025-01-27	m³	54
3307	0	2025-02-06	m³	54
3317	0	2025-02-16	m³	54
3327	0	2024-12-26	m³	55
3337	0	2025-01-05	m³	55
3347	0	2025-01-15	m³	55
3357	26.18	2025-01-25	m³	55
1503	0	2024-12-16	m³	59
3367	0	2025-02-04	m³	55
3377	0	2025-02-14	m³	55
2458	0	2024-12-25	m³	64
2468	0	2025-01-04	m³	64
2478	0	2025-01-14	m³	64
2488	0	2025-01-24	m³	64
2498	0	2025-02-03	m³	64
2508	0	2025-02-13	m³	64
2518	16.40991447	2024-12-23	m³	65
2528	0	2025-01-02	m³	65
2538	0	2025-01-12	m³	65
2548	0	2025-01-22	m³	65
2558	0	2025-02-01	m³	65
2568	9.994356798	2025-02-11	m³	65
1542	0	2024-12-16	m³	52
2578	0	2024-12-21	m³	60
2588	0	2024-12-31	m³	60
2598	0	2025-01-10	m³	60
2608	0	2025-01-20	m³	60
2618	0.162980724	2025-01-30	m³	60
2628	0	2025-02-09	m³	60
2638	0	2024-12-19	m³	46
2648	0	2024-12-29	m³	46
2658	0	2025-01-08	m³	46
2668	7.328736828	2025-01-18	m³	46
2678	11.46354603	2025-01-28	m³	46
2688	0	2025-02-07	m³	46
2698	0	2024-12-17	m³	66
2708	11.08368262	2024-12-27	m³	66
2718	0	2025-01-06	m³	66
2728	0	2025-01-16	m³	66
2738	0	2025-01-26	m³	66
2748	0	2025-02-05	m³	66
2758	0	2025-02-15	m³	66
2768	0	2024-12-25	m³	63
2778	0.225365454	2025-01-04	m³	63
2788	0	2025-01-14	m³	63
2798	0	2025-01-24	m³	63
2808	0	2025-02-03	m³	63
2818	0	2025-02-13	m³	63
2828	0	2024-12-23	m³	61
2838	0	2025-01-02	m³	61
2848	0	2025-01-12	m³	61
2858	0	2025-01-22	m³	61
2868	0	2025-02-01	m³	61
2878	0	2025-02-11	m³	61
2888	0	2024-12-21	m³	62
2898	0	2024-12-31	m³	62
2908	0	2025-01-10	m³	62
2918	0	2025-01-20	m³	62
2928	0	2025-01-30	m³	62
2938	0	2025-02-09	m³	62
2948	0	2024-12-19	m³	56
1581	0	2024-12-16	m³	54
2958	0.039049552	2024-12-29	m³	56
2968	0	2025-01-08	m³	56
2978	0	2025-01-18	m³	56
2988	0	2025-01-28	m³	56
2998	0	2025-02-07	m³	56
3008	0	2024-12-17	m³	58
3018	15.87119495	2024-12-27	m³	58
3028	0	2025-01-06	m³	58
3038	6.34022072	2025-01-16	m³	58
3048	0.395978796	2025-01-26	m³	58
3058	0	2025-02-05	m³	58
3068	0	2025-02-15	m³	58
3078	6.786666032	2024-12-25	m³	57
3088	0	2025-01-04	m³	57
3098	0	2025-01-14	m³	57
3108	0	2025-01-24	m³	57
3118	0	2025-02-03	m³	57
3128	6.239710694	2025-02-13	m³	57
3138	0	2024-12-23	m³	59
3148	0	2025-01-02	m³	59
3158	0	2025-01-12	m³	59
3168	0	2025-01-22	m³	59
3178	0	2025-02-01	m³	59
3188	0	2025-02-11	m³	59
3198	0	2024-12-21	m³	52
3208	0	2024-12-31	m³	52
3218	0	2025-01-10	m³	52
3228	0	2025-01-20	m³	52
3238	0	2025-01-30	m³	52
3248	13.11678328	2025-02-09	m³	52
3258	0	2024-12-19	m³	54
3268	0	2024-12-29	m³	54
3278	0	2025-01-08	m³	54
3288	0	2025-01-18	m³	54
3298	0	2025-01-28	m³	54
3308	0	2025-02-07	m³	54
3318	0	2024-12-17	m³	55
3328	0	2024-12-27	m³	55
1620	0	2024-12-16	m³	55
3338	0	2025-01-06	m³	55
3348	13.09	2025-01-16	m³	55
3358	0	2025-01-26	m³	55
3368	0	2025-02-05	m³	55
3378	0	2025-02-15	m³	55
2459	0	2024-12-26	m³	64
2469	12.87769626	2025-01-05	m³	64
2479	0	2025-01-15	m³	64
2489	0	2025-01-25	m³	64
2499	0	2025-02-04	m³	64
2509	0	2025-02-14	m³	64
2519	19.42418453	2024-12-24	m³	65
2529	0	2025-01-03	m³	65
2539	0	2025-01-13	m³	65
2549	0	2025-01-23	m³	65
2559	0	2025-02-02	m³	65
2569	0	2025-02-12	m³	65
2579	0	2024-12-22	m³	60
2589	0	2025-01-01	m³	60
2599	0	2025-01-11	m³	60
2609	0	2025-01-21	m³	60
2619	0	2025-01-31	m³	60
2629	4.696561197	2025-02-10	m³	60
2639	22.10251597	2024-12-20	m³	46
2649	0	2024-12-30	m³	46
2659	0	2025-01-09	m³	46
2669	0	2025-01-19	m³	46
2679	0	2025-01-29	m³	46
2689	0	2025-02-08	m³	46
2699	0	2024-12-18	m³	66
2709	1.799651883	2024-12-28	m³	66
2719	0	2025-01-07	m³	66
2729	0	2025-01-17	m³	66
2739	0	2025-01-27	m³	66
2749	0	2025-02-06	m³	66
2759	0	2025-02-16	m³	66
2769	0	2024-12-26	m³	63
2779	5.543200658	2025-01-05	m³	63
2789	0	2025-01-15	m³	63
2799	0	2025-01-25	m³	63
2809	0	2025-02-04	m³	63
2819	0	2025-02-14	m³	63
2829	0	2024-12-24	m³	61
2839	0	2025-01-03	m³	61
2849	0	2025-01-13	m³	61
2859	0	2025-01-23	m³	61
2869	0	2025-02-02	m³	61
2879	6.957771246	2025-02-12	m³	61
2889	0	2024-12-22	m³	62
2899	0	2025-01-01	m³	62
2909	0	2025-01-11	m³	62
2919	0	2025-01-21	m³	62
2929	0	2025-01-31	m³	62
2939	5.698717238	2025-02-10	m³	62
2949	0	2024-12-20	m³	56
2959	0	2024-12-30	m³	56
2969	0	2025-01-09	m³	56
2979	0	2025-01-19	m³	56
2989	0	2025-01-29	m³	56
2999	0	2025-02-08	m³	56
3009	0	2024-12-18	m³	58
3019	0	2024-12-28	m³	58
3029	0	2025-01-07	m³	58
3039	0	2025-01-17	m³	58
3049	0	2025-01-27	m³	58
3059	0	2025-02-06	m³	58
3069	0	2025-02-16	m³	58
3079	8.362339388	2024-12-26	m³	57
3089	2.551905764	2025-01-05	m³	57
3099	0	2025-01-15	m³	57
3109	0	2025-01-25	m³	57
3119	0	2025-02-04	m³	57
3129	0	2025-02-14	m³	57
3139	0	2024-12-24	m³	59
3149	0	2025-01-03	m³	59
3159	0	2025-01-13	m³	59
3169	0	2025-01-23	m³	59
3179	0	2025-02-02	m³	59
3189	0.058083856	2025-02-12	m³	59
3199	0	2024-12-22	m³	52
3209	0	2025-01-01	m³	52
3219	0	2025-01-11	m³	52
3229	0	2025-01-21	m³	52
3239	0	2025-01-31	m³	52
3249	0	2025-02-10	m³	52
3259	0	2024-12-20	m³	54
3269	0	2024-12-30	m³	54
3279	0	2025-01-09	m³	54
3289	0	2025-01-19	m³	54
3299	0	2025-01-29	m³	54
3309	0	2025-02-08	m³	54
3319	0	2024-12-18	m³	55
3329	19.635	2024-12-28	m³	55
3339	0	2025-01-07	m³	55
3349	0	2025-01-17	m³	55
3359	0	2025-01-27	m³	55
3369	0	2025-02-06	m³	55
3379	0	2025-02-16	m³	55
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
-- Data for Name: models_only_remote_sensing; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_remote_sensing (id, datetime, path, "RS_type", source, field_id_id) FROM stdin;
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
-- Data for Name: spatial_ref_sys; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.spatial_ref_sys (srid, auth_name, auth_srid, srtext, proj4text) FROM stdin;
\.


--
-- Data for Name: user_groups; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.user_groups (id, user_id, group_id) FROM stdin;
2	2	1
3	3	2
\.


--
-- Data for Name: user_user_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: geocode_settings; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.geocode_settings (name, setting, unit, category, short_desc) FROM stdin;
\.


--
-- Data for Name: pagc_gaz; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.pagc_gaz (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_lex; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.pagc_lex (id, seq, word, stdword, token, is_custom) FROM stdin;
\.


--
-- Data for Name: pagc_rules; Type: TABLE DATA; Schema: tiger; Owner: admin
--

COPY tiger.pagc_rules (id, rule, is_custom) FROM stdin;
\.


--
-- Data for Name: topology; Type: TABLE DATA; Schema: topology; Owner: admin
--

COPY topology.topology (id, name, srid, "precision", hasz) FROM stdin;
\.


--
-- Data for Name: layer; Type: TABLE DATA; Schema: topology; Owner: admin
--

COPY topology.layer (topology_id, layer_id, schema_name, table_name, feature_column, feature_type, level, child_id) FROM stdin;
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_id_seq', 2, true);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.auth_permission_id_seq', 148, true);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_admin_log_id_seq', 17, true);


--
-- Name: django_celery_beat_clockedschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_celery_beat_clockedschedule_id_seq', 1, false);


--
-- Name: django_celery_beat_crontabschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_celery_beat_crontabschedule_id_seq', 1, false);


--
-- Name: django_celery_beat_intervalschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_celery_beat_intervalschedule_id_seq', 1, false);


--
-- Name: django_celery_beat_periodictask_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_celery_beat_periodictask_id_seq', 1, false);


--
-- Name: django_celery_beat_solarschedule_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_celery_beat_solarschedule_id_seq', 1, false);


--
-- Name: django_celery_results_chordcounter_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_celery_results_chordcounter_id_seq', 1, false);


--
-- Name: django_celery_results_groupresult_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_celery_results_groupresult_id_seq', 1, false);


--
-- Name: django_celery_results_taskresult_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_celery_results_taskresult_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_content_type_id_seq', 37, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.django_migrations_id_seq', 54, true);


--
-- Name: models_only_aquacrop_output_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_aquacrop_output_id_seq', 1, false);


--
-- Name: models_only_crop_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_crop_id_seq', 1, false);


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
-- Name: models_only_field_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_field_id_seq', 1, false);


--
-- Name: models_only_forcast_weather_date_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_forcast_weather_date_id_seq', 1, false);


--
-- Name: models_only_irrigation_amount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_irrigation_amount_id_seq', 3379, true);


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
-- Name: models_only_remote_sensing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_remote_sensing_id_seq', 1, false);


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

SELECT pg_catalog.setval('public.models_only_soil_id_seq', 1, false);


--
-- Name: models_only_sol_fao_parametre_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_sol_fao_parametre_id_seq', 1, false);


--
-- Name: models_only_station_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_station_id_seq', 1, false);


--
-- Name: models_only_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_user_groups_id_seq', 3, true);


--
-- Name: models_only_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_user_id_seq', 3, true);


--
-- Name: models_only_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_user_user_permissions_id_seq', 1, false);


--
-- Name: models_only_weather_date_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_weather_date_id_seq', 1, false);


--
-- Name: topology_id_seq; Type: SEQUENCE SET; Schema: topology; Owner: admin
--

SELECT pg_catalog.setval('topology.topology_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--


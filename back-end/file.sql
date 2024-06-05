--
-- PostgreSQL database dump
--

-- Dumped from database version 16.2 (Debian 16.2-1.pgdg110+2)
-- Dumped by pg_dump version 16.2 (Debian 16.2-1.pgdg110+2)

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
-- Name: models_only_ogimet_stations; Type: TABLE; Schema: public; Owner: admin
--

CREATE TABLE public.models_only_ogimet_stations (
    id bigint NOT NULL,
    lat text,
    long text,
    location_name text,
    station_id bigint
);


ALTER TABLE public.models_only_ogimet_stations OWNER TO admin;

--
-- Name: models_only_ogimet_stations_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE public.models_only_ogimet_stations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.models_only_ogimet_stations_id_seq OWNER TO admin;

--
-- Name: models_only_ogimet_stations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE public.models_only_ogimet_stations_id_seq OWNED BY public.models_only_ogimet_stations.id;


--
-- Name: models_only_ogimet_stations id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY public.models_only_ogimet_stations ALTER COLUMN id SET DEFAULT nextval('public.models_only_ogimet_stations_id_seq'::regclass);


--
-- Data for Name: models_only_ogimet_stations; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY public.models_only_ogimet_stations (id, lat, long, location_name, station_id) FROM stdin;
1	29.366666666666667	-10.183055555555555	Sidi ifni	60060
2	35.726111111111116	-5.905277777777778	Tanger Aerodrome	60101
3	35.17222222222222	-5.313055555555556	Chefchaouen	60106
4	34.783055555555556	-1.9330555555555553	Oujda	60115
5	34.30027777777777	-6.594444444444444	Kenitra	60120
6	34.39666666666667	-2.8980555555555556	Taourirt	60128
7	34.045833333333334	-6.757777777777778	Rabat-Sale	60135
8	33.9325	-4.974722222222223	Fes-Sais	60141
9	34.22944444444445	-3.943611111111111	Taza Hammou Meftah	60144
10	33.88194444444444	-5.522777777777778	Meknes	60150
11	33.56666666666667	-7.666666666666667	Casablanca	60155
12	33.36666666666667	-7.583055555555555	Nouasseur	60156
13	33.645833333333336	-7.214166666666667	Benslimane	60158
14	33.5	-5.166666666666667	Ifrane	60160
15	33.23305555555556	-8.516666666666667	El Jadida	60165
16	32.86666666666667	-6.966666666666667	Khouribga	60178
17	32.283055555555556	-9.233055555555556	Safi	60185
18	32.683055555555555	-4.733055555555556	Midelt	60195
19	32.56638888888889	-1.7833333333333332	Bouarfa	60200
20	31.93305555555556	-4.4	Errachidia	60210
21	31.616388888888892	-8.033055555555556	Marrakech	60230
22	30.5	-8.816666666666666	Taroudant	60253
23	30.93305555555556	-6.9	Ouarzazate	60265
24	29.68305555555556	-9.733055555555556	Tiznit	60270
25	29.016666666666666	-10.05	Guelmin	60280
26	28.445833333333333	-11.158055555555556	Tan-Tan	60285
27	34.98305555555556	-3.0166666666666666	Nador-Aroui	60340
\.


--
-- Name: models_only_ogimet_stations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('public.models_only_ogimet_stations_id_seq', 27, true);


--
-- PostgreSQL database dump complete
--


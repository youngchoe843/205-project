--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

--
-- Name: plpgsql; Type: PROCEDURAL LANGUAGE; Schema: -; Owner: postgres
--

CREATE PROCEDURAL LANGUAGE plpgsql;


ALTER PROCEDURAL LANGUAGE plpgsql OWNER TO postgres;

SET search_path = public, pg_catalog;

--
-- Name: etl_latency(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION etl_latency() RETURNS interval
    LANGUAGE plpgsql
    AS $$
BEGIN
    RETURN NOW() - MAX(tweet_date + tweet_time)::timestamp AS latency FROM tweettable_fast;
END;
$$;


ALTER FUNCTION public.etl_latency() OWNER TO postgres;

--
-- Name: process_tweettable_fast(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION process_tweettable_fast() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
    BEGIN
        INSERT INTO tweettable_fast SELECT NEW.*;
        RETURN NULL;-- result is ignored since this is an AFTER trigger
    END;
$$;


ALTER FUNCTION public.process_tweettable_fast() OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: approvalratings; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE approvalratings (
    datesource text NOT NULL,
    source text NOT NULL,
    date text NOT NULL,
    rating integer NOT NULL
);


ALTER TABLE public.approvalratings OWNER TO postgres;

--
-- Name: stockhist; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE stockhist (
    tickerdate date NOT NULL,
    symbol character varying(5) NOT NULL,
    price smallint NOT NULL
);


ALTER TABLE public.stockhist OWNER TO postgres;

--
-- Name: topiccount; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE topiccount (
    tweet_date date,
    topic_id text,
    topic_count bigint
);


ALTER TABLE public.topiccount OWNER TO postgres;

--
-- Name: traveltrends; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE traveltrends (
    trend_date date NOT NULL,
    kw0 double precision NOT NULL,
    kw1 double precision NOT NULL,
    kw2 double precision NOT NULL,
    kw3 double precision NOT NULL,
    kw4 double precision NOT NULL
);


ALTER TABLE public.traveltrends OWNER TO postgres;

--
-- Name: tweettable; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tweettable (
    tweet_id bigint NOT NULL,
    tweet_text text NOT NULL,
    tweet_date date NOT NULL,
    tweet_time time without time zone NOT NULL,
    user_id bigint NOT NULL,
    reply_id bigint,
    retweets bigint,
    topic_id text,
    sent_score real NOT NULL
);


ALTER TABLE public.tweettable OWNER TO postgres;

--
-- Name: tweettable_fast; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tweettable_fast (
    tweet_id bigint NOT NULL,
    tweet_text text NOT NULL,
    tweet_date date NOT NULL,
    tweet_time time without time zone NOT NULL,
    user_id bigint NOT NULL,
    reply_id bigint,
    retweets bigint,
    topic_id text,
    sent_score real NOT NULL
);


ALTER TABLE public.tweettable_fast OWNER TO postgres;

--
-- Name: tweettopic; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tweettopic (
    topicname character varying(30) NOT NULL,
    searchphrase character varying(50) NOT NULL
);


ALTER TABLE public.tweettopic OWNER TO postgres;

--
-- Name: approvalratings_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY approvalratings
    ADD CONSTRAINT approvalratings_pkey PRIMARY KEY (datesource);


--
-- Name: stockhist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY stockhist
    ADD CONSTRAINT stockhist_pkey PRIMARY KEY (tickerdate, symbol);


--
-- Name: traveltrends_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY traveltrends
    ADD CONSTRAINT traveltrends_pkey PRIMARY KEY (trend_date);


--
-- Name: tweettable_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY tweettable
    ADD CONSTRAINT tweettable_pkey PRIMARY KEY (tweet_id);


--
-- Name: tweettable_fast; Type: TRIGGER; Schema: public; Owner: postgres
--

CREATE TRIGGER tweettable_fast
    AFTER INSERT ON tweettable
    FOR EACH ROW
    EXECUTE PROCEDURE process_tweettable_fast();


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--
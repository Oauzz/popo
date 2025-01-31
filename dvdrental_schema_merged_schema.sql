

--
-- Name: customer; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.customer (
    customer_id integer DEFAULT nextval('public.customer_customer_id_seq'::regclass) NOT NULL,
    store_id smallint NOT NULL,
    first_name character varying(45) NOT NULL,
    last_name character varying(45) NOT NULL,
    email character varying(50),
    address_id smallint NOT NULL,
    activebool boolean DEFAULT true NOT NULL,
    create_date date DEFAULT ('now'::text)::date NOT NULL,
    last_update timestamp without time zone DEFAULT now(),
    active integer
  ,  CONSTRAINT  customer_pkey  PRIMARY KEY  (customer_id)  ,  CONSTRAINT  customer_address_id_fkey  FOREIGN  KEY  (address_id)  REFERENCES  public.address(address_id)  ON  UPDATE  CASCADE  ON  DELETE  RESTRICT ;);



--
-- Name: actor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.actor (
    actor_id integer DEFAULT nextval('public.actor_actor_id_seq'::regclass) NOT NULL,
    first_name character varying(45) NOT NULL,
    last_name character varying(45) NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
  ,  CONSTRAINT  actor_pkey  PRIMARY KEY  (actor_id) ;);



--
-- Name: category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.category (
    category_id integer DEFAULT nextval('public.category_category_id_seq'::regclass) NOT NULL,
    name character varying(25) NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
  ,  CONSTRAINT  category_pkey  PRIMARY KEY  (category_id) ;);



--
-- Name: film; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.film (
    film_id integer DEFAULT nextval('public.film_film_id_seq'::regclass) NOT NULL,
    title character varying(255) NOT NULL,
    description text,
    release_year public.year,
    language_id smallint NOT NULL,
    rental_duration smallint DEFAULT 3 NOT NULL,
    rental_rate numeric(4,2) DEFAULT 4.99 NOT NULL,
    length smallint,
    replacement_cost numeric(5,2) DEFAULT 19.99 NOT NULL,
    rating public.mpaa_rating DEFAULT 'G'::public.mpaa_rating,
    last_update timestamp without time zone DEFAULT now() NOT NULL,
    special_features text[],
    fulltext tsvector NOT NULL
  ,  CONSTRAINT  film_pkey  PRIMARY KEY  (film_id)  ,  CONSTRAINT  film_language_id_fkey  FOREIGN  KEY  (language_id)  REFERENCES  public.language(language_id)  ON  UPDATE  CASCADE  ON  DELETE  RESTRICT ;);



--
-- Name: film_actor; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.film_actor (
    actor_id smallint NOT NULL,
    film_id smallint NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
  ,  CONSTRAINT  film_actor_pkey  PRIMARY KEY  (actor_id, film_id)  ,  CONSTRAINT  film_actor_actor_id_fkey  FOREIGN  KEY  (actor_id)  REFERENCES  public.actor(actor_id)  ON  UPDATE  CASCADE  ON  DELETE  RESTRICT  ,  CONSTRAINT  film_actor_film_id_fkey  FOREIGN  KEY  (film_id)  REFERENCES  public.film(film_id)  ON  UPDATE  CASCADE  ON  DELETE  RESTRICT ;);



--
-- Name: film_category; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.film_category (
    film_id smallint NOT NULL,
    category_id smallint NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
  ,  CONSTRAINT  film_category_pkey  PRIMARY KEY  (film_id, category_id)  ,  CONSTRAINT  film_category_category_id_fkey  FOREIGN  KEY  (category_id)  REFERENCES  public.category(category_id)  ON  UPDATE  CASCADE  ON  DELETE  RESTRICT  ,  CONSTRAINT  film_category_film_id_fkey  FOREIGN  KEY  (film_id)  REFERENCES  public.film(film_id)  ON  UPDATE  CASCADE  ON  DELETE  RESTRICT ;);



--
-- Name: address; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.address (
    address_id integer DEFAULT nextval('public.address_address_id_seq'::regclass) NOT NULL,
    address character varying(50) NOT NULL,
    address2 character varying(50),
    district character varying(20) NOT NULL,
    city_id smallint NOT NULL,
    postal_code character varying(10),
    phone character varying(20) NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
  ,  CONSTRAINT  address_pkey  PRIMARY KEY  (address_id)  ,  CONSTRAINT  fk_address_city  FOREIGN  KEY  (city_id)  REFERENCES  public.city(city_id) ;);



--
-- Name: city; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.city (
    city_id integer DEFAULT nextval('public.city_city_id_seq'::regclass) NOT NULL,
    city character varying(50) NOT NULL,
    country_id smallint NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
  ,  CONSTRAINT  city_pkey  PRIMARY KEY  (city_id)  ,  CONSTRAINT  fk_city  FOREIGN  KEY  (country_id)  REFERENCES  public.country(country_id) ;);



--
-- Name: country; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.country (
    country_id integer DEFAULT nextval('public.country_country_id_seq'::regclass) NOT NULL,
    country character varying(50) NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
  ,  CONSTRAINT  country_pkey  PRIMARY KEY  (country_id) ;);



--
-- Name: inventory; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.inventory (
    inventory_id integer DEFAULT nextval('public.inventory_inventory_id_seq'::regclass) NOT NULL,
    film_id smallint NOT NULL,
    store_id smallint NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
  ,  CONSTRAINT  inventory_pkey  PRIMARY KEY  (inventory_id)  ,  CONSTRAINT  inventory_film_id_fkey  FOREIGN  KEY  (film_id)  REFERENCES  public.film(film_id)  ON  UPDATE  CASCADE  ON  DELETE  RESTRICT ;);



--
-- Name: language; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.language (
    language_id integer DEFAULT nextval('public.language_language_id_seq'::regclass) NOT NULL,
    name character(20) NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
  ,  CONSTRAINT  language_pkey  PRIMARY KEY  (language_id) ;);



--
-- Name: payment; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.payment (
    payment_id integer DEFAULT nextval('public.payment_payment_id_seq'::regclass) NOT NULL,
    customer_id smallint NOT NULL,
    staff_id smallint NOT NULL,
    rental_id integer NOT NULL,
    amount numeric(5,2) NOT NULL,
    payment_date timestamp without time zone NOT NULL
  ,  CONSTRAINT  payment_pkey  PRIMARY KEY  (payment_id)  ,  CONSTRAINT  payment_customer_id_fkey  FOREIGN  KEY  (customer_id)  REFERENCES  public.customer(customer_id)  ON  UPDATE  CASCADE  ON  DELETE  RESTRICT  ,  CONSTRAINT  payment_rental_id_fkey  FOREIGN  KEY  (rental_id)  REFERENCES  public.rental(rental_id)  ON  UPDATE  CASCADE  ON  DELETE  SET  NULL  ,  CONSTRAINT  payment_staff_id_fkey  FOREIGN  KEY  (staff_id)  REFERENCES  public.staff(staff_id)  ON  UPDATE  CASCADE  ON  DELETE  RESTRICT ;);



--
-- Name: rental; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.rental (
    rental_id integer DEFAULT nextval('public.rental_rental_id_seq'::regclass) NOT NULL,
    rental_date timestamp without time zone NOT NULL,
    inventory_id integer NOT NULL,
    customer_id smallint NOT NULL,
    return_date timestamp without time zone,
    staff_id smallint NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
  ,  CONSTRAINT  rental_pkey  PRIMARY KEY  (rental_id)  ,  CONSTRAINT  rental_customer_id_fkey  FOREIGN  KEY  (customer_id)  REFERENCES  public.customer(customer_id)  ON  UPDATE  CASCADE  ON  DELETE  RESTRICT  ,  CONSTRAINT  rental_inventory_id_fkey  FOREIGN  KEY  (inventory_id)  REFERENCES  public.inventory(inventory_id)  ON  UPDATE  CASCADE  ON  DELETE  RESTRICT  ,  CONSTRAINT  rental_staff_id_key  FOREIGN  KEY  (staff_id)  REFERENCES  public.staff(staff_id) ;);



--
-- Name: staff; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.staff (
    staff_id integer DEFAULT nextval('public.staff_staff_id_seq'::regclass) NOT NULL,
    first_name character varying(45) NOT NULL,
    last_name character varying(45) NOT NULL,
    address_id smallint NOT NULL,
    email character varying(50),
    store_id smallint NOT NULL,
    active boolean DEFAULT true NOT NULL,
    username character varying(16) NOT NULL,
    password character varying(40),
    last_update timestamp without time zone DEFAULT now() NOT NULL,
    picture bytea
  ,  CONSTRAINT  staff_pkey  PRIMARY KEY  (staff_id)  ,  CONSTRAINT  staff_address_id_fkey  FOREIGN  KEY  (address_id)  REFERENCES  public.address(address_id)  ON  UPDATE  CASCADE  ON  DELETE  RESTRICT ;);



--
-- Name: store; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.store (
    store_id integer DEFAULT nextval('public.store_store_id_seq'::regclass) NOT NULL,
    manager_staff_id smallint NOT NULL,
    address_id smallint NOT NULL,
    last_update timestamp without time zone DEFAULT now() NOT NULL
  ,  CONSTRAINT  store_pkey  PRIMARY KEY  (store_id)  ,  CONSTRAINT  store_address_id_fkey  FOREIGN  KEY  (address_id)  REFERENCES  public.address(address_id)  ON  UPDATE  CASCADE  ON  DELETE  RESTRICT  ,  CONSTRAINT  store_manager_staff_id_fkey  FOREIGN  KEY  (manager_staff_id)  REFERENCES  public.staff(staff_id)  ON  UPDATE  CASCADE  ON  DELETE  RESTRICT ;);


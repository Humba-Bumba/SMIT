CREATE TABLE public.human (
    id integer NOT NULL,
    "Date" date,
    respondent integer NOT NULL,
    "Sex" smallint NOT NULL,
    "Age" smallint NOT NULL,
    "Weight" double precision NOT NULL
);

COPY public.human (id, "Date", respondent, "Sex", "Age", "Weight")
FROM '/docker-entrypoint-initdb.d/data1.csv'
DELIMITER ';'
CSV HEADER;
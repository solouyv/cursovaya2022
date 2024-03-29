/* ---------------------------------------------------- */
/*  Generated by Enterprise Architect Version 16.0 		*/
/*  Created On : 19-окт-2022 20:23:53 				*/
/*  DBMS       : PostgreSQL 						*/
/* ---------------------------------------------------- */

/* Drop Sequences for Autonumber Columns */

DROP SEQUENCE IF EXISTS currency_id_seq
;

DROP SEQUENCE IF EXISTS customer_id_seq
;

DROP SEQUENCE IF EXISTS dailycashamount_id_seq
;

DROP SEQUENCE IF EXISTS deal_id_seq
;

DROP SEQUENCE IF EXISTS role_id_seq
;

DROP SEQUENCE IF EXISTS salary_level_seq
;

DROP SEQUENCE IF EXISTS user_id_seq
;

/* Drop Tables */

DROP TABLE IF EXISTS "Currency" CASCADE
;

DROP TABLE IF EXISTS "Customer" CASCADE
;

DROP TABLE IF EXISTS "DailyCashAmount" CASCADE
;

DROP TABLE IF EXISTS "Deal" CASCADE
;

DROP TABLE IF EXISTS "Role" CASCADE
;

DROP TABLE IF EXISTS "Salary" CASCADE
;

DROP TABLE IF EXISTS "User" CASCADE
;

/* Create Tables */

CREATE TABLE "Currency"
(
    id       integer     NOT NULL DEFAULT NEXTVAL(('"currency_id_seq"'::text)::regclass),
    code     varchar(10) NOT NULL,
    data     date        NOT NULL,
    rate_in  money       NOT NULL,
    rate_out money       NOT NULL
)
;

CREATE TABLE "Customer"
(
    id           integer     NOT NULL DEFAULT NEXTVAL(('"customer_id_seq"'::text)::regclass),
    first_name   varchar(50) NOT NULL,
    last_name    varchar(50) NOT NULL,
    passport_id  varchar(50) NOT NULL,
    bank_card_id varchar(50) NULL
)
;

CREATE TABLE "DailyCashAmount"
(
    id          integer NOT NULL DEFAULT NEXTVAL(('"dailycashamount_id_seq"'::text)::regclass),
    currency_id integer NOT NULL,
    amount      money   NOT NULL
)
;

CREATE TABLE "Deal"
(
    id                integer NOT NULL DEFAULT NEXTVAL(('"deal_id_seq"'::text)::regclass),
    customer_id       integer NOT NULL,
    user_id           integer NOT NULL,
    currency_in_id    integer NOT NULL,
    currency_out_id   integer NOT NULL,
    currency_in_count money   NOT NULL,
    data              date    NOT NULL,
    time              time    NOT NULL
)
;

CREATE TABLE "Role"
(
    id   integer     NOT NULL DEFAULT NEXTVAL(('"role_id_seq"'::text)::regclass),
    name varchar(50) NOT NULL
)
;

CREATE TABLE "Salary"
(
    level           integer NOT NULL DEFAULT NEXTVAL(('"salary_level_seq"'::text)::regclass),
    salary          money   NOT NULL,
    salary_increase integer NOT NULL
)
;

CREATE TABLE "User"
(
    id                  integer     NOT NULL DEFAULT NEXTVAL(('"user_id_seq"'::text)::regclass),
    email               varchar(50) NULL,
    first_name          varchar(50) NOT NULL,
    last_name           varchar(50) NOT NULL,
    has_salary_increase boolean     NOT NULL DEFAULT true,
    password            varchar(50) NOT NULL,
    role_id             integer     NOT NULL,
    level_id            integer     NOT NULL,
    active              boolean     NOT NULL DEFAULT true
)
;

/* Create Primary Keys, Indexes, Uniques, Checks */

ALTER TABLE "Currency"
    ADD CONSTRAINT "PK_Currency"
        PRIMARY KEY (id)
;

ALTER TABLE "Customer"
    ADD CONSTRAINT "PK_Customer"
        PRIMARY KEY (id)
;

ALTER TABLE "DailyCashAmount"
    ADD CONSTRAINT "PK_DailyCashAmount"
        PRIMARY KEY (id)
;

CREATE INDEX "IXFK_DailyCashAmount_Currency" ON "DailyCashAmount" (currency_id ASC)
;

ALTER TABLE "Deal"
    ADD CONSTRAINT "PK_Deal"
        PRIMARY KEY (id)
;

CREATE INDEX "IXFK_Deal_Currency" ON "Deal" (currency_in_id ASC)
;

CREATE INDEX "IXFK_Deal_Currency_02" ON "Deal" (currency_out_id ASC)
;

CREATE INDEX "IXFK_Deal_Customer" ON "Deal" (customer_id ASC)
;

CREATE INDEX "IXFK_Deal_User" ON "Deal" (user_id ASC)
;

ALTER TABLE "Role"
    ADD CONSTRAINT "PK_Role"
        PRIMARY KEY (id)
;

ALTER TABLE "Salary"
    ADD CONSTRAINT "PK_Salary"
        PRIMARY KEY (level)
;

ALTER TABLE "User"
    ADD CONSTRAINT "PK_User"
        PRIMARY KEY (id)
;

CREATE INDEX "IXFK_User_Role" ON "User" (role_id ASC)
;

CREATE INDEX "IXFK_User_Salary" ON "User" (level_id ASC)
;

/* Create Foreign Key Constraints */

ALTER TABLE "DailyCashAmount"
    ADD CONSTRAINT "FK_DailyCashAmount_Currency"
        FOREIGN KEY (currency_id) REFERENCES "Currency" (id) ON DELETE No Action ON UPDATE No Action
;

ALTER TABLE "Deal"
    ADD CONSTRAINT "FK_Deal_Currency"
        FOREIGN KEY (currency_in_id) REFERENCES "Currency" (id) ON DELETE Restrict ON UPDATE Cascade
;

ALTER TABLE "Deal"
    ADD CONSTRAINT "FK_Deal_Currency_02"
        FOREIGN KEY (currency_out_id) REFERENCES "Currency" (id) ON DELETE Restrict ON UPDATE Cascade
;

ALTER TABLE "Deal"
    ADD CONSTRAINT "FK_Deal_Customer"
        FOREIGN KEY (customer_id) REFERENCES "Customer" (id) ON DELETE Restrict ON UPDATE Cascade
;

ALTER TABLE "Deal"
    ADD CONSTRAINT "FK_Deal_User"
        FOREIGN KEY (user_id) REFERENCES "User" (id) ON DELETE Restrict ON UPDATE Cascade
;

ALTER TABLE "User"
    ADD CONSTRAINT "FK_User_Role"
        FOREIGN KEY (role_id) REFERENCES "Role" (id) ON DELETE Restrict ON UPDATE Cascade
;

ALTER TABLE "User"
    ADD CONSTRAINT "FK_User_Salary"
        FOREIGN KEY (level_id) REFERENCES "Salary" (level) ON DELETE Restrict ON UPDATE Cascade
;

/* Create Table Comments, Sequences for Autonumber Columns */

CREATE SEQUENCE currency_id_seq INCREMENT 1 START 30
;

CREATE SEQUENCE customer_id_seq INCREMENT 1 START 30
;

CREATE SEQUENCE dailycashamount_id_seq INCREMENT 1 START 30
;

CREATE SEQUENCE deal_id_seq INCREMENT 1 START 30
;

CREATE SEQUENCE role_id_seq INCREMENT 1 START 30
;

CREATE SEQUENCE salary_level_seq INCREMENT 1 START 30
;

CREATE SEQUENCE user_id_seq INCREMENT 1 START 30
;

create view user_view_with_roles(user_id, "user", password, email, role, level) as
SELECT u.id                                                   AS user_id,
       (u.first_name::text || ' '::text) || u.last_name::text AS "user",
       u.password,
       u.email,
       r.name                                                 AS role,
       s.level
FROM "User" u
         LEFT JOIN "Role" r ON u.role_id = r.id
         LEFT JOIN "Salary" s ON s.level = u.level_id
WHERE u.active = true;

alter table user_view_with_roles
    owner to postgres
;

create view daily_currency_rate_view(id, code, rate_in, rate_out, data) as
SELECT "Currency".id,
       "Currency".code,
       "Currency".rate_in::numeric,
       "Currency".rate_out::numeric,
       "Currency".data
FROM "Currency"
ORDER BY "Currency".id DESC
LIMIT 5
;

alter table daily_currency_rate_view
    owner to postgres
;

create view card_ids_view(bank_card_id) as
SELECT "Customer".bank_card_id
FROM "Customer"
WHERE "Customer".bank_card_id IS NOT NULL
  AND "Customer".bank_card_id::text <> ''::text;

alter table card_ids_view
    owner to postgres
;

create procedure add_customer(fname text, lname text, pid text, bcid text)
    language plpgsql
as
'
    BEGIN
        insert into "Customer" (first_name, last_name, passport_id, bank_card_id)
        values (fname, lname, pid, bcid);
    end;';

alter procedure add_customer(text, text, text, text) owner to postgres
;

create view byn_currency_view(id, code, rate_in, rate_out, data) as
SELECT "Currency".id,
       "Currency".code,
       "Currency".rate_in::numeric  AS rate_in,
       "Currency".rate_out::numeric AS rate_out,
       "Currency".data
FROM "Currency"
where "Currency".code = 'BYN';

alter table daily_currency_rate_view
    owner to postgres
;

create function check_password(user_name text, password text) returns boolean
    language plpgsql
as
'
    declare
        passed boolean;
    BEGIN
        select ("User".password = $2 and "User".active = true)
        into passed
        from "User"
        where "User".email = $1;
        return passed;
    end;';

alter function check_password(text, text) owner to postgres
;


create function add_deal(
    customer_id integer,
    user_id integer,
    currency_in_id integer,
    currency_out_id integer,
    currency_in_count numeric
) returns integer
    language plpgsql
as
'
    declare
        deal_id integer;
    BEGIN
        insert into "Deal" (customer_id, user_id, currency_in_id, currency_out_id, currency_in_count, data, time)
        values (customer_id, user_id, currency_in_id, currency_out_id, currency_in_count, now(), now())
        returning "Deal".id into deal_id;
        return deal_id;
    end;';

alter function add_deal(integer, integer, integer, integer, numeric) owner to postgres
;

create procedure add_cash_amount(c integer, a money)
    language plpgsql
as
'
    BEGIN
        insert into "DailyCashAmount" (currency_id, amount)
        values (c, a);
    end;';

alter procedure add_cash_amount(integer, money) owner to postgres
;

create procedure add_currency_rate(code_ varchar, rin numeric, rout numeric)
    language plpgsql
as
'
    BEGIN
        insert into "Currency" (code, data, rate_in, rate_out)
        values (code_, now(), rin, rout);
    end;';

alter procedure add_currency_rate(varchar, numeric, numeric) owner to postgres
;

create procedure truncate_daily_cash_amount()
    language plpgsql
as
'
    BEGIN
        truncate table "DailyCashAmount";
    end;';

alter procedure truncate_daily_cash_amount() owner to postgres
;

create view daily_cash_amount(code, amount) as
SELECT c.code,
       d.amount::numeric
FROM "DailyCashAmount" d
         LEFT JOIN "Currency" c ON c.id = d.currency_id;

alter table daily_cash_amount
    owner to postgres
;

create view deal_data_view
            (deal_id, deal_date, deal_time, customer_id, customer_first_name, customer_last_name, teller_id, teller_first_name,
             teller_last_name, currency_out_code, currency_in_count, currency_out_rate_in, currency_in_code, currency_out_count,
             currency_in_rate_out)
as
SELECT d.id                                                      AS deal_id,
       d.data                                                    AS deal_date,
       d."time"                                                  AS deal_time,
       c3.id                                                     AS customer_id,
       c3.first_name                                             AS customer_first_name,
       c3.last_name                                              AS customer_last_name,
       u.id                                                      AS teller_id,
       u.first_name                                              AS teller_first_name,
       u.last_name                                               AS teller_last_name,
       c2.code                                                   AS currency_out_code,
       d.currency_in_count::numeric                              AS currency_in_count,
       c2.rate_in::numeric                                       AS currency_out_rate_in,
       c1.code                                                   AS currency_in_code,
       (c1.rate_in / c2.rate_out * d.currency_in_count)::numeric AS currency_out_count,
       c1.rate_out::numeric                                      AS currency_in_rate_out,
       c1.id                                                     AS currency_in_id,
       c2.id                                                     AS currency_out_id
FROM "Deal" d
         LEFT JOIN "Currency" c1 ON c1.id = d.currency_in_id
         LEFT JOIN "Currency" c2 ON c2.id = d.currency_out_id
         LEFT JOIN "User" u ON u.id = d.user_id
         LEFT JOIN "Customer" c3 ON c3.id = d.customer_id;

alter table deal_data_view
    owner to postgres
;

create or replace function update_daily_cash() returns trigger
    language plpgsql
as
'
    declare
        deal_data deal_data_view; existing_amount "DailyCashAmount";
    BEGIN
        for deal_data in select *
                         from deal_data_view
                         where deal_id = NEW.id
            loop
                for existing_amount in
                    select *
                    from "DailyCashAmount"
                    loop
                        if existing_amount.currency_id = deal_data.currency_out_id then
                            if (existing_amount.amount::numeric - deal_data.currency_out_count) < 0 then
                                RAISE EXCEPTION ''There are not cash enough!'';
                            end if;
                            update "DailyCashAmount"
                            set amount = existing_amount.amount - deal_data.currency_out_count::money
                            where currency_id = deal_data.currency_out_id;
                        end if;
                        if existing_amount.currency_id = deal_data.currency_in_id then
                            update "DailyCashAmount"
                            set amount = deal_data.currency_in_count::money + existing_amount.amount
                            where currency_id = deal_data.currency_in_id;
                        end if;
                    end loop;
            end loop;
        return NEW;
    end;
';

create trigger update_daily_cash_amount_trigger
    after insert
    on "Deal"
    for each row
execute function update_daily_cash()
;

create view roles_view(id, name) as
SELECT "Role".id,
       "Role".name
FROM "Role";

alter table roles_view
    owner to postgres
;

create view salaries_view(level, salary, salary_increase) as
SELECT "Salary".level,
       "Salary".salary::numeric,
       "Salary".salary_increase
FROM "Salary";

alter table salaries_view
    owner to postgres
;

create procedure add_user(
    em character varying,
    fn character varying,
    ln character varying,
    pwd character varying,
    rid integer,
    lid integer,
    hsi boolean
)
    language plpgsql
as
'
    BEGIN
        insert into "User" (email, first_name, last_name, password, role_id, level_id, has_salary_increase)
        values (em, fn, ln, pwd, rid, lid, hsi);
    end;';

alter procedure add_user(varchar, varchar, varchar, varchar, integer, integer, boolean) owner to postgres
;

create function del_user(e character varying) returns void
    language plpgsql
as
'
    BEGIN
        update "User"
        set active = false
        where "User".email = e;
    end;
';

alter function del_user(varchar) owner to postgres
;

create view compensation_view(id, name, role, level, salary, increase, compensation, date) as
SELECT u.id,
       (u.first_name::text || ' '::text) || u.last_name::text AS name,
       r.name                                                 AS role,
       s.level,
       s.salary::numeric                                      AS salary,
       s.salary_increase                                      AS increase,
       CASE
           WHEN u.has_salary_increase THEN s.salary + s.salary * s.salary_increase / 100
           ELSE s.salary
           END::numeric                                       AS compensation,
       now()::date                                            AS date
FROM "User" u
         LEFT JOIN "Salary" s ON s.level = u.level_id
         LEFT JOIN "Role" r ON r.id = u.role_id
ORDER BY ((u.first_name::text || ' '::text) || u.last_name::text);

alter table compensation_view
    owner to postgres
;

create view teller_report_view(name, level, deal_count) as
SELECT (u.first_name::text || ' '::text) || u.last_name::text AS name,
       u.level_id                                             AS level,
       count(d.id)                                            AS deal_count
FROM "User" u
         LEFT JOIN "Deal" d ON u.id = d.user_id
WHERE u.active
  AND date_part('year'::text, d.data) = date_part('year'::text, now())
  AND date_part('month'::text, d.data) = date_part('month'::text, now())
  AND u.role_id = 2
GROUP BY u.id
ORDER BY ((u.first_name::text || ' '::text) || u.last_name::text);

alter table teller_report_view
    owner to postgres
;

create view deal_report_view(name, level, role, deal_count) as
SELECT (u.first_name::text || ' '::text) || u.last_name::text AS name,
       u.level_id                                             AS level,
       max(r.name::text)                                      AS role,
       count(d.id)                                            AS deal_count
FROM "User" u
         LEFT JOIN "Deal" d ON u.id = d.user_id
         LEFT JOIN "Role" r ON r.id = u.role_id
WHERE u.active
  AND date_part('year'::text, d.data) = date_part('year'::text, now())
  AND date_part('month'::text, d.data) = date_part('month'::text, now())
GROUP BY u.id
ORDER BY ((u.first_name::text || ' '::text) || u.last_name::text);

alter table deal_report_view
    owner to postgres
;

create view monthly_currency_amounts(bcode, bought_amount, scode, sold_amount) as
SELECT mbc.bcode,
       mbc.bought_amount,
       msc.scode,
       msc.sold_amount
FROM (SELECT d.currency_in_code       AS bcode,
             sum(d.currency_in_count) AS bought_amount
      FROM deal_data_view d
      WHERE date_part('year'::text, d.deal_date) = date_part('year'::text, now())
        AND date_part('month'::text, d.deal_date) = date_part('month'::text, now())
      GROUP BY d.currency_in_code
      ORDER BY d.currency_in_code) mbc
         FULL JOIN (SELECT d.currency_out_code       AS scode,
                           sum(d.currency_out_count) AS sold_amount
                    FROM deal_data_view d
                    WHERE date_part('year'::text, d.deal_date) = date_part('year'::text, now())
                      AND date_part('month'::text, d.deal_date) = date_part('month'::text, now())
                    GROUP BY d.currency_out_code
                    ORDER BY d.currency_out_code) msc ON mbc.bcode::text = msc.scode::text;

alter table monthly_currency_amounts
    owner to postgres
;

alter database movies_database owner to app;
create schema if not exists content;
SET search_path TO content,public;

-- auto-generate test table
create table if not exists test_table
(
    id   uuid not null
        primary key,
    name varchar(255)
);

-- auto-generated definition
create table if not exists film_work
(
    created_at    timestamp with time zone not null,
    updated_at    timestamp with time zone not null,
    id            uuid                     not null
        primary key,
    title         varchar(255),
    description   text,
    creation_date date null,
    rating        double precision,
    type          varchar(20),
    file_path     varchar(100)
);

alter table film_work
    owner to app;

create unique index if not exists film_work_id_uindex
    on film_work (id);

-- auto-generated definition
create table if not exists genre
(
    created_at  timestamp with time zone not null,
    updated_at  timestamp with time zone not null,
    id          uuid                     not null
        primary key,
    name        varchar(255),
    description text
);

alter table genre
    owner to app;

create unique index if not exists genre_id_uindex
    on genre (id);

-- auto-generated definition
create table if not exists person
(
    created_at timestamp with time zone not null,
    updated_at timestamp with time zone not null,
    id         uuid                     not null
        primary key,
    full_name  varchar(255)
);

alter table person
    owner to app;

create unique index if not exists person_id_uindex
    on person (id);

-- auto-generated definition
create table if not exists genre_film_work
(
    created_at   timestamp with time zone not null,
    id           uuid                     not null
        primary key,
    film_work_id uuid
        constraint genre_film_work_film_work_id_cddf0c18_fk_film_work_id
            references film_work
            deferrable initially deferred,
    genre_id     uuid
        constraint genre_film_work_genre_id_2a834109_fk_genre_id
            references genre
            deferrable initially deferred
);

alter table genre_film_work
    owner to app;

create index if not exists genre_film_work_film_work_id_cddf0c18
    on genre_film_work (film_work_id);

create index if not exists genre_film_work_genre_id_2a834109
    on genre_film_work (genre_id);

-- auto-generated definition
create table if not exists person_film_work
(
    created_at   timestamp with time zone not null,
    id           uuid                     not null
        primary key,
    role         text,
    film_work_id uuid
        constraint person_film_work_film_work_id_0bf9a19b_fk_film_work_id
            references film_work
            deferrable initially deferred,
    person_id    uuid
        constraint person_film_work_person_id_33bd8260_fk_person_id
            references person
            deferrable initially deferred
);

alter table person_film_work
    owner to app;

create index if not exists person_film_work_film_work_id_0bf9a19b
    on person_film_work (film_work_id);

create index if not exists person_film_work_person_id_33bd8260
    on person_film_work (person_id);


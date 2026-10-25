-- Esquema de demo de la slide 11 de S12: cadenas · hoteles · usuarios · reseñas
-- Ejecutar en Supabase → SQL Editor ANTES de importar los CSV.

create extension if not exists vector with schema extensions;

create table public.cadenas (
  id     bigint primary key,
  nombre text   not null,
  plan   text   not null check (plan in ('Básico', 'Pro', 'Enterprise'))
);

create table public.hoteles (
  id        bigint primary key,
  cadena_id bigint not null references public.cadenas (id) on delete cascade,
  nombre    text   not null,
  provincia text   not null
);

create table public.usuarios (
  id        bigint primary key,
  cadena_id bigint not null references public.cadenas (id) on delete cascade,
  nombre    text   not null,
  email     text   not null unique,
  rol       text   not null check (rol in ('admin', 'analista', 'lector'))
);

create table public.resenas (
  id               bigint   primary key,
  hotel_id         bigint   not null references public.hoteles (id) on delete cascade,
  nota             smallint not null check (nota between 1 and 5),
  titulo           text,
  texto            text     not null,
  embedding        extensions.vector(1536),
  modelo_embedding text     default 'text-embedding-3-small'
);

create index on public.hoteles (cadena_id);
create index on public.usuarios (cadena_id);
create index on public.resenas (hotel_id);
create index on public.resenas using hnsw (embedding vector_cosine_ops);

-- Seguridad por fila activada en todas las tablas (sin políticas: nadie lee desde el cliente web;
-- el panel de Supabase y los scripts con la service_role key sí pueden).
alter table public.cadenas  enable row level security;
alter table public.hoteles  enable row level security;
alter table public.usuarios enable row level security;
alter table public.resenas  enable row level security;

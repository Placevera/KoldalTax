-- Stores every contact form message and newsletter signup, so nothing is lost even if an email fails.
create table if not exists public.submissions (
  id bigint generated always as identity primary key,
  created_at timestamptz not null default now(),
  kind text not null check (kind in ('contact', 'newsletter')),
  first_name text,
  last_name text,
  email text not null,
  phone text,
  service text,
  message text,
  page text,
  emailed boolean not null default false
);

-- Only the edge function (service role) writes here; the public site cannot read or write directly.
alter table public.submissions enable row level security;

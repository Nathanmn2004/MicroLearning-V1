create extension if not exists pgcrypto;

create type processing_status as enum (
  'pending',
  'extracting',
  'cleaning',
  'chunking',
  'analyzing_chunks',
  'analyzing_chapters',
  'building_book_map',
  'generating_lesson',
  'validating_quotes',
  'completed',
  'failed'
);

create type lesson_status as enum (
  'draft',
  'review',
  'approved',
  'archived'
);

create type subscription_status as enum (
  'pending',
  'active',
  'overdue',
  'cancelled',
  'expired',
  'refunded',
  'unknown'
);

create type delivery_channel as enum (
  'email',
  'whatsapp'
);

create type delivery_status as enum (
  'pending',
  'scheduled',
  'sending',
  'sent',
  'delivered',
  'failed',
  'cancelled'
);

create or replace function set_updated_at()
returns trigger
language plpgsql
as $$
begin
  new.updated_at = now();
  return new;
end;
$$;

create table profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  name text,
  email text,
  phone text,
  preferred_channel text default 'email',
  preferred_time time,
  timezone text default 'America/Sao_Paulo',
  whatsapp_enabled boolean not null default false,
  email_enabled boolean not null default true,
  is_admin boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table books (
  id uuid primary key default gen_random_uuid(),
  slug text not null unique,
  title text not null,
  author text,
  description text,
  category text,
  language text not null default 'pt-BR',
  file_path text not null,
  page_count integer,
  processing_status processing_status not null default 'pending',
  processing_version integer not null default 1,
  processed_at timestamptz,
  enabled boolean not null default true,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table book_pages (
  id uuid primary key default gen_random_uuid(),
  book_id uuid not null references books(id) on delete cascade,
  page_number integer not null,
  original_text text,
  cleaned_text text,
  created_at timestamptz not null default now(),
  unique (book_id, page_number)
);

create table book_chunks (
  id uuid primary key default gen_random_uuid(),
  book_id uuid not null references books(id) on delete cascade,
  chapter text,
  page_start integer,
  page_end integer,
  position integer not null,
  original_text text,
  cleaned_text text,
  token_count integer,
  created_at timestamptz not null default now(),
  unique (book_id, position)
);

create table chunk_analyses (
  id uuid primary key default gen_random_uuid(),
  chunk_id uuid not null references book_chunks(id) on delete cascade,
  provider text not null,
  model text not null,
  summary text,
  structured_content jsonb not null default '{}'::jsonb,
  prompt_version text,
  created_at timestamptz not null default now()
);

create table chapter_analyses (
  id uuid primary key default gen_random_uuid(),
  book_id uuid not null references books(id) on delete cascade,
  chapter text not null,
  summary text,
  structured_content jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  unique (book_id, chapter)
);

create table book_analyses (
  id uuid primary key default gen_random_uuid(),
  book_id uuid not null references books(id) on delete cascade,
  main_thesis text,
  book_objective text,
  structured_content jsonb not null default '{}'::jsonb,
  provider text not null,
  model text not null,
  version integer not null default 1,
  created_at timestamptz not null default now(),
  unique (book_id, version)
);

create table lessons (
  id uuid primary key default gen_random_uuid(),
  book_id uuid not null references books(id) on delete cascade,
  title text not null,
  content_markdown text,
  content_html text,
  whatsapp_content text,
  word_count integer,
  estimated_reading_minutes integer,
  status lesson_status not null default 'draft',
  version integer not null default 1,
  approved_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table lesson_quotes (
  id uuid primary key default gen_random_uuid(),
  lesson_id uuid not null references lessons(id) on delete cascade,
  book_id uuid not null references books(id) on delete cascade,
  chunk_id uuid references book_chunks(id) on delete set null,
  quote_text text not null,
  page_number integer,
  chapter text,
  verified boolean not null default false,
  created_at timestamptz not null default now()
);

create table subscriptions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  provider text not null default 'cakto',
  provider_customer_id text,
  provider_subscription_id text,
  plan_name text,
  status subscription_status not null default 'unknown',
  started_at timestamptz,
  current_period_end timestamptz,
  cancelled_at timestamptz,
  last_verified_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (provider, provider_subscription_id)
);

create table payment_events (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete set null,
  event_type text not null,
  provider_event_id text,
  payload jsonb not null default '{}'::jsonb,
  processed boolean not null default false,
  received_at timestamptz not null default now(),
  processed_at timestamptz,
  unique (provider_event_id)
);

create table deliveries (
  id uuid primary key default gen_random_uuid(),
  lesson_id uuid not null references lessons(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  channel delivery_channel not null,
  status delivery_status not null default 'pending',
  scheduled_at timestamptz,
  sent_at timestamptz,
  delivered_at timestamptz,
  provider_message_id text,
  error_message text,
  retry_count integer not null default 0,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (lesson_id, user_id, channel)
);

create index idx_books_processing_status on books(processing_status);
create index idx_book_pages_book_id on book_pages(book_id);
create index idx_book_chunks_book_id on book_chunks(book_id);
create index idx_chunk_analyses_chunk_id on chunk_analyses(chunk_id);
create index idx_chapter_analyses_book_id on chapter_analyses(book_id);
create index idx_book_analyses_book_id on book_analyses(book_id);
create index idx_lessons_book_id on lessons(book_id);
create index idx_lessons_status on lessons(status);
create index idx_lesson_quotes_lesson_id on lesson_quotes(lesson_id);
create index idx_subscriptions_user_id on subscriptions(user_id);
create index idx_subscriptions_status on subscriptions(status);
create index idx_payment_events_user_id on payment_events(user_id);
create index idx_payment_events_event_type on payment_events(event_type);
create index idx_deliveries_user_id on deliveries(user_id);
create index idx_deliveries_lesson_id on deliveries(lesson_id);
create index idx_deliveries_status on deliveries(status);
create index idx_deliveries_channel on deliveries(channel);

create trigger set_profiles_updated_at
before update on profiles
for each row execute function set_updated_at();

create trigger set_books_updated_at
before update on books
for each row execute function set_updated_at();

create trigger set_lessons_updated_at
before update on lessons
for each row execute function set_updated_at();

create trigger set_subscriptions_updated_at
before update on subscriptions
for each row execute function set_updated_at();

create trigger set_deliveries_updated_at
before update on deliveries
for each row execute function set_updated_at();

alter table profiles enable row level security;
alter table books enable row level security;
alter table book_pages enable row level security;
alter table book_chunks enable row level security;
alter table chunk_analyses enable row level security;
alter table chapter_analyses enable row level security;
alter table book_analyses enable row level security;
alter table lessons enable row level security;
alter table lesson_quotes enable row level security;
alter table subscriptions enable row level security;
alter table payment_events enable row level security;
alter table deliveries enable row level security;

create policy "profiles_select_own"
on profiles for select
using (auth.uid() = id);

create policy "profiles_update_own"
on profiles for update
using (auth.uid() = id)
with check (auth.uid() = id);

create policy "profiles_insert_own"
on profiles for insert
with check (auth.uid() = id);

create policy "books_select_enabled"
on books for select
using (enabled = true);

create policy "lessons_select_approved"
on lessons for select
using (status = 'approved');

create policy "subscriptions_select_own"
on subscriptions for select
using (auth.uid() = user_id);

create policy "deliveries_select_own"
on deliveries for select
using (auth.uid() = user_id);

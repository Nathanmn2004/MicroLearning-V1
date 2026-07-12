drop table if exists profiles cascade;
drop table if exists chunk_analyses cascade;
drop table if exists chapter_analyses cascade;
drop table if exists book_analyses cascade;
drop table if exists book_pages cascade;
drop table if exists book_chunks cascade;

drop policy if exists "books_select_enabled" on books;
drop policy if exists "lessons_select_approved" on lessons;
drop policy if exists "subscriptions_select_own" on subscriptions;
drop policy if exists "deliveries_select_own" on deliveries;

alter table lesson_quotes
  drop column if exists chunk_id;

alter table lesson_quotes
  add column if not exists source_note text;

alter table subscriptions
  drop constraint if exists subscriptions_user_id_fkey;

alter table subscriptions
  drop column if exists user_id;

alter table payment_events
  drop constraint if exists payment_events_user_id_fkey;

alter table payment_events
  drop column if exists user_id;

alter table payment_events
  add column if not exists subscriber_id uuid references subscribers(id) on delete set null;

alter table deliveries
  drop constraint if exists deliveries_user_id_fkey;

alter table deliveries
  drop column if exists user_id;

drop index if exists idx_subscriptions_user_id;
drop index if exists idx_payment_events_user_id;
drop index if exists idx_deliveries_user_id;
drop index if exists idx_book_pages_book_id;
drop index if exists idx_book_chunks_book_id;
drop index if exists idx_chunk_analyses_chunk_id;
drop index if exists idx_chapter_analyses_book_id;
drop index if exists idx_book_analyses_book_id;

create index if not exists idx_payment_events_subscriber_id on payment_events(subscriber_id);

alter table books enable row level security;
alter table lessons enable row level security;
alter table lesson_quotes enable row level security;
alter table subscriptions enable row level security;
alter table payment_events enable row level security;
alter table deliveries enable row level security;
alter table subscribers enable row level security;
alter table delivery_parts enable row level security;

create table subscribers (
  id uuid primary key default gen_random_uuid(),
  name text,
  email text,
  phone text,
  preferred_channel text default 'both',
  whatsapp_enabled boolean not null default true,
  email_enabled boolean not null default true,
  source text not null default 'cakto',
  provider_customer_id text,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (email),
  unique (phone),
  unique (source, provider_customer_id)
);

alter table subscriptions
  add column if not exists subscriber_id uuid references subscribers(id) on delete cascade;

alter table subscriptions
  alter column user_id drop not null;

alter table deliveries
  add column if not exists subscriber_id uuid references subscribers(id) on delete cascade;

alter table deliveries
  alter column user_id drop not null;

create table delivery_parts (
  id uuid primary key default gen_random_uuid(),
  delivery_id uuid not null references deliveries(id) on delete cascade,
  position integer not null,
  content text not null,
  status delivery_status not null default 'pending',
  provider_message_id text,
  error_message text,
  sent_at timestamptz,
  delivered_at timestamptz,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (delivery_id, position)
);

create index idx_subscribers_email on subscribers(email);
create index idx_subscribers_phone on subscribers(phone);
create index idx_subscribers_provider_customer_id on subscribers(provider_customer_id);
create index idx_subscriptions_subscriber_id on subscriptions(subscriber_id);
create index idx_deliveries_subscriber_id on deliveries(subscriber_id);
create index idx_delivery_parts_delivery_id on delivery_parts(delivery_id);
create index idx_delivery_parts_status on delivery_parts(status);

create trigger set_subscribers_updated_at
before update on subscribers
for each row execute function set_updated_at();

create trigger set_delivery_parts_updated_at
before update on delivery_parts
for each row execute function set_updated_at();

alter table subscribers enable row level security;
alter table delivery_parts enable row level security;

drop policy if exists "subscriptions_select_own" on subscriptions;
drop policy if exists "deliveries_select_own" on deliveries;

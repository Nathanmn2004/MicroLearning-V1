alter table subscriptions
  add column if not exists provider_product_id text,
  add column if not exists provider_offer_id text;

create index if not exists idx_subscriptions_provider_product_id
  on subscriptions(provider_product_id);

create index if not exists idx_subscriptions_provider_offer_id
  on subscriptions(provider_offer_id);

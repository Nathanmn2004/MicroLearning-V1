create unique index if not exists idx_deliveries_unique_subscriber_lesson_channel
  on deliveries (subscriber_id, lesson_id, channel)
  where subscriber_id is not null;

create index if not exists idx_deliveries_scheduled_at
  on deliveries (scheduled_at);

create index if not exists idx_deliveries_due_email
  on deliveries (scheduled_at, status)
  where channel = 'email';

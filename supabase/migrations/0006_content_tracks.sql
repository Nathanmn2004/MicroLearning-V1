alter table subscribers
  add column if not exists content_track text not null default 'todos';

alter table books
  add column if not exists content_track text not null default 'todos';

alter table lessons
  add column if not exists content_track text not null default 'todos';

update subscribers
set content_track = 'todos'
where content_track is null or content_track = '';

update books
set content_track = case
  when category in (
    'habitos',
    'produtividade',
    'desenvolvimento-pessoal',
    'comunicacao',
    'filosofia'
  ) then 'mente-desenvolvimento-pessoal'
  when category in (
    'negocios',
    'financas',
    'estrategia'
  ) then 'carreira-negocios-dinheiro'
  when category in (
    'historia',
    'ciencia',
    'tecnologia'
  ) then 'historia-sociedade'
  else 'todos'
end
where content_track is null or content_track = '' or content_track = 'todos';

update lessons
set content_track = books.content_track
from books
where lessons.book_id = books.id
  and (lessons.content_track is null or lessons.content_track = '' or lessons.content_track = 'todos');

alter table subscribers
  add constraint subscribers_content_track_check
  check (content_track in (
    'todos',
    'mente-desenvolvimento-pessoal',
    'carreira-negocios-dinheiro',
    'historia-sociedade'
  ));

alter table books
  add constraint books_content_track_check
  check (content_track in (
    'todos',
    'mente-desenvolvimento-pessoal',
    'carreira-negocios-dinheiro',
    'historia-sociedade'
  ));

alter table lessons
  add constraint lessons_content_track_check
  check (content_track in (
    'todos',
    'mente-desenvolvimento-pessoal',
    'carreira-negocios-dinheiro',
    'historia-sociedade'
  ));

create index if not exists idx_subscribers_content_track
  on subscribers(content_track);

create index if not exists idx_books_content_track
  on books(content_track);

create index if not exists idx_lessons_content_track_status_created_at
  on lessons(content_track, status, created_at);

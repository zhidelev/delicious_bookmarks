create table links (
  id integer primary key autoincrement not null,
  link text,
  is_private integer,
  add_date integer,
  is_deleted integer
);
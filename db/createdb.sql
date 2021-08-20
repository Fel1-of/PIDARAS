create table client(
    telegram_id integer primary key,
    is_pro_account boolean,
    lang varchar(2)
);

create table category(
    id integer primary key,
    name varchar(255),
    icon varchar(1),
    client_telegram_id integer,
    FOREIGN KEY(client_telegram_id) REFERENCES client(telegram_id)
);

create table expense(
    id integer primary key,
    amount integer,
    creation_time datetime,
    category_id integer,
    client_telegram_id integer,
    FOREIGN KEY(category_id) REFERENCES category(id),
    FOREIGN KEY(client_telegram_id) REFERENCES client(telegram_id)
);

insert into client (telegram_id, is_pro_account)
values (285942176, 0);


insert into category (id, name, icon, client_telegram_id)
values
    (1, "продукты", "🍴", 285942176),
    (2, "кофе", "☕", 285942176),
    (3, "пиво", "🍻", 285942176),
    (4, "общественный транспорт", "🚌", 285942176),
    (5, "такси", "🚕", 285942176);
--    ("coffee", "кофе", 1, ""),
--    ("dinner", "обед", 1, "столовая, ланч, бизнес-ланч, бизнес ланч"),
--    ("cafe", "кафе", 1, "ресторан, рест, мак, макдональдс, макдак, kfc, ilpatio, il patio"),
--    ("transport", "общ. транспорт", 0, "метро, автобус, metro"),
--    ("taxi", "такси", 0, "яндекс такси, yandex taxi"),
--    ("phone", "телефон", 0, "теле2, связь"),
--    ("books", "книги", 0, "литература, литра, лит-ра"),
--    ("internet", "интернет", 0, "инет, inet"),
--    ("subscriptions", "подписки", 0, "подписка"),
--    ("other", "прочее", 1, "");

--insert into budget(codename, daily_limit) values ("base", 500);

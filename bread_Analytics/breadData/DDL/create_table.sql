create table products(
product_id int(11) NOT NULL PRIMARY KEY,
product_name varchar(256),
product_name2 varchar(256),
bread_type varchar(32),
ferment varchar(32),
gain1 varchar(32),
gain2 varchar(32),
country varchar(32),
memo varchar(512)
)

create table shops_main_products(
shop_id int(11) NOT NULL,
product_id int(11) NOT NULL,
memo varchar(512),
PRIMARY KEY(shop_id, product_id)
);

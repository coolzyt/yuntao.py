create table rss_article(
	id bigint auto_increment not null,
	title varchar(500) not null,
	description longtext not null,
	pubdate datetime not null,
	source varchar(500) not null,
	primary key (id)
)default charset UTF8 ENGINE INNODB ;
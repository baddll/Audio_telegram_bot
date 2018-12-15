BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS `users` (
	`id`	INT,
	`counter`	INT,
	`last_artist`	TEXT
);
CREATE TABLE IF NOT EXISTS `top_art_table` (
	`artist`	TEXT,
	`song`	TEXT,
	`file_id`	TEXT
);
CREATE TABLE IF NOT EXISTS `for_send` (
	`id`	INT,
	`song`	TEXT
);
CREATE TABLE IF NOT EXISTS `basic_lib` (
	`id_users`	INT,
	`audio_id`	TEXT,
	`duration`	INT,
	`format`	TEXT,
	`artist`	TEXT,
	`album`	TEXT,
	`track`	TEXT,
	`tag0`	TEXT,
	`tag1`	TEXT,
	`tag2`	TEXT,
	`teg3`	TEXT,
	`tag4`	TEXT,
	`time`	INT
);
CREATE TABLE IF NOT EXISTS `artist_info` (
	`artist`	TEXT,
	`url`	TEXT,
	`tag0`	TEXT,
	`tag1`	TEXT,
	`tag2`	TEXT,
	`tag3`	TEXT,
	`tag4`	TEXT,
	`len_art`	INTEGER
);
COMMIT;

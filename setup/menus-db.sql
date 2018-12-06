CREATE DATABASE IF NOT EXISTS menus_db;

USE menus_db;

# remove the following after development is complete
drop table IF EXISTS menus;

CREATE TABLE IF NOT EXISTS `menus` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(40),
   title VARCHAR(100),
   description VARCHAR(1000),
   descrip2 VARCHAR(1000),
   descrip3 VARCHAR(1000),
   present BOOLEAN DEFAULT 0,
   extra_html VARCHAR(4000),
   icon MEDIUMBLOB,
   zim_name VARCHAR(100),
   lang VARCHAR(10),
   logo_url VARCHAR(100),
   intended_use VARCHAR(40),
   moddir VARCHAR(200),
   menu_item_name VARCHAR(40),
   start_url VARCHAR(400),
   apk_file VARCHAR(400),
   apk_file_size LONG,
  `datetime_created` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `js` VARCHAR(10000),
  PRIMARY KEY (`id`),
  CONSTRAINT  `name` UNIQUE (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;


drop table IF EXISTS chosen;
CREATE TABLE IF NOT EXISTS `chosen` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `site` VARCHAR(20) DEFAULT 'default',
  `menus_id` LONG NOT NULL,
  `seq` TINYINT DEFAULT 0,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, CREATE TEMPORARY TABLES ON menus_db.* TO 'menus_user'@'localhost';

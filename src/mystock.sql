SHOW DATABASES;

CREATE SCHEMA `mystock` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;
USE mystock;

CREATE TABLE `mystock`.`company` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(20) NOT NULL,
  `name` VARCHAR(45) NOT NULL,
  `updatetime` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);

DROP TABLE `mystock`.`company`;
TRUNCATE TABLE `mystock`.`company`;

ALTER TABLE `mystock`.`company` 
ADD COLUMN `products` VARCHAR(45) NULL AFTER `field`,
ADD COLUMN `publicdate` DATE NULL AFTER `products`,
ADD COLUMN `representative` VARCHAR(20) NULL AFTER `publicdate`,
ADD COLUMN `homepage` VARCHAR(45) NULL AFTER `representative`,
ADD COLUMN `region` VARCHAR(45) NULL AFTER `homepage`,
CHANGE COLUMN `field` `field` VARCHAR(20) NULL DEFAULT NULL AFTER `name`;

CREATE TABLE `mystock`.`price` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `code` VARCHAR(20) NOT NULL,
  `date` DATE NOT NULL,
  `open` INT UNSIGNED NULL,
  `high` INT UNSIGNED NULL,
  `low` INT UNSIGNED NULL,
  `close` INT UNSIGNED NULL,
  `diff` INT NULL,
  `volume` INT UNSIGNED NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE);

DESCRIBE company;
INSERT INTO company(code, name) VALUES ('100300', '삼성전자');
SELECT * FROM company;
TRUNCATE TABLE company;

DESCRIBE price;
SELECT * FROM price;
SELECT * FROM price WHERE code = 004840;
SELECT min(date) FROM price;
SELECT max(date) FROM price;
TRUNCATE TABLE price;

SHOW CREATE TABLE company;
SHOW CREATE TABLE price;

CREATE TABLE `company` (
  `id` int unsigned NOT NULL AUTO_INCREMENT,
  `code` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `name` varchar(45) COLLATE utf8mb4_bin NOT NULL,
  `field` varchar(45) COLLATE utf8mb4_bin DEFAULT NULL,
  `publicdate` date DEFAULT NULL,
  `homepage` varchar(200) COLLATE utf8mb4_bin DEFAULT NULL,
  `updatetime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id_UNIQUE` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=29389 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

CREATE TABLE `price` (
  `code` varchar(20) COLLATE utf8mb4_bin NOT NULL,
  `date` date NOT NULL,
  `open` int unsigned DEFAULT NULL,
  `high` int unsigned DEFAULT NULL,
  `low` int unsigned DEFAULT NULL,
  `close` int unsigned DEFAULT NULL,
  `diff` int DEFAULT NULL,
  `volume` int unsigned DEFAULT NULL,
  PRIMARY KEY (`code`,`date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;



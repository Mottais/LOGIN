-- A exécuter dans la console :
-- cat Pour_tester.sql | mysql -u root -proot
CREATE DATABASE IF NOT EXISTS charpente_db;
USE charpente_db;


-- Supprimer la table si elle existe
DROP TABLE IF EXISTS utilisateur;


-- Création de la  table
CREATE TABLE utilisateur (
	id INT AUTO_INCREMENT PRIMARY KEY,
	nom VARCHAR(50) NOT NULL,
	email VARCHAR(100) UNIQUE NOT NULL,
	mot_de_passe VARCHAR(255) NOT NULL
);


CREATE USER IF NOT EXISTS 'toto'@'localhost' IDENTIFIED BY 'toto';
GRANT ALL PRIVILEGES ON charpente_db.* TO 'toto'@'localhost';
FLUSH PRIVILEGES;

SHOW TABLES;
SELECT * FROM utilisateur;



-- DELETE FROM utilisateur WHERE id = 1;


-- |  1 | toto | toto@test.com | scrypt:32768:8:1$ijfa9mis8drDcWK6$e0f4dff8ed568e29a797590c1312a231f1a23d3e47722470aa8da5d91ec8847611eecde10f2cfbd5efe667676e8bca37555c750bd3967dce6e3193550dc550fa |
-- |  2 | titi | titi@test.com | scrypt:32768:8:1$rScbuXXjPlkfFxXS$5fe605cfdbb3cc721220bc044221d2dec091ef62551e97e63477888d72f8ed6d199c63696376052c40e047902e7645a16a5db03da9471b00ef0b4ee8b35fd88d |

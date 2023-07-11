CREATE DATABASE  IF NOT EXISTS `b4y_user_db` /*!40100 DEFAULT CHARACTER SET utf8 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `b4y_user_db`;
-- MySQL dump 10.13  Distrib 8.0.22, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: b4y_user_db
-- ------------------------------------------------------
-- Server version	8.0.22

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `cashback`
--

DROP TABLE IF EXISTS `cashback`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `cashback` (
  `saldo` decimal(6,2) NOT NULL,
  `tmstmp` datetime NOT NULL,
  `utente` varchar(128) NOT NULL,
  PRIMARY KEY (`utente`),
  KEY `fk_utente_cb_idx` (`utente`),
  CONSTRAINT `fk_utente_cb` FOREIGN KEY (`utente`) REFERENCES `utente` (`mail`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `cashback`
--

LOCK TABLES `cashback` WRITE;
/*!40000 ALTER TABLE `cashback` DISABLE KEYS */;
/*!40000 ALTER TABLE `cashback` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `fermata`
--

DROP TABLE IF EXISTS `fermata`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `fermata` (
  `nome` varchar(256) NOT NULL,
  `lat` decimal(8,6) NOT NULL,
  `lon` decimal(8,6) NOT NULL,
  `indirizzo` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`lat`,`lon`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `fermata`
--

LOCK TABLES `fermata` WRITE;
/*!40000 ALTER TABLE `fermata` DISABLE KEYS */;
/*!40000 ALTER TABLE `fermata` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itinerario_proposto`
--

DROP TABLE IF EXISTS `itinerario_proposto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itinerario_proposto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `costo` decimal(6,2) NOT NULL,
  `distanza` decimal(8,4) NOT NULL,
  `orario_partenza_proposto` datetime NOT NULL,
  `orario_arrivo_proposto` datetime NOT NULL,
  `orario_partenza_effettivo` datetime DEFAULT NULL,
  `orario_arrivo_effettivo` datetime DEFAULT NULL,
  `stato` enum('rejected','confirmed','pending') NOT NULL DEFAULT 'pending',
  `utente` varchar(128) NOT NULL,
  `itinerario_richiesto` bigint NOT NULL,
  `percorso` bigint NOT NULL,
  `fermata_lat_partenza` decimal(8,6) NOT NULL,
  `fermata_lon_partenza` decimal(8,6) NOT NULL,
  `fermata_lat_arrivo` decimal(8,6) NOT NULL,
  `fermata_lon_arrivo` decimal(8,6) NOT NULL,
  PRIMARY KEY (`id`,`utente`,`itinerario_richiesto`,`percorso`),
  KEY `fk_percorso_prop_idx` (`percorso`),
  KEY `idx_data_prop` (`stato`),
  KEY `fk_itinerario_richiesto_user_prop_idx` (`utente`),
  KEY `fk_itinerario_richiesto_id_prop_idx` (`itinerario_richiesto`),
  KEY `fk_itinerario_proposto_fermata1_idx` (`fermata_lat_partenza`,`fermata_lon_partenza`),
  KEY `fk_itinerario_proposto_fermata2_idx` (`fermata_lat_arrivo`,`fermata_lon_arrivo`),
  CONSTRAINT `fk_itinerario_proposto_fermata1` FOREIGN KEY (`fermata_lat_partenza`, `fermata_lon_partenza`) REFERENCES `fermata` (`lat`, `lon`) ON UPDATE CASCADE,
  CONSTRAINT `fk_itinerario_proposto_fermata2` FOREIGN KEY (`fermata_lat_arrivo`, `fermata_lon_arrivo`) REFERENCES `fermata` (`lat`, `lon`) ON UPDATE CASCADE,
  CONSTRAINT `fk_itinerario_richiesto_id_prop` FOREIGN KEY (`itinerario_richiesto`) REFERENCES `itinerario_richiesto` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_itinerario_richiesto_user_prop` FOREIGN KEY (`utente`) REFERENCES `itinerario_richiesto` (`utente`) ON UPDATE CASCADE,
  CONSTRAINT `fk_percorso_prop` FOREIGN KEY (`percorso`) REFERENCES `percorso` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itinerario_proposto`
--

LOCK TABLES `itinerario_proposto` WRITE;
/*!40000 ALTER TABLE `itinerario_proposto` DISABLE KEYS */;
/*!40000 ALTER TABLE `itinerario_proposto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `itinerario_richiesto`
--

DROP TABLE IF EXISTS `itinerario_richiesto`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `itinerario_richiesto` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `ora_inizio` datetime DEFAULT NULL,
  `ora_fine` datetime DEFAULT NULL,
  `costo_max` decimal(6,2) DEFAULT NULL,
  `distanza` decimal(8,4) DEFAULT NULL,
  `utente` varchar(128) NOT NULL,
  `fermata_lat_partenza` decimal(8,6) NOT NULL,
  `fermata_lon_partenza` decimal(8,6) NOT NULL,
  `fermata_lat_arrivo` decimal(8,6) NOT NULL,
  `fermata_lon_arrivo` decimal(8,6) NOT NULL,
  PRIMARY KEY (`id`,`utente`),
  KEY `fk_utente_req_idx` (`utente`),
  KEY `fk_itinerario_richiesto_fermata1_idx` (`fermata_lat_partenza`,`fermata_lon_partenza`),
  KEY `fk_itinerario_richiesto_fermata2_idx` (`fermata_lat_arrivo`,`fermata_lon_arrivo`),
  CONSTRAINT `fk_itinerario_richiesto_fermata1` FOREIGN KEY (`fermata_lat_partenza`, `fermata_lon_partenza`) REFERENCES `fermata` (`lat`, `lon`) ON UPDATE CASCADE,
  CONSTRAINT `fk_itinerario_richiesto_fermata2` FOREIGN KEY (`fermata_lat_arrivo`, `fermata_lon_arrivo`) REFERENCES `fermata` (`lat`, `lon`) ON UPDATE CASCADE,
  CONSTRAINT `fk_utente_req` FOREIGN KEY (`utente`) REFERENCES `utente` (`mail`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `itinerario_richiesto`
--

LOCK TABLES `itinerario_richiesto` WRITE;
/*!40000 ALTER TABLE `itinerario_richiesto` DISABLE KEYS */;
/*!40000 ALTER TABLE `itinerario_richiesto` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `ordinamento`
--

DROP TABLE IF EXISTS `ordinamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `ordinamento` (
  `numero` int DEFAULT NULL,
  `percorso` bigint NOT NULL,
  `fermata_lat` decimal(8,6) NOT NULL,
  `fermata_lon` decimal(8,6) NOT NULL,
  PRIMARY KEY (`percorso`,`fermata_lat`,`fermata_lon`),
  KEY `fk_percorso_ord_idx` (`percorso`),
  KEY `fk_ordinamento_fermata1_idx` (`fermata_lat`,`fermata_lon`),
  CONSTRAINT `fk_ordinamento_fermata1` FOREIGN KEY (`fermata_lat`, `fermata_lon`) REFERENCES `fermata` (`lat`, `lon`) ON UPDATE CASCADE,
  CONSTRAINT `fk_percorso_ord` FOREIGN KEY (`percorso`) REFERENCES `percorso` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `ordinamento`
--

LOCK TABLES `ordinamento` WRITE;
/*!40000 ALTER TABLE `ordinamento` DISABLE KEYS */;
/*!40000 ALTER TABLE `ordinamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `pagamento`
--

DROP TABLE IF EXISTS `pagamento`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pagamento` (
  `tmstmp` datetime DEFAULT NULL,
  `file_fattura` blob,
  `percorso` bigint NOT NULL,
  `itinerario_richiesto` bigint NOT NULL,
  `utente` varchar(128) NOT NULL,
  `itinerario_proposto` bigint NOT NULL,
  PRIMARY KEY (`itinerario_proposto`,`utente`,`itinerario_richiesto`,`percorso`),
  KEY `fk_itinerario_proposto_id_pay_idx` (`itinerario_proposto`) /*!80000 INVISIBLE */,
  KEY `fk_itinerario_proposto_req_pay_idx` (`itinerario_richiesto`),
  KEY `fk_itinerario_proposto_route_pay_idx` (`percorso`) /*!80000 INVISIBLE */,
  KEY `fk_itinerario_proposto_user_pay` (`utente`),
  CONSTRAINT `fk_itinerario_proposto_id_pay` FOREIGN KEY (`itinerario_proposto`) REFERENCES `itinerario_proposto` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_itinerario_proposto_req_pay` FOREIGN KEY (`itinerario_richiesto`) REFERENCES `itinerario_proposto` (`itinerario_richiesto`) ON UPDATE CASCADE,
  CONSTRAINT `fk_itinerario_proposto_route_pay` FOREIGN KEY (`percorso`) REFERENCES `itinerario_proposto` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_utente` FOREIGN KEY (`utente`) REFERENCES `utente` (`mail`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pagamento`
--

LOCK TABLES `pagamento` WRITE;
/*!40000 ALTER TABLE `pagamento` DISABLE KEYS */;
/*!40000 ALTER TABLE `pagamento` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `percorso`
--

DROP TABLE IF EXISTS `percorso`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `percorso` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `scadenza` datetime NOT NULL,
  `archiviato` tinyint NOT NULL DEFAULT '0',
  `stato` enum('rejected','confirmed','pending') NOT NULL DEFAULT 'pending',
  `tmstmp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_archiviato_route` (`archiviato`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `percorso`
--

LOCK TABLES `percorso` WRITE;
/*!40000 ALTER TABLE `percorso` DISABLE KEYS */;
/*!40000 ALTER TABLE `percorso` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `utente`
--

DROP TABLE IF EXISTS `utente`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `utente` (
  `mail` varchar(128) NOT NULL,
  `pwd` varchar(128) NOT NULL,
  `nome` varchar(128) NOT NULL,
  `cognome` varchar(128) NOT NULL,
  `username` varchar(128) NOT NULL,
  `data_nascita` date NOT NULL,
  `saldo` decimal(6,2) NOT NULL DEFAULT '0.00',
  PRIMARY KEY (`mail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utente`
--

LOCK TABLES `utente` WRITE;
/*!40000 ALTER TABLE `utente` DISABLE KEYS */;
/*!40000 ALTER TABLE `utente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'b4y_user_db'
--

--
-- Dumping routines for database 'b4y_user_db'
--
/*!50003 DROP PROCEDURE IF EXISTS `confirm_it` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `confirm_it`(in id BIGINT)
BEGIN
UPDATE b4y_user_db.itinerario_proposto
SET itinerario_proposto.stato='confirmed'
WHERE itinerario_proposto.id=id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_it_req_info_with_it_prop_id` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_it_req_info_with_it_prop_id`(in it_prop_id BIGINT)
BEGIN
declare it_req_id BIGINT;
select itinerario_richiesto from b4y_user_db.itinerario_proposto where id=it_prop_id into it_req_id;
select i.id, i.ora_inizio, i.ora_fine, i.costo_max, i.distanza, i.utente, i.fermata_lat_partenza,
i.fermata_lon_partenza, i.fermata_lat_arrivo, i.fermata_lon_arrivo, fp.nome, fa.nome
from b4y_user_db.itinerario_richiesto as i
join
b4y_user_db.fermata as fp
on
i.fermata_lat_partenza=fp.lat and i.fermata_lon_partenza=fp.lon
join
b4y_user_db.fermata as fa
on
i.fermata_lat_arrivo=fa.lat and i.fermata_lon_arrivo=fa.lon
where i.id=it_req_id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_prepared_route_info` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_prepared_route_info`(in id bigint)
BEGIN
SELECT scadenza, costo, distanza, orario_partenza_proposto, orario_arrivo_proposto, utente, fermata_lat_partenza, 
fermata_lon_partenza, fp.nome as nome_partenza, fa.nome as nome_arrivo
FROM b4y_user_db.percorso as p 
join 
b4y_user_db.itinerario_proposto as i 
on p.id=i.percorso 
join
b4y_user_db.fermata as fp
on
i.fermata_lat_partenza=fp.lat and i.fermata_lon_partenza=fp.lon
join
b4y_user_db.fermata as fa
on
i.fermata_lat_arrivo=fa.lat and i.fermata_lon_arrivo=fa.lon
where p.id=id and i.percorso=id and p.stato='pending' and i.stato='pending';
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_stops` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_stops`()
BEGIN
SELECT *
FROM 
    b4y_user_db.fermata;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_stops_from_it` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_stops_from_it`(IN id_it BIGINT)
BEGIN
	SELECT ordinamento.numero, ordinamento.fermata_lat, ordinamento.fermata_lon
    FROM percorso, itinerario_proposto as it, ordinamento
    WHERE it.id = id_it AND
		it.percorso = percorso.id AND
        ordinamento.percorso = percorso.id AND
        ordinamento.numero >= (SELECT distinct o2.numero 
								FROM ordinamento as o2
                                WHERE o2.percorso = percorso.id AND
									o2.fermata_lat = it.fermata_lat_partenza AND
                                    o2.fermata_lon = it.fermata_lon_partenza) 
		AND ordinamento.numero <= (SELECT distinct o3.numero 
								FROM ordinamento as o3
                                WHERE o3.percorso = percorso.id AND
									o3.fermata_lat = it.fermata_lat_arrivo AND
                                    o3.fermata_lon = it.fermata_lon_arrivo)
	ORDER BY ordinamento.numero;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_stops_rect` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_stops_rect`(in x DECIMAL(8, 6), in y DECIMAL(8, 6), in height DECIMAL(8, 6), in width DECIMAL(8, 6))
BEGIN
SELECT *
FROM b4y_user_db.fermata as fermata
WHERE fermata.lat < x AND fermata.lat > x - height
AND fermata.lon > y AND fermata.lon < y + width;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `get_user_routes` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `get_user_routes`(in mail varchar(128))
BEGIN
SELECT i.costo, i.orario_partenza_proposto, i.orario_arrivo_proposto, i.stato, p. archiviato, p.stato, p.scadenza, f_start.nome, f_end.nome, i.id
FROM 
b4y_user_db.itinerario_proposto as i join b4y_user_db.percorso as p on i.percorso=p.id
join b4y_user_db.fermata as f_start on i.fermata_lat_partenza=f_start.lat and i.fermata_lon_partenza=f_start.lon 
join b4y_user_db.fermata as f_end on i.fermata_lat_arrivo=f_end.lat and i.fermata_lon_arrivo=f_end.lon
where i.utente=mail;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_it_proposed` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_it_proposed`(in costo DECIMAL(6,2), in distanza DECIMAL(8,4), 
in orario_partenza_proposto DATETIME, in orario_arrivo_proposto DATETIME, in utente VARCHAR(128),
in id_it_requested BIGINT, in id_route BIGINT, in fermata_lat_partenza DECIMAL(8,6), 
in fermata_lon_partenza DECIMAL(8,6), in fermata_lat_arrivo DECIMAL(8,6), in fermata_lon_arrivo DECIMAL(8,6))
BEGIN
insert into b4y_user_db.itinerario_proposto(costo, distanza, orario_partenza_proposto, orario_arrivo_proposto,
stato, utente, itinerario_richiesto, percorso, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo,
fermata_lon_arrivo) values (costo, distanza, orario_partenza_proposto, orario_arrivo_proposto, 'pending', utente,
id_it_requested, id_route, fermata_lat_partenza, fermata_lon_partenza, fermata_lat_arrivo, fermata_lon_arrivo);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_it_req` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_it_req`(in orario DATETIME, in costo_max DECIMAL(6,2), in utente VARCHAR(128), in fermata_lat_partenza DECIMAL(8,6),
in fermata_lon_partenza DECIMAL(8,6), in fermata_lat_arrivo DECIMAL(8,6), in fermata_lon_arrivo DECIMAL(8,6), in isStartHour TINYINT)
BEGIN
	IF isStartHour = 1 THEN 
		insert into b4y_user_db.itinerario_richiesto(ora_inizio, utente, fermata_lat_partenza, fermata_lon_partenza,
		fermata_lat_arrivo, fermata_lon_arrivo, costo_max) values(orario, utente, fermata_lat_partenza, fermata_lon_partenza,
		fermata_lat_arrivo, fermata_lon_arrivo, costo_max);
	ELSE
		insert into b4y_user_db.itinerario_richiesto(ora_fine, utente, fermata_lat_partenza, fermata_lon_partenza,
		fermata_lat_arrivo, fermata_lon_arrivo, costo_max) values(orario, utente, fermata_lat_partenza, fermata_lon_partenza,
		fermata_lat_arrivo, fermata_lon_arrivo, costo_max);
	END IF;
	select last_insert_id();
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_order` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_order`(in numero INT, in percorso BIGINT, in fermata_lat DECIMAL(8,6), 
in fermata_lon DECIMAL(8,6))
BEGIN
insert into b4y_user_db.ordinamento values (numero, percorso, fermata_lat, fermata_lon);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `insert_route` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `insert_route`(in scadenza DATETIME)
BEGIN
#scadenza in formato yyyy-mm-dd hh:mm:ss
insert into b4y_user_db.percorso (scadenza, archiviato, stato, tmstmp) values(scadenza, 0, 'pending', now());
select last_insert_id();
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `login` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `login`(in mail varchar(128), in pwd varchar(128))
BEGIN
SELECT count(*)
FROM 
    b4y_user_db.utente
WHERE
    b4y_user_db.utente.mail = mail
        AND b4y_user_db.utente.pwd = pwd;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `reject_it` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `reject_it`(in id BIGINT)
BEGIN
UPDATE b4y_user_db.itinerario_proposto
SET itinerario_proposto.stato='rejected'
WHERE itinerario_proposto.id=id;
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 DROP PROCEDURE IF EXISTS `sign_up` */;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
CREATE DEFINER=`root`@`localhost` PROCEDURE `sign_up`(in nome varchar(128), in cognome varchar(128), in mail varchar(128), in pwd varchar(128), in username varchar(128), in data_nascita date)
BEGIN
insert into b4y_user_db.utente (nome, cognome, mail, pwd, username, data_nascita) values (nome, cognome, mail, pwd, username, data_nascita);
END ;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-07-11 16:39:18

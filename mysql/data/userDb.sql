CREATE DATABASE  IF NOT EXISTS `b4y_user_db` /*!40100 DEFAULT CHARACTER SET utf8mb3 */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `b4y_user_db`;
-- MySQL dump 10.13  Distrib 8.0.32, for Win64 (x86_64)
--
-- Host: localhost    Database: b4y_user_db
-- ------------------------------------------------------
-- Server version	8.0.32

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
  `saldo` float NOT NULL,
  `timestamp` datetime NOT NULL,
  `percorso` bigint NOT NULL,
  `utente` varchar(128) NOT NULL,
  PRIMARY KEY (`percorso`,`utente`),
  KEY `fk_utente_cb_idx` (`utente`),
  CONSTRAINT `fk_percorso_cb` FOREIGN KEY (`percorso`) REFERENCES `percorso` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_utente_cb` FOREIGN KEY (`utente`) REFERENCES `utente` (`mail`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
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
  `wkt_x` float NOT NULL,
  `wkt_y` float NOT NULL,
  `indirizzo` varchar(256) DEFAULT NULL,
  PRIMARY KEY (`nome`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
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
  `id` bigint NOT NULL,
  `costo` float NOT NULL,
  `distanza` float NOT NULL,
  `orario_partenza_proposto` datetime NOT NULL,
  `orario_arrivo_proposto` datetime NOT NULL,
  `orario_partenza_effettivo` datetime DEFAULT NULL,
  `orario_arrivo_effettivo` datetime DEFAULT NULL,
  `stato` enum('rejected','confirmed','pending') NOT NULL DEFAULT 'pending',
  `utente` varchar(128) NOT NULL,
  `itinerario_richiesto` bigint NOT NULL,
  `fermata_partenza` varchar(256) NOT NULL,
  `fermata_arrivo` varchar(256) NOT NULL,
  `percorso` bigint NOT NULL,
  PRIMARY KEY (`id`,`utente`,`itinerario_richiesto`,`percorso`),
  KEY `fk_fermata_partenza_prop_idx` (`fermata_partenza`) /*!80000 INVISIBLE */,
  KEY `fk_percorso_prop_idx` (`percorso`),
  KEY `idx_data_prop` (`stato`),
  KEY `fk_fermata_arrivo_prop_idx` (`fermata_arrivo`),
  KEY `fk_itinerario_richiesto_user_prop_idx` (`utente`),
  KEY `fk_itinerario_richiesto_id_prop_idx` (`itinerario_richiesto`),
  CONSTRAINT `fk_fermata_arrivo_prop` FOREIGN KEY (`fermata_arrivo`) REFERENCES `fermata` (`nome`) ON UPDATE CASCADE,
  CONSTRAINT `fk_fermata_partenza_prop` FOREIGN KEY (`fermata_partenza`) REFERENCES `fermata` (`nome`) ON UPDATE CASCADE,
  CONSTRAINT `fk_itinerario_richiesto_id_prop` FOREIGN KEY (`itinerario_richiesto`) REFERENCES `itinerario_richiesto` (`id`) ON UPDATE CASCADE,
  CONSTRAINT `fk_itinerario_richiesto_user_prop` FOREIGN KEY (`utente`) REFERENCES `itinerario_richiesto` (`utente`) ON UPDATE CASCADE,
  CONSTRAINT `fk_percorso_prop` FOREIGN KEY (`percorso`) REFERENCES `percorso` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
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
  `ora_inizio` datetime NOT NULL,
  `ora_fine` datetime NOT NULL,
  `costo_max` float DEFAULT NULL,
  `distanza` float NOT NULL,
  `utente` varchar(128) NOT NULL,
  `fermata_partenza` varchar(256) NOT NULL,
  `fermata_arrivo` varchar(256) NOT NULL,
  PRIMARY KEY (`id`,`utente`),
  KEY `fk_fermata_partenza_req_idx` (`fermata_partenza`),
  KEY `fk_utente_req_idx` (`utente`),
  KEY `fk_fermata_arrivo_req_idx` (`fermata_arrivo`),
  CONSTRAINT `fk_fermata_arrivo_req` FOREIGN KEY (`fermata_arrivo`) REFERENCES `fermata` (`nome`) ON UPDATE CASCADE,
  CONSTRAINT `fk_fermata_partenza_req` FOREIGN KEY (`fermata_partenza`) REFERENCES `fermata` (`nome`) ON UPDATE CASCADE,
  CONSTRAINT `fk_utente_req` FOREIGN KEY (`utente`) REFERENCES `utente` (`mail`) ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
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
  `fermata` varchar(256) NOT NULL,
  PRIMARY KEY (`fermata`,`percorso`),
  KEY `fk_percorso_ord_idx` (`percorso`),
  CONSTRAINT `fk_fermata_ord` FOREIGN KEY (`fermata`) REFERENCES `fermata` (`nome`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_percorso_ord` FOREIGN KEY (`percorso`) REFERENCES `percorso` (`id`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
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
  `timestamp` datetime DEFAULT NULL,
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
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
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
  `id` bigint NOT NULL,
  `scadenza` datetime NOT NULL,
  `archiviato` tinyint NOT NULL DEFAULT '0',
  `stato` enum('rejected','confirmed','pending') NOT NULL DEFAULT 'pending',
  `timestamp` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_archiviato_route` (`archiviato`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
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
  `saldo` float NOT NULL DEFAULT '0',
  PRIMARY KEY (`mail`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `utente`
--

LOCK TABLES `utente` WRITE;
/*!40000 ALTER TABLE `utente` DISABLE KEYS */;
INSERT INTO `utente` VALUES ('prova@gmail.com','1234','prova','prova','prova','1997-07-19',0);
/*!40000 ALTER TABLE `utente` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'b4y_user_db'
--

--
-- Dumping routines for database 'b4y_user_db'
--
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

-- Dump completed on 2023-06-02 17:54:26

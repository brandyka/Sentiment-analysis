-- MySQL dump 10.13  Distrib 8.0.42, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: sentiment_db
-- ------------------------------------------------------
-- Server version	8.0.42

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
-- Table structure for table `sentiment_results`
--

DROP TABLE IF EXISTS `sentiment_results`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sentiment_results` (
  `id` int NOT NULL AUTO_INCREMENT,
  `text_input` text NOT NULL,
  `prediction` tinyint DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sentiment_results`
--

LOCK TABLES `sentiment_results` WRITE;
/*!40000 ALTER TABLE `sentiment_results` DISABLE KEYS */;
INSERT INTO `sentiment_results` VALUES (1,'Food was great i really like with it thanks',2,'2025-10-19 15:34:16'),(2,'the food was bad i don\'t like it not reccomended',1,'2025-10-19 15:35:37'),(3,'The staff were super friendly and made me feel welcome.',2,'2025-10-19 15:40:56'),(4,'I loved the cozy atmosphere and the music selection was great.',2,'2025-10-19 15:41:16'),(5,'The dessert was heavenly — I’ll definitely come back for more!',2,'2025-10-19 15:41:25'),(6,'The food was cold and tasteless when it arrived.',2,'2025-10-19 15:41:42'),(7,'The staff were rude and completely ignored our table.',1,'2025-10-19 15:41:58'),(8,'The portion size was tiny compared to the price.',1,'2025-10-19 15:42:10'),(9,'Not reccomended seller i was bought a new laptop but he give me a second stuff',1,'2025-10-19 16:51:13'),(10,'Nice product five stars',2,'2025-10-19 16:51:28'),(11,'My drink tasted watered down and had no flavor at all.',2,'2025-10-20 05:07:57'),(12,'hey messed up my order twice and didn’t even apologize.',1,'2025-10-20 05:08:05'),(13,'he delivery was fast, and the packaging was neat and eco-friendly.',2,'2025-10-20 05:08:42'),(14,'The coffee was smooth and rich, just the way I like it.',2,'2025-10-20 05:08:55'),(15,'Totally disappointed — not coming back again.',1,'2025-10-20 05:09:04'),(16,'The burger was burnt on the outside and raw inside — disgusting.',1,'2025-10-20 05:09:14'),(17,'I loved how the waiter remembered my usual order — such great service!',2,'2025-10-20 07:52:03'),(18,'he sushi was so fresh it literally melted in my mouth.',2,'2025-10-20 07:52:09'),(19,'Our waiter seemed annoyed the entire time and barely spoke to us.',1,'2025-10-20 07:53:20'),(20,'I found a hair in my food — that’s unacceptable.',1,'2025-10-20 07:54:04');
/*!40000 ALTER TABLE `sentiment_results` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-10-20 17:52:02

-- MySQL dump 10.13  Distrib 8.0.45, for Linux (x86_64)
--
-- Host: localhost    Database: PD_db
-- ------------------------------------------------------
-- Server version	8.0.45-0ubuntu0.22.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `pd_users`
--

DROP TABLE IF EXISTS `pd_users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `pd_users` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `name` varchar(64) NOT NULL,
  `account` varchar(64) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `role` varchar(32) NOT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `email` varchar(128) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updated_at` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` tinyint DEFAULT '0' COMMENT '0=正常,1=冻结,2=已注销',
  PRIMARY KEY (`id`),
  UNIQUE KEY `account` (`account`),
  CONSTRAINT `pd_users_chk_1` CHECK ((`role` in (_utf8mb4'管理员',_utf8mb4'大区经理',_utf8mb4'自营库管理',_utf8mb4'财务',_utf8mb4'会计')))
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `pd_users`
--

LOCK TABLES `pd_users` WRITE;
/*!40000 ALTER TABLE `pd_users` DISABLE KEYS */;
INSERT INTO `pd_users` VALUES (1,'余诗晨','admin','$2b$12$v1Hu/6dLCf.EZiNYoo4vEuotgv8psMTghgG/UFDq0li61AAcCviVe','管理员','17280180659','ysc025316@qq.com','2026-02-25 02:29:29','2026-03-10 12:59:24',0),(2,'孔翔','kxnb','$2b$12$9G6vxV02KC2DffB3867aRO65VEtLDJngN9pSbwGNmZJgLfauiwUpa','大区经理','19700784868',NULL,'2026-03-10 12:58:57','2026-03-10 12:58:57',0),(3,'高美良','mhmt','$2b$12$08a.vY9e1j/S2o5SQ.MzA.A.qPzhQDaWxzLB1P2nlaBwsopaYW3rS','管理员','15489787898',NULL,'2026-03-11 08:09:18','2026-03-11 08:09:18',0),(4,'黄德如','hdr','$2b$12$a213SHWKGekejASRBiHzX.qD0smL531VRFqB/GQir5z56DQStMKxu','管理员','16448789484',NULL,'2026-03-11 08:10:30','2026-03-11 08:10:30',0),(5,'雨慧','yuhui','$2b$12$SYsHe1uIirMQIc.QAJx1auhmklUUB/srpmPmos3pH0ULxQtGajsVG','管理员','15996394511',NULL,'2026-03-12 09:18:49','2026-03-12 09:18:49',0),(6,'诸葛','zhuge','$2b$12$0iTExYsPh.DL23m8k/JNNOJ.JeybIjwwkXnjIdJIjA39TDRI.0T/q','管理员','15996396666',NULL,'2026-03-12 09:21:10','2026-03-12 09:21:10',0),(7,'胜达','jsd','$2b$12$gudnEDctj4hAxbmI0ihuEeYAxH76s9BASJbSf9oi6eQaoYTyGd58K','管理员','15996396668',NULL,'2026-03-12 09:22:00','2026-03-12 09:22:00',0),(8,'书书','shushu','$2b$12$XLsFxdq/nY2ucDKOp.96tuiAcb/VIurxxoBxahNhmXaI4GDsYNiAu','管理员','15996399999',NULL,'2026-03-12 09:30:25','2026-03-12 09:30:25',0);
/*!40000 ALTER TABLE `pd_users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-03-12 19:26:32

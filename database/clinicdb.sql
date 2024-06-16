-- MySQL dump 10.13  Distrib 8.0.34, for Win64 (x86_64)
--
-- Host: localhost    Database: clinicdb
-- ------------------------------------------------------
-- Server version	8.0.35

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
-- Table structure for table `appointments`
--

DROP TABLE IF EXISTS `appointments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `appointments` (
  `id` int NOT NULL AUTO_INCREMENT,
  `patient_id` int NOT NULL,
  `patient_name` varchar(255) NOT NULL,
  `patient_contact_number` varchar(20) NOT NULL,
  `patient_email` varchar(255) NOT NULL,
  `doctor_id` int NOT NULL,
  `doctor_name` varchar(255) NOT NULL,
  `doctor_contact_number` varchar(20) NOT NULL,
  `appointment_date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `patient_id` (`patient_id`),
  KEY `doctor_id` (`doctor_id`),
  CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`patient_id`) REFERENCES `patient` (`id`),
  CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`doctor_id`) REFERENCES `doctor` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `appointments`
--

LOCK TABLES `appointments` WRITE;
/*!40000 ALTER TABLE `appointments` DISABLE KEYS */;
INSERT INTO `appointments` VALUES (4,2,'Bilal Mashmoushi','+961 70 544 073','bilal@gmail.com',6,'Mohammad Al-Mokdad','+961 76 032 425','2024-05-19'),(5,3,'Mohammad Al-Mokdad','+961 76 032 425','mhmdmkdd25@gmail.com',7,'bilal mashmoushi','66','2024-05-20');
/*!40000 ALTER TABLE `appointments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `doctor`
--

DROP TABLE IF EXISTS `doctor`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `doctor` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `contact_number` varchar(20) NOT NULL,
  `email` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `speciality` varchar(255) NOT NULL,
  `date_of_birth` date NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `doctor`
--

LOCK TABLES `doctor` WRITE;
/*!40000 ALTER TABLE `doctor` DISABLE KEYS */;
INSERT INTO `doctor` VALUES (6,'Mohammad Al-Mokdad','+961 76 032 425','mhmdmkdd25@gmail.com','Beirut','Cardiology','2004-02-26'),(7,'bilal mashmoushi','961+ 70 544 073','bilal@gmail.com','lebanon','Heart surgeon','2003-09-07');
/*!40000 ALTER TABLE `doctor` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `insurance`
--

DROP TABLE IF EXISTS `insurance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `insurance` (
  `id` int NOT NULL AUTO_INCREMENT,
  `insurance_name` varchar(255) NOT NULL,
  `coverage_details` text,
  `contact_number` varchar(20) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `insurance`
--

LOCK TABLES `insurance` WRITE;
/*!40000 ALTER TABLE `insurance` DISABLE KEYS */;
INSERT INTO `insurance` VALUES (1,'HealthPlus','Full coverage including dental and vision','123-456-7890','123 Health St, Wellness City, TX'),(2,'MediCare','Coverage for hospitalization and outpatient services','234-567-8901','234 Medi Rd, Careville, CA'),(3,'WellCare','Comprehensive health and wellness coverage','345-678-9012','345 Well Ave, Healthtown, NY'),(4,'SecureHealth','Emergency and specialist coverage','456-789-0123','456 Secure Ln, Safety City, FL'),(5,'PrimeHealth','Basic and preventive care coverage','567-890-1234','567 Prime Blvd, Protectionville, IL'),(6,'LifeGuard','Full coverage including maternity and pediatric care','678-901-2345','678 Life Dr, Guard City, GA'),(7,'VitalCare','Coverage for chronic illnesses and medications','789-012-3456','789 Vital Way, Wellness City, TX');
/*!40000 ALTER TABLE `insurance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medicines`
--

DROP TABLE IF EXISTS `medicines`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medicines` (
  `id` int NOT NULL AUTO_INCREMENT,
  `medicine_name` varchar(255) NOT NULL,
  `manufacturer` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  `expiration_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medicines`
--

LOCK TABLES `medicines` WRITE;
/*!40000 ALTER TABLE `medicines` DISABLE KEYS */;
INSERT INTO `medicines` VALUES (1,'Aspirin','Bayer',5.99,'2025-12-31'),(2,'Paracetamol','Tylenol',3.49,'2024-06-30'),(3,'Ibuprofen','Advil',6.99,'2026-01-15'),(4,'Amoxicillin','Pfizer',12.50,'2025-11-20'),(5,'Metformin','Merck',15.75,'2024-03-10'),(6,'Lisinopril','Novartis',20.00,'2023-09-25'),(7,'Atorvastatin','Pfizer',22.50,'2025-07-18'),(8,'Omeprazole','AstraZeneca',8.99,'2024-05-30');
/*!40000 ALTER TABLE `medicines` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `patient`
--

DROP TABLE IF EXISTS `patient`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `patient` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `date_of_birth` date NOT NULL,
  `gender` varchar(10) NOT NULL,
  `address` varchar(255) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `email` varchar(255) NOT NULL,
  `nationality` varchar(255) NOT NULL,
  `profession` varchar(255) NOT NULL,
  `blood_type` varchar(10) NOT NULL,
  `religion` varchar(255) NOT NULL,
  `garantor_name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `patient`
--

LOCK TABLES `patient` WRITE;
/*!40000 ALTER TABLE `patient` DISABLE KEYS */;
INSERT INTO `patient` VALUES (2,'Bilal Mashmoushi','2003-05-09','Male','Beirut','+961 70 544 073','bilalmashmoushi@gmail.com','Lebanese','Software Engineer','B','Muslim','GOD'),(3,'Mohammad Al-Mokdad','2004-04-26','Male','Beirut','+961 76 032 425','mhmdmkdd25@gmail.com','Lebanese','Software Engineer','O+','Muslim','Talal');
/*!40000 ALTER TABLE `patient` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `speciality`
--

DROP TABLE IF EXISTS `speciality`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `speciality` (
  `id` int NOT NULL AUTO_INCREMENT,
  `speciality_name` varchar(255) NOT NULL,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `speciality`
--

LOCK TABLES `speciality` WRITE;
/*!40000 ALTER TABLE `speciality` DISABLE KEYS */;
INSERT INTO `speciality` VALUES (1,'Cardiology','Medical specialty dealing with disorders of the heart'),(2,'Dermatology','Branch of medicine dealing with the skin'),(3,'Neurology','Medical specialty dealing with disorders of the nervous system'),(4,'Orthopedics','Branch of medicine dealing with the correction of deformities of bones or muscles'),(5,'Pediatrics','Branch of medicine dealing with children and their diseases'),(6,'Psychiatry','Medical specialty dealing with mental health'),(7,'Oncology','Branch of medicine dealing with cancer'),(8,'Gynecology','Medical specialty dealing with the health of the female reproductive systems');
/*!40000 ALTER TABLE `speciality` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `user`
--

DROP TABLE IF EXISTS `user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `user`
--

LOCK TABLES `user` WRITE;
/*!40000 ALTER TABLE `user` DISABLE KEYS */;
INSERT INTO `user` VALUES (2,'admin','admin','$2b$12$iyscjJep0Jd7p79nIkm9xemL/DuPie5sV3PuFhQPD2rhtQ5lIujZu'),(7,'Bilal Mashmoushi','bam604@usal.edu.lb','$2b$12$Y.hkmZO2tNV1WV/HQbk4U.Y5q0Lr3u3/4Gm9oUVL3QcOst.cd9ywu'),(8,'Ahmad Sleem','ahs450@usal.edu.lb','$2b$12$5E1LfogMe4oDtAyi7fzfjeKnBpb3DZJqKaYFHrq2G.3Su6P3yTOtG'),(9,'Mohammad Al-Mokdad','mhmdmkdd25@gmail.com','$2b$12$cbtCshAet6ryDJkK/X0XqenzjPlXN1.U2HkSSHn/QqxKM/skxyrn6');
/*!40000 ALTER TABLE `user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-05-19 23:30:26

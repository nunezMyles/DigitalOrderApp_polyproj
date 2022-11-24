-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: localhost    Database: project_v2
-- ------------------------------------------------------
-- Server version	8.0.28

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
-- Table structure for table `customer`
--

DROP TABLE IF EXISTS `customer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer` (
  `CustomerID` int NOT NULL AUTO_INCREMENT,
  `Customer_Name` varchar(45) NOT NULL,
  `Customer_Address` varchar(45) NOT NULL,
  `Region` varchar(45) NOT NULL,
  `Unit_Number` varchar(45) NOT NULL,
  `Postal_Code` int NOT NULL,
  `Customer_Phone` varchar(45) NOT NULL,
  PRIMARY KEY (`CustomerID`),
  UNIQUE KEY `Customer_Phone_UNIQUE` (`Customer_Phone`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer`
--

LOCK TABLES `customer` WRITE;
/*!40000 ALTER TABLE `customer` DISABLE KEYS */;
INSERT INTO `customer` VALUES (1,'Cheers Hougang Central','810 Hougang Central','North East','#03-10',530810,'67589651'),(3,'bro','somewhere 711','North East','#06-14',770234,'90352532');
/*!40000 ALTER TABLE `customer` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `customer_order`
--

DROP TABLE IF EXISTS `customer_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `customer_order` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `Order_Date` datetime NOT NULL,
  `CustomerID` int NOT NULL,
  `Revenue` decimal(5,2) NOT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `FKCustomerID` (`CustomerID`),
  CONSTRAINT `FKCustomerID` FOREIGN KEY (`CustomerID`) REFERENCES `customer` (`CustomerID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `customer_order`
--

LOCK TABLES `customer_order` WRITE;
/*!40000 ALTER TABLE `customer_order` DISABLE KEYS */;
INSERT INTO `customer_order` VALUES (10,'2022-07-23 15:39:26',3,16.00),(12,'2022-07-30 17:38:24',1,8.00);
/*!40000 ALTER TABLE `customer_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `customer_sales_info`
--

DROP TABLE IF EXISTS `customer_sales_info`;
/*!50001 DROP VIEW IF EXISTS `customer_sales_info`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `customer_sales_info` AS SELECT 
 1 AS `OrderID`,
 1 AS `CustomerID`,
 1 AS `Customer_Name`,
 1 AS `Region`,
 1 AS `Revenue`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `order_deliver`
--

DROP TABLE IF EXISTS `order_deliver`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_deliver` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `Deliverer_StaffID` int DEFAULT NULL,
  `Deliverer_Name` varchar(45) DEFAULT NULL,
  `Delivery_Status` varchar(9) NOT NULL,
  `Delivery_Date` datetime DEFAULT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `FKStaffID_idx` (`Deliverer_StaffID`),
  CONSTRAINT `FKOrderID_od` FOREIGN KEY (`OrderID`) REFERENCES `customer_order` (`OrderID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FKStaffID_od` FOREIGN KEY (`Deliverer_StaffID`) REFERENCES `staff` (`StaffID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_deliver`
--

LOCK TABLES `order_deliver` WRITE;
/*!40000 ALTER TABLE `order_deliver` DISABLE KEYS */;
INSERT INTO `order_deliver` VALUES (10,1,'Nunez','Fulfilled','2022-07-30 17:37:37'),(12,NULL,NULL,'Pending',NULL);
/*!40000 ALTER TABLE `order_deliver` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `order_info`
--

DROP TABLE IF EXISTS `order_info`;
/*!50001 DROP VIEW IF EXISTS `order_info`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `order_info` AS SELECT 
 1 AS `OrderID`,
 1 AS `Order_Date`,
 1 AS `CustomerID`,
 1 AS `Packing_Status`,
 1 AS `Delivery_Status`,
 1 AS `Packer_StaffID`,
 1 AS `Packer_Name`,
 1 AS `Pack_Date`,
 1 AS `Deliverer_StaffID`,
 1 AS `Deliverer_Name`,
 1 AS `Delivery_Date`,
 1 AS `Merchandiser_StaffID`,
 1 AS `Merchandiser_Name`,
 1 AS `ProductID`,
 1 AS `Product_Quantity`,
 1 AS `Product_Revenue`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `order_merchandise`
--

DROP TABLE IF EXISTS `order_merchandise`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_merchandise` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `Merchandiser_StaffID` int NOT NULL,
  `Merchandiser_Name` varchar(45) NOT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `FKStaffID_idx` (`Merchandiser_StaffID`),
  CONSTRAINT `FKOrderID_om` FOREIGN KEY (`OrderID`) REFERENCES `customer_order` (`OrderID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FKStaffID_om` FOREIGN KEY (`Merchandiser_StaffID`) REFERENCES `staff` (`StaffID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_merchandise`
--

LOCK TABLES `order_merchandise` WRITE;
/*!40000 ALTER TABLE `order_merchandise` DISABLE KEYS */;
INSERT INTO `order_merchandise` VALUES (10,1,'Nunez'),(12,1,'Nunez');
/*!40000 ALTER TABLE `order_merchandise` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_pack`
--

DROP TABLE IF EXISTS `order_pack`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_pack` (
  `OrderID` int NOT NULL AUTO_INCREMENT,
  `Packer_StaffID` int DEFAULT NULL,
  `Packer_Name` varchar(45) DEFAULT NULL,
  `Packing_Status` varchar(9) NOT NULL,
  `Pack_Date` datetime DEFAULT NULL,
  PRIMARY KEY (`OrderID`),
  KEY `FKStaffID_idx` (`Packer_StaffID`),
  CONSTRAINT `FKOrderID_op` FOREIGN KEY (`OrderID`) REFERENCES `customer_order` (`OrderID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FKStaffID_op` FOREIGN KEY (`Packer_StaffID`) REFERENCES `staff` (`StaffID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_pack`
--

LOCK TABLES `order_pack` WRITE;
/*!40000 ALTER TABLE `order_pack` DISABLE KEYS */;
INSERT INTO `order_pack` VALUES (10,1,'Nunez','Fulfilled','2022-07-25 18:48:54'),(12,1,'Nunez','Fulfilled','2022-07-30 17:41:10');
/*!40000 ALTER TABLE `order_pack` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `order_product`
--

DROP TABLE IF EXISTS `order_product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `order_product` (
  `OrderID` int NOT NULL,
  `ProductID` int NOT NULL,
  `Product_Quantity` int NOT NULL,
  `Product_Revenue` decimal(5,2) NOT NULL,
  PRIMARY KEY (`OrderID`,`ProductID`),
  KEY `FKProductID_opd` (`ProductID`),
  CONSTRAINT `FKOrderID_opd` FOREIGN KEY (`OrderID`) REFERENCES `customer_order` (`OrderID`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `FKProductID_opd` FOREIGN KEY (`ProductID`) REFERENCES `product` (`ProductID`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `order_product`
--

LOCK TABLES `order_product` WRITE;
/*!40000 ALTER TABLE `order_product` DISABLE KEYS */;
INSERT INTO `order_product` VALUES (10,4,20,16.00),(12,4,10,8.00);
/*!40000 ALTER TABLE `order_product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `order_product_info`
--

DROP TABLE IF EXISTS `order_product_info`;
/*!50001 DROP VIEW IF EXISTS `order_product_info`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `order_product_info` AS SELECT 
 1 AS `OrderID`,
 1 AS `ProductID`,
 1 AS `Product_Quantity`,
 1 AS `Product_Revenue`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `product`
--

DROP TABLE IF EXISTS `product`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `product` (
  `ProductID` int NOT NULL AUTO_INCREMENT,
  `Category` varchar(45) NOT NULL,
  `Item` varchar(45) NOT NULL,
  `Product_Code` varchar(45) NOT NULL,
  `Unit_Price` decimal(5,2) NOT NULL,
  `Stock_Level` int NOT NULL,
  PRIMARY KEY (`ProductID`),
  UNIQUE KEY `Product_Code_UNIQUE` (`Product_Code`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `product`
--

LOCK TABLES `product` WRITE;
/*!40000 ALTER TABLE `product` DISABLE KEYS */;
INSERT INTO `product` VALUES (1,'Diary','Milk','DKRS35501',2.30,500),(2,'Bakery','Bread','BVR30221',2.70,500),(3,'Canned Goods','Tomato','CVOMS3681',1.00,500),(4,'Condiments','Fine Salt','CON2ASR801',0.80,470),(5,'Beverages','Green Tea','BRTE39861',5.00,500);
/*!40000 ALTER TABLE `product` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Temporary view structure for view `product_info`
--

DROP TABLE IF EXISTS `product_info`;
/*!50001 DROP VIEW IF EXISTS `product_info`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `product_info` AS SELECT 
 1 AS `ProductID`,
 1 AS `Category`,
 1 AS `Item`,
 1 AS `Product_Code`,
 1 AS `Unit_Price`,
 1 AS `Stock_Level`*/;
SET character_set_client = @saved_cs_client;

--
-- Temporary view structure for view `product_sales_info`
--

DROP TABLE IF EXISTS `product_sales_info`;
/*!50001 DROP VIEW IF EXISTS `product_sales_info`*/;
SET @saved_cs_client     = @@character_set_client;
/*!50503 SET character_set_client = utf8mb4 */;
/*!50001 CREATE VIEW `product_sales_info` AS SELECT 
 1 AS `OrderID`,
 1 AS `ProductID`,
 1 AS `Category`,
 1 AS `Product_Revenue`*/;
SET character_set_client = @saved_cs_client;

--
-- Table structure for table `staff`
--

DROP TABLE IF EXISTS `staff`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `staff` (
  `StaffID` int NOT NULL AUTO_INCREMENT,
  `Staff_Name` varchar(45) NOT NULL,
  `Role` varchar(45) NOT NULL,
  `NRIC` varchar(9) NOT NULL,
  `Username` varchar(45) DEFAULT NULL,
  `Password` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`StaffID`),
  UNIQUE KEY `NRIC_UNIQUE` (`NRIC`),
  UNIQUE KEY `Username_UNIQUE` (`Username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `staff`
--

LOCK TABLES `staff` WRITE;
/*!40000 ALTER TABLE `staff` DISABLE KEYS */;
INSERT INTO `staff` VALUES (1,'Nunez','Admin','T0332991C','myles','myles991C'),(5,'joe','Packer','T0112334C','joe','joe123'),(6,'Ossas','Manager','T0124234C','ossas','ossas123'),(7,'cheryl','Merchandiser','T0244323C','cheryl','cheryl123'),(8,'lex','Deliverer','T2109421E','lex','lex123');
/*!40000 ALTER TABLE `staff` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping routines for database 'project_v2'
--

--
-- Final view structure for view `customer_sales_info`
--

/*!50001 DROP VIEW IF EXISTS `customer_sales_info`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `customer_sales_info` AS select `customer_order`.`OrderID` AS `OrderID`,`customer`.`CustomerID` AS `CustomerID`,`customer`.`Customer_Name` AS `Customer_Name`,`customer`.`Region` AS `Region`,`customer_order`.`Revenue` AS `Revenue` from (`customer_order` join `customer` on((`customer_order`.`CustomerID` = `customer`.`CustomerID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `order_info`
--

/*!50001 DROP VIEW IF EXISTS `order_info`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `order_info` AS select `customer_order`.`OrderID` AS `OrderID`,`customer_order`.`Order_Date` AS `Order_Date`,`customer_order`.`CustomerID` AS `CustomerID`,`order_pack`.`Packing_Status` AS `Packing_Status`,`order_deliver`.`Delivery_Status` AS `Delivery_Status`,`order_pack`.`Packer_StaffID` AS `Packer_StaffID`,`order_pack`.`Packer_Name` AS `Packer_Name`,`order_pack`.`Pack_Date` AS `Pack_Date`,`order_deliver`.`Deliverer_StaffID` AS `Deliverer_StaffID`,`order_deliver`.`Deliverer_Name` AS `Deliverer_Name`,`order_deliver`.`Delivery_Date` AS `Delivery_Date`,`order_merchandise`.`Merchandiser_StaffID` AS `Merchandiser_StaffID`,`order_merchandise`.`Merchandiser_Name` AS `Merchandiser_Name`,`order_product`.`ProductID` AS `ProductID`,`order_product`.`Product_Quantity` AS `Product_Quantity`,`order_product`.`Product_Revenue` AS `Product_Revenue` from ((((`customer_order` join `order_deliver` on((`customer_order`.`OrderID` = `order_deliver`.`OrderID`))) join `order_pack` on((`customer_order`.`OrderID` = `order_pack`.`OrderID`))) join `order_merchandise` on((`customer_order`.`OrderID` = `order_merchandise`.`OrderID`))) join `order_product` on((`customer_order`.`OrderID` = `order_product`.`OrderID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `order_product_info`
--

/*!50001 DROP VIEW IF EXISTS `order_product_info`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `order_product_info` AS select `order_product`.`OrderID` AS `OrderID`,`order_product`.`ProductID` AS `ProductID`,`order_product`.`Product_Quantity` AS `Product_Quantity`,`order_product`.`Product_Revenue` AS `Product_Revenue` from `order_product` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `product_info`
--

/*!50001 DROP VIEW IF EXISTS `product_info`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `product_info` AS select `product`.`ProductID` AS `ProductID`,`product`.`Category` AS `Category`,`product`.`Item` AS `Item`,`product`.`Product_Code` AS `Product_Code`,`product`.`Unit_Price` AS `Unit_Price`,`product`.`Stock_Level` AS `Stock_Level` from `product` */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;

--
-- Final view structure for view `product_sales_info`
--

/*!50001 DROP VIEW IF EXISTS `product_sales_info`*/;
/*!50001 SET @saved_cs_client          = @@character_set_client */;
/*!50001 SET @saved_cs_results         = @@character_set_results */;
/*!50001 SET @saved_col_connection     = @@collation_connection */;
/*!50001 SET character_set_client      = utf8mb4 */;
/*!50001 SET character_set_results     = utf8mb4 */;
/*!50001 SET collation_connection      = utf8mb4_0900_ai_ci */;
/*!50001 CREATE ALGORITHM=UNDEFINED */
/*!50013 DEFINER=`root`@`localhost` SQL SECURITY DEFINER */
/*!50001 VIEW `product_sales_info` AS select `order_product`.`OrderID` AS `OrderID`,`product`.`ProductID` AS `ProductID`,`product`.`Category` AS `Category`,`order_product`.`Product_Revenue` AS `Product_Revenue` from (`product` join `order_product` on((`product`.`ProductID` = `order_product`.`ProductID`))) */;
/*!50001 SET character_set_client      = @saved_cs_client */;
/*!50001 SET character_set_results     = @saved_cs_results */;
/*!50001 SET collation_connection      = @saved_col_connection */;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-08-12 21:52:13

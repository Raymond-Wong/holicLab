-- MySQL dump 10.13  Distrib 5.6.27, for debian-linux-gnu (i686)
--
-- Host: localhost    Database: holicLab
-- ------------------------------------------------------
-- Server version	5.6.27-0ubuntu1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(80) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_group_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `group_id` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_5f412f9a` (`group_id`),
  KEY `auth_group_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `group_id_refs_id_f4b32aac` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `permission_id_refs_id_6ba0f519` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content_type_id` (`content_type_id`,`codename`),
  KEY `auth_permission_37ef4eb4` (`content_type_id`),
  CONSTRAINT `content_type_id_refs_id_d043b34a` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=55 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add permission',1,'add_permission'),(2,'Can change permission',1,'change_permission'),(3,'Can delete permission',1,'delete_permission'),(4,'Can add group',2,'add_group'),(5,'Can change group',2,'change_group'),(6,'Can delete group',2,'delete_group'),(7,'Can add user',3,'add_user'),(8,'Can change user',3,'change_user'),(9,'Can delete user',3,'delete_user'),(10,'Can add content type',4,'add_contenttype'),(11,'Can change content type',4,'change_contenttype'),(12,'Can delete content type',4,'delete_contenttype'),(13,'Can add session',5,'add_session'),(14,'Can change session',5,'change_session'),(15,'Can delete session',5,'delete_session'),(16,'Can add site',6,'add_site'),(17,'Can change site',6,'change_site'),(18,'Can delete site',6,'delete_site'),(19,'Can add user',7,'add_user'),(20,'Can change user',7,'change_user'),(21,'Can delete user',7,'delete_user'),(22,'Can add coupon',8,'add_coupon'),(23,'Can change coupon',8,'change_coupon'),(24,'Can delete coupon',8,'delete_coupon'),(25,'Can add time_ limit_ coupon',9,'add_time_limit_coupon'),(26,'Can change time_ limit_ coupon',9,'change_time_limit_coupon'),(27,'Can delete time_ limit_ coupon',9,'delete_time_limit_coupon'),(28,'Can add tries_ limit_ coupon',10,'add_tries_limit_coupon'),(29,'Can change tries_ limit_ coupon',10,'change_tries_limit_coupon'),(30,'Can delete tries_ limit_ coupon',10,'delete_tries_limit_coupon'),(31,'Can add shop',11,'add_shop'),(32,'Can change shop',11,'change_shop'),(33,'Can delete shop',11,'delete_shop'),(34,'Can add course',12,'add_course'),(35,'Can change course',12,'change_course'),(36,'Can delete course',12,'delete_course'),(37,'Can add time_ bucket',13,'add_time_bucket'),(38,'Can change time_ bucket',13,'change_time_bucket'),(39,'Can delete time_ bucket',13,'delete_time_bucket'),(40,'Can add bookable_ time',14,'add_bookable_time'),(41,'Can change bookable_ time',14,'change_bookable_time'),(42,'Can delete bookable_ time',14,'delete_bookable_time'),(43,'Can add service',15,'add_service'),(44,'Can change service',15,'change_service'),(45,'Can delete service',15,'delete_service'),(46,'Can add password',16,'add_password'),(47,'Can change password',16,'change_password'),(48,'Can delete password',16,'delete_password'),(49,'Can add order',17,'add_order'),(50,'Can change order',17,'change_order'),(51,'Can delete order',17,'delete_order'),(52,'Can add image',18,'add_image'),(53,'Can change image',18,'change_image'),(54,'Can delete image',18,'delete_image');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime NOT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(30) NOT NULL,
  `first_name` varchar(30) NOT NULL,
  `last_name` varchar(30) NOT NULL,
  `email` varchar(75) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_groups`
--

DROP TABLE IF EXISTS `auth_user_groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_groups` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `group_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`group_id`),
  KEY `auth_user_groups_6340c63c` (`user_id`),
  KEY `auth_user_groups_5f412f9a` (`group_id`),
  CONSTRAINT `group_id_refs_id_274b862c` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  CONSTRAINT `user_id_refs_id_40c41112` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_groups`
--

LOCK TABLES `auth_user_groups` WRITE;
/*!40000 ALTER TABLE `auth_user_groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `user_id` (`user_id`,`permission_id`),
  KEY `auth_user_user_permissions_6340c63c` (`user_id`),
  KEY `auth_user_user_permissions_83d7f98b` (`permission_id`),
  CONSTRAINT `permission_id_refs_id_35d9ac25` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `user_id_refs_id_4dc23c39` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `app_label` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'permission','auth','permission'),(2,'group','auth','group'),(3,'user','auth','user'),(4,'content type','contenttypes','contenttype'),(5,'session','sessions','session'),(6,'site','sites','site'),(7,'user','holicLab','user'),(8,'coupon','holicLab','coupon'),(9,'time_ limit_ coupon','holicLab','time_limit_coupon'),(10,'tries_ limit_ coupon','holicLab','tries_limit_coupon'),(11,'shop','holicLab','shop'),(12,'course','holicLab','course'),(13,'time_ bucket','holicLab','time_bucket'),(14,'bookable_ time','holicLab','bookable_time'),(15,'service','holicLab','service'),(16,'password','holicLab','password'),(17,'order','holicLab','order'),(18,'image','holicLab','image');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_b7b81f0c` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
INSERT INTO `django_session` VALUES ('70uyk2otxgjc1z8j0iqso52wr4yg9p3h','MWNiYmYwYzNlY2I3MjdkZWJhMTZjNTI1NDg0Y2QyMjgwMDMxNjYyNzqAAn1xAVUHbG9naW5lZHECiHMu','2016-07-13 16:17:08');
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_site`
--

DROP TABLE IF EXISTS `django_site`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `django_site` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `domain` varchar(100) NOT NULL,
  `name` varchar(50) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_site`
--

LOCK TABLES `django_site` WRITE;
/*!40000 ALTER TABLE `django_site` DISABLE KEYS */;
INSERT INTO `django_site` VALUES (1,'example.com','example.com');
/*!40000 ALTER TABLE `django_site` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `holicLab_bookable_time`
--

DROP TABLE IF EXISTS `holicLab_bookable_time`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `holicLab_bookable_time` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `course_id` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `occupation` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  KEY `holicLab_bookable_time_6234103b` (`course_id`),
  CONSTRAINT `course_id_refs_id_bbafad3d` FOREIGN KEY (`course_id`) REFERENCES `holicLab_course` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `holicLab_bookable_time`
--

LOCK TABLES `holicLab_bookable_time` WRITE;
/*!40000 ALTER TABLE `holicLab_bookable_time` DISABLE KEYS */;
/*!40000 ALTER TABLE `holicLab_bookable_time` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `holicLab_coupon`
--

DROP TABLE IF EXISTS `holicLab_coupon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `holicLab_coupon` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `price` int(10) unsigned NOT NULL,
  `description` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `holicLab_coupon_6340c63c` (`user_id`),
  CONSTRAINT `user_id_refs_id_71986aca` FOREIGN KEY (`user_id`) REFERENCES `holicLab_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `holicLab_coupon`
--

LOCK TABLES `holicLab_coupon` WRITE;
/*!40000 ALTER TABLE `holicLab_coupon` DISABLE KEYS */;
/*!40000 ALTER TABLE `holicLab_coupon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `holicLab_course`
--

DROP TABLE IF EXISTS `holicLab_course`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `holicLab_course` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `coach_description` longtext NOT NULL,
  `coach_cover` longtext NOT NULL,
  `cover_type` varchar(5) NOT NULL,
  `cover` longtext NOT NULL,
  `price` int(10) unsigned NOT NULL,
  `capacity` int(10) unsigned NOT NULL,
  `shop_id` int(11) NOT NULL,
  `last_modified_time` datetime NOT NULL,
  `state` varchar(10) NOT NULL,
  `notice` longtext NOT NULL,
  PRIMARY KEY (`id`),
  KEY `holicLab_course_74d4252d` (`shop_id`),
  CONSTRAINT `shop_id_refs_id_a02511f0` FOREIGN KEY (`shop_id`) REFERENCES `holicLab_shop` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `holicLab_course`
--

LOCK TABLES `holicLab_course` WRITE;
/*!40000 ALTER TABLE `holicLab_course` DISABLE KEYS */;
/*!40000 ALTER TABLE `holicLab_course` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `holicLab_image`
--

DROP TABLE IF EXISTS `holicLab_image`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `holicLab_image` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `url` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `holicLab_image`
--

LOCK TABLES `holicLab_image` WRITE;
/*!40000 ALTER TABLE `holicLab_image` DISABLE KEYS */;
INSERT INTO `holicLab_image` VALUES (1,'images/1467217037_E._用户管理.png');
/*!40000 ALTER TABLE `holicLab_image` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `holicLab_order`
--

DROP TABLE IF EXISTS `holicLab_order`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `holicLab_order` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `create_time` datetime NOT NULL,
  `pay_time` datetime DEFAULT NULL,
  `finish_time` datetime DEFAULT NULL,
  `user_id` int(11) NOT NULL,
  `price` int(10) unsigned NOT NULL,
  `course_id` int(11) NOT NULL,
  `order_type` varchar(10) NOT NULL,
  `coupons_id` int(11) DEFAULT NULL,
  `password_id` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `people_amount` int(10) unsigned NOT NULL,
  `state` varchar(20) NOT NULL,
  `shop_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `password_id` (`password_id`),
  KEY `holicLab_order_6340c63c` (`user_id`),
  KEY `holicLab_order_6234103b` (`course_id`),
  KEY `holicLab_order_410a1f60` (`coupons_id`),
  KEY `holicLab_order_74d4252d` (`shop_id`),
  CONSTRAINT `coupons_id_refs_id_0762a3ae` FOREIGN KEY (`coupons_id`) REFERENCES `holicLab_coupon` (`id`),
  CONSTRAINT `course_id_refs_id_41d39897` FOREIGN KEY (`course_id`) REFERENCES `holicLab_course` (`id`),
  CONSTRAINT `password_id_refs_id_0ab131d4` FOREIGN KEY (`password_id`) REFERENCES `holicLab_password` (`id`),
  CONSTRAINT `shop_id_refs_id_3b412bf1` FOREIGN KEY (`shop_id`) REFERENCES `holicLab_shop` (`id`),
  CONSTRAINT `user_id_refs_id_f0a03d14` FOREIGN KEY (`user_id`) REFERENCES `holicLab_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `holicLab_order`
--

LOCK TABLES `holicLab_order` WRITE;
/*!40000 ALTER TABLE `holicLab_order` DISABLE KEYS */;
/*!40000 ALTER TABLE `holicLab_order` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `holicLab_order_services`
--

DROP TABLE IF EXISTS `holicLab_order_services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `holicLab_order_services` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `order_id` int(11) NOT NULL,
  `service_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `order_id` (`order_id`,`service_id`),
  KEY `holicLab_order_services_68d25c7a` (`order_id`),
  KEY `holicLab_order_services_91a0ac17` (`service_id`),
  CONSTRAINT `order_id_refs_id_3cc6f63c` FOREIGN KEY (`order_id`) REFERENCES `holicLab_order` (`id`),
  CONSTRAINT `service_id_refs_id_3a682bf6` FOREIGN KEY (`service_id`) REFERENCES `holicLab_service` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `holicLab_order_services`
--

LOCK TABLES `holicLab_order_services` WRITE;
/*!40000 ALTER TABLE `holicLab_order_services` DISABLE KEYS */;
/*!40000 ALTER TABLE `holicLab_order_services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `holicLab_password`
--

DROP TABLE IF EXISTS `holicLab_password`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `holicLab_password` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  `content` varchar(4) NOT NULL,
  `used_times` int(10) unsigned NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `content` (`content`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `holicLab_password`
--

LOCK TABLES `holicLab_password` WRITE;
/*!40000 ALTER TABLE `holicLab_password` DISABLE KEYS */;
INSERT INTO `holicLab_password` VALUES (1,'2016-06-29 16:13:58','2016-06-29 17:13:58','1i28',0);
/*!40000 ALTER TABLE `holicLab_password` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `holicLab_service`
--

DROP TABLE IF EXISTS `holicLab_service`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `holicLab_service` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(20) NOT NULL,
  `description` varchar(100) NOT NULL,
  `price` int(10) unsigned NOT NULL,
  `shop_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `holicLab_service_74d4252d` (`shop_id`),
  CONSTRAINT `shop_id_refs_id_f2f374ea` FOREIGN KEY (`shop_id`) REFERENCES `holicLab_shop` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `holicLab_service`
--

LOCK TABLES `holicLab_service` WRITE;
/*!40000 ALTER TABLE `holicLab_service` DISABLE KEYS */;
/*!40000 ALTER TABLE `holicLab_service` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `holicLab_shop`
--

DROP TABLE IF EXISTS `holicLab_shop`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `holicLab_shop` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(50) NOT NULL,
  `description` longtext NOT NULL,
  `notice` longtext NOT NULL,
  `cover_type` varchar(5) NOT NULL,
  `cover` longtext NOT NULL,
  `location` varchar(200) NOT NULL,
  `price` int(10) unsigned NOT NULL,
  `capacity` int(10) unsigned NOT NULL,
  `invalide_times` longtext NOT NULL,
  `last_modified_time` datetime NOT NULL,
  `state` varchar(10) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `holicLab_shop`
--

LOCK TABLES `holicLab_shop` WRITE;
/*!40000 ALTER TABLE `holicLab_shop` DISABLE KEYS */;
INSERT INTO `holicLab_shop` VALUES (1,'场地名称1','场地介绍1','注意事项1','image','[\"url(\\\"http://localhost:8000/media/images/1467217037_E._%E7%94%A8%E6%88%B7%E7%AE%A1%E7%90%86.png\\\")\"]','场地地址1',1000,10,'[]','2016-06-29 16:17:32','1');
/*!40000 ALTER TABLE `holicLab_shop` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `holicLab_time_bucket`
--

DROP TABLE IF EXISTS `holicLab_time_bucket`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `holicLab_time_bucket` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `occupation` longtext NOT NULL,
  `shop_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `holicLab_time_bucket_74d4252d` (`shop_id`),
  CONSTRAINT `shop_id_refs_id_a1be52f1` FOREIGN KEY (`shop_id`) REFERENCES `holicLab_shop` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `holicLab_time_bucket`
--

LOCK TABLES `holicLab_time_bucket` WRITE;
/*!40000 ALTER TABLE `holicLab_time_bucket` DISABLE KEYS */;
/*!40000 ALTER TABLE `holicLab_time_bucket` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `holicLab_time_limit_coupon`
--

DROP TABLE IF EXISTS `holicLab_time_limit_coupon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `holicLab_time_limit_coupon` (
  `coupon_ptr_id` int(11) NOT NULL,
  `start_time` datetime NOT NULL,
  `end_time` datetime NOT NULL,
  PRIMARY KEY (`coupon_ptr_id`),
  CONSTRAINT `coupon_ptr_id_refs_id_2889f339` FOREIGN KEY (`coupon_ptr_id`) REFERENCES `holicLab_coupon` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `holicLab_time_limit_coupon`
--

LOCK TABLES `holicLab_time_limit_coupon` WRITE;
/*!40000 ALTER TABLE `holicLab_time_limit_coupon` DISABLE KEYS */;
/*!40000 ALTER TABLE `holicLab_time_limit_coupon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `holicLab_tries_limit_coupon`
--

DROP TABLE IF EXISTS `holicLab_tries_limit_coupon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `holicLab_tries_limit_coupon` (
  `coupon_ptr_id` int(11) NOT NULL,
  `reuse_times` int(11) NOT NULL,
  PRIMARY KEY (`coupon_ptr_id`),
  CONSTRAINT `coupon_ptr_id_refs_id_ac51ec8e` FOREIGN KEY (`coupon_ptr_id`) REFERENCES `holicLab_coupon` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `holicLab_tries_limit_coupon`
--

LOCK TABLES `holicLab_tries_limit_coupon` WRITE;
/*!40000 ALTER TABLE `holicLab_tries_limit_coupon` DISABLE KEYS */;
/*!40000 ALTER TABLE `holicLab_tries_limit_coupon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `holicLab_user`
--

DROP TABLE IF EXISTS `holicLab_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `holicLab_user` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `wx_openid` longtext NOT NULL,
  `nickname` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `bind_date` date DEFAULT NULL,
  `total_order_times` int(10) unsigned NOT NULL,
  `total_order_days` int(10) unsigned NOT NULL,
  `total_order_duration` int(10) unsigned NOT NULL,
  `invite_code` varchar(4) NOT NULL,
  `use_invite_code` tinyint(1) NOT NULL,
  `balance` int(10) unsigned NOT NULL,
  `consumption` int(10) unsigned NOT NULL,
  `user_type` varchar(3) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=52 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `holicLab_user`
--

LOCK TABLES `holicLab_user` WRITE;
/*!40000 ALTER TABLE `holicLab_user` DISABLE KEYS */;
INSERT INTO `holicLab_user` VALUES (2,'','user0','13888888888','2016-09-27',0,0,0,'',0,0,0,'1'),(3,'','user1','13888888888','2016-09-20',0,0,0,'',0,0,0,'1'),(4,'','user2','13888888888','2016-04-29',0,0,0,'',0,0,0,'1'),(5,'','user3','13888888888','2016-05-25',0,0,0,'',0,0,0,'1'),(6,'','user4','13888888888','2016-07-06',0,0,0,'',0,0,0,'1'),(7,'','user5','13888888888','2016-08-15',0,0,0,'',0,0,0,'1'),(8,'','user6','13888888888','2016-09-10',0,0,0,'',0,0,0,'1'),(9,'','user7','13888888888','2016-09-20',0,0,0,'',0,0,0,'1'),(10,'','user8','13888888888','2016-06-05',0,0,0,'',0,0,0,'1'),(11,'','user9','13888888888','2016-07-11',0,0,0,'',0,0,0,'1'),(12,'','user10','13888888888','2016-04-29',0,0,0,'',0,0,0,'1'),(13,'','user11','13888888888','2016-06-14',0,0,0,'',0,0,0,'1'),(14,'','user12','13888888888','2016-08-24',0,0,0,'',0,0,0,'1'),(15,'','user13','13888888888','2016-05-09',0,0,0,'',0,0,0,'1'),(16,'','user14','13888888888','2016-05-06',0,0,0,'',0,0,0,'1'),(17,'','user15','13888888888','2016-04-29',0,0,0,'',0,0,0,'1'),(18,'','user16','13888888888','2016-04-12',0,0,0,'',0,0,0,'1'),(19,'','user17','13888888888','2016-07-23',0,0,0,'',0,0,0,'1'),(20,'','user18','13888888888','2016-07-01',0,0,0,'',0,0,0,'1'),(21,'','user19','13888888888','2016-09-22',0,0,0,'',0,0,0,'1'),(22,'','user20','13888888888','2016-06-09',0,0,0,'',0,0,0,'1'),(23,'','user21','13888888888','2016-10-03',0,0,0,'',0,0,0,'1'),(24,'','user22','13888888888','2016-05-23',0,0,0,'',0,0,0,'1'),(25,'','user23','13888888888','2016-05-25',0,0,0,'',0,0,0,'1'),(26,'','user24','13888888888','2016-04-16',0,0,0,'',0,0,0,'1'),(27,'','user25','13888888888','2016-06-04',0,0,0,'',0,0,0,'1'),(28,'','user26','13888888888','2016-05-19',0,0,0,'',0,0,0,'1'),(29,'','user27','13888888888','2016-08-24',0,0,0,'',0,0,0,'1'),(30,'','user28','13888888888','2016-08-16',0,0,0,'',0,0,0,'1'),(31,'','user29','13888888888','2016-08-04',0,0,0,'',0,0,0,'1'),(32,'','user30','13888888888','2016-05-15',0,0,0,'',0,0,0,'1'),(33,'','user31','13888888888','2016-05-30',0,0,0,'',0,0,0,'1'),(34,'','user32','13888888888','2016-09-21',0,0,0,'',0,0,0,'1'),(35,'','user33','13888888888','2016-06-09',0,0,0,'',0,0,0,'1'),(36,'','user34','13888888888','2016-06-01',0,0,0,'',0,0,0,'1'),(37,'','user35','13888888888','2016-06-19',0,0,0,'',0,0,0,'1'),(38,'','user36','13888888888','2016-09-05',0,0,0,'',0,0,0,'1'),(39,'','user37','13888888888','2016-07-14',0,0,0,'',0,0,0,'1'),(40,'','user38','13888888888','2016-06-19',0,0,0,'',0,0,0,'1'),(41,'','user39','13888888888','2016-05-20',0,0,0,'',0,0,0,'1'),(42,'','user40','13888888888','2016-06-26',0,0,0,'',0,0,0,'1'),(43,'','user41','13888888888','2016-06-02',0,0,0,'',0,0,0,'1'),(44,'','user42','13888888888','2016-09-15',0,0,0,'',0,0,0,'1'),(45,'','user43','13888888888','2016-08-12',0,0,0,'',0,0,0,'1'),(46,'','user44','13888888888','2016-10-02',0,0,0,'',0,0,0,'1'),(47,'','user45','13888888888','2016-09-16',0,0,0,'',0,0,0,'1'),(48,'','user46','13888888888','2016-05-06',0,0,0,'',0,0,0,'1'),(49,'','user47','13888888888','2016-05-18',0,0,0,'',0,0,0,'1'),(50,'','user48','13888888888','2016-07-15',0,0,0,'',0,0,0,'1'),(51,'','user49','13888888888','2016-07-01',0,0,0,'',0,0,0,'1');
/*!40000 ALTER TABLE `holicLab_user` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2016-06-30  0:21:12

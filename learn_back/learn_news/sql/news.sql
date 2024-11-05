CREATE TABLE `news` (
  `id` int NOT NULL AUTO_INCREMENT,
  `category` varchar(255) DEFAULT NULL,
  `title` varchar(500) DEFAULT NULL,
  `link` varchar(500) DEFAULT NULL,
  `time` varchar(100) DEFAULT NULL,
  `content` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=140983 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci
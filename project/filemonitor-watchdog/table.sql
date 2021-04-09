CREATE TABLE `img_info` (
  `project` int(11) NOT NULL,
  `shop` int(11) NOT NULL,
  `camera` int(11) NOT NULL,
  `image_name` varchar(50) NOT NULL,
  `image_path` varchar(500) DEFAULT NULL,
  `timestamp` int(11) DEFAULT NULL,
  PRIMARY KEY (`project`,`shop`,`camera`,`image_name`) USING BTREE,
  KEY `ix_img_info_timestamp` (`timestamp`) USING BTREE
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
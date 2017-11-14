CREATE TABLE `tyreinfo` (
  `tyreID` int(11) NOT NULL,
  `brand` varchar(16) DEFAULT NULL,
  `streak` varchar(32) DEFAULT NULL,
  `name` varchar(128) DEFAULT NULL,
  `standard` varchar(16) DEFAULT NULL,
  `loaded` varchar(32) DEFAULT NULL,
  `speed` varchar(32) DEFAULT NULL,
  `wearproof` varchar(16) DEFAULT NULL,
  `traction` varchar(16) DEFAULT NULL,
  `highTemperature` varchar(16) DEFAULT NULL,
  PRIMARY KEY (`tyreID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


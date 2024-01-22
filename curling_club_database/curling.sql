DROP TABLE IF EXISTS `match`;
CREATE TABLE `match` (
  `match_id` int PRIMARY KEY,
  `teamA_id` int,
  `teamB_id` int,
  `trainerA_id` int,
  `trainerB_id` int,
  `match_date` datetime
);

DROP TABLE IF EXISTS `player`;
CREATE TABLE `player` (
  `player_id` int PRIMARY KEY,
  `first_name` varchar(255),
  `last_name` varchar(255),
  `gender` varchar(255),
  `birthdate` date,
  `contract_from` date,
  `contract_to` date,
  `phone` varchar(255),
  `email` varchar(255)
);

DROP TABLE IF EXISTS `equipment`;
CREATE TABLE `equipment` (
  `equipment_id` int PRIMARY KEY,
  `category` varchar(255) ,
  `brand` varchar(255),
  `model` varchar(255)
);

DROP TABLE IF EXISTS `staff`;
CREATE TABLE `staff` (
  `staff_id` int,
  `first_name` varchar(255) ,
  `last_name` varchar(255) ,
  `position` varchar(255) ,
  `hire_date` date,
  `end_date` date,
  `phone` varchar(255),
  `email` varchar(255)
);

DROP TABLE IF EXISTS `sponsor`;
CREATE TABLE `sponsor` (
  `sponsor_id` int PRIMARY KEY,
  `full_name` varchar(255) ,
  `contract_from` datetime,
  `contract_to` datetime,
  `phone` varchar(255),
  `email` varchar(255)
);

DROP TABLE IF EXISTS `scores`;
CREATE TABLE `scores` (
  `match_id` int,
  `round_number` int,
  `teamA_score` int ,
  `teamB_score` int ,
  PRIMARY KEY (`match_id`, `round_number`)
);

DROP TABLE IF EXISTS `team`;
CREATE TABLE `team` (
  `team_id` int PRIMARY KEY,
  `player_id` int,
  `position` varchar(255),
  `contract_start` date
);

DROP TABLE IF EXISTS `salary`;
CREATE TABLE `salary` (
  `transaction_id` int PRIMARY KEY,
  `staff_id` int,
  `year` date,
  `month` date
);

DROP TABLE IF EXISTS `expenses`;
CREATE TABLE `expenses` (
  `equipment_id` int PRIMARY KEY,
  `scategory`varchar(255),
  `date` date,
  `price` float,
  `transaction_id` int
);

DROP TABLE IF EXISTS `financials`;
CREATE TABLE `financials` (
  `transaction_id` int PRIMARY KEY,
  `amount` float
);

DROP TABLE IF EXISTS `sponsor_transaction`;
CREATE TABLE `sponsor_transaction` (
  `transaction_id` int,
  `sponsor_id` int,
  `amount` float,
  `date` date
)
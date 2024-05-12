-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               5.0.17-nt - MySQL Community Edition (GPL)
-- Server OS:                    Win32
-- HeidiSQL Version:             9.4.0.5174
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;


-- Dumping database structure for timetable
CREATE DATABASE IF NOT EXISTS `timetable` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `timetable`;

-- Dumping structure for table timetable.admin
CREATE TABLE IF NOT EXISTS `admin` (
  `id` int(11) NOT NULL auto_increment,
  `email` varchar(100) NOT NULL default '0',
  `pass` varchar(100) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table timetable.admin: ~1 rows (approximately)
/*!40000 ALTER TABLE `admin` DISABLE KEYS */;
INSERT INTO `admin` (`id`, `email`, `pass`) VALUES
	(1, 'admin@gmail.com', '123');
/*!40000 ALTER TABLE `admin` ENABLE KEYS */;

-- Dumping structure for table timetable.seating
CREATE TABLE IF NOT EXISTS `seating` (
  `id` int(11) NOT NULL auto_increment,
  `filename` varchar(500) NOT NULL default '0',
  `branch1` varchar(500) NOT NULL default '0',
  `branch2` varchar(500) NOT NULL default '0',
  `year` varchar(500) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table timetable.seating: ~2 rows (approximately)
/*!40000 ALTER TABLE `seating` DISABLE KEYS */;
INSERT INTO `seating` (`id`, `filename`, `branch1`, `branch2`, `year`) VALUES
	(1, 'seating1styearCOMPUTER SCIENCEELECTRONICS AND COMMUNICATION.xlsx', 'COMPUTER SCIENCE', 'ELECTRONICS AND COMMUNICATION', '1styear'),
	(2, 'seating1styearCOMPUTER SCIENCEELECTRONICS AND COMMUNICATION.xlsx', 'COMPUTER SCIENCE', 'ELECTRONICS AND COMMUNICATION', '1styear');
/*!40000 ALTER TABLE `seating` ENABLE KEYS */;

-- Dumping structure for table timetable.student
CREATE TABLE IF NOT EXISTS `student` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(150) NOT NULL default '0',
  `email` varchar(150) NOT NULL default '0',
  `phone` varchar(150) NOT NULL default '0',
  `gender` varchar(150) NOT NULL default '0',
  `address` varchar(150) NOT NULL default '0',
  `usn` varchar(150) NOT NULL default '0',
  `branch` varchar(150) NOT NULL default '0',
  `year` varchar(150) NOT NULL default '0',
  `pass` varchar(150) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table timetable.student: ~8 rows (approximately)
/*!40000 ALTER TABLE `student` DISABLE KEYS */;
INSERT INTO `student` (`id`, `name`, `email`, `phone`, `gender`, `address`, `usn`, `branch`, `year`, `pass`) VALUES
	(1, 'arvind', 'arvind@gmail.com', '9874562147', 'Male', 'sdghsdhs', '1nc12cs418', 'COMPUTER SCIENCE', '1styear', '123'),
	(2, 'abc', 'abc@gmaill.com', '8745124789', 'Male', 'fsgaer', '1nc12ec418', 'ELECTRONICS AND COMMUNICATION', '1styear', '123'),
	(3, 'ram', 'ram@gmail.com', '8789874569', 'Male', 'sfgsag', '1nc12cs001', 'COMPUTER SCIENCE', '1styear', '123'),
	(4, 'ravi', 'ravi@gmail.com', '9874563214', 'Male', 'asgar', '1nc12cs002', 'COMPUTER SCIENCE', '1styear', '123'),
	(5, 'sneha', 'sneha@gmail.com', '7896547485', 'Male', 'sg', '1nc12ec001', 'ELECTRONICS AND COMMUNICATION', '1styear', '123'),
	(6, 'sunil', 'sunil@gmail.com', '8745784589', 'Male', 'sg', '1nc12ec002', 'ELECTRONICS AND COMMUNICATION', '1styear', '123'),
	(7, 'rajesh', 'rajesh@gmail.com', '8965898569', 'Male', 'sfgfgsf', '1nc12is001', 'INFORMATION SCIENCE', '1styear', '123'),
	(8, 'pavan', 'pavan@gmail.com', '8741223652', 'Male', 'sg', '1nc12ec003', 'ELECTRONICS AND COMMUNICATION', '1styear', '123');
/*!40000 ALTER TABLE `student` ENABLE KEYS */;

-- Dumping structure for table timetable.subject
CREATE TABLE IF NOT EXISTS `subject` (
  `id` int(11) NOT NULL auto_increment,
  `sname` varchar(150) NOT NULL default '0',
  `tid` int(11) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_subject_teacher` (`tid`),
  CONSTRAINT `FK_subject_teacher` FOREIGN KEY (`tid`) REFERENCES `teacher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table timetable.subject: ~8 rows (approximately)
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` (`id`, `sname`, `tid`) VALUES
	(1, 'kannada', 1),
	(2, 'hindi', 1),
	(3, 'english', 2),
	(4, 'maths', 3),
	(5, 'vlsi', 4),
	(6, 'social', 5),
	(7, 'science', 6),
	(8, 'grammer', 7);
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;

-- Dumping structure for table timetable.substitute
CREATE TABLE IF NOT EXISTS `substitute` (
  `id` int(11) NOT NULL auto_increment,
  `stid` int(11) NOT NULL default '0',
  `atid` int(11) NOT NULL default '0',
  `ssubject` varchar(50) NOT NULL default '0',
  `sdate` varchar(50) NOT NULL default '0',
  `stime` varchar(50) NOT NULL default '0',
  `status` varchar(50) NOT NULL default '0',
  PRIMARY KEY  (`id`),
  KEY `FK_substitute_teacher` (`stid`),
  KEY `FK_substitute_teacher_2` (`atid`),
  CONSTRAINT `FK_substitute_teacher` FOREIGN KEY (`stid`) REFERENCES `teacher` (`id`),
  CONSTRAINT `FK_substitute_teacher_2` FOREIGN KEY (`atid`) REFERENCES `teacher` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table timetable.substitute: ~2 rows (approximately)
/*!40000 ALTER TABLE `substitute` DISABLE KEYS */;
INSERT INTO `substitute` (`id`, `stid`, `atid`, `ssubject`, `sdate`, `stime`, `status`) VALUES
	(1, 3, 2, 'maths', '2024-04-13', '12:00', 'Pending'),
	(2, 2, 1, 'english', '2024-04-13', '15:00', 'Accepted');
/*!40000 ALTER TABLE `substitute` ENABLE KEYS */;

-- Dumping structure for table timetable.teacher
CREATE TABLE IF NOT EXISTS `teacher` (
  `id` int(11) NOT NULL auto_increment,
  `name` varchar(100) NOT NULL default '0',
  `email` varchar(100) NOT NULL default '0',
  `phone` varchar(100) NOT NULL default '0',
  `pass` varchar(100) NOT NULL default '0',
  PRIMARY KEY  (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Dumping data for table timetable.teacher: ~7 rows (approximately)
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` (`id`, `name`, `email`, `phone`, `pass`) VALUES
	(1, 'aruna', 'aruna@gmail.com', '9874562147', '123'),
	(2, 'varsha', 'varsha@gmail.com', '8745124789', '123'),
	(3, 'nandakishore', 'nandakishor@gmail.com', '8745123698', '123'),
	(4, 'sadist', 'sadist@gmail.com', '7418524789', '123'),
	(5, 'praveen', 'praveen@gmail.com', '8745874587', '123'),
	(6, 'nithya', 'nithya@gmail.com', '8965896589', '123'),
	(7, 'spoorthy', 'spoorthy@gmail.com', '7512541256', '123');
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;

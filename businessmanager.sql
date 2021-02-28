-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 28, 2021 at 12:45 PM
-- Server version: 10.4.14-MariaDB
-- PHP Version: 7.2.34

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `businessmanager`
--

-- --------------------------------------------------------

--
-- Table structure for table `category`
--

CREATE TABLE `category` (
  `id` int(100) NOT NULL,
  `category` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `category`
--

INSERT INTO `category` (`id`, `category`) VALUES
(1, 'sticker'),
(3, 'mystick'),
(10, 'test');

-- --------------------------------------------------------

--
-- Table structure for table `employee`
--

CREATE TABLE `employee` (
  `id` int(100) NOT NULL,
  `username` varchar(255) NOT NULL,
  `fullname` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `contact` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` varchar(255) NOT NULL,
  `image` varchar(255) NOT NULL,
  `lastlogin` varchar(255) NOT NULL,
  `attempt` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `employee`
--

INSERT INTO `employee` (`id`, `username`, `fullname`, `email`, `contact`, `password`, `role`, `image`, `lastlogin`, `attempt`) VALUES
(1, 'rever', 'arnab gupta', 'rever@rd.com', '7044287686', 'pbkdf2:sha256:150000$PyZKQE0C$887260c6e2c94515fc9a75f692da7ee4836f64d90f450505a5ca8e9801d56ce3', 'superuser', 'test.png', '00:56:38', 0);

-- --------------------------------------------------------

--
-- Table structure for table `products`
--

CREATE TABLE `products` (
  `id` int(100) NOT NULL,
  `name` varchar(255) NOT NULL,
  `productid` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `barcode` varchar(255) NOT NULL,
  `vartype` varchar(255) NOT NULL,
  `vars` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `seller` varchar(255) NOT NULL,
  `quantity` varchar(255) NOT NULL,
  `unitprice` varchar(255) NOT NULL,
  `sellprice` varchar(255) NOT NULL,
  `tax` varchar(255) NOT NULL,
  `dimension` varchar(255) NOT NULL,
  `weight` varchar(255) NOT NULL,
  `image` varchar(255) NOT NULL,
  `date` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `products`
--

INSERT INTO `products` (`id`, `name`, `productid`, `status`, `barcode`, `vartype`, `vars`, `category`, `seller`, `quantity`, `unitprice`, `sellprice`, `tax`, `dimension`, `weight`, `image`, `date`) VALUES
(19, 'saringan2.5', 'test1234', 'active', 'nocode', 'color', 'red', 'sticker', 'new2', '50', '20', '41', '5', '15x12x2 mm', '500 gm', 'c9942021bb564529b8b658de61569a1f.jpeg', '02/20/21'),
(20, 'saringanshoot', 'test1234', 'active', 'nocode', 'color', 'red', 'sticker', 'new2', '50', '20', '41', '5', '15x12x2 mm', '500 gm', '4b684a38a8cc4d0cbd7cf867c2b3c73f.png', '02/25/21'),
(21, 'saringan', 'sar2', 'active', 'nocode', 'shape', 'test', 'mystick', 'vendor 2', '100', '50', '100', '10', '15x12x2 cm', '600', '4b684a38a8cc4d0cbd7cf867c2b3c73f.png', '02/20/21');

-- --------------------------------------------------------

--
-- Table structure for table `seller`
--

CREATE TABLE `seller` (
  `id` int(100) NOT NULL,
  `seller` varchar(255) NOT NULL,
  `contact` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `seller`
--

INSERT INTO `seller` (`id`, `seller`, `contact`, `address`) VALUES
(3, 'new2', 'zsdfdfds', 'sfsfsf'),
(7, 'vendor 2', '74044287696', 'barasat');

-- --------------------------------------------------------

--
-- Table structure for table `variation`
--

CREATE TABLE `variation` (
  `id` int(100) NOT NULL,
  `type` varchar(255) NOT NULL,
  `variations` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `variation`
--

INSERT INTO `variation` (`id`, `type`, `variations`) VALUES
(1, 'color', 'red,green,blue,yellow'),
(2, 'shape', 'test,test2'),
(21, 'new', 'new,new2,new3'),
(22, 'new2', 'new,new2,new3');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `seller`
--
ALTER TABLE `seller`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `variation`
--
ALTER TABLE `variation`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `seller`
--
ALTER TABLE `seller`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `variation`
--
ALTER TABLE `variation`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

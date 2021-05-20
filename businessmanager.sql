-- phpMyAdmin SQL Dump
-- version 5.0.3
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 15, 2021 at 05:09 PM
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
-- Table structure for table `alldues`
--

CREATE TABLE `alldues` (
  `id` int(100) NOT NULL,
  `date` varchar(255) NOT NULL,
  `reference` varchar(255) NOT NULL,
  `account` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `amount` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `alldues`
--

INSERT INTO `alldues` (`id`, `date`, `reference`, `account`, `name`, `amount`) VALUES
(6, '02-05-2021', 'refduearnabsalary2021', 'salary', 'arnab', '500'),
(7, '02-05-2021', 'refduebabulaoinvestor2021', 'investor', 'babulao', '1000'),
(9, '06-05-2021', 'Inv/05/230818', 'sale', 'arnab gupta', '10'),
(13, '07-05-2021', 'Inv/07/05/202005', 'sale', 'tulika gupta', '1000'),
(14, '07-05-2021', 'Inv/07/05/202205', 'sale', 'arnab gupta', '10'),
(15, '09-05-2021', 'Inv-09-05-132654', 'sale', 'arnab gupta', '500');

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
-- Table structure for table `customer`
--

CREATE TABLE `customer` (
  `id` int(100) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `custid` varchar(255) NOT NULL,
  `address` varchar(255) NOT NULL,
  `gender` varchar(255) NOT NULL,
  `birthday` varchar(255) NOT NULL,
  `joindate` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`id`, `name`, `phone`, `custid`, `address`, `gender`, `birthday`, `joindate`) VALUES
(1, 'tulika gupta', '7003391137', '7003391137', 'barasat', 'female', '07-05-1967', '06-05-2021'),
(2, 'arnab gupta', '7044287686', '7044287686', 'shalbagan,barasat', 'male', '10-08-1996', '06-05-2021'),
(3, 'test cust', '8585858585', '8585858585', 'barasattest', 'other', '08-07-2020', '08-05-2021'),
(4, 'test cust 2', '8585858584', '8585858584', 'dfsfdsfsfsf', 'male', '20-02-2019', '08-05-2021'),
(13, 'ashok gupta', '9830108453', '9830108453', 'shalbagan barasat', 'male', '07-05-1967', '15-05-2021'),
(14, 'new test cust 2', '8585858596', '8585858596', 'treadfsdfsfsf', 'other', '01-05-2020', '15-05-2021');

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
(1, 'rever', 'arnab gupta', 'rever@rd.com', '7044287686', 'pbkdf2:sha256:150000$PyZKQE0C$887260c6e2c94515fc9a75f692da7ee4836f64d90f450505a5ca8e9801d56ce3', 'superuser', 'test.png', '20:39:27', 0);

-- --------------------------------------------------------

--
-- Table structure for table `orderprocess`
--

CREATE TABLE `orderprocess` (
  `id` int(100) NOT NULL,
  `orderid` varchar(255) NOT NULL,
  `product` varchar(255) NOT NULL,
  `quantity` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `orderprocess`
--

INSERT INTO `orderprocess` (`id`, `orderid`, `product`, `quantity`, `status`) VALUES
(1, '2287655', 'selfless', '20', 'Cancelled'),
(2, '2287656', 'selfless', '10', ''),
(3, '2287657', 'sar2', '10', ''),
(4, '2287658', 'test12345', '20', ''),
(5, '2287659', 'test1234', '10', ''),
(6, '2287660', 'test12345', '10', ''),
(7, '2287661', 'selfless', '10', ''),
(8, '2287662', 'test1234', '10', 'Received'),
(9, 'Ord-09-05-112944', 'test12345:test1234', '10:10', 'Received'),
(10, 'Inv-09-05-132654', 'msngr-link:selfless', '5:10', 'sold'),
(11, 'Inv-11-05-113551', 'test1234:selfless', '5:10', 'Cancelled'),
(12, 'Ord-13-05-102910', 'selfless', '50', 'Received'),
(13, 'Inv-13-05-141048', 'msngr-link', '5', 'Cancelled'),
(14, 'Inv-13-05-141344', 'msngr-link', '5', 'Cancelled'),
(15, 'Inv-14-05-140853', 'selfless', '10', 'Refunded'),
(16, 'Inv-14-05-141432', 'msngr-link', '5', 'Refunded');

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
(19, 'saringan2.5', 'test1234', 'active', 'nocode', 'color', 'red', 'sticker', 'new2', '15', '10', '41', '5', '15x12x2 mm', '500 gm', 'c9942021bb564529b8b658de61569a1f.jpeg', '09-05-2021'),
(20, 'saringanshoot', 'test12345', 'active', 'nocode', 'color', 'red', 'sticker', 'new2', '110', '20', '41', '5', '15x12x2 mm', '500 gm', '4b684a38a8cc4d0cbd7cf867c2b3c73f.png', '02/25/21'),
(21, 'saringan', 'sar2', 'active', 'nocode', 'shape', 'test', 'mystick', 'vendor 2', '10', '50', '100', '10', '15x12x2 cm', '600 kg', '4b684a38a8cc4d0cbd7cf867c2b3c73f.png', '09-05-2021'),
(22, 'myself', 'selfless', 'active', '00123457', 'shape', 'test', 'mystick', 'vendor 2', '40', '50', '100', '5', '50x50x50 in', '85 kg', '8eeb1dd2fa7f4d0db056987e1c06bee3.jpeg', '10-05-2021'),
(24, 'messenger', 'msngr-link', 'active', 'nocode', 'shape', 'test', 'sticker', 'new2', '45', '50', '100', '10', '10x20x3 mm', '500 gm', '6e87c415caa448d1bf2fed8cf7f3f2d0.png', '06-05-2021');

-- --------------------------------------------------------

--
-- Table structure for table `purchaseorder`
--

CREATE TABLE `purchaseorder` (
  `id` int(100) NOT NULL,
  `orderid` varchar(255) NOT NULL,
  `vendor` varchar(255) NOT NULL,
  `date` varchar(100) NOT NULL,
  `status` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `purchaseorder`
--

INSERT INTO `purchaseorder` (`id`, `orderid`, `vendor`, `date`, `status`) VALUES
(1, '2287655', 'vendor 2', '2021-04-25', 'Cancelled'),
(2, '2287656', 'vendor 2', '2021-04-25', 'processing'),
(3, '2287657', 'vendor 2', '2021-04-25', 'processing'),
(4, '2287658', 'new2', '2021-04-25', 'processing'),
(5, '2287659', 'new2', '2021-05-01', 'processing'),
(6, '2287660', 'new2', '2021-05-01', 'processing'),
(7, '2287661', 'vendor 2', '2021-', 'processing'),
(8, '2287662', 'new2', '01-05-2021', 'Received'),
(9, 'Ord-09-05-112944', 'new2', '2021-05-09', 'Received'),
(10, 'Ord-13-05-102910', 'vendor 2', '13-05-2021', 'Received');

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
-- Table structure for table `sellorder`
--

CREATE TABLE `sellorder` (
  `id` int(100) NOT NULL,
  `pmode` varchar(255) NOT NULL,
  `invid` varchar(255) NOT NULL,
  `custid` varchar(255) NOT NULL,
  `date` varchar(255) NOT NULL,
  `status` varchar(255) NOT NULL,
  `refundable` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `sellorder`
--

INSERT INTO `sellorder` (`id`, `pmode`, `invid`, `custid`, `date`, `status`, `refundable`) VALUES
(1, 'cash', 'Inv/07/05/201016', '7003391137', '07-05-2021', 'sold', 'no'),
(3, 'cash', 'Inv/07/05/202005', '7003391137', '07-05-2021', 'sold', 'no'),
(4, 'cash', 'Inv/07/05/202205', '7044287686', '07-05-2021', 'sold', 'no'),
(5, 'online', 'Inv/08/05/122019', '7044287686', '08-05-2021', 'sold', 'no'),
(12, 'cash', 'Inv-08-05-210131', '7044287686', '08-05-2021', 'sold', 'no'),
(16, 'cash', 'Inv-08-05-230539', '7003391137', '08-05-2021', 'sold', 'no'),
(17, 'online', 'Inv-09-05-112446', '8585858585', '09-05-2021', 'sold', 'no'),
(18, 'cash', 'Inv-09-05-132654', '7044287686', '09-05-2021', 'cancelled', 'no'),
(19, 'cash', 'Inv-11-05-113551', '7044287686', '11-05-2021', 'Cancelled', 'no'),
(20, 'online', 'Inv-11-05-115835', '7044287686', '11-05-2021', 'Refunded', 'no'),
(21, 'online', 'Inv-11-05-115835', '7044287686', '11-05-2021', 'Refunded', 'yes'),
(22, 'cash', 'Inv-13-05-141048', '7044287686', '13-05-2021', 'Cancelled', 'no'),
(23, 'cash', 'Inv-13-05-141344', '7003391137', '13-05-2021', 'Cancelled', 'no'),
(24, 'cash', 'Inv-14-05-140853', '7044287686', '14-05-2021', 'Refunded', 'yes'),
(25, 'cash', 'Inv-14-05-141432', '7044287686', '14-05-2021', 'Refunded', 'yes');

-- --------------------------------------------------------

--
-- Table structure for table `services`
--

CREATE TABLE `services` (
  `id` int(100) NOT NULL,
  `name` varchar(255) NOT NULL,
  `serviceid` varchar(255) NOT NULL,
  `price` varchar(255) NOT NULL,
  `tax` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `services`
--

INSERT INTO `services` (`id`, `name`, `serviceid`, `price`, `tax`) VALUES
(1, 'computer repair', 'comp-rp', '500', '0'),
(2, 'laptop repair', 'lap-rp', '500', '0'),
(3, 'laptop service', 'lap-ser', '700', '0');

-- --------------------------------------------------------

--
-- Table structure for table `transaction`
--

CREATE TABLE `transaction` (
  `id` int(100) NOT NULL,
  `date` varchar(255) NOT NULL,
  `reference` varchar(255) NOT NULL,
  `account` varchar(255) NOT NULL,
  `debit` varchar(255) NOT NULL,
  `credit` varchar(255) NOT NULL,
  `balance` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `transaction`
--

INSERT INTO `transaction` (`id`, `date`, `reference`, `account`, `debit`, `credit`, `balance`) VALUES
(1, '04/30/21', 'ref22456', 'recharge', '500', '0', '500'),
(2, '04/30/21', 'ref22456', 'xerox', '0', '100', '400'),
(3, '04/30/21', 'ref22456', 'investor', '600', '0', '1000'),
(4, '04/30/21', 'ref22456', 'service', '500', '0', '1500'),
(5, '04/30/21', 'ref22456', 'service', '500', '0', '2000'),
(6, '05/01/21', 'ref22456', 'service', '500', '0', '2500'),
(7, '05/01/21', 'ref22456', 'xerox', '2000', '0', '4500'),
(8, '2021-05-01', '2287659', 'purchase', '0', '105', '4605'),
(9, '2021-05-01', '2287660', 'purchase', '0', '210', '4395'),
(10, '2021-', '2287661', 'purchase', '0', '525', '3870'),
(11, '01-05-2021', '2287662', 'purchase', '0', '105', '3765'),
(12, '01-05-21', 'ref22456', 'recharge', '100', '0', '3865'),
(13, '01-05-2021', 'ref22456', 'recharge', '0', '500', '3365'),
(14, '01-05-2021', '2287663', 'purchase', '0', '500', '2865'),
(15, '02-05-2021', 'ref22456', 'salary', '500', '0', '3365'),
(16, '02-05-2021', 'debit/xerox/2021', 'xerox', '500', '0', '3865'),
(17, '02-05-2021', 'refcreditservice2021', 'service', '0', '100', '3765'),
(18, '02-05-2021', 'refdebitpurchase2021', 'purchase', '100', '0', '3865'),
(19, '02-05-2021', 'refdebitxerox1042', 'xerox', '1052', '0', '4917'),
(20, '02-05-2021', 'refduearnabpurchase104331', 'purchase', '100', '0', '5017'),
(21, '06-05-2021', '2287663', 'purchase', '0', '1000', '4017'),
(22, '06-05-2021', 'Inv/05/225503', 'sale', '1000', '0', '5017'),
(23, '06-05-2021', 'Inv/05/230818', 'sale', '410', '0', '5427'),
(24, '06-05-2021', 'Inv/05/231128', 'sale', '300', '0', '5727'),
(25, '06-05-2021', 'Inv/05/231128', 'sale', '110', '0', '5837'),
(26, '07-05-2021', 'Inv/07/05/195644', 'sale', '1000', '0', '6837'),
(29, '07-05-2021', 'Inv/07/05/201016', 'sale', '100', '0', '6937'),
(30, '07-05-2021', 'Inv/07/05/202205', 'sale', '400', '0', '7337'),
(31, '08-05-2021', 'Inv/08/05/122019', 'sale', '410', '0', '7747'),
(38, '08-05-2021', 'Inv-08-05-210131', 'sale', '410', '0', '8157'),
(42, '08-05-2021', 'Inv-08-05-230539', 'sale', '820', '0', '8977'),
(43, '09-05-2021', 'Inv-09-05-112446', 'sale', '1000', '0', '9977'),
(44, '2021-05-09', 'Ord-09-05-112944', 'purchase', '0', '315', '9662'),
(45, '09-05-2021', 'Inv-09-05-132654', 'sale', '1000', '0', '10662'),
(46, '11-05-2021', 'Inv-11-05-113551', 'sale', '1265', '0', '11927'),
(47, '11-05-2021', 'Inv-11-05-115835', 'service', '1200', '0', '13127'),
(48, '11-05-2021', 'Inv-11-05-115835', 'service', '1200', '0', '14327'),
(49, '13-05-2021', 'Ord-13-05-102910', 'purchase', '0', '2625', '11702'),
(50, '13-05-2021', 'Inv-13-05-141048', 'sale', '500', '0', '12202'),
(51, '13-05-2021', 'Inv-13-05-141048', 'refund', '0', '500', '11702'),
(52, '13-05-2021', 'Inv-13-05-141344', 'sale', '500', '0', '12202'),
(53, '13-05-2021', 'Inv-13-05-141344', 'refund', '0', '500', '11702'),
(54, '14-05-2021', 'Inv-14-05-140853', 'sale', '1050', '0', '12752'),
(55, '14-05-2021', 'Inv-14-05-140853', 'refund', '0', '1050', '11702'),
(56, '14-05-2021', 'Inv-11-05-115835', 'refund', '0', '1200', '10502'),
(57, '14-05-2021', 'Inv-14-05-141432', 'sale', '550', '0', '11052'),
(58, '14-05-2021', 'Inv-14-05-141432', 'refund', '0', '550', '10502');

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
-- Indexes for table `alldues`
--
ALTER TABLE `alldues`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `category`
--
ALTER TABLE `category`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `customer`
--
ALTER TABLE `customer`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `employee`
--
ALTER TABLE `employee`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orderprocess`
--
ALTER TABLE `orderprocess`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `products`
--
ALTER TABLE `products`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `purchaseorder`
--
ALTER TABLE `purchaseorder`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `seller`
--
ALTER TABLE `seller`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `sellorder`
--
ALTER TABLE `sellorder`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `services`
--
ALTER TABLE `services`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `transaction`
--
ALTER TABLE `transaction`
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
-- AUTO_INCREMENT for table `alldues`
--
ALTER TABLE `alldues`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `category`
--
ALTER TABLE `category`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `customer`
--
ALTER TABLE `customer`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=15;

--
-- AUTO_INCREMENT for table `employee`
--
ALTER TABLE `employee`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `orderprocess`
--
ALTER TABLE `orderprocess`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `products`
--
ALTER TABLE `products`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `purchaseorder`
--
ALTER TABLE `purchaseorder`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `seller`
--
ALTER TABLE `seller`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `sellorder`
--
ALTER TABLE `sellorder`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=26;

--
-- AUTO_INCREMENT for table `services`
--
ALTER TABLE `services`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `transaction`
--
ALTER TABLE `transaction`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=59;

--
-- AUTO_INCREMENT for table `variation`
--
ALTER TABLE `variation`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

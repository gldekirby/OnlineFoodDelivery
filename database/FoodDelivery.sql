-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 30, 2025 at 07:39 AM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `food_delivery`
--

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE `menu` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `photo_path` varchar(255) DEFAULT NULL,
  `category` enum('Premium','Steak','Rice Meal','Family Meal','Snacks','House Specialty','Special Offer Vj''s Shawarma') DEFAULT NULL,
  `status` enum('available','not available') NOT NULL DEFAULT 'available'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`id`, `name`, `description`, `price`, `photo_path`, `category`, `status`) VALUES
(15, 'Wagyu Beef Steak', 'Intense marbling, tenderness, and, rich flavor', 2550.00, '494822324_683980157815900_6807596636096023203_n.jpg', 'Premium', 'available'),
(16, 'Sliced Ribeye Steak', 'Cooked to medium-rare with a reddish-pink center and a browned exterior', 1119.00, '494815606_9059508927485369_1089659799176002555_n.jpg', 'Premium', 'available'),
(17, 'Grilled Ribeye Steak', 'Grilled ribeye steak, garnished with grilled vegetables and a sauce', 800.00, '494815982_1260765442059383_6058301454415089532_n.jpg', 'Premium', 'available'),
(18, 'Smoke Salmon', 'Preparation of salmon that has been cured and smoked', 1016.00, '494820545_712060001184775_350753135813829478_n.jpg', 'Premium', 'available'),
(19, 'Baked Caesar Chicken with Creamy Parmesan Sauce', 'Chicken breast coated in a creamy dressing and topped with a buttery parmesab mixture', 500.00, '494887004_2520928981576522_8963098383743652951_n.jpg', 'Rice Meal', 'not available'),
(20, 'Salisbury Steak with mushroom gravy', 'Ground beef patties cooked in a savory sauce', 365.00, '494816113_1217106313420599_2844538694718482133_n.jpg', 'Rice Meal', 'available'),
(21, 'Hamburger Steak', 'Ground beef patties cooked and often simmered in gravy', 170.00, '494820809_1608822173026107_4911525199531730122_n.jpg', 'Rice Meal', 'available'),
(22, 'Air-fried Teritaki Chicken', 'Garnished with sesame seeds and green onions and served with chopsticks', 339.00, '494886776_1829439404296201_7785565072794417055_n.jpg', 'Rice Meal', 'available'),
(23, 'Crispy Fried Chicken', 'Crispy fried chicken, likely wings, served with a dipping sauce', 860.00, '494815992_1224001262611377_5747455956739026783_n.jpg', 'Rice Meal', 'available'),
(24, 'Baked Tahong', 'Filipino appetizer also known as baked mussels', 300.00, '491351668_1021144859466195_8514758261613532410_n.jpg', 'Family Meal', 'available'),
(25, 'Cooked Shrimp', 'Popular shellfish enjoyed worldwide and is known for its nutritional value and flavor', 704.00, '494818738_671764229016655_3437338645712882803_n.jpg', 'Family Meal', 'available'),
(26, 'Cooked pampano Fish', 'Cooked pampano fish with a side of shredded cabbage and carrots', 750.00, '494817479_1042277674030216_8887274905083134795_n.jpg', 'Family Meal', 'available'),
(27, 'Steamed Pompano Fish', 'Gentle cooking method that produces flaky, moist, and flavorful seafood', 400.00, '494820459_679505765041644_1856903509359839266_n.jpg', 'Family Meal', 'available'),
(28, 'Dragon Chicken', 'Popular Indo-chinese appetizer', 1500.00, '494813156_1947003572772188_5017131150608848534_n.jpg', 'Family Meal', 'available'),
(29, 'Close-up of chicken wings, likely sweet and spicy chicken wings', 'Glazed and slightly charred, suggesting a flavorful marinade', 455.00, '495270115_1196165398909258_5465205171405805934_n.jpg', 'Family Meal', 'available'),
(30, 'Chicken Marbella', 'dish originating from the 198-s Silver Palate Cookbook featuring chicken thinghs marinated and baked with prunes, olives, capers, garlic, and white wine', 500.00, '494817097_1399387741090147_3674888148227857350_n.jpg', 'Family Meal', 'available'),
(31, 'Beef Brisket Chuck Burger', '1', 1.00, '494886809_1223490619371177_5267385445059937295_n.jpg', 'Snacks', 'available'),
(32, 'Cheese Burger with Fries', 'Sandwich consisting of a cooked meat patty, typically beef, placed inside a sliced bun', 170.00, '494827992_1250728853286876_1602684073958584211_n.jpg', 'Snacks', 'available'),
(33, 'Bang Bang Chicken Slider', 'A mini-sandwich featuring crispy fried chicken coated', 150.00, '494826277_1388301402384738_2559719256625728789_n.jpg', 'Snacks', 'available');

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `order_date` timestamp NOT NULL DEFAULT current_timestamp(),
  `status` enum('Pending','Preparing','Ready','Completed','Cancelled') DEFAULT 'Pending',
  `amount` decimal(10,2) NOT NULL DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `order_date`, `status`, `amount`) VALUES
(48, '2025-05-30 02:16:24', 'Pending', 100.00),
(49, '2025-05-30 04:53:56', 'Pending', 4808.00),
(50, '2025-05-30 05:01:27', 'Pending', 750.00),
(51, '2025-05-30 05:37:36', 'Cancelled', 2954.00);

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `item_id`, `quantity`) VALUES
(66, 48, 17, 1),
(67, 49, 15, 1),
(68, 49, 16, 1),
(69, 49, 17, 1),
(70, 49, 22, 1),
(71, 50, 26, 1),
(72, 51, 25, 1),
(73, 51, 26, 1),
(74, 51, 28, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `item_id` (`item_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=35;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=52;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=75;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`),
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `menu` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;

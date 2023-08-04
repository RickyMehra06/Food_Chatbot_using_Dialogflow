-- To create the `food_database`
CREATE DATABASE IF NOT EXISTS `food_database`;
USE `food_database`;

-- To create the `orders` table
DROP TABLE IF EXISTS `orders`;
CREATE TABLE `orders` (
  `order_id` int NOT NULL,
  `item_id` int NOT NULL,  
  `item_name` varchar(255) DEFAULT NULL,
  `quantity` int DEFAULT NULL,
  `total_price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`order_id`,`item_id`)
);

-- To Insert data into `orders` table
INSERT INTO `orders` VALUES (100, 1, 'Dal Makhani', 2, 400.00),
                           (100, 2, 'Butter Paneer', 1, 300.00),
                           (101, 10, 'Chole Bhature', 2, 200.00),
                           (101, 13, 'Lassi', 4, 200.00),
                           (102, 3, 'Pindi Chole', 1, 200.00),
                           (102, 5, 'Naan', 3, 150.00),
                           (102, 7, 'Raita', 2, 100.00);

Select * from orders;

-- To create the `order_tracking` table
DROP TABLE IF EXISTS `order_tracking`;
CREATE TABLE `order_tracking` (
  `order_id` int NOT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`order_id`)
);
-- To Insert data into `order_tracking` table
INSERT INTO `order_tracking` VALUES (100, 'Delivered'), 
									(101, 'In-Transit'), 
                                    (102, 'In-Process');

Select * from order_tracking;


-- food_menu table is not required as we are performing calculation using python
DROP TABLE IF EXISTS `food_menu`;
CREATE TABLE `food_menu` (
  `item_id` int NOT NULL,
  `item_name` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`item_id`)
);

INSERT INTO `food_menu` VALUES
(1, 'Dal Makhani', 200.00),
(2, 'Butter Paneer', 300.00),
(3, 'Pindi Chole', 200.00),
(4, 'Roti', 25.00),
(5, 'Naan', 50.00),
(6, 'Lachha Parantha', 50.00),
(7, 'Raita', 50.00),
(8, 'Rice', 100.00),
(9, 'Biryani', 200.00),
(10, 'Chole Bhature', 100.00),
(11, 'Paneer Tikka', 300.00),
(12, 'Malai Chaap', 250.00),
(13, 'Lassi', 50.00),
(14, 'Samosa', 20.00),
(15, 'Pizza', 150.00);

Select * from food_menu;




Select * from orders;
Select * from order_tracking;

Select sum(total_price) from orders where order_id = 102;
Select status from order_tracking where order_id = 102;
delete from orders where order_id >= 103;






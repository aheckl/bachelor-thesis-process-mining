USE db_gbs_information_system;

CREATE TABLE bike_type
(
bike_type_id INT PRIMARY KEY AUTO_INCREMENT,
bike_type_name VARCHAR(30) NOT NULL,
cost_per_minute_in_cents INT DEFAULT 1
);


CREATE TABLE location
(
location_id INT PRIMARY KEY AUTO_INCREMENT,
location_name VARCHAR(30) NOT NULL,
credit_check BOOL DEFAULT FALSE
);


CREATE TABLE customer
(
customer_id INT PRIMARY KEY AUTO_INCREMENT,
customer_name VARCHAR(30) NOT NULL,
customer_email VARCHAR(50),
blocked BOOL DEFAULT FALSE
);


CREATE TABLE case_table
(
case_id INT PRIMARY KEY AUTO_INCREMENT,
casetime TIMESTAMP NOT NULL CHECK (casetime > 0),
customer_id INT CHECK (customer_id > 0),
customer_name VARCHAR(30),
bike_type_id INT CHECK (bike_type_id > 0),
bike_type_name VARCHAR(30),
location_id INT CHECK (location_id > 0),
location_name VARCHAR(30),
renting_duration INT,
net_value INT,
variant_id INT CHECK (variant_id > 0),
FOREIGN KEY (customer_id) REFERENCES customer(customer_id),
FOREIGN KEY (bike_type_id) REFERENCES bike_type(bike_type_id),
FOREIGN KEY (location_id) REFERENCES location(location_id)
);


CREATE TABLE activity_table
(
case_id INT NOT NULL CHECK(case_id > 0),
activity VARCHAR(30) NOT NULL,
eventtime TIMESTAMP NOT NULL CHECK (eventtime > 0),
sort INT NOT NULL CHECK (sort > 0)
);


CREATE TABLE bike_type_distr
(
bike_type_id INT PRIMARY KEY,
percentage DECIMAL(3,2) NOT NULL CHECK (percentage BETWEEN 0 AND 1),
FOREIGN KEY (bike_type_id) REFERENCES bike_type(bike_type_id)
);


CREATE TABLE location_distr
(
location_id INT PRIMARY KEY,
percentage DECIMAL(3,2) NOT NULL CHECK (percentage BETWEEN 0 AND 1),
FOREIGN KEY (location_id) REFERENCES location(location_id)
);


CREATE TABLE month_distr
(
month_id INT PRIMARY KEY CHECK (month_id BETWEEN 1 AND 12),
percentage DECIMAL(3,2) NOT NULL CHECK (percentage BETWEEN 0 AND 1)
);


CREATE TABLE hour_distr
(
hour_id INT PRIMARY KEY CHECK (hour_id BETWEEN 0 AND 23),
percentage DECIMAL(3,2) NOT NULL CHECK (percentage BETWEEN 0 AND 1)
);


CREATE TABLE variant_distr
(
variant_id INT PRIMARY KEY,
percentage DECIMAL(3,2) NOT NULL CHECK (percentage BETWEEN 0 AND 1)
);


CREATE TABLE customer_discount_rate
(
customer_id INT NOT NULL,
discount_rate DECIMAL(3,2) DEFAULT 0.00,
FOREIGN KEY (customer_id) REFERENCES customer(customer_id)
);


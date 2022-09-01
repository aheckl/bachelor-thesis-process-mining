USE db_gbs_information_system;


INSERT INTO bike_type VALUES (1, "DXTS1000 - Red", 100), (2, "DXTS1000 - Silver", 200), (3, "DXTS1000 - Gold", 300);

INSERT INTO location VALUES (1, "Munich", FALSE), (2, "Garching", FALSE), (3, "New York", FALSE), (4, "Unterschleissheim", FALSE);

INSERT INTO customer (customer_name) VALUES 
("Michael Huber"),
("Markus Maier"),
("John Doe"),
("Alex Smith"),
("Nick Foles"),
("Tom Brady"),
("Laura Mayer"),
("Jennifer Huber"),
("Jack Wilson"),
("Theresa Lagos");


UPDATE customer SET customer_email = "a.heckl@hotmail.de" WHERE customer_id = 1;
UPDATE customer SET customer_email = "asgeirebybembo@web.de" WHERE customer_id = 2;
UPDATE customer SET customer_email = "heckla@in.tum.de" WHERE customer_id = 3;
UPDATE customer SET customer_email = "heckla@cs.tum.edu" WHERE customer_id = 4;
UPDATE customer SET customer_email = "heckla@informatik.tu-muenchen.de" WHERE customer_id = 5;
UPDATE customer SET customer_email = "andreas.heckl@in.tum.de" WHERE customer_id = 6;
UPDATE customer SET customer_email = "andreas.heckl@cs.tum.edu" WHERE customer_id = 7;
UPDATE customer SET customer_email = "andreas.heckl@informatik.tu-muenchen.de" WHERE customer_id = 8;
UPDATE customer SET customer_email = "andi808@outlook.de" WHERE customer_id = 9;
UPDATE customer SET customer_email = "ga48qeb@mytum.de" WHERE customer_id = 10;


INSERT INTO bike_type_distr VALUES (1, 0.86), (2, 0.08), (3, 0.06);

INSERT INTO location_distr VALUES (1, 0.42), (2, 0.32), (3, 0.15), (4, 0.11);


INSERT INTO month_distr VALUES 
(1, 0.04),
(2, 0.04),
(3, 0.04),
(4, 0.09),
(5, 0.10),
(6, 0.13),
(7, 0.18),
(8, 0.17),
(9, 0.09),
(10, 0.04),
(11, 0.04),
(12, 0.04);


INSERT INTO hour_distr VALUES 
(0, 0.01),
(1, 0.03),
(2, 0.02),
(3, 0.02),
(4, 0.02),
(5, 0.03),
(6, 0.10),
(7, 0.12),
(8, 0.13),
(9, 0.02),
(10, 0.08), 
(11, 0.12),
(12, 0.02),
(13, 0.02),
(14, 0.04),
(15, 0.07),
(16, 0.05),
(17, 0.01),
(18, 0.01),
(19, 0.01),
(20, 0.02),
(21, 0.03),
(22, 0.01),
(23, 0.01);


INSERT INTO variant_distr VALUES 
(1, 0.42),
(2, 0.06),
(3, 0.22),
(4, 0.12),
(5, 0.02),
(6, 0.02),
(7, 0.02),
(8, 0.01),
(9, 0.02),
(10, 0.04),
(11, 0.01),
(12, 0.04);


INSERT INTO customer_discount_rate (customer_id) VALUES 
(1),
(2),
(3),
(4),
(5),
(6),
(7),
(8),
(9),
(10);




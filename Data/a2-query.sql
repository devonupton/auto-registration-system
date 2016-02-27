PROMPT Question 1 - hreherch
-- List the serial_no of all vehicles that are owned by people who live 
-- outside of Edmonton. (A person is considered to live outside of Edmonton 
-- if his/her address does not contains a pattern of 'Edmonton'). 
-- Note that a vehcile will be selected as long as it has one owner who 
-- lives outside of Edmonton.

SELECT 	DISTINCT vehicle.serial_no
FROM 	owner, people, vehicle
WHERE 	vehicle.serial_no = owner.vehicle_id and 
	owner.owner_id = people.sin and 
	people.addr NOT LIKE '%Edmonton%';
	PROMPT Question 2 - hreherch
-- Find the name and address of all people (without duplicates) who are a 
-- primary owner of at least three SUVs.

SELECT 	UNIQUE name, addr
FROM 	owner owner1, owner owner2, owner owner3, people, vehicle_type V, vehicle vehicle1, vehicle vehicle2, vehicle vehicle3
WHERE 	-- ensure owner is the same person
		people.sin = owner1.owner_id and 
		people.sin = owner2.owner_id and
		people.sin = owner3.owner_id and
		-- ensure primary owner of the three
		owner1.is_primary_owner = 'y' and
		owner2.is_primary_owner = 'y' and
		owner3.is_primary_owner = 'y' and
		-- ensure 3 different vehicles 
		owner1.vehicle_id <> owner2.vehicle_id and
		owner2.vehicle_id <> owner3.vehicle_id and
		owner3.vehicle_id <> owner1.vehicle_id and
		-- ensure the vehicles are part of the ownership (or something I don't know wtf is SQL)
		vehicle1.serial_no = owner1.vehicle_id and
		vehicle2.serial_no = owner2.vehicle_id and
		vehicle3.serial_no = owner3.vehicle_id and
		-- ensure all the vehicles are of the type SUV
		V.type = 'SUV' and 
		V.type_id = vehicle1.type_id and
		V.type_id = vehicle2.type_id and
		V.type_id = vehicle3.type_id;
		PROMPT Question 3 - hreherch
-- List the licence_no and name of all drivers (a driver is a person with a 
-- licence of any class other than 'nondriving') who do not own a red vehicle.

-- make table with all names/licence_no who do not have a nondriving licence
(SELECT licence_no, name
 FROM 	people P, drive_licence L
 WHERE 	P.sin = L.sin and
		L.class <> 'nondriving')
MINUS
-- subtract the licences and names of people with red vehicles
(SELECT	licence_no, name
 FROM	People P, drive_licence L, Owner O, Vehicle V
 WHERE	P.sin = L.sin and
	O.owner_id = P.sin and
	V.serial_no = O.vehicle_id and
	V.color = 'red');
PROMPT Question 4 - hreherch
-- List the name of all drivers who have received tickets with the total fine 
-- larger than the average fine. Note that the average fine is the total fine 
-- received by all drivers divided by the number of drivers, and thus all the 
-- tickets received by non-drivers and/or persons without any licences are irrelevant.

SELECT 	name
FROM 	Ticket T, Ticket_Type TT, People P
WHERE 	TT.vtype = T.vtype
		AND P.sin = T.violator_no
		AND P.sin IN ( 	SELECT 	P.sin
						FROM 	People P, drive_Licence L
						WHERE 	P.sin = L.sin
						   		AND L.class <> 'nondriving')
GROUP BY name
HAVING SUM( fine ) > (( SELECT 	SUM( fine )
						FROM 	People P, drive_Licence L, Ticket T, Ticket_Type TT
						WHERE 	TT.vtype = T.vtype 
								AND L.sin = P.sin
								AND L.class <> 'nondriving'
								AND P.sin = T.violator_no )
						/ ( SELECT 	COUNT( * )
						   FROM 	People P, drive_Licence L
						   WHERE 	P.sin = L.sin
						   			AND L.class <> 'nondriving') );
-- The sume of all tickets from drivers (not nondrivers)
-- SELECT 	SUM( fine )
-- FROM 	People P, drive_Licence L, Ticket T, Ticket_Type TT
-- WHERE 	TT.vtype = T.vtype 
-- 		AND L.sin = P.sin
-- 		AND L.class <> 'nondriving'
-- 		AND P.sin = T.violator_no;

-- Count the number of 
-- SELECT 	COUNT( * )
-- FROM 	People P, drive_Licence L
-- WHERE 	P.sin = L.sin
-- 		AND L.class <> 'nondriving';
PROMPT Question 5 - hreherch
-- List the (yearly) average selling price for each type of vehicle, 
-- for 2010 - 2013, inclusive. One needs not consider types with no sales 
-- for the year.

SELECT 	EXTRACT( year FROM TO_DATE( AUS.s_date, 'DD-MM-RR' ) ) AS YEAR, VT.type, AVG( price )
FROM 	Vehicle V, Vehicle_Type VT, AUto_Sale AUS
WHERE 	EXTRACT( year FROM TO_DATE( AUS.s_date, 'DD-MM-RR' ) ) >= 2010
	AND EXTRACT( year FROM TO_DATE( AUS.s_date, 'DD-MM-RR' ) ) <= 2013
	AND V.type_id = VT.type_id
	AND V.serial_no = AUS.vehicle_id
GROUP BY EXTRACT( year FROM TO_DATE( AUS.s_date, 'DD-MM-RR' ) ), VT.type
ORDER BY EXTRACT( year FROM TO_DATE( AUS.s_date, 'DD-MM-RR' ) ) DESC;
PROMPT Question 6 - hreherch
-- The most popular vehicle of a given type in a given year is the the maker 
-- and model with more vehicles registered than any others in its type.  
-- List the name of all people who never own a most popular vehicle 
-- (with duplication possible).

-- minus all names from names that own a most popular vehicle
(SELECT name 
 FROM People)
MINUS
(SELECT name
 FROM 	People P, 
	Owner O, 
	vehicle_type VT, 
	Vehicle V, 
	-- add table of "most popular" cars
	(SELECT VT1.type, V1.maker, V1.model, V1.year
	 FROM vehicle V1, vehicle_type VT1
	 WHERE V1.type_id = VT1.type_id
	 GROUP BY VT1.type, V1.maker, V1.model, V1.year
	 HAVING COUNT( * ) >= ALL ( SELECT COUNT( * )
				    FROM   vehicle V2, vehicle_type VT2
				    WHERE  V2.type_id = VT2.type_id
					   AND VT1.type = VT2.type
				    GROUP BY VT2.type, V2.maker, V2.model, V2.year )) PVT
WHERE 	P.sin = O.owner_id  
	AND O.vehicle_id = V.serial_no
	AND VT.type_id = V.type_id
	AND PVT.type = VT.type
	AND PVT.maker = V.maker
	AND PVT.model = V.model
	AND PVT.year = V.year);

-- used in the above table 
-- list cars which are the "most popular"
-- SELECT VT1.type, V1.maker, V1.model, V1.year
-- FROM vehicle V1, vehicle_type VT1
-- WHERE v1.type_id = VT1.type_id
-- GROUP BY VT1.type, V1.maker, V1.model, V1.year
-- HAVING COUNT( * ) >= ALL ( SELECT COUNT( * )
-- 			   FROM   vehicle V2, vehicle_type VT2
-- 			   WHERE  V2.type_id = VT2.type_id
-- 			   	  AND VT1.type = VT2.type
-- 			   GROUP BY VT2.type, V2.maker, V2.model, V2.year );
PROMPT Question 7 - hreherch
-- A moving ticket is any ticket that are not a ticket of 'parking' type. 
-- List the sin, name, and address of all people who have received three 
-- moving tickets during last one year, i.e. since one year before today.

-- Select the the sin number, name, and address of someone who 
-- has 3 or more non 'parking' tickets
SELECT 	P.sin, P.name, P.addr
FROM 	People P, Ticket T
WHERE 	P.sin = T.violator_no 
	AND T.vtype <> 'parking'
	-- add -12 month to the current date to find all tickets from now to a year before today
	AND T.vdate >= ADD_MONTHS( SYSDATE, -12 )
	-- make sure that no violations after today are picked up 
	AND T.vdate <= SYSDATE
GROUP BY P.sin, P.name, P.addr
HAVING COUNT( * ) >= 3;
PROMPT Question 4 - hreherch
-- List the name of all drivers who have received tickets with the total fine 
-- larger than the average fine. Note that the average fine is the total fine 
-- received by all drivers divided by the number of drivers, and thus all the 
-- tickets received by non-drivers and/or persons without any licences are irrelevant.

SELECT 	name
FROM 	Ticket T, Ticket_Type TT, People P
WHERE 	TT.vtype = T.vtype
		AND P.sin = T.violator_no
		AND P.sin IN ( 	SELECT 	P.sin
						FROM 	People P, drive_Licence L
						WHERE 	P.sin = L.sin
						   		AND L.class <> 'nondriving')
GROUP BY name
HAVING SUM( fine ) > (( SELECT 	SUM( fine )
						FROM 	People P, drive_Licence L, Ticket T, Ticket_Type TT
						WHERE 	TT.vtype = T.vtype 
								AND L.sin = P.sin
								AND L.class <> 'nondriving'
								AND P.sin = T.violator_no )
						/ ( SELECT 	COUNT( * )
						   FROM 	People P, drive_Licence L
						   WHERE 	P.sin = L.sin
						   			AND L.class <> 'nondriving') );
-- The sume of all tickets from drivers (not nondrivers)
-- SELECT 	SUM( fine )
-- FROM 	People P, drive_Licence L, Ticket T, Ticket_Type TT
-- WHERE 	TT.vtype = T.vtype 
-- 		AND L.sin = P.sin
-- 		AND L.class <> 'nondriving'
-- 		AND P.sin = T.violator_no;

-- Count the number of 
-- SELECT 	COUNT( * )
-- FROM 	People P, drive_Licence L
-- WHERE 	P.sin = L.sin
-- 		AND L.class <> 'nondriving';
PROMPT Question 5 - hreherch
-- List the (yearly) average selling price for each type of vehicle, 
-- for 2010 - 2013, inclusive. One needs not consider types with no sales 
-- for the year.

SELECT 	EXTRACT( year FROM TO_DATE( AUS.s_date, 'DD-MM-RR' ) ) AS YEAR, VT.type, AVG( price )
FROM 	Vehicle V, Vehicle_Type VT, AUto_Sale AUS
WHERE 	EXTRACT( year FROM TO_DATE( AUS.s_date, 'DD-MM-RR' ) ) >= 2010
	AND EXTRACT( year FROM TO_DATE( AUS.s_date, 'DD-MM-RR' ) ) <= 2013
	AND V.type_id = VT.type_id
	AND V.serial_no = AUS.vehicle_id
GROUP BY EXTRACT( year FROM TO_DATE( AUS.s_date, 'DD-MM-RR' ) ), VT.type
ORDER BY EXTRACT( year FROM TO_DATE( AUS.s_date, 'DD-MM-RR' ) ) DESC;
PROMPT Question 6 - hreherch
-- The most popular vehicle of a given type in a given year is the the maker 
-- and model with more vehicles registered than any others in its type.  
-- List the name of all people who never own a most popular vehicle 
-- (with duplication possible).

-- minus all names from names that own a most popular vehicle
(SELECT name 
 FROM People)
MINUS
(SELECT name
 FROM 	People P, 
	Owner O, 
	vehicle_type VT, 
	Vehicle V, 
	-- add table of "most popular" cars
	(SELECT VT1.type, V1.maker, V1.model, V1.year
	 FROM vehicle V1, vehicle_type VT1
	 WHERE V1.type_id = VT1.type_id
	 GROUP BY VT1.type, V1.maker, V1.model, V1.year
	 HAVING COUNT( * ) >= ALL ( SELECT COUNT( * )
				    FROM   vehicle V2, vehicle_type VT2
				    WHERE  V2.type_id = VT2.type_id
					   AND VT1.type = VT2.type
				    GROUP BY VT2.type, V2.maker, V2.model, V2.year )) PVT
WHERE 	P.sin = O.owner_id  
	AND O.vehicle_id = V.serial_no
	AND VT.type_id = V.type_id
	AND PVT.type = VT.type
	AND PVT.maker = V.maker
	AND PVT.model = V.model
	AND PVT.year = V.year);

-- used in the above table 
-- list cars which are the "most popular"
-- SELECT VT1.type, V1.maker, V1.model, V1.year
-- FROM vehicle V1, vehicle_type VT1
-- WHERE v1.type_id = VT1.type_id
-- GROUP BY VT1.type, V1.maker, V1.model, V1.year
-- HAVING COUNT( * ) >= ALL ( SELECT COUNT( * )
-- 			   FROM   vehicle V2, vehicle_type VT2
-- 			   WHERE  V2.type_id = VT2.type_id
-- 			   	  AND VT1.type = VT2.type
-- 			   GROUP BY VT2.type, V2.maker, V2.model, V2.year );
PROMPT Question 7 - hreherch
-- A moving ticket is any ticket that are not a ticket of 'parking' type. 
-- List the sin, name, and address of all people who have received three 
-- moving tickets during last one year, i.e. since one year before today.

-- Select the the sin number, name, and address of someone who 
-- has 3 or more non 'parking' tickets
SELECT 	P.sin, P.name, P.addr
FROM 	People P, Ticket T
WHERE 	P.sin = T.violator_no 
	AND T.vtype <> 'parking'
	-- add -12 month to the current date to find all tickets from now to a year before today
	AND T.vdate >= ADD_MONTHS( SYSDATE, -12 )
	-- make sure that no violations after today are picked up 
	AND T.vdate <= SYSDATE
GROUP BY P.sin, P.name, P.addr
HAVING COUNT( * ) >= 3;
PROMPT Question 8 - hreherch
-- Create a view called vehicle_history with columns vehicle_no, number_sales, 
-- average_price, and total_tickets to record, for each vehicle, the number of 
-- times the vehicle has been changed hand, the average price, and the number 
-- of tickets it has been involved. One may assume that each vehicle has gone 
-- through at least one sale. Note that  total_tickets is counted as the number 
-- of distinct ticket_no's associated with one vehicle.

-- COLUMNS: vehicle_no, number_sales, AVG(price), total_tickets
-- EVERY VEHICLE HAS GONE THROUGH AT LEAST ONE SALE

-- Drop the view to prevent errors
DROP VIEW vehicle_history;

-- create: VEHICLE_HISTORY( vehicle_no, number_sales, average_price, total_tickets )
CREATE VIEW vehicle_history AS
	SELECT 	V.serial_no vehicle_no, 
		-- COUNT all the auto_sales a vehicle has been in
		(SELECT COUNT( * )
		 FROM 	auto_sale
		 WHERE 	V.serial_no = vehicle_id ) number_sales,
		-- AVG the price of all he auto sales of a serial_no
		(SELECT AVG( price )
		 FROM 	auto_sale
		 WHERE V.serial_no = vehicle_id ) average_price,
		-- COUNT the number of tickets a serial_no recieved 
		(SELECT COUNT( * )
		 FROM 	Ticket T
		 WHERE 	T.vehicle_id = V.serial_no ) total_tickets
	FROM Vehicle V;

COMMIT;

--SELECT * FROM Vehicle_History;
PROMPT Question 9 - hreherch
-- Use the view created earlier to list the sin and name of all persons who
-- own the vehicle(s) with the least average sale price, the highest number of 
-- sales, or the largest total tickets.

-- @8.sql

-- Select the sin(s) and name(s) of people who own vehicle(s) that match the Q criteria
SELECT 	DISTINCT P.sin, P.name
FROM 	People P, Owner O, Vehicle V
WHERE 	-- ensure that the 3 tables are naturally joined 
	P.sin = O.owner_id
	AND O.vehicle_id = V.serial_no
	-- compare person's vehicle with the list of vehicle serial numbers that meet the conditions
	AND V.serial_no IN (SELECT VH.vehicle_no
			    FROM   Vehicle_History VH
			    WHERE  VH.average_price = (SELECT MIN( average_price )
			 			       FROM   Vehicle_History )
				   OR VH.number_sales = (SELECT MAX( number_sales )
			     				 FROM   Vehicle_History )
				   OR VH.total_tickets = (SELECT MAX( total_tickets )
			    			          FROM   Vehicle_History )
			);

--Used in the above query
--Create a list of vehicle serial numbers that meet the conditions
--SELECT VH.vehicle_no
--FROM Vehicle_History VH
--WHERE VH.average_price = (SELECT MIN( average_price )
--			    FROM   Vehicle_History )
--	OR VH.number_sales = (SELECT MAX( number_sales )
--			      FROM   Vehicle_History )
--	OR total_tickets = (SELECT MAX( total_tickets )
--			    FROM   Vehicle_History );

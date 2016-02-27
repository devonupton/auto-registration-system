/*
 *  Solutions to Assignment 2
 *   CMPUT 291,  W2016
 *   Prepared by A Teaching Assistant
 */
prompt Question 1 - haiming1
/*
 *   (1) check if the address starting or ending with 'Edmonton'
 *   
 */
SELECT DISTINCT	vehicle_id
FROM	owner o, people p
WHERE	o.owner_id = p.sin AND
	p.addr NOT LIKE '%Edmonton%';

prompt Question 2 - haiming1
/**
*  (1) be able to avoid duplicates
**/
SELECT DISTINCT p.name, p.addr
FROM   people p, owner o1, owner o2, owner o3,
       vehicle v1, vehicle v2, vehicle v3, vehicle_type t1
WHERE p.sin = o1.owner_id AND
      p.sin = o2.owner_id AND
      p.sin = o3.owner_id AND
      o1.vehicle_id = v1.serial_no AND 
      o1.is_primary_owner = 'y' AND 
      v1.type_id = t1.type_id  AND
      o2.vehicle_id = v2.serial_no AND 
      o2.is_primary_owner = 'y' AND 
      v2.type_id = t1.type_id  AND
      o3.vehicle_id = v3.serial_no AND 
      o3.is_primary_owner = 'y' AND 
      v3.type_id = t1.type_id  AND
      v1.serial_no <> v2.serial_no AND
      v2.serial_no <> v3.serial_no AND
      v3.serial_no <> v1.serial_no AND
      t1.type = 'SUV';

prompt Question 3 - haiming1
/*
 *   (1) be able to check if a person own one red car and at least one car of
 *       other color.
 *   (2) be able to check if a non-driver who owns a red car and
 *       a non-driver who does not own a red car
 */
SELECT licence_no, name
FROM   people p, drive_licence d
WHERE  p.sin = d.sin AND
       d.class <> 'nondriving'
MINUS 
SELECT licence_no, name
FROM   people p, drive_licence d, owner o, vehicle v
WHERE  p.sin = d.sin AND
       d.class <> 'nondriving' AND
       p.sin = o.owner_id AND
       o.vehicle_id = v.serial_no AND
       v.color = 'red' ;

prompt Question 4 - haiming1
/*
 *   (1) all drivers without tickets must be counted,
 *   (2) all non-drivers shall not be counted
 *   (3) at least one driver with multiple tickets 
 *       to check if distinct is used in count(d.licence_no)
 *   (4) should group by p.sin and p.name to avoid same names
 */
SELECT p.name
FROM   people p, drive_licence d, ticket t, ticket_type tt
WHERE  p.sin = d.sin AND
       d.class <> 'nondriving' AND
       p.sin = t.violator_no AND
       t.vtype = tt.vtype
GROUP BY p.sin, p.name
HAVING SUM(tt.fine) >= ALL ( SELECT SUM(tt.fine) / COUNT(distinct d.licence_no)
	                     FROM   people p, drive_licence d, ticket t,ticket_type tt
	                     WHERE  p.sin = d.sin AND
				    d.class <> 'nondriving' AND
		                    t.violator_no(+) = p.sin AND
		                    tt.vtype (+) = t.vtype 
	                     );

prompt Question 5 - haiming1
/*
 *    (1) be able to include both 2003 and 2010
 *    (2) selling price is the price when it was sold.
 */
SELECT extract(year from a.s_date) AS YEAR, vt.type, AVG(price)
FROM   auto_sale a, vehicle v, vehicle_type vt
WHERE  a.vehicle_id = v.serial_no AND
       v.type_id = vt.type_id AND
       extract(year from a.s_date) between 2003 and 2010
GROUP BY  extract(year from a.s_date), vt.type;

prompt Question 6 - haiming1
/*
 *   (1) the same maker/model but difference year than a popular one is not
 *       a popular vehicle
 *
 */
SELECT name
FROM   people
MINUS
SELECT name
FROM   people p, owner o, vehicle v1
WHERE  p.sin = o.owner_id AND   
       o.vehicle_id = v1.serial_no AND
       (v1.maker, v1.model, v1.year)
       IN (SELECT  v2.maker, v2.model, v2.year
           FROM    vehicle v2
           GROUP BY v2.maker, v2.model, v2.year ,v2.type_id
           HAVING  count(*)>= ALL(SELECT  count(*)
 			          FROM    vehicle v3
			          WHERE   v2.year = v3.year AND
				          v2.type_id = v3.type_id
		                  GROUP BY v3.maker,v3.model,v3.year,v3.type_id
		                 )
         );

prompt Question 7 - haiming1
/*
 *    (1) be able to differentiate 'parking' and other 'moving' tickets
 *    (2) tolerate either 365 or 366 shall be fine
 *    (3) be able to check if it is exactly 3.
 */
SELECT sin, name, addr
FROM   people p, ticket t
WHERE  p.sin = t.violator_no AND
       t.vtype <> 'parking' AND
       t.vdate > sysdate -365
GROUP BY sin, name, addr
HAVING count(*) = 3;

prompt Question 8 - haiming1
/*
 *   (1)  be able to check if count(distinct ticket_no) is used for total_tickets.
 *   (2)  be able to check if count(distinct transaction_id) is used for number_sales.
 *   (3)  we may assume each vehicle has at least one sales, though
 *        it is not neccessary.
 */
DROP VIEW vehicle_history;
CREATE VIEW vehicle_history 
(vehicle_no, number_sales, average_price, total_tickets)
AS
SELECT  h.serial_no, count(DISTINCT transaction_id), avg(price), count(DISTINCT t.ticket_no)
FROM   	vehicle h, auto_sale a, ticket t
WHERE   t.vehicle_id (+) = h.serial_no AND
        a.vehicle_id (+) = h.serial_no
GROUP BY h.serial_no;

prompt Question 9 - haiming1
/*
 *   (1) must be albe to check all three cases
 *
 */
SELECT DISTINCT sin, name
FROM   people p, owner o, vehicle_history h
WHERE  p.sin = o.owner_id AND
       o.vehicle_id = h.vehicle_no AND
       ( h.average_price <= ALL( SELECT average_price
			 FROM vehicle_history )    
         OR 
         (h.number_sales  >= ALL ( SELECT number_sales
	 	           	   FROM vehicle_history
		                  )
         )
         OR
         (h.total_tickets >= ALL ( SELECT total_tickets
			           FROM vehicle_history )
         )
       );

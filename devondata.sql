/* People */

INSERT INTO people 
VALUES('Person1','Devon Upton', 6, 140, 'Blue', 'Brown', '1234 NotMyAddress Ave Edmonton AB', 'm', '18-SEP-1995');

INSERT INTO people 
VALUES('Person2','Bob Guy', 6.5, 200, 'Brown', 'Blonde', '123 Red Deer', 'm', '12-NOV-1979'); 

INSERT INTO people 
VALUES('President','Barack Obama', 6.1, 180, 'Brown', 'Brown', 'The White House', 'm', '4-AUG-1961'); 

INSERT INTO people 
VALUES('NotAnOwner','Melissa Parker', 4.5, 130, 'Brown', 'Blonde', '456 Edmonton', 'f', '27-MAY-1994');

INSERT INTO people 
VALUES('OfficerID','Clancy Wiggum', 5, 250, 'Black', 'Blue', 'The Police Department, Springfield', 'm', '27-MAY-1960');


/* Licences */

INSERT INTO drive_licence
VALUES('100', 'Person1', 'nondriving', NULL, '18-OCT-2012', '18-OCT-2016');

INSERT INTO drive_licence
VALUES('200', 'Person2', 'driving', NULL, '18-OCT-2012', '18-OCT-2016');

INSERT INTO drive_licence
VALUES('300', 'President', 'driving', NULL, '18-OCT-2012', '18-OCT-2016');

INSERT INTO drive_licence
VALUES('400', 'NotAnOwner', 'driving', NULL, '18-OCT-2012', '18-OCT-2016');


/* Vehicle Types */

INSERT INTO vehicle_type
VALUES(1,'SUV');

INSERT INTO vehicle_type
VALUES(2,'CAR');


/* Vehicles */

INSERT INTO vehicle
VALUES('111','Ford','Strawberry', 2005, 'red', 1);

INSERT INTO vehicle
VALUES('222','Ford','Strawberry', 2005, 'blue', 1);

INSERT INTO vehicle
VALUES('333','Trucker','Cheese', 2005, 'red', 2);

INSERT INTO vehicle
VALUES('444','Tesla','Model S', 2013, 'orange', 1);

INSERT INTO vehicle
VALUES('555','Awesome','Presidents SUV', 2005, 'black', 1);


/* Ownerships */

INSERT INTO owner
VALUES('Person1', '111', 'y');

INSERT INTO owner
VALUES('Person1', '222', 'y');

INSERT INTO owner
VALUES('Person2', '333', 'y');

INSERT INTO owner
VALUES('Person1', '444', 'y');

INSERT INTO owner
VALUES('President', '555', 'y');


/* Auto Sales */

INSERT INTO auto_sale
VALUES(1,'NotAnOwner','Person1','222','19-OCT-2010', 20000);

INSERT INTO auto_sale
VALUES(2,'NotAnOwner','Person1','444','19-OCT-2010', 40000);

INSERT INTO auto_sale
VALUES(3,'NotAnOwner','Person2','333','19-OCT-2010', 3456);

INSERT INTO auto_sale
VALUES(4,'NotAnOwner','Person1','111','19-OCT-2012', 30000);

INSERT INTO auto_sale
VALUES(5,'NotAnOwner','Person1','111','19-NOV-2012', 50000);

INSERT INTO auto_sale
VALUES(6,'NotAnOwner','President','555','19-NOV-2013', 567899);


/* Ticket types */

INSERT INTO ticket_type
VALUES('moving',100);

INSERT INTO ticket_type
VALUES('parking', 40);

INSERT INTO ticket_type
VALUES('other', 90);


/* Tickets */

INSERT INTO ticket
VALUES(001,'Person1','444', 'OfficerID', 'moving', '12-OCT-2015', 'Edmonton', 'Notes');

INSERT INTO ticket
VALUES(002,'Person1','444', 'OfficerID', 'moving', '12-JAN-2016', 'Edmonton', 'Notes');

INSERT INTO ticket
VALUES(003,'Person1','444', 'OfficerID', 'moving', '12-DEC-2015', 'Edmonton', 'Notes');

INSERT INTO ticket
VALUES(004,'Person2','444', 'OfficerID', 'parking', '12-OCT-2015', 'Edmonton', 'A deer damaged the bumper');

INSERT INTO ticket
VALUES(005,'NotAnOwner','111', 'OfficerID', 'moving', '26-JAN-2016', 'Edmonton', 'She crashed into a car');

INSERT INTO ticket
VALUES(006,'President','555', 'OfficerID', 'other', '12-JAN-2016', 'Washington DC', 'The back wheels fell off');

commit;

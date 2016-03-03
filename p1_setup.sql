/*
 *  This file is used to create the database schema for Assignment 2
 *  CMPUT291, Winter Term, 2016.
 *  It is the same as the one for Assignment 2, except some comments are added.
 * 
 *  Author: Li-Yan Yuan
 *  University of Alberta
 *  
 */
DROP TABLE owner;
DROP TABLE auto_sale;
DROP TABLE restriction;
DROP TABLE driving_condition;
DROP TABLE ticket;
DROP TABLE ticket_type;
DROP TABLE vehicle;
DROP TABLE vehicle_type;
DROP TABLE drive_licence;
DROP TABLE people;

/*
 *  Table containing all the info for each person
 */
CREATE TABLE  people (
  sin           CHAR(15),  
  name          VARCHAR(40),
  height        number(5,2),
  weight        number(5,2),
  eyecolor      VARCHAR (10),
  haircolor     VARCHAR(10),
  addr          VARCHAR2(50),
  gender        CHAR,
  birthday      DATE,
  PRIMARY KEY (sin),
  CHECK ( gender IN ('m', 'f') )
);

/*
 *  Table containing drive_licence info
 */
CREATE TABLE drive_licence (
  licence_no      CHAR(15),
  sin             char(15),
  class           VARCHAR(10),
  photo           BLOB,
  issuing_date    DATE,
  expiring_date   DATE,
  PRIMARY KEY (licence_no),
  UNIQUE (sin),
  FOREIGN KEY (sin) REFERENCES people
        ON DELETE CASCADE
);

/*
 *  The driving conditions
 */
CREATE TABLE driving_condition (
  c_id        INTEGER,
  description VARCHAR(1024),
  PRIMARY KEY (c_id)
);

/*
 *   to indicate the driving conditions for each drive licence
 */
CREATE TABLE restriction(
  licence_no   CHAR(15),
  r_id         INTEGER,
  PRIMARY KEY (licence_no, r_id),
  FOREIGN KEY (licence_no) REFERENCES drive_licence,
  FOREIGN KEY (r_id) REFERENCES driving_condition
);

/*
 *  to store all the typles of vehicles
 */
CREATE TABLE vehicle_type (
  type_id       integer,
  type          CHAR(10),
  PRIMARY KEY (type_id)
);

/*
 *   Vehicle information
 */
CREATE TABLE vehicle (
  serial_no    CHAR(15),
  maker        VARCHAR(20),	
  model        VARCHAR(20),
  year         number(4,0),
  color        VARCHAR(10),
  type_id      integer,
  PRIMARY KEY (serial_no),
  FOREIGN KEY (type_id) REFERENCES vehicle_type
);

/*
 *   The ownership of each vehicle
 */
CREATE TABLE owner (
  owner_id          CHAR(15),
  vehicle_id        CHAR(15),
  is_primary_owner  CHAR(1),
  PRIMARY KEY (owner_id, vehicle_id),
  FOREIGN KEY (owner_id) REFERENCES people,
  FOREIGN KEY (vehicle_id) REFERENCES vehicle,
  CHECK ( is_primary_owner IN ('y', 'n'))
);

/*
 *  To record auto sales
 */
CREATE TABLE auto_sale (
  transaction_id  int,
  seller_id   CHAR(15),
  buyer_id    CHAR(15),
  vehicle_id  CHAR(15),
  s_date      date,
  price       numeric(9,2),
  PRIMARY KEY (transaction_id),
  FOREIGN KEY (seller_id) REFERENCES people,
  FOREIGN KEY (buyer_id) REFERENCES people,
  FOREIGN KEY (vehicle_id) REFERENCES vehicle
);

/*
 *  all the ticket types
 */
CREATE TABLE ticket_type (
  vtype     CHAR(10),
  fine      number(5,2),
  PRIMARY KEY (vtype)
);

/*
 *  Ticket records
 */
CREATE TABLE ticket (
  ticket_no     int,
  violator_no   CHAR(15),  
  vehicle_id    CHAR(15),
  office_no     CHAR(15),
  vtype        char(10),
  vdate        date,
  place        varchar(20),
  descriptions varchar(1024),
  PRIMARY KEY (ticket_no),
  FOREIGN KEY (vtype) REFERENCES ticket_type,
  FOREIGN KEY (violator_no) REFERENCES people ON DELETE CASCADE,
  FOREIGN KEY (vehicle_id)  REFERENCES vehicle,
  FOREIGN KEY (office_no) REFERENCES people ON DELETE CASCADE
);


-- vehicle types
INSERT INTO vehicle_type VALUES ( 101, 'SUV' );
INSERT INTO vehicle_type VALUES ( 202, 'Mini Van' );
INSERT INTO vehicle_type VALUES ( 303, 'pickup' );

-- the salesman
INSERT INTO people VALUES ( '05-12345tsm', 'Thay Salesmen', 176, 200, 'blue', 'black', 'Edmonton', 'm', '27-JUN-1987');
INSERT INTO drive_licence VALUES ( 'ln-0006tsm', '05-12345tsm', 'driving', NULL, NULL, NULL );
INSERT INTO vehicle VALUES ( 'q5-vin001', 'TESLA', 'E70-t', 2004, 'orange', 303 );
INSERT INTO vehicle VALUES ( 'q5-vin002', 'FORD', 'best', 2007, 'silver', 202 );
INSERT INTO vehicle VALUES ( 'q5-vin003', 'HONDA', 'F2', 2008, 'green', 101 );
INSERT INTO vehicle VALUES ( 'q5-vin004', 'TYOTA', 'F6-50', 2003, 'orange', 101 );
INSERT INTO vehicle VALUES ( 'q5-vin008', 'SUZUKI', 'Crush', 2012, 'pink', 101 );
INSERT INTO vehicle VALUES ( 'q5-vin005', 'VOLKS', 'G6', 2010, 'yellow', 202 );
INSERT INTO vehicle VALUES ( 'q5-vin006', 'TESLA', 'E70-t', 2014, 'blue', 303 );
INSERT INTO vehicle VALUES ( 'q5-vin007', 'AUDI', 'lemon', 2013, 'cyan', 202 );

-- Person - CHAR sin, varchar name, num height, num weight, varchar eye color, haricolor varchar, addr varchar, gender CHAR, birthday DATE (sin key)
INSERT INTO people VALUES ( '00-12345kb', 'Kieter Balisnomo', 175, 125, 'brown', 'black', 'Edmonton', 'm', '21-JAN-1997');
INSERT INTO drive_licence VALUES ( 'ln-0001kb', '00-12345kb', 'nondriving', NULL, NULL, NULL );
INSERT INTO vehicle VALUES ( 'q1-trivialtest2', 'AUDI', 'sexbomb', 2009, 'black', 101 );
INSERT INTO auto_sale VALUES ( 18, '05-12345tsm', '00-12345kb', 'q1-trivialtest2', '21-JUL-2011', 1950.5 );
INSERT INTO owner VALUES ( '00-12345kb', 'q1-trivialtest2', 'y' );

INSERT INTO people VALUES ( '01-12345bh', 'Bennett Hreherchuk', 180, 172, 'blue', 'brown', 'Deadmonton', 'm', '14-DEC-1995');
INSERT INTO drive_licence VALUES ( 'ln-0002bh', '01-12345bh', 'driving', NULL, NULL, NULL );
INSERT INTO vehicle VALUES ( 'q1-trivialtest', 'TYOTA', 'F1-50', 2005, 'pink', 101 );
INSERT INTO auto_sale VALUES ( 17, '05-12345tsm', '01-12345bh', 'q1-trivialtest', '14-JUN-2012', 950 );
INSERT INTO owner VALUES ( '01-12345bh', 'q1-trivialtest', 'y' );
INSERT INTO owner VALUES ( '01-12345bh', 'q5-vin001', 'n' );

-- test 3 SUVs
INSERT INTO people VALUES ( '02-12345vrl', 'Veri Richlady', 165, 112, 'brown', 'black', 'Little old mansion lane, Calgary', 'f', '4-MAR-1977');
INSERT INTO drive_licence VALUES ( 'ln-0003vrl', '02-12345vrl', 'driving', NULL, NULL, NULL );
INSERT INTO vehicle VALUES ( 'q2-trivial01', 'CHEVI', 'richVer', 2013, 'purple', 101 );
INSERT INTO auto_sale VALUES ( 16, '05-12345tsm', '02-12345vrl', 'q2-trivial01', '1-MAY-2013', 950 );
INSERT INTO owner VALUES ( '02-12345vrl', 'q2-trivial01', 'y' );
INSERT INTO vehicle VALUES ( 'q2-trivial02', 'HONDA', 'yknow', 2015, 'red', 101 );
INSERT INTO auto_sale VALUES ( 15, '05-12345tsm', '02-12345vrl', 'q2-trivial02', '1-MAY-2013', 1650 );
INSERT INTO owner VALUES ( '02-12345vrl', 'q2-trivial02', 'y' );
INSERT INTO vehicle VALUES ( 'q2-trivial03', 'SUZUKI', 'that one', 2007, 'orange', 101 );
INSERT INTO auto_sale VALUES ( 14, '05-12345tsm', '02-12345vrl', 'q2-trivial03', '12-FEB-2011', 1250 );
INSERT INTO owner VALUES ( '02-12345vrl', 'q2-trivial03', 'y' );

-- test 3 variable cars
INSERT INTO people VALUES ( '03-12345tc', 'Thee Collktar', 190, 250, 'amber', 'red', 'The junkyard of Edmonton', 'm', '12-APR-1967');
INSERT INTO drive_licence VALUES ( 'ln-0004tc', '03-12345tc', 'driving', NULL, NULL, NULL );
INSERT INTO vehicle VALUES ( 'q2-complic01', 'CHEVI', 'jank ver', 2005, 'green', 202 );
INSERT INTO auto_sale VALUES ( 13, '05-12345tsm', '03-12345tc', 'q2-complic01', '1-MAR-2010', 1650 );
INSERT INTO owner VALUES ( '03-12345tc', 'q2-complic01', 'y' );
INSERT INTO vehicle VALUES ( 'q2-complic02', 'HONDA', 'ratchver', 2001, 'pink', 101 );
INSERT INTO auto_sale VALUES ( 12, '05-12345tsm', '03-12345tc', 'q2-complic02', '12-APR-2011', 1150 );
INSERT INTO owner VALUES ( '03-12345tc', 'q2-complic02', 'y' );
INSERT INTO vehicle VALUES ( 'q2-complic03', 'SUZUKI', 'that one', 1995, 'blue', 101 );
INSERT INTO auto_sale VALUES ( 11, '05-12345tsm', '03-12345tc', 'q2-complic03', '1-AUG-2012', 950 );
INSERT INTO owner VALUES ( '03-12345tc', 'q2-complic03', 'y' );

-- test non-primary owner 3 SUVs
INSERT INTO people VALUES ( '04-12345tso', 'Ther Skondownr', 160, 145, 'hazel', 'orange', 'Sylvan Lake', 'f', '27-FEB-1982');
INSERT INTO drive_licence VALUES ( 'ln-0005tso', '04-12345tso', 'driving', NULL, NULL, NULL );
INSERT INTO owner VALUES ( '04-12345tso', 'q2-complic02', 'n' ); 
INSERT INTO owner VALUES ( '04-12345tso', 'q2-trivial01', 'n' ); 
INSERT INTO vehicle VALUES ( 'q2-complic04', 'AUDI', 'the one', 2010, 'black', 101 );
INSERT INTO auto_sale VALUES ( 20, '05-12345tsm', '04-12345tso', 'q2-complic04', '11-AUG-2013', 2550 );
INSERT INTO owner VALUES ( '04-12345tso', 'q2-complic03', 'y' );

-- TICKET TYPES
INSERT INTO ticket_type VALUES ( 'being fine', 100 );
INSERT INTO ticket_type VALUES ( 'parking', 50 );
INSERT INTO ticket_type VALUES ( 'moving', 150 );
INSERT INTO ticket_type VALUES ( 'v manslgt', 999 );

-- giving tickets
-- give kieter some fines 
INSERT INTO ticket VALUES ( 0, '00-12345kb', 'q1-trivialtest2', '01-12345bh', 'being fine', SYSDATE, NULL, NULL );
INSERT INTO ticket VALUES ( 2, '00-12345kb', 'q1-trivialtest2', '01-12345bh', 'being fine', '1-JAN-2016', NULL, NULL );
INSERT INTO ticket VALUES ( 3, '00-12345kb', 'q1-trivialtest2', '01-12345bh', 'being fine', '4-JAN-2016', NULL, NULL );
INSERT INTO ticket VALUES ( 4, '00-12345kb', 'q1-trivialtest2', '01-12345bh', 'being fine', '16-OCT-2015', NULL, NULL );
INSERT INTO ticket VALUES ( 5, '00-12345kb', 'q1-trivialtest2', '01-12345bh', 'parking', '18-NOV-2015', NULL, NULL );
-- give bennett some fines
INSERT INTO ticket VALUES ( 1, '01-12345bh', 'q1-trivialtest', '00-12345kb', 'being fine', '16-OCT-2015', NULL, NULL );
INSERT INTO ticket VALUES ( 9, '01-12345bh', 'q1-trivialtest', '00-12345kb', 'moving', '16-OCT-2015', NULL, NULL );
INSERT INTO ticket VALUES ( 30, '01-12345bh', 'q1-trivialtest', '00-12345kb', 'parking', '18-NOV-2015', NULL, NULL );
INSERT INTO ticket VALUES ( 31, '01-12345bh', 'q1-trivialtest', '00-12345kb', 'parking', '19-DEC-2015', NULL, NULL );
INSERT INTO ticket VALUES ( 32, '01-12345bh', 'q1-trivialtest', '00-12345kb', 'parking', '20-MAR-2015', NULL, NULL );
-- give a v. mnslgt fine
INSERT INTO ticket VALUES ( 6, '02-12345vrl', 'q2-trivial01', '01-12345bh', 'v manslgt', '25-MAR-2013', NULL, NULL );
INSERT INTO ticket VALUES ( 7, '02-12345vrl', 'q2-trivial02', '01-12345bh', 'v manslgt', '14-DEC-2014', NULL, NULL );
INSERT INTO ticket VALUES ( 8, '02-12345vrl', 'q2-trivial03', '01-12345bh', 'v manslgt', '16-OCT-2014', NULL, NULL );

-- give kieter anything but a rolls royce
INSERT INTO auto_sale VALUES ( 7, '05-12345tsm', '00-12345kb', 'q5-vin006', '21-JAN-2010', 100 );
INSERT INTO owner VALUES ( '00-12345kb', 'q5-vin006', 'y' ); 
INSERT INTO auto_sale VALUES ( 8, '05-12345tsm', '00-12345kb', 'q5-vin007', '21-JAN-2013', 3400 );
INSERT INTO owner VALUES ( '00-12345kb', 'q5-vin007', 'y' ); 

-- various buyers
INSERT INTO people VALUES ( '07-buysin01', 'Tink Hart', 130, 150, 'green', 'brown', 'Red Deer', 'f', '13-OCT-1993');
INSERT INTO drive_licence VALUES ( 'ln-0007b01', '07-buysin01', 'driving', NULL, NULL, NULL );
INSERT INTO auto_sale VALUES ( 0, '05-12345tsm', '07-buysin01', 'q5-vin001', '4-JAN-2011', 4050 );
INSERT INTO owner VALUES ( '07-buysin01', 'q5-vin001', 'y' ); 
INSERT INTO auto_sale VALUES ( 1, '05-12345tsm', '07-buysin01', 'q5-vin002', '25-FEB-2010', 3050 );

INSERT INTO people VALUES ( '08-buysin02', 'JOHN CENA', 999, 999, 'brown', 'brown', 'The Ring', 'm', '1-SEP-1975');
INSERT INTO drive_licence VALUES ( 'ln-0008b02', '08-buysin02', 'nondriving', NULL, NULL, NULL );
INSERT INTO auto_sale VALUES ( 2, '07-buysin01', '08-buysin02', 'q5-vin002', '2-OCT-2012', 2000 );
INSERT INTO owner VALUES ( '08-buysin02', 'q5-vin002', 'y' ); 

-- Give John Cena edge-case (no driver tickets)
INSERT INTO ticket VALUES ( 10, '08-buysin02', 'q5-vin002', '01-12345bh', 'v manslgt', '31-OCT-2013', NULL, NULL );
INSERT INTO ticket VALUES ( 11, '08-buysin02', 'q5-vin002', '01-12345bh', 'v manslgt', '31-OCT-2013', NULL, NULL );
INSERT INTO ticket VALUES ( 12, '08-buysin02', 'q5-vin002', '01-12345bh', 'v manslgt', '31-OCT-2013', NULL, NULL );

INSERT INTO people VALUES ( '09-buysin03', 'Calvin Jensen', 165, 200, 'blue', 'ginger', 'Edmonton', 'm', '6-APR-1993');
INSERT INTO drive_licence VALUES ( 'ln-0009b03', '09-buysin03', 'driving', NULL, NULL, NULL );
INSERT INTO auto_sale VALUES ( 3, '05-12345tsm', '09-buysin03', 'q5-vin003', '15-OCT-2011', 2050 );
INSERT INTO owner VALUES ( '09-buysin03', 'q5-vin003', 'y' ); 
INSERT INTO auto_sale VALUES ( 4, '05-12345tsm', '09-buysin03', 'q5-vin004', '15-OCT-2012', 1550 );
INSERT INTO owner VALUES ( '09-buysin03', 'q5-vin004', 'y' ); 
INSERT INTO auto_sale VALUES ( 5, '05-12345tsm', '09-buysin03', 'q5-vin008', '15-OCT-2013', 1750 );
INSERT INTO owner VALUES ( '09-buysin03', 'q5-vin008', 'y' ); 

INSERT INTO people VALUES ( '10-buysin04', 'Devon Upton', 125, 170, 'blue', 'blonde', 'Calgary', 'm', '18-SEP-1995');
INSERT INTO drive_licence VALUES ( 'ln-0010b04', '10-buysin04', 'nondriving', NULL, NULL, NULL );
INSERT INTO auto_sale VALUES ( 6, '05-12345tsm', '10-buysin04', 'q5-vin005', '21-NOV-2010', 3400.5 );
INSERT INTO owner VALUES ( '10-buysin04', 'q5-vin005', 'y' ); 
INSERT INTO owner VALUES ( '10-buysin04', 'q1-trivialtest', 'n' );

-- test most popular vehicle
INSERT INTO vehicle VALUES ( 'q6-popsuv1', 'AUDI', 'sonic', 2011, 'black', 101 );
INSERT INTO vehicle VALUES ( 'q6-popsuv2', 'AUDI', 'sonic', 2011, 'black', 101 );
INSERT INTO vehicle VALUES ( 'q6-popsuv3', 'AUDI', 'sonic', 2011, 'black', 101 );
INSERT INTO owner VALUES ( '00-12345kb', 'q6-popsuv3', 'y' );

-- add glasses restriction for Devon
INSERT INTO driving_condition VALUES ( 0, 'Requires glasses to drive.' );
INSERT INTO driving_condition VALUES ( 1, 'Requires glare glasses to drive.' );
INSERT INTO driving_condition VALUES ( 2, 'ALBERTA DEMERIT RECOVERY CONDITION. Required to drive with an authourized adult at all times.' );

INSERT INTO restriction VALUES ( 'ln-0010b04', 0 );

-- add glasses and glare restriction for Bennett
INSERT INTO restriction VALUES ( 'ln-0002bh', 0 );
INSERT INTO restriction VALUES ( 'ln-0002bh', 1 );

-- test if multiple people break the system
INSERT INTO people VALUES ( '02-multisin', 'Bennett Hreherchuk', 150, 172, 'blue', 'brown', 'Sylvan Lake', 'm', '14-DEC-1995' );

-- test some long values
INSERT INTO people VALUES ( '123456789012345', 'SuperMax-LongName withtheLongestName', 150, 190, 'burgandy', 'burgandy', '0118999-8119991197253 street Edmonton', 'm', '14-DEC-1996' );
INSERT INTO drive_licence VALUES ( 'ln-maxnalong', '123456789012345', 'driving', NULL, '10-DEC-2016', '15-OCT-2017'  );
INSERT INTO restriction VALUES ( 'ln-maxnalong', 0 );
INSERT INTO restriction VALUES ( 'ln-maxnalong', 1 );
INSERT INTO restriction VALUES ( 'ln-maxnalong', 2 );



COMMIT;
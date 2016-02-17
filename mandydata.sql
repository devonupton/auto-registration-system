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

CREATE TABLE driving_condition (
  c_id        INTEGER,
  description VARCHAR(1024),
  PRIMARY KEY (c_id)
);

CREATE TABLE restriction(
  licence_no   CHAR(15),
  r_id         INTEGER,
  PRIMARY KEY (licence_no, r_id),
  FOREIGN KEY (licence_no) REFERENCES drive_licence,
  FOREIGN KEY (r_id) REFERENCES driving_condition
);

CREATE TABLE vehicle_type (
  type_id       integer,
  type          CHAR(10),
  PRIMARY KEY (type_id)
);

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


CREATE TABLE owner (
  owner_id          CHAR(15),
  vehicle_id        CHAR(15),
  is_primary_owner  CHAR(1),
  PRIMARY KEY (owner_id, vehicle_id),
  FOREIGN KEY (owner_id) REFERENCES people,
  FOREIGN KEY (vehicle_id) REFERENCES vehicle,
  CHECK ( is_primary_owner IN ('y', 'n'))
);


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

CREATE TABLE ticket_type (
  vtype     CHAR(10),
  fine      number(5,2),
  PRIMARY KEY (vtype)
);

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

--These are all the types of vehicle I have
insert into vehicle_type values (0, 'SUV');
insert into vehicle_type values (1, 'truck');
insert into vehicle_type values (2, 'car');

--These are all the ticket types I have
insert into ticket_type values ('speeding', 200.00);
insert into ticket_type values ('red light', 300.00);
insert into ticket_type values ('wreck-less', 150.00);
insert into ticket_type values ('parking', 100.00);


--This is my first person: Mandy
insert into people values ('123 456 789','Mandy',345,678,'brown','blonde','45 Roland Street, Red Deer, Alberta, T4P 3K9','f','31-May-1995');
insert into drive_licence values ('12345','123 456 789','7',NULL,'02-Dec-2012','02-Dec-2018');
insert into driving_condition values (0,'nothing');
insert into restriction values ('12345',0);
--She owns 1 vehicle and is a secondary owner in another vehicle
insert into vehicle values ('555-555','Kia','Rio',2013,'blue',2);
insert into vehicle values ('1110-1110','Honda','Civic',2013,'red',2);
insert into owner values ('123 456 789','555-555','y');
insert into owner values ('123 456 789','1110-1110','n');

--This is my second person: Andy
insert into people values ('987 654 321','Andy',35,6,'gold','blonde','1137 82 Ave, NW Edmonton, Alberta, T6G 2X7','m','24-Jul-1996');
insert into drive_licence values ('54321','987 654 321','5',NULL,'02-Dec-2011','02-Dec-2017');
insert into driving_condition values (1,'nothing');
insert into restriction values ('54321',0);
--He owns three vehicles
insert into vehicle values ('666-666','Dodge','Avenger',2010,'blue',0);
insert into vehicle values ('777-777','Dodge','Challenger',2013,'red',0);
insert into vehicle values ('888-888','Honda','Civic',2011,'hot pink',0);
insert into owner values ('987 654 321','666-666','y');
insert into owner values ('987 654 321','777-777','y');
insert into owner values ('987 654 321','888-888','y');
insert into owner values ('987 654 321','1110-1110','y');


--This is my third person: Sarah (she gives out all the tickets)
insert into people values ('111 222 333','Sarah',355,65,'green','brown','123 Apple Street, Okotoks, Alberta, T5P 3K9','f','05-Feb-1996');
insert into drive_licence values ('111222','111 222 333','nondriving',NULL,'02-Dec-2015','02-Dec-2020');
insert into driving_condition values (2,'nothing');
insert into restriction values ('111222',0);
--She owns two SUV's
insert into vehicle values ('999-999','kia','spectra',2012,'blue',0);
insert into vehicle values ('444-444','kia','rio',2012,'blue',0);
insert into owner values ('111 222 333','999-999','y');
insert into owner values ('111 222 333','444-444','y');


--This is my fourth person: Sylvia
insert into people values ('222 222 222','Sylvia',35,6,'brown','blonde','43 Rikely Street, Red Deer, Alberta, T4P 3K9','f','10-Sep-1950');
insert into drive_licence values ('55555','222 222 222','5',NULL,'02-Dec-2011','02-Dec-2017');
insert into driving_condition values (3,'nothing');
insert into restriction values ('55555',0);
--She owns three vehicles
insert into vehicle values ('333-333','Dodge','Avenger',2010,'blue',0);
insert into vehicle values ('222-222','Subaru','STI',2013,'red',0);
insert into vehicle values ('111-111','Honda','Civic',2011,'hot pink',1);
insert into owner values ('222 222 222','333-333','y');
insert into owner values ('222 222 222','222-222','y');
insert into owner values ('222 222 222','111-111','y');


--These are all the tickets that Sarah has given out
--to Andy:
insert into ticket values ('555','987 654 321','666-666','111 222 333','wreck-less','02-Feb-2016','Fort McMurray','Swerving through traffic');
--to Mandy:
insert into ticket values ('999','123 456 789','555-555','111 222 333','red light','02-Feb-2016','Edmonton','She came very close to hitting me while she was ignoring the light');
insert into ticket values ('888','123 456 789','555-555','111 222 333','speeding','02-Feb-2016','Calgary','She was not going very fast over but still got a ticket');
insert into ticket values ('777','123 456 789','555-555','111 222 333','speeding','02-Feb-2016','Edmonton','Radar ticket');
insert into ticket values ('666','123 456 789','555-555','111 222 333','speeding','02-Feb-2016','Red Deer','caught speeding yet again');
--to Sylvia
insert into ticket values ('444','111 222 333','555-555','111 222 333','red light','02-Feb-2016','Edmonton','blew through the red on 40th');





--These are all the auto sales recorded
--listed with seller sin first
--Andy bought:
insert into auto_sale values (0,'123 456 789','987 654 321','1110-1110','03-May-2013',12000.00);
insert into auto_sale values (1,'123 456 789','987 654 321','666-666','03-May-2013',12000.00);
insert into auto_sale values (2,'123 456 789','987 654 321','777-777','03-May-2013',12000.00);
insert into auto_sale values (3,'123 456 789','987 654 321','888-888','03-May-2013',14000.00);
--Mandy bought:
insert into auto_sale values (4,'987 654 321','123 456 789','555-555','03-May-2013',15000.00);
--Sylvia and Sarah sold their cars back and fourth one day for fun:
--Sarah bought:
insert into auto_sale values (5,'123 456 789','111 222 333','999-999','03-May-2013',16000.00);
insert into auto_sale values (6,'123 456 789','111 222 333','444-444','03-May-2013',13000.00);
insert into auto_sale values (7,'222 222 222','111 222 333','333-333','03-May-2013',13000.00);
insert into auto_sale values (8,'222 222 222','111 222 333','222-222','03-May-2013',12000.00);
insert into auto_sale values (9,'222 222 222','111 222 333','111-111','03-May-2013',13000.00);
insert into auto_sale values (10,'222 222 222','111 222 333','111-111','03-May-2013',14000.00);
insert into auto_sale values (11,'222 222 222','111 222 333','111-111','03-May-2013',14000.00);
insert into auto_sale values (12,'222 222 222','111 222 333','111-111','03-May-2013',13000.00);
insert into auto_sale values (13,'222 222 222','111 222 333','111-111','03-May-2013',14000.00);
--Sylvia bought:
insert into auto_sale values (14,'111 222 333','222 222 222','999-999','03-May-2013',16000.00);
insert into auto_sale values (15,'111 222 333','222 222 222','444-444','03-May-2013',13000.00);
insert into auto_sale values (16,'111 222 333','222 222 222','333-333','03-May-2013',13000.00);
insert into auto_sale values (17,'111 222 333','222 222 222','222-222','03-May-2013',12000.00);
insert into auto_sale values (18,'111 222 333','222 222 222','111-111','03-May-2013',13000.00);
insert into auto_sale values (19,'111 222 333','222 222 222','111-111','03-May-2013',14000.00);
insert into auto_sale values (20,'111 222 333','222 222 222','111-111','03-May-2013',14000.00);
insert into auto_sale values (21,'111 222 333','222 222 222','111-111','03-May-2013',13000.00);
insert into auto_sale values (22,'111 222 333','222 222 222','111-111','03-May-2013',14000.00);

COMMIT;
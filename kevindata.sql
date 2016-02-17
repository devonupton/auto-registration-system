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

insert into people values('p1','Tom',161.12, 62.12, 'brown','black', '#01, 100 Street, Edmonton, CA', 'm', DATE'1990-01-15');

insert into people values('p2','Kim',167.52, 59.99, 'brown','black', '#06, 130 Street, Calgary, CA', 'm', DATE'1994-06-25');

insert into people values('p3','Sam',152.29, 66.34, 'brown','black', '#21, 107 Street, Edmonton, CA', 'm', DATE'1991-03-21');

insert into people values('p4','Peter',191.32,67.77, 'blue','brown', '#11, 109 Street, Edmonton, CA', 'm', DATE'1985-04-12');

insert into people values('p5','Bill',172.11, 63.65, 'brown','black', '#07, 123 Street, Calgary, CA', 'm', DATE'1983-07-27');

insert into people values('p6','Marry',135.12, 69.12, 'brown','brown', '#23, 160 Street, Edmonton, CA', 'f', DATE'1992-04-25');

insert into people values('p7','Jane',166.32, 60.76, 'brown','brown', '#09, 123 Street, Calgary, CA', 'f', DATE'1984-06-14');

insert into people values('p8','Jenny',157.59, 60.44, 'brown','black', '#16, 117 Street, Edmonton, CA', 'f', DATE'1991-04-22');

insert into people values('p9','Catherine',171.12, 61.23, 'blue','brown', '#11, 149 Street, Edmonton, CA', 'f', DATE'1995-07-15');

insert into people values('p10','Kelly',157.32, 69.99, 'brown','black', '#17, 133 Street, Calgary, CA', 'f', DATE'1986-03-22');


insert into drive_licence values('L123', 'p1', 'A', NULL, DATE'2000-01-15', DATE'2010-01-15');

insert into drive_licence values('L124', 'p2', 'nondriving', NULL, DATE'2009-05-25', DATE'2019-05-25');

insert into drive_licence values('L125', 'p3', 'A', NULL, DATE'2007-06-27', DATE'2017-06-27');

insert into drive_licence values('L126', 'p4', 'B', NULL, DATE'2006-04-22', DATE'2016-04-22');

insert into drive_licence values('L127', 'p5', 'A', NULL, DATE'2001-08-21', DATE'2011-08-21');

insert into drive_licence values('L128', 'p6', 'C', NULL, DATE'2009-07-12', DATE'2019-07-12');

insert into drive_licence values('L129', 'p7', 'A', NULL, DATE'2007-03-07', DATE'2017-03-07');

insert into drive_licence values('L130', 'p8', 'C', NULL, DATE'2000-01-25', DATE'2010-01-25');

insert into drive_licence values('L131', 'p9', 'D', NULL, DATE'2009-04-22', DATE'2019-04-22');

insert into drive_licence values('L132', 'p10', 'B', NULL, DATE'2008-11-24', DATE'2018-11-24');

insert into driving_condition values(1, 'none');

insert into driving_condition values(2, 'learners');

insert into driving_condition values(3, 'need glasses');


insert into restriction values('L123', 1);

insert into restriction values('L124', 1);

insert into restriction values('L125', 1);

insert into restriction values('L126', 3);

insert into restriction values('L127', 2);

insert into restriction values('L128', 1);

insert into restriction values('L129', 1);

insert into restriction values('L130', 1);

insert into restriction values('L131', 1);

insert into restriction values('L132', 1);


insert into vehicle_type values(1,'car');

insert into vehicle_type values(2,'truck');

insert into vehicle_type values(3,'SUV');



insert into vehicle values('v1', 'Ford', 'fc1', 2008.00, 'red', 1);

insert into vehicle values('v2', 'honda', 'hc1', 2009.00, 'blue', 1);

insert into vehicle values('v3', 'honda', 'hc2', 2010.00, 'red', 1);

insert into vehicle values('v4', 'toyota', 'tc1', 2011.00, 'black', 1);

insert into vehicle values('v5', 'toyota', 'tc2', 2011.00, 'black', 1);

insert into vehicle values('v6', 'Ford', 'ft1', 2008.00, 'black', 2);

insert into vehicle values('v7', 'honda', 'ht1', 2009.00, 'blue', 2);

insert into vehicle values('v8', 'honda', 'ft2', 2010.00, 'red', 2);

insert into vehicle values('v9', 'toyota', 'tt1', 2011.00, 'black', 2);

insert into vehicle values('v10', 'toyota', 'tt2', 2011.00, 'black', 2);

insert into vehicle values('v11', 'Ford', 'fs1', 2008.00, 'black', 3);

insert into vehicle values('v12', 'honda', 'hs1', 2009.00, 'blue', 3);

insert into vehicle values('v13', 'honda', 'fs2', 2010.00, 'red', 3);

insert into vehicle values('v14', 'toyota', 'ts1', 2011.00, 'black', 3);

insert into vehicle values('v15', 'toyota', 'ts2', 2011.00, 'black', 3);



insert into owner values('p1','v1','y');

insert into owner values('p2','v1','n');

insert into owner values('p1','v2','y');

insert into owner values('p3','v3','y');

insert into owner values('p4','v4','y');

insert into owner values('p5','v6','y');

insert into owner values('p6','v5','y');

insert into owner values('p7','v8','y');

insert into owner values('p8','v12','y');

insert into owner values('p9','v13','y');

insert into owner values('p8','v14','y');

insert into owner values('p8','v15','y');






insert into auto_sale values(1, 'p10', 'p1', 'v1', DATE'2012-06-15' , 43829.00);

insert into auto_sale values(2, 'p10', 'p1', 'v2', DATE'2012-03-15', 44123.00);

insert into auto_sale values(3, 'p10', 'p3', 'v3', DATE'2012-05-14', 45377.00);

insert into auto_sale values(4, 'p10', 'p4', 'v4', DATE'2011-01-15', 49222.00);

insert into auto_sale values(5, 'p10', 'p5', 'v6', DATE'2012-03-19', 46422.00);

insert into auto_sale values(6, 'p10', 'p6', 'v5', DATE'2012-04-21', 55000.00);

insert into auto_sale values(7, 'p10', 'p7', 'v8', DATE'2012-10-25', 32145.00);

insert into auto_sale values(8, 'p10', 'p8', 'v12', DATE'2012-11-15', 23278.00);

insert into auto_sale values(9, 'p10', 'p9', 'v13', DATE'2011-08-22', 39821.00);

insert into auto_sale values(10, 'p10', 'p8', 'v14', DATE'2012-1-15', 23499.00);

insert into auto_sale values(11, 'p10', 'p8', 'v15', DATE'2012-01-16', 23600.00);


insert into ticket_type values('speeding', 900.00);

insert into ticket_type values('red light', 500.00);

insert into ticket_type values('parking', 200.00);



insert into ticket values(1, 'p1', 'v1', 'p9', 'speeding', DATE'2016-01-22', '123 Street,Edmonton', NULL);

insert into ticket values(2, 'p1', 'v1', 'p9', 'speeding', DATE'2015-03-28', '123 Street,Edmonton', NULL);

insert into ticket values(3, 'p1', 'v2', 'p9', 'red light', DATE'2015-04-12', '123 Street,Edmonton', NULL);

insert into ticket values(4, 'p7', 'v8', 'p9', 'speeding', DATE'2015-02-22', '103 Street,Calgary', NULL);

insert into ticket values(5, 'p8', 'v12', 'p9', 'speeding', DATE'2014-03-20', '120 Street,Edmonton', NULL);


COMMIT;
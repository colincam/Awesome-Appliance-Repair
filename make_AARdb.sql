CREATE DATABASE AARdb
  DEFAULT CHARACTER SET utf8;

USE AARdb;

CREATE TABLE `customer` (
    `cid` mediumint NOT NULL auto_increment,
    `fname` varchar(20) DEFAULT NULL,
    `lname` varchar(20) NOT NULL,
    primary key(cid)
) ENGINE=InnoDB;

CREATE TABLE `jobs` (
  `jid` mediumint NOT NULL auto_increment,
  `cid` mediumint,
  `make` varchar(20) DEFAULT NULL,
  `appliance` char(20) DEFAULT NULL,
  `appointment` date DEFAULT NULL,
  `job_status` enum('pending','approved','completed') DEFAULT NULL,
  `description` varchar(140) default null,
  primary key(jid),
  foreign key(cid) references customer(cid)
) ENGINE=InnoDB;

insert into customer (fname,lname) values
    ('Miguel','Cervantes'),
    ('Eleanor','Roosevelt');

insert into jobs (cid, make, appliance, appointment, job_status, description) values
    (1,'maytag','washer', null, 'pending', "outflow hoses leak"),
    (2,'GE','refrigerator', '2013-11-05', 'approved', "Ices up; won't defrost");
    
# notes
# ALTER TABLE Orders
# ADD FOREIGN KEY (P_Id)
# REFERENCES Persons(P_Id)

# ALTER TABLE jobs add column tid mediumint, add foreign key(tid) references tech(tid);

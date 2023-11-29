-- Drops all tables if it exists
set foreign_key_checks=0;
set autocommit=0;
drop table if exists Gyms, Courts, Reservations, Members, GymMemberships;

-- -----CREATE TABLES-----

-- Create Gyms entity
create table Gyms(
	gym_ID int auto_increment unique not null,
	location varchar(255) not null,
	email varchar(255) not null,
	opening_time time not null,
	closing_time time not null,
	primary key (gym_ID)
);

-- Create Courts entity
create table Courts(
	court_ID int auto_increment unique not null,
	gym_ID int,
	court_name varchar(255) unique not null,
	primary key (court_ID),
	foreign key (gym_ID) references Gyms(gym_ID) on delete cascade
);

-- Create Members entity
create table Members(
	member_ID int auto_increment unique not null,
	first_name varchar(255) not null,
	last_name varchar(255) not null,
	age int not null,
	email varchar(255) not null,
	gender char(1) not null,
	primary key (member_ID)
);

-- Create GymMemberships entity (intersection table b/w Gyms and Members)
create table GymMemberships(
	gym_ID int,
	member_ID int,
	gym_memberships_ID int auto_increment unique not null,
	paid tinyint(1),
	PRIMARY key (gym_memberships_ID), 
	foreign key (gym_ID) references Gyms(gym_ID) on delete cascade,
	foreign key (member_ID) references Members(member_ID) on delete cascade
);

-- Create Reservations entity
create table Reservations(
	reservation_ID int auto_increment unique not null,
	court_ID int,
	member_ID int,
	reservation_start datetime not null,
	reservation_end datetime not null,
	paid tinyint(1),
	primary key (reservation_ID),
	foreign key (court_ID) references Courts(court_ID) on delete set null,
	foreign key (member_ID) references Members(member_ID) on delete set null
);


-- -----SAMPLE DATA-----

-- Inserting sample Gyms data
insert into Gyms(location, email, opening_time, closing_time) values
	("San Diego", "sandiego@greatfitness.com", "08:00:00", "20:00:00"),
	("Los Angeles", "losangeles@greatfitness.com", "08:00:00", "20:00:00"),
	("Irvine", "irvine@greatfitness.com", "08:00:00", "20:00:00");
	
-- Inserting sample Courts data
-- San Diego has 3 courts, Los Angeles has 1 court, Irvine has 2 courts
insert into Courts(gym_ID, court_name) values
	((select gym_ID from Gyms where location="San Diego"), "San Diego 1"),
	((select gym_ID from Gyms where location="San Diego"), "San Diego 2"),
	((select gym_ID from Gyms where location="San Diego"), "San Diego 3"),
	((select gym_ID from Gyms where location="Los Angeles"), "Los Angeles 1"),
	((select gym_ID from Gyms where location="Irvine"), "Irvine 1"),
	((select gym_ID from Gyms where location="Irvine"), "Irvine 2");
	
-- Inserting sample Members data
insert into Members(first_name, last_name, age, email, gender) values
	("David", "Nguyen", 19, "davidnguyen@gmail.com", "M"),
	("Eleanor", "Zhao", 30, "eleanorzhao@gmail.com", "F"),
	("Melissa", "Lee", 42, "melissalee@gmail.com", "F");
	
-- Inserting sample GymMemberships data
-- It is assumed all members have access to all gyms
insert into GymMemberships(gym_ID, member_ID, paid) values
	((select gym_ID from Gyms where location="San Diego"), (select member_ID from Members where first_name="David" and last_name="Nguyen"), 1),
	((select gym_ID from Gyms where location="Los Angeles"), (select member_ID from Members where first_name="David" and last_name="Nguyen"), 1),
	((select gym_ID from Gyms where location="Irvine"), (select member_ID from Members where first_name="David" and last_name="Nguyen"), 1),
	((select gym_ID from Gyms where location="San Diego"), (select member_ID from Members where first_name="Eleanor" and last_name="Zhao"), 1),
	((select gym_ID from Gyms where location="Los Angeles"), (select member_ID from Members where first_name="Eleanor" and last_name="Zhao"), 1),
	((select gym_ID from Gyms where location="Irvine"), (select member_ID from Members where first_name="Eleanor" and last_name="Zhao"), 1),
	((select gym_ID from Gyms where location="San Diego"), (select member_ID from Members where first_name="Melissa" and last_name="Lee"), 1),
	((select gym_ID from Gyms where location="Los Angeles"), (select member_ID from Members where first_name="Melissa" and last_name="Lee"), 1),
	((select gym_ID from Gyms where location="Irvine"), (select member_ID from Members where first_name="Melissa" and last_name="Lee"), 1);

-- Inserting sample Reservations data
-- David Nguyen is reserving a court in the San Diego location
-- Eleanor Zhao is reserving a court in the Los Angeles location
-- Melissa Lee is reserving a court in the Irvine location
insert into Reservations(court_ID, member_ID, reservation_start, reservation_end, paid) values
	(1, (select member_ID from Members where first_name="David" and last_name="Nguyen"), '2023-06-18 10:30:00', '2023-06-18 11:30:00', 1),
	(4, (select member_ID from Members where first_name="Eleanor" and last_name="Zhao"), '2023-06-20 13:00:00', '2023-06-20 14:00:00', 1),
	(5, (select member_ID from Members where first_name="Melissa" and last_name="Lee"), '2023-06-20 08:00:00', '2023-06-20 09:00:00', 1);

set foreign_key_checks=1;
commit;

create table Gyms(
	gym_ID int auto_increment unique not null,
	location varchar(255) not null,
	email varchar(255) not null,
	opening_time time not null,
	closing_time time not null,
	primary key (gym_ID)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

insert into Gyms(location, email, opening_time, closing_time) values
	("San Diego", "sandiego@greatfitness.com", "08:00:00", "20:00:00"),
	("Los Angeles", "losangeles@greatfitness.com", "08:00:00", "20:00:00"),
	("Irvine", "irvine@greatfitness.com", "08:00:00", "20:00:00");
create table track(
id int primary key,
start datetime not null,
end datetime not null);

create table dice(
id int auto_increment PRIMARY KEY,
num int,
created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
TrackId int,
    FOREIGN KEY (`TrackId`) REFERENCES `track` (`id`)
);

create table hastrack(
date datetime primary key,
normal int not null,
defect int not null);

create table malfunction(
date datetime primary key,
normal int not null,
defect int not null);

create table misconduct(
date datetime primary key,
normal int not null,
defect int not null);

create table operation(
date datetime primary key,
first int not null,
second int not null,
third int not null);

create table radiation(
id int primary key,
figure int not null,
created_at timestamp not null default current_timestamp,
TrackId int,
foreign key (TrackId) references track(id)
);

create table record (
id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    Datetime DATETIME,
    Start boolean,
    No1Action boolean,
    No2InPoint boolean,
    No3Motor1 int,
    No3Motor2 int,
    Dicevalue int,
    TrackId int,
    FOREIGN KEY (`TrackId`) REFERENCES `track` (`id`)
);
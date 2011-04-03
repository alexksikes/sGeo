#create database zipcodesdotcom

#drop table if exists zipcodes
create table zipcodes
(    
    id                      int(11) not null auto_increment primary key, 
    ZipCode                 varchar(5),
    City                    varchar(32),
    State                   char(2),
    CountyName              varchar(45),
    AreaCode                varchar(55),
    CityType                char(1),
    CityAliasAbbreviation   varchar(13),
    CityAliasName           varchar(35),
    Latitude                decimal(12,8),
    Longitude               decimal(12,8),
    TimeZone                char(2),
    Elevation               int,
    CountyFIPS              char(3),
    DayLightSavings         char(1),
    PreferredLastLineKey    varchar(10),
    ClassificationCode      char(1),
    MultiCounty             char(1),
    StateFIPS               char(2),
    CityStateKey            char(6)
) engine=myisam default charset=utf8;

load data infile '/projects/data/zip-codes.com/zip-codes-database-formatted.csv' 
    into table zipcodes
    fields terminated by ','
    ignore 1 lines
    (ZipCode,City,State,CountyName,AreaCode,CityType,CityAliasAbbreviation,CityAliasName,Latitude,Longitude,TimeZone,Elevation,CountyFIPS,DayLightSavings,PreferredLastLineKey,ClassificationCode,MultiCounty,StateFIPS,CityStateKey);

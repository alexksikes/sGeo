#The data format is tab-delimited text in utf8 encoding, with the following fields :

#country code      : iso country code, 2 characters
#postal code       : varchar(10)
#place name        : varchar(120)
#admin name1       : 1. order subdivision (state) varchar(100)
#admin code1       : 1. order subdivision (state) varchar(20)
#admin name2       : 2. order subdivision (county/province) varchar(100)
#admin code2       : 2. order subdivision (county/province) varchar(20)
#admin name3       : 3. order subdivision (community) varchar(100)
#admin code3       : 3. order subdivision (community) varchar(20)
#latitude          : estimated latitude (wgs84)
#longitude         : estimated longitude (wgs84)
#accuracy          : accuracy of lat/lng from 1=estimated to 6=centroid

#drop table if exists postals;
create table postals
(
#    id                      int(11) not null auto_increment primary key,
    iso                     varchar(2),
    postal_code             varchar(10),
    place_name              varchar(120),
    admin1_name             varchar(100),
    admin1                  varchar(20),
    admin2_name             varchar(100),
    admin2                  varchar(20),
    admin3_name             varchar(100),
    admin3                  varchar(20),
    latitude                dec(10,7),
    longitude               dec(10,7),
    accuracy                smallint(1)
) engine=myisam default charset=utf8;

load data infile '/projects/data/geonames/postals.txt' 
    into table postals
    fields terminated by '\t';

# we add the id afterwards for consitency
alter table postals add column id int(11) not null auto_increment primary key;
#The main 'geoname' table has the following fields :
#---------------------------------------------------
#geonameid         : integer id of record in geonames database
#name              : name of geographical point (utf8) varchar(200)
#asciiname         : name of geographical point in plain ascii characters, varchar(200)
#alternatenames    : alternatenames, comma separated varchar(4000)
#latitude          : latitude in decimal degrees (wgs84)
#longitude         : longitude in decimal degrees (wgs84)
#feature class     : see http://www.geonames.org/export/codes.html, char(1)
#feature code      : see http://www.geonames.org/export/codes.html, varchar(10)
#country code      : ISO-3166 2-letter country code, 2 characters
#cc2               : alternate country codes, comma separated, ISO-3166 2-letter country code, 60 characters
#admin1 code       : fipscode (subject to change to iso code), isocode for the us and ch, see file #admin1Codes.txt for display names of this code; varchar(20)
#admin2 code       : code for the second administrative division, a county in the US, see file admin2Codes.txt; #varchar(80) 
#admin3 code       : code for third level administrative division, varchar(20)
#admin4 code       : code for fourth level administrative division, varchar(20)
#population        : integer 
#elevation         : in meters, integer
#gtopo30           : average elevation of 30'x30' (ca 900mx900m) area in meters, integer
#timezone          : the timezone id (see file timeZone.txt)
#modification date : date of last modification in yyyy-MM-dd format

#create database geonames character set utf8;

#drop table if exists geoname;
create table geoname
(
    id                  int(11) not null primary key,
    name                varchar(200),
    ascii_name          varchar(200),
    alternate_names     varchar(4000),
    latitude            dec(10,7),
    longitude           dec(10,7),
    feature_class       char(1),
    feature_code        varchar(10),
    country_code        char(2),
    cc2                 varchar(60),
    admin1_code         varchar(20),
    admin2_code         varchar(80),
    admin3_code         varchar(20),
    admin4_code         varchar(20),
    population          int(11) not null,
    elevation           int(11),
    gtopo30             int(11),
    timezoneid          varchar(200),
    modification_date   date,
    index(country_code)
) engine=myisam default charset=utf8;

load data infile '/projects/data/geonames/geoname.txt' 
    into table geoname
    fields terminated by '\t';

# Problems with encoding (avoid major headaches)?
# - make sure character set of db is utf8 for data load infile!!
# >> the charset of the DB must be the same as the loaded file with "load data infile"
# - for debugging set mysql client and server to utf8 (set names=utf8) 
# - and of course your terminal should assume utf8.
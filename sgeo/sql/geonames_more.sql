#The table 'alternate names' :
#-----------------------------
#alternateNameId   : the id of this alternate name, int
#geonameid         : geonameId referring to id in table 'geoname', int
#isolanguage       : iso 639 language code 2- or 3-characters; 4-characters 'post' for postal codes and 'iata' or 'icao' for airport codes, fr-1793 for French Revolution names, varchar(7)
#alternate name    : alternate name or name variant, varchar(200)
#isPreferredName   : '1', if this alternate name is an official/preferred name
#isShortName       : '1', if this is a short name like 'California' for 'State of California'

#Remark : the field 'alternatenames' in the table 'geoname' is a short version of the 'alternatenames' table. You probably don't need both. 
#If you don't need to know the language of a name variant, the field 'alternatenames' will be sufficient. If you need to know the language of a name variant, then you will need to load the table 'alternatenames' and you can drop the column in the geoname table.

#admin1Codes.txt          : names for administrative subdivision 'admin1 code' (UTF8), the code '00' stands for 'unkown code', includes obsolete codes
#admin1CodesASCII.txt     : ascii names of admin divisions. (beta > http://forum.geonames.org/gforum/posts/list/208.page#1143)
#iso-languagecodes.txt    : iso 639 language codes, as used for alternate names in file alternateNames.zip
#featureCodes.txt         : name and description for feature classes and feature codes 
#timeZones.txt            : timezoneId, gmt offset on 1st of January, dst offset to gmt on 1st of July (of the current year)

#countryInfo.txt          : country information : iso codes, fips codes, languages, capital ,...
#ISO ISO3    ISO-Numeric fips    Country Capital Area(in sq km)  Population  Continent   tld CurrencyCode    CurrencyName    Phone   Postal Code Format  Postal Code Regex   Lang    uages   geonameid   neighbours  EquivalentFipsCode

#drop table if exists alternate_names;
create table alternate_names
(
    id                       int(11) not null primary key,
    geonameid                int(11),
    isolanguage              varchar(7),
    alternate_name           varchar(200),
    is_preferred_name        boolean,
    is_short_name            boolean
) engine=myisam default charset=utf8;

load data infile '/projects/data/geonames/alternateNames.txt' 
    into table alternate_names
    fields terminated by '\t';
    
#drop table if exists admin1;
create table admin1
(
    country_code            char(2),
    admin1_code             varchar(20),
    name                    varchar(200),
    primary key(country_code, admin1_code)
) engine=myisam default charset=utf8;

# the file admin1Codes.tabbed.txt is admin1Codes.txt with country_code and admin1_code delimited by a tab.
load data infile '/projects/data/geonames/admin1Codes.tabbed.txt' 
    into table admin1
    fields terminated by '\t';

#drop table if exists admin1_ascii;
create table admin1_ascii
(
    country_code            char(2),
    admin1_code             varchar(20),
    name                    varchar(200),
    name_alt                varchar(200),
    geonameid               int(11),
    primary key(country_code, admin1_code)
) engine=myisam default charset=utf8;

# the file admin1CodesASCII.tabbed.txt is admin1CodesASCII.txt with country_code and admin1_code delimited by a tab.
load data infile '/projects/data/geonames/admin1CodesASCII.tabbed.txt' 
    into table admin1_ascii
    fields terminated by '\t';

#drop table if exists admin2;
create table admin2
(
    country_code            char(2),
    admin1_code             varchar(20),
    admin2_code             varchar(80),
    name                    varchar(200),
    name_ascii              varchar(200),
    geonameid               int(11),
    primary key(country_code, admin1_code, admin2_code)
) engine=myisam default charset=utf8;

# the file admin2Codes.tabbed.txt is admin2Codes.txt with country_code, admin1_code and admin2_code delimited by a tab.
load data infile '/projects/data/geonames/admin2Codes.tabbed.txt' 
    into table admin2
    fields terminated by '\t';

#drop table if exists isolanguage;
create table isolanguage
(
    iso3                    varchar(7),
    iso2                    varchar(7),
    iso1                    varchar(7),
    language_name           varchar(200),
    primary key(iso3, iso2)
) engine=myisam default charset=utf8;

# iso-languagecodes.formated.txt is iso-languagecodes.txt without the header.
load data infile '/projects/data/geonames/iso-languagecodes.formatted.txt' 
    into table isolanguage
    fields terminated by '\t';

#drop table if exists features;
create table features
(
    feature_class           char(1),
    feature_code            varchar(10),
    kind                    varchar(400),
    description             varchar(500),
    primary key(feature_class, feature_code)
) engine=myisam default charset=utf8;

load data infile '/projects/data/geonames/featureCodes.tabbed.txt' 
    into table features
    fields terminated by '\t';

#drop table if exists timezone;
create table timezone
(
    id                      varchar(200) not null primary key,    # had to change the id to 200 char instead of 400
    offset_gmt              dec(4,1),
    offset_dmt              dec(4,1)
) engine=myisam default charset=utf8;

load data infile '/projects/data/geonames/timeZones.txt' 
    into table timezone
    fields terminated by '\t';

#drop table if exists country_info;
create table country_info
(
    iso                     char(2) not null primary key,
    iso3                    varchar(7),
    isonum                  int(3),
    fips                    char(2),
    country                 varchar(200),
    capital                 varchar(200),
    area                    double,
    population              int(11),
    continent               varchar(3),
    tld                     varchar(3),
    currency_code           varchar(7),
    currency_name           varchar(200),
    phone                   varchar(20),
    postal_code_format      varchar(400),
    postal_code_regex       varchar(500),
    languages               varchar(100),
    geonameid               int(11),
    neighbours              varchar(50),
    equivalent_fips         varchar(200)
) engine=myisam default charset=utf8;

# countryInfo.formated.txt is countryInfo.txt without the comments and header.
load data infile '/projects/data/geonames/countryInfo.formatted.txt' 
    into table country_info
    fields terminated by '\t';
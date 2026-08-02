CREATE KEYSPACE LCDisc
WITH REPLICATION={
    'class':'SimpleStrategy',
    'replication_factor':1
};

CREATE TABLE LCDisc.Users(
    author text PRIMARY KEY,
    username text,
);

CREATE TABLE LCDisc.Teams(
    TeamName text Primary KEY,
    TeamLeader text,
    TeamSize INT,
    Mem1 text ,
    Mem2 text ,
    Mem3 text
);
CREATE TABLE LCDisc.Matches(
    MatchName text Primary Key,
    started boolean,
    registeredTeams SET<Text> 
);
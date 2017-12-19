#Duplicate the original tip table 
#This table is created for natural language processing
CREATE TABLE tip_token like tip;


load data local infile '/Users/yuyanzhang/Desktop/CMU/10605/yelp/10805-YelpChallenge/tip_token.csv' into table tip_token fields terminated by ','
lines terminated by '\n' (user_id, business_id, text,date,likes);

select text from tip_token where likes>10;


USE yelp_db;
Create table review_token like review;
alter table review_token drop column user_id;
describe review_token;

load data local infile '/Users/yuyanzhang/Desktop/CMU/10605/yelp/10805-YelpChallenge/review_token.csv' into table review_token fields terminated by '\t'
lines terminated by '\n' (id,  text);

select text from review_token limit 10;
select review.id,review_token.text, (useful+funny+cool) from review, review_token where review.id=review_token.id;

select (useful+funny+cool)  from review limit 50000;



select count(distinct id) from business;
select count(distinct business_id) from tip;

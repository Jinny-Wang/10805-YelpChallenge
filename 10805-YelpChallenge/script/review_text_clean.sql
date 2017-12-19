#Duplicate the original tip table 
#This table is created for natural language processing
CREATE TABLE tip_token like tip;


load data local infile '/Users/yuyanzhang/Desktop/CMU/10605/yelp/10805-YelpChallenge/tip_token.csv' into table tip_token fields terminated by ','
lines terminated by '\n' (user_id, business_id, text,date,likes);

select text from tip_token where likes>10;





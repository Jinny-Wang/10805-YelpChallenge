USE yelp_db;
#Data imported through "Server-> Data import"

######Review#########
#Basic summary statistics of review table
#Time frame
select min(date) from review; 
select max(date) from review; 

#Number of review versus year/day/month posted
select year(date), count(id) from review group by year(date);
select month(date), count(id) from review group by month(date);
select dayofweek(date), count(id) from review group by dayofweek(date);

#Useful/cool/funny distribution
select useful, count(useful) from review group by useful;
select cool, count(cool) from review group by cool;
select funny, count(funny) from review group by funny;

#Star distribution 
select stars, count(stars) from review group by stars;


########TIP###########
select min(date) from tip; 
select max(date) from tip; 

select count(date) from tip;
select year(date), count(date) from tip group by year(date);
select month(date), count(date) from tip group by month(date);
select dayofweek(date), count(date) from tip group by dayofweek(date);

select likes, count(likes) from tip group by likes;
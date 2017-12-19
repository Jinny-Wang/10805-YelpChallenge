Useful SQL queries for business , photo, check-in dataset. 
Might also be useful for other queries as well. 
Feel free to take this as reference.

```sql

use yelp_db;

-- 1.count number of businesses in one state , rank the records in descedning order of cnt
SELECT count(*) AS cnt, state FROM business GROUP BY state ORDER BY cnt DESC;


-- 2. select businesses with state = 'PA'
SELECT *  FROM business WHERE state='PA';

-- 3.select businesses with city='Pittsburgh'
SELECT * from business where city='Pittsburgh';

-- 4. join business and photo_count of each business.
--    order by review_count then by photo count
select * from business, 
(SELECT business.id as bid, count(distinct photo.id) as cnt FROM photo JOIN business on photo.business_id = business.id GROUP BY bid ORDER BY cnt DESC, bid ASC) 
 AS b1 WHERE business.id = b1.bid ORDER BY business.review_count DESC , b1.cnt DESC;

--5. find reviews of businesses in Quebec  (too see if they are in French)
SELECT * from review join business on business.id=review.business_id   WHERE business.state='QC';--


-- 6. count number of checkins per businesses, join with business to show other attributes of businesses
--     very important :     select * from tableA,tableB   -> if there is no "where" following it you are computing len(tableA)*len(tableB) records..[cross join]
select * from 
(SELECT business_id,sum(count) as cnt from checkin group by business_id) as agg_checkin, business
where agg_checkin.business_id = business.id;
```

use yelp_db; 
set session wait_timeout=3600;

select sample.review_id, sample.ind, review.user_id, review.useful, review.funny, review.cool, review.useful + review.funny + review.cool as new_useful, review.stars, 
u.yelping_since, u.fans, 
u.compliment_hot + u.compliment_more + u.compliment_profile + u.compliment_cute + u.compliment_list + u.compliment_note + u.compliment_plain
 + u.compliment_cool + u.compliment_funny + u.compliment_writer as compliment, 
 f.friend_num, e.elite_year
from sample
left join review 
on sample.review_id = review.id
left join user as u
on u.id = review.user_id
left join friend_count as f
on f.user_id = review.user_id
left join elite_count as e
on e.user_id = review.user_id;




select DATEDIFF((review.date), "2004-07-22 00:00:00") from review limit 100;



select id, date, if(date>"2016-01-01 00:00:00", 0, 1) as valid from review where id = "-ExTGqIibCfNAfMl-T0fOA" ; 
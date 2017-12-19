use yelp_db; 

#Extract following features from the business data
#stars, review_count, business category, state


-- select sample.review_id, sample.ind, review.user_id, review.useful, review.funny, review.cool, review.useful + review.funny + review.cool as new_useful, review.stars, 
-- u.yelping_since, u.fans, u.compliment_hot + u.compliment_more + u.compliment_profile + u.compliment_cute + u.compliment_list + u.compliment_note + u.compliment_plain+ u.compliment_cool + u.compliment_funny + u.compliment_writer as compliment, 
--  f.friend_num, e.elite_year
-- from sample
-- left join review 
-- on sample.review_id = review.id
-- left join user as u
-- on u.id = review.user_id
-- left join friend_count as f
-- on f.user_id = review.user_id
-- left join elite_count as e
-- on e.user_id = review.user_id;

select sample.review_id, b.id,sample.ind, b.review_count, b.stars, b.state,b.latitude,b.longitude,b.postal_code, group_concat(c.category)
from review
left join business as b
on b.id = review.business_id
left join category as c
on c.business_id = review.business_id 
left join sample
on sample.review_id =review.id
group by c.business_id limit 100;



select review.id, b.id, b.review_count, b.stars, b.state,b.latitude,b.longitude,b.postal_code, group_concat(c.category)
from review
left join business as b
on b.id = review.business_id
left join category as c
on c.business_id = review.business_id 
group by c.business_id;



####brain hole####
select review.id, review.business_id from review where review.useful > 8 limit 5000;
select review.date, review.text, review.useful from review where review.business_id = "YQFcxE9UXrKc-QuTUu7twQ";












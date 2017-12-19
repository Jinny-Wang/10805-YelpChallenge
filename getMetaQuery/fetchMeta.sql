## 10-805 Machine Learning with Large Dataset  Final Project
## Yelp Challenge
## Author: Yi Xu

use yelp_db; 

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
on e.user_id = review.user_id
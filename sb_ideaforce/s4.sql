select author, count(author) as NumSuggestions from sbf_suggestion S group by author having count(S.author) > 1;
select * from sbf_suggestion order by suggestionId;
select S.suggestionId, S.category, S.author, C.author, C.commentId
from sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId;

select *
from sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId;

select author, count(author) from sbf_suggestion;
select * from sbf_comment order by suggestionId;

select author, count(author) as NumComments from sbf_comment C group by author  having count(C.author) > 5 order by count(author) desc;

select * from sbf_suggestion where author like "sbx_%";
select * from sbf_comment where author like "sbx%";
select * from sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId;
select S.suggestionId, S.author, C.author, commentId from sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId limit 40;
select * from sbf_suggestion S join sbf_comment C;

select distinct author from sbf_suggestion;
select distinct author from sbf_comment;

SELECT S.suggestionId, S.author, C.author, C.suggestionId, C.commentId FROM sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId limit 1000;
select * from sbf_suggestion where suggestionId = 1000;
select * from sbf_comment where suggestionId = 463;
select * from sbf_suggestion where author like "sbf_%";

select votes from sbf_suggestion where votes is not null;

select S.suggestionId, votes, count(C.suggestionId) from sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId
group by S.suggestionId
order by S.votes desc limit 500;

select * from sbf_suggestion S order by votes desc limit 500;

SELECT * 
INTO OUTFILE 'C:\Users\14107\Desktop\Courses\COSC710 SocialNetwork\Assignments\Assignment02\suggestion.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
FROM sbf_suggestion;

select S.suggestionId, votes, count(C.author) from sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId where votes = 0 group by S.suggestionId  having count(C.author) > 0 order by count(C.author) desc ; 
select S.suggestionId, votes, count(C.author) from sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId where votes = 0 group by S.suggestionId order by count(C.author) desc ; 

select S.suggestionId, votes, C.author from sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId and C.suggestionId = 4024;

select * from sbf_suggestion S order by S.votes desc limit 1000;

SELECT *
FROM (
    SELECT * FROM sbf_suggestion
    ORDER BY votes DESC
    LIMIT 1000
) AS highest_votes
UNION ALL
SELECT * FROM (
    SELECT * FROM sbf_suggestion
    ORDER BY votes asc
    LIMIT 1000
) AS lowest_votes;

 select * from sbf_comment C where C.suggestionId = 41944;
 
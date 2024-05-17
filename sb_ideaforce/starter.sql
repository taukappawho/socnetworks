select author, count(author) as NumSuggestions from sbf_suggestion S group by author having count(S.author) > 1;
select author, count(author) as NumSuggestions, sum(votes)  from sbf_suggestion S group by author order by sum(votes) desc,count(author) desc;
select author, count(author) as NumSuggestions  from sbf_suggestion S group by author order by count(author) desc;

select * from sbf_suggestion;

select S.suggestionId, S.category, S.author, C.author, C.commentId
from sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId;

select *
from sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId;

select author, count(author) from sbf_suggestion;
select * from sbf_comment;
select author from sbf_comment where UPPER(author) like "SBX%";
select * from sbf_suggestion where author like "sbx_%";

select * from sbf_comment where UPPER(author) like "SBX%";

select * from sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId;

select S.suggestionId, S.author, C.author, commentId from sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId limit 40;

select * from sbf_suggestion S join sbf_comment C;

select distinct author from sbf_suggestion;
select  author from sbf_suggestion where UPPER(author) like "SBF_%";
select distinct author from sbf_comment;

SELECT S.suggestionId, S.author, C.author, C.suggestionId, C.commentId FROM sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId limit 1000;

select * from sbf_suggestion where suggestionId = 1000;

select * from sbf_comment where suggestionId = 463;

select * from sbf_suggestion where author like "sbf_%";

select S.suggestionId, votes, S.title, S.category, count(C.suggestionId) from sbf_suggestion S join sbf_comment C on S.suggestionId = C.suggestionId
group by S.suggestionId
order by S.votes desc limit 500;

select * from sbf_suggestion S order by votes desc;
select votes from sbf_suggestion S where votes < 0  order by votes desc;

-- list the different categories
select distinct(category) from sbf_suggestion;


;
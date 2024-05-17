select author, count(author) as NumSuggestions from sbf_suggestion S group by author having count(S.author) > 1;
select author, count(author) as NumSuggestions from sbf_suggestion S group by author order by count(S.author) desc;
select author, count(author) as NumSuggestions from sbf_comment S group by author order by count(S.author) desc;
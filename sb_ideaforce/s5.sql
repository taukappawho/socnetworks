SELECT DISTINCT author
FROM (
    SELECT DISTINCT author FROM sbf_suggestion
    UNION
    SELECT DISTINCT author FROM sbf_comment
) AS combined_authors;
SELECT DISTINCT author FROM (
    SELECT author FROM sbf_suggestion
    UNION
    SELECT author FROM sbf_comment
) AS combined_authors;

SELECT author, count(author)
FROM sbf_comment
GROUP BY author
ORDER BY COUNT(author) DESC limit 40;

select author,votes, timestamp from sbf_suggestion where author like "cupaj%" order by votes desc;
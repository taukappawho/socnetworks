-- 2000 suggestions, show the distinct authors
WITH
Top1000 AS (
  SELECT suggestionId
  FROM sbf_suggestion
  ORDER BY votes DESC
  LIMIT 1000
),
Bottom1000 AS (
  SELECT suggestionId
  FROM sbf_suggestion
  ORDER BY votes ASC
  LIMIT 1000
),
SelectedSuggestions AS (
  -- Combine the top and bottom 1000 suggestions
  SELECT suggestionId FROM Top1000
  UNION ALL
  SELECT suggestionId FROM Bottom1000
)
SELECT  distinct C.author , count(C.author)
FROM sbf_comment C
INNER JOIN SelectedSuggestions S
ON C.suggestionId = S.suggestionId
group by C.author
having count(C.author) > 5
order by count(C.author) desc;

-- 2000 suggestions, show the total # of comments
WITH
Top1000 AS (
  SELECT suggestionId
  FROM sbf_suggestion
  ORDER BY votes DESC
  LIMIT 1000
),
Bottom1000 AS (
  SELECT suggestionId
  FROM sbf_suggestion
  ORDER BY votes ASC
  LIMIT 1000
),
SelectedSuggestions AS (
  -- Combine the top and bottom 1000 suggestions
  SELECT suggestionId FROM Top1000
  UNION ALL
  SELECT suggestionId FROM Bottom1000
)
SELECT C.commentId
FROM sbf_comment C
INNER JOIN SelectedSuggestions S
ON C.suggestionId = S.suggestionId;


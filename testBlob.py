from textblob import TextBlob
text = "donald trump is the worst"
print(text,": ", TextBlob(text).sentiment)
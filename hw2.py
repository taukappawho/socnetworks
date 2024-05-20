import pymysql
import networkx as nx
import matplotlib.pyplot as plt
import datetime
from textblob import TextBlob
from datetime import datetime
from collections import Counter
date_format = '%m/%d/%Y %I:%M %p'


# Connect to MySQL database
conn = pymysql.connect(
    host="localhost",
    user="python",
    password="Python12",
    database="set_local"
)

# Fetch data from MySQL tables
def fetch_data(query):
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data

def most_freq(ele, num):
    counts = Counter(ele)
    most = counts.most_common(num)
    return most


def isDate1GTDate2(date1, date2):
    date1 = datetime.strptime(date1, date_format)
    date2 = datetime.strptime(date2, date_format)
    if date1 <= date2:
        return False
    else:
        return True

# Add an edge with weight handling duplicates
def add_edge(graph, node_a, node_b, sentiment, timestamp):
    if graph.has_edge(node_a, node_b):
        # If edge already exists, increment the weight by 1
        graph.edges[(node_a, node_b)]['weight'] += 1
        graph.edges[(node_a, node_b)]['sentiment'] += sentiment
        if isDate1GTDate2(graph.edges[(node_a, node_b)]['timestamp'], timestamp):
            graph.edges[(node_a, node_b)]['timestamp'] = timestamp
    else:
        # Otherwise, add a new edge with weight 1
        graph.add_edge(node_a, node_b, weight=1, sentiment=sentiment, timestamp=timestamp)

def inGraph(node): #same result as G.hasEdge except slower
    for i in range(len(idea_list)):
        if idea_list[i] == node:
            return True
    return False

def getInfluencer(idea):
    # top community,  top earliest community comment node,  top earliest community.timestamp, earliest community, earliest community.timestamp
    sentiment = -2
    earliest = None
    influencer = None
    # print("\n\nIn getInfuluencer. idea: ", idea)
    for idx, comment in enumerate(idea):
        # print("\nIn getInfuluencer. comment: ", comment)
        if comment['sentiment'] != "":
            if comment['sentiment'] > sentiment:
                sentiment = comment['sentiment']
                influencer = idx
            if earliest is None: 
                earliest = idx
            if isDate1GTDate2(idea[earliest]['timestamp'], comment['timestamp']):
                earliest = idx


    if earliest is None or influencer is None:
        return None, None, None, None, None
    return influencer, idea[influencer]['author'], idea[influencer]['timestamp'], earliest, idea[earliest]['timestamp']

# Create network directed graph. decided to go with undirected
# G is for suggestion node and attribute
# C is for relationship between comment authors
# build G, build C, find louvain(C)
G = nx.Graph()
C = nx.Graph()
# number = input("number: ")
number = 5000 #this is the 5000 highest upvote getters and 5000 lowest downvote getter; no checking is performed

# Fetch data from sbf_suggestion table
# suggestion_query = SELECT suggestionId, body, author, title, category, votes FROM sbf_suggestion limit 1000"
suggestion_query = """SELECT suggestionId, body, author, title, category, votes
FROM (
    SELECT suggestionId, body, author, title, category, votes FROM sbf_suggestion
    ORDER BY votes DESC
    LIMIT """ + str(number) + """
) AS highest_votes
UNION ALL
SELECT suggestionId, body, author, title, category, votes FROM (
    SELECT suggestionId, body, author, title, category, votes FROM sbf_suggestion
    ORDER BY votes asc
    LIMIT """ + str(number) + """
) AS lowest_votes;"""
suggestions_data = fetch_data(suggestion_query)

# Add nodes to the graph
suggestionId=0
body=1
author=2
votes = 5
idea_list = []
for suggestion in suggestions_data:
    idea_list.append(suggestion[suggestionId])
    G.add_node(suggestion[suggestionId],author=suggestion[author],votes=suggestion[votes])
# print("Num suggestions: ", nx.number_of_nodes(G))
# print("\tNum nodes: ", nx.number_of_nodes(G))
# print("\tNum Edges: ", nx.number_of_edges(G))


comment_query = "select suggestionId, commentId, author, body, timestamp from sbf_comment"
comment_data = fetch_data(comment_query)
suggestionId = 0
comment_text = 3
timestamp = 4
idea_node = -1
c_count = 0
comment_author_list = []
for comment in comment_data:
    if (G.has_node(comment[suggestionId])):
    # if inGraph(comment[suggestionId]):
        c_count = c_count + 1
        sentiment = TextBlob(comment[comment_text]).sentiment.polarity
        ts = comment[timestamp]
        add_edge(G, comment[author], comment[suggestionId], sentiment,  ts)
        if comment[suggestionId] == idea_node:
            for c_author in comment_author_list:
                C.add_edge(comment[author],c_author)
            comment_author_list.append(comment[author])
        else:
            comment_author_list = list(comment[author])
            idea_node = comment[suggestionId]

# for n in nx.nodes(C):
#     pos = nx.spring_layout(C)  # positions for all nodes
#     nx.draw(C, pos,  node_color='lightblue', edge_color='gray', node_size=2, font_size=10, font_weight='bold')
#     plt.title("Graph C")
#     plt.show()

    # print(comment[comment_text][:40], ": ",sentiment)

# Print info about the graph
print("After comments")
print("G: Number of nodes:", G.number_of_nodes())
print("G: Number of edges:", G.number_of_edges())
print()
print("C: Number of nodes:", C.number_of_nodes())
print("C: Number of edges:", C.number_of_edges())

x = nx.community.louvain_communities(G)
print("\nG louvain communities: ", len (x))
communities = nx.community.louvain_communities(C)
print("C louvain communities: ", len(communities))

#for each suggestionId
#find all connected nodes (ones that voted on suggestionId) - use G
#   from each comment node, collect the sentiment nad timestamp on edge
#   for each community
#       if comment node in community
#           add sentiment to community sentiment for suggestionId
#           if community.timestamp == null or community.timestmp > node.timestamp
#               community.timestamp = node.timestamp
#           delete node from list
#for each suggestionId node
#print top community,  top earliest community comment node,  top earliest community.timestamp, earliest community, earliest community.timestamp
#
#total things up
#top community overall
#top earliest community comment node
#earliest community

#for each suggestionId
results = []
for i in range(2 * int(number)):
    idea_results = []
    for j in range(len(communities)):
        community_results = {"timestamp":"", "sentiment":"", "author":""}
        idea_results.append(community_results)
    results.append(idea_results)
count = 0
idea_index = 0
for idea in idea_list:
    #find all connected nodes (ones that voted on suggestionId) - use G
    node_list = list(G.neighbors(idea))
    remove_list = []
    #   for each community
    community_index = 0
    for community in communities:
    #       if comment node in community
        for node in node_list:
            if node in community:
#           add sentiment to community sentiment for suggestionId
                remove_list.append(node)
                sentiment = G[idea][node]['sentiment']
                timestamp = G[idea][node]['timestamp']
                author = node
                # print(sentiment, timestamp,author)
                count = count + 1
                if results[idea_index][community_index]["timestamp"] == "" or isDate1GTDate2(results[idea_index][community_index]["timestamp"], timestamp):
                    results[idea_index][community_index]["timestamp"] = timestamp
                    results[idea_index][community_index]["sentiment"] = sentiment 
                    results[idea_index][community_index]["author"] = author
        community_index = community_index + 1
    idea_index = idea_index + 1

community = []
author = []
earliest_community = []
for idx, idea in enumerate(results):
    item = getInfluencer(idea)
    if item[0] is not None:
        community.append(item[0])
        author.append(item[1])
        earliest_community.append(item[3])

community = most_freq(community,10)
author = most_freq(author, 10)
earliest_community = most_freq(earliest_community, 10)
print("Top 10 communities [#times had highest sentiment for a given idea, format (community#, #times)]\n", community)
print("Top 10 authors - comment author who commentted first comment on idea\n", author)
print("Top 10 earliest_communities - the earliest community to comment, but might not have had the highest sentiment\n", earliest_community)

# Close database connection
conn.close()
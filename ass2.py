import pymysql
import networkx as nx
import matplotlib.pyplot as plt
import datetime
from textblob import TextBlob


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

# Add an edge with weight handling duplicates
def add_edge(graph, node_a, node_b, sentiment, votes):
    if graph.has_edge(node_a, node_b):
        # If edge already exists, increment the weight by 1
        graph.edges[(node_a, node_b)]['weight'] += 1
        graph.edges[(node_a, node_b)]['sentiment'] += sentiment
    else:
        # Otherwise, add a new edge with weight 1
        graph.add_edge(node_a, node_b, weight=1, sentiment=sentiment)
        if votes:
            nx.set_node_attributes(graph, {node_a : votes}, "votes")
            # graph.edges[(node_a, node_b)]['votes'] = votes

curr_time = datetime.datetime.now()
print("Current time: ", curr_time)

# Create network directed graph
G = nx.DiGraph()
C = nx.Graph()

# Fetch data from sbf_suggestion table
# suggestion_query = SELECT suggestionId, body, author, title, category, votes FROM sbf_suggestion limit 1000"
suggestion_query = """SELECT suggestionId, body, author, title, category, votes
FROM (
    SELECT suggestionId, body, author, title, category, votes FROM sbf_suggestion
    ORDER BY votes DESC
    LIMIT 100
) AS highest_votes
UNION ALL
SELECT suggestionId, body, author, title, category, votes FROM (
    SELECT suggestionId, body, author, title, category, votes FROM sbf_suggestion
    ORDER BY votes asc
    LIMIT 100
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
    add_edge(G, suggestion[suggestionId], suggestion[author], TextBlob(suggestion[body]).sentiment, suggestion[votes])
num_suggestions = nx.number_of_edges(G)
print("Num suggestions: ", num_suggestions)
print("\tNum nodes: ", nx.number_of_nodes(G))
print("\tNum Edges: ", nx.number_of_edges(G))

comment_query = "select suggestionId, commentId, author, body from sbf_comment"
comment_data = fetch_data(comment_query)
suggestionId = 0
comment_text = 3
idea_node = -1
comment_author_list = []
for comment in comment_data:
    if (G.has_node(comment[suggestionId])):
        sentiment = TextBlob(comment[comment_text]).sentiment.polarity
        add_edge(G, comment[author], comment[suggestionId], sentiment, None)
        if comment[suggestionId] == idea_node:
            for c_author in comment_author_list:
                C.add_edge(comment[author],c_author)
            comment_author_list.append(comment[author])
        else:
            comment_author_list = list(comment[author])
            idea_node = comment[suggestionId]

for n in nx.nodes(C):
    pos = nx.spring_layout(C)  # positions for all nodes
    nx.draw(C, pos,  node_color='lightblue', edge_color='gray', node_size=2, font_size=10, font_weight='bold')
    plt.title("Graph C")
    plt.show()

    # print(comment[comment_text][:40], ": ",sentiment)

# Print info about the graph
print("After comments")
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

print("\n\nElapsed time: ", datetime.datetime.now() - curr_time)


x = nx.community.louvain_communities(G)
print(x)
print(len(x))
for n in x:
    print(n)
    subgraph = nx.subgraph(G, n)
    pos = nx.spring_layout(subgraph)
    nx.draw(subgraph, pos, with_labels=False)
    # edge_weights = [subgraph.edges[edge]['weight'] for edge in edges]
    # nx.draw_networkx_edges(subgraph, pos, edgelist=edges, edge_color='black', width=edge_weights)
num = 1
node_num = 0

# do the comment author thing


while num != 0:
    num = idea_list[node_num]
    node_num = node_num + 1
    nodes = list(G.predecessors(num)) + list(G.successors(num)) + [num]
    print("#nodes: ", len(nodes) - 1)
    edges = list(G.in_edges(num)) + list(G.out_edges(num))
    print("#edges: ", len(edges))
    subgraph = G.subgraph(nodes)
    
    sentiments = nx.get_edge_attributes(subgraph, "sentiment")
    print("sentiiments: ",sentiments)
    weights = nx.get_edge_attributes(subgraph, "weight")
    print("weights: ",weights)

    # num = int(input("Suggestion: "))

        # Create a list of node sizes based on 'votes' attribute or default to 500
    node_sizes = [subgraph.nodes[node].get('votes', 50) for node in subgraph.nodes()]
    
    # Draw the subgraph
    pos = nx.spring_layout(subgraph)
    
    nx.draw(subgraph, pos, with_labels=False, node_size=node_sizes)
    
    # Edges weighted by weight attribute
    edge_weights = [subgraph.edges[edge]['weight'] for edge in edges]
    nx.draw_networkx_edges(subgraph, pos, edgelist=edges, edge_color='black', width=edge_weights)
    
    plt.show()
    
    num = input("Suggestion: ")
    num = 1

# Close database connection
conn.close()
print("\n\nElapsed time: ", datetime.datetime.now() - curr_time)

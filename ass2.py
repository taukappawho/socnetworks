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

# Fetch data from sbf_suggestion table
suggestion_query = "SELECT suggestionId, body, author, title, category, votes FROM sbf_suggestion limit 10000"
suggestions_data = fetch_data(suggestion_query)

# Add nodes to the graph
author=2
suggestionId=0
votes = 5
for suggestion in suggestions_data:
    add_edge(G, suggestion[suggestionId], suggestion[author], TextBlob(suggestion[1]).sentiment, suggestion[votes])

num_suggestions = nx.number_of_edges(G)
print("Num suggestions: ", num_suggestions)

comment_query = "select suggestionId, commentId, author, body from sbf_comment limit 10000"
comment_data = fetch_data(comment_query)
comment_text = 3
for comment in comment_data:
    sentiment = TextBlob(comment[comment_text]).sentiment.polarity
    add_edge(G, comment[author], comment[suggestionId], sentiment, None)
    # print(comment[comment_text][:40], ": ",sentiment)

# Print info about the graph
print("Number of nodes:", G.number_of_nodes())
print("Number of edges:", G.number_of_edges())

print("\n\nElapsed time: ", datetime.datetime.now() - curr_time)

# x = nx.community.louvain_communities(G)
# print(len(x))
num = int(input("Suggestion: "))
while 0< num <= num_suggestions:

    nodes = list(G.predecessors(num)) + list(G.successors(num)) + [num]
    print("#nodes: ", len(nodes) - 1)
    edges = list(G.in_edges(num)) + list(G.out_edges(num))
    print("#edges: ", len(edges))
    subgraph = G.subgraph(nodes)
    
    sentiments = nx.get_edge_attributes(subgraph, "sentiment")
    print("sentiiments: ",sentiments)
    weights = nx.get_edge_attributes(subgraph, "weight")
    print("weights: ",weights)

    # # Draw the subgraph
    # pos = nx.spring_layout(subgraph)
    # nx.draw(subgraph, pos, with_labels=True, node_color='lightblue', node_size=500)
    # nx.draw_networkx_edges(subgraph, pos, edgelist=edges, edge_color='black', width=[subgraph.edges[edge]['weight'] for edge in edges])
    # plt.show()

    # num = int(input("Suggestion: "))

        # Create a list of node sizes based on 'votes' attribute or default to 500
    node_sizes = [subgraph.nodes[node].get('votes', 50) for node in subgraph.nodes()]
    
    # Draw the subgraph
    pos = nx.spring_layout(subgraph)
    
    nx.draw(subgraph, pos, with_labels=True, node_size=node_sizes)
    
    # Edges weighted by weight attribute
    edge_weights = [subgraph.edges[edge]['weight'] for edge in edges]
    nx.draw_networkx_edges(subgraph, pos, edgelist=edges, edge_color='black', width=edge_weights)
    
    plt.show()
    
    num = int(input("Suggestion: "))

# # Draw the graph
# plt.figure(figsize=(10, 6))
# pos = nx.spring_layout(G)  # Positions for all nodes
# nx.draw(G, pos, with_labels=True, node_size=10, node_color='skyblue', font_size=5, font_weight='bold', edge_color='gray')

# # Customize the plot
# plt.title('Network Graph of Comments and Suggestions')
# plt.axis('off')  # Turn off the axis
# plt.tight_layout()  # Adjust layout to make sure everything fits without overlapping

# # Display the plot
# plt.show()

# Close database connection
conn.close()
print("\n\nElapsed time: ", datetime.datetime.now() - curr_time)

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd

G = nx.Graph()
df = pd.read_csv("all_video_games(cleaned).csv")
df = df.head(500) #limits the graph to 500 nodes to keep graph to a somewhat reasonable size

df = df.drop("Release Date" , axis=1)
df = df.drop("Product Rating" , axis=1)
df = df.drop("User Score" , axis=1)
df = df.drop("User Ratings Count" , axis=1)
df = df.drop("Platforms Info", axis = 1)
df = df.drop("Developer" , axis=1)
df = df.drop("Publisher" , axis=1)
df['Genres Splitted'] = df['Genres Splitted'].apply(lambda x: x.strip("[]").replace("'", ""))

print(df.head())

for index, row in df.iterrows():
    #Splits the genres by comma and remove any whitespaces
    genres = [genre.strip() for genre in row['Genres Splitted'].split(',')]
    
    # Add the game as a node to the graph
    G.add_node(row['Title'])

    # Iterate through all other rows to compare genres and create edges
    for _, other_row in df.iterrows():
        if row['Title'] != other_row['Title']:
            other_genres = [genre.strip() for genre in other_row['Genres Splitted'].split(',')]
            
            # Calculate the weight of the edge based on the number of common genres
            weight = len(set(genres).intersection(other_genres))
            
            # Add the edge between the two games with the weight as the weight of the edge
            if weight > 0:
                G.add_edge(row['Title'], other_row['Title'], weight=weight)

# gets a list of all genres and then determines which genre shows up the most
all_genres = [genre.strip() for sublist in df['Genres Splitted'].apply(lambda x: x.split(',')) for genre in sublist]
most_common_genre = max(set(all_genres), key=all_genres.count)

print("The most common genre is:", most_common_genre)

# Calculate the top 10 nodes in terms of total edge weight
node_weights = {node: sum([data['weight'] for _, data in G[node].items()]) for node in G.nodes()}
top_50_nodes = sorted(node_weights, key=node_weights.get, reverse=True)[:50]

print("Top 50 nodes in terms of total edge weight:")
for i, node in enumerate(top_50_nodes, 1):
    print(f"{i}. {node}: {node_weights[node]}")

# Draws the graph
pos = nx.spring_layout(G)  # Positions for all nodes

# Draw the nodes
nx.draw_networkx_nodes(G, pos, node_size=100, node_color='skyblue')

# Draw the edges
nx.draw_networkx_edges(G, pos, width=1.0, alpha=0.5, edge_color='red')

# shorten the labels to 8 characters
truncated_labels = {node: node[:8] for node in G.nodes()}

# Draw the labels
nx.draw_networkx_labels(G, pos, labels=truncated_labels, font_size=8, font_family='sans-serif')

# Show the plot
plt.axis('off') 
plt.show()

import module_settings_airlines_airports as setair
import module_visualization as worldmap
import os
os.environ["PROJ_LIB"] = os.path.join(os.environ["CONDA_PREFIX"], "share", "proj")
import networkx as nx
import pandas as pd
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np



def calculate_network_metrics_from_df(df):
    

    graph_airline = setair.create_graph_object(df)
    
    nnodes = graph_airline.number_of_nodes()
    nedges = graph_airline.number_of_edges()
    

    density_airline = nx.density(graph_airline)
    closeness_centrality = nx.closeness_centrality(graph_airline)
    clustering_coefficient = nx.average_clustering(graph_airline)
    
    short_path_av_airline = nx.average_shortest_path_length(graph_airline)
    global_efficiency_airline = 1/short_path_av_airline
    
    hub_table_airline = setair.find_hubs_in_df(df, 1)
    hub_airline = hub_table_airline.iloc[0,0]

    graph_metrics = [nnodes, nedges, density_airline, global_efficiency_airline, hub_airline, closeness_centrality, clustering_coefficient]

    return graph_metrics


def create_graph_metrics_table(df1, df2):
    
    list_graph_metrics_airline1 = calculate_network_metrics_from_df(df1)
    list_graph_metrics_airline2 = calculate_network_metrics_from_df(df2)

    graph_metrics = pd.DataFrame({"metrics":["no of nodes", "no of edges", "density", "global efficiency", "biggest hub", "closeness centrality", "clustering coefficient"], "airline 1": list_graph_metrics_airline1, "airline 2":list_graph_metrics_airline2})
    print(graph_metrics)
    
   
    
    
    
def visualize_two_networks_on_worldmap(df1, df2):
        
    graph_df1 = worldmap.create_graph_object(df1, nx.Graph())

    graph_df2 = worldmap.create_graph_object(df2, nx.Graph())

    plt.figure(figsize = (15,20))
    m = Basemap(projection='merc',
                llcrnrlon=-180,
                llcrnrlat=-80,
                urcrnrlon=180,
                urcrnrlat=80)
    
    m.drawcoastlines()
    m.drawmapboundary()
    m.drawcountries()


    m.drawparallels(np.arange(-90,90,30))
    m.drawmeridians(np.arange(-180,180,60))

    

    pos1 = worldmap.create_pos_variable(df1, m)
    pos2 = worldmap.create_pos_variable(df2, m)

    node_size1 = worldmap.node_size_degree(graph_df1)
    node_size2 = worldmap.node_size_degree(graph_df2)
    
    worldmap.draw_nodes_and_edges(graph_df1, pos1, node_size1, node_visibility = 0.8, edge_visibility = 0.5, ncolor = "#FF6347", ecolor = '#FFBABA')
    worldmap.draw_nodes_and_edges(graph_df2, pos2, node_size2, node_visibility = 0.8, edge_visibility = 0.5, ncolor = '#20B2AA', ecolor = '#AFEEEE')                     
                 
    worldmap.draw_biggest_hubs(df1, 1, graph_df1, pos1, '#CC0000')
    worldmap.draw_biggest_hubs(df2, 1, graph_df2, pos2, '#0000CC')
    

    hub1 = setair.find_hubs_in_df(df1, 1)
    worldmap.hub_network_labels(hub1, graph_df1, pos1)
       
    hub2 = setair.find_hubs_in_df(df2, 1)
    worldmap.hub_network_labels(hub2, graph_df2, pos2)
        
    plt.show()    
       



def compare_airlines_program(df):
    
    print("\nYou chose to compare airlines.")
    
    df_airline1 = setair.define_airline_through_user_input(df)
    
    print("\n\tYou choose your first airline. Now select another one to compare!")
    
    df_airline2 = setair.define_airline_through_user_input(df)
    
    visualize_two_networks_on_worldmap(df_airline1, df_airline2)  
    
    create_graph_metrics_table(df_airline1, df_airline2)

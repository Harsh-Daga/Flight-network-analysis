import module_inspect_data as inspect
import module_settings_airlines_airports as setair
import networkx as nx
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np



def create_graph_object(df, directionality):
    graph = nx.from_pandas_edgelist(df, source = 'source airport', \
                                 target = 'destination airport', create_using = directionality)
    return graph   


def create_pos_variable(df, m):
    
    mx, my = m(df['longitude'].values, df['latitude'].values)
    pos = {}
    for count, elem in enumerate (df['source airport']):
         pos[elem] = (mx[count], my[count])
    return pos

def draw_nodes_and_edges(graph, pos, node_size, node_visibility, edge_visibility, ncolor='#F7A538', ecolor='#5EC4B7', ewidth = 2):
    
    nx.draw_networkx_nodes(graph, pos, node_size = node_size, node_color = ncolor, alpha = node_visibility)
    nx.draw_networkx_edges(graph, pos, edge_color = ecolor, width = ewidth, alpha = edge_visibility)
        
    

def node_size_degree(graph):

    degree = dict(graph.degree())

    node_size_list = []
    for h in degree.values():
        node_size_list = node_size_list + [h * 1.5]
    
    return node_size_list



def draw_biggest_hubs(df, hub_nr, graph_df, pos, color):
    
    hub_table = setair.find_hubs_in_df(df, hub_nr)

    hublist = hub_table["airport"].tolist()
    node_size = hub_table["degree"].tolist()

    nx.draw_networkx_nodes(graph_df, pos, nodelist=hublist, node_color=color, node_size = node_size) 
    
    


def hub_network_labels(hub_table, graph, pos):
    

    hublist = hub_table["airport"].tolist()
    
    labels = {}

    for hub in hublist:
        labels[hub] = hub    
    nx.draw_networkx_labels(graph, pos, labels=labels, font_size=12, font_color='#000000')                                          
             





def visualize_on_worldmap(dataframe, directionality=nx.Graph(), node_size=20, hub_nr=0, node_visibility=0.8, edge_visibility=0.1):
     
    graph = create_graph_object(dataframe, directionality)

    graph_info = nx.info(graph)
    print(graph_info)

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

    pos = create_pos_variable(dataframe, m)   
    
    draw_nodes_and_edges(graph, pos, node_size, node_visibility, edge_visibility)
    
    if hub_nr > 0:
        draw_biggest_hubs(dataframe, hub_nr, graph, pos, '#CC0000')
        
        hub_table = setair.find_hubs_in_df(dataframe, hub_nr)
        hub_network_labels(hub_table, graph, pos)

    plt.show()




def demo_program(dataframe):
    
    demo_options = input("""What do you want to do?
    1\tShow both airports and flight routes             
    2\tShow only airports
    3\tShow only flight routes
    enter answer (1/2/3): """)
    if demo_options == '1':
        print('You chose to show both airports and flight routes')
        visualize_on_worldmap(dataframe)
    
    elif demo_options == '2':
        print('You chose to show only the airports')

        visualize_on_worldmap(dataframe, edge_visibility = 0)
        
    elif demo_options == '3':
        print('You chose to show only the flight routes')

        visualize_on_worldmap(dataframe, node_visibility = 0)

    else:
        print('\nSorry, this is not an option, we will return to the main program')
        
    
def visualisation_worldmap_program(dataframe):

    dataframe = dataframe
    directionality = nx.Graph()
    node_size = 20
    hub_nr = 0
    
    map_amount = input("""What do you want to do?
    1\tSelect all airlines and airports              
    2\tSelect specific airlines
    3\tSelect specific airports
    enter answer (1/2/3): """)
    
    if map_amount == '1':
        print('You chose to plot all airlines and airports')
          
    elif map_amount == '2':
        print('You chose to plot specific airlines')
        choice_airlines = input("""What do you want to do?
        1\tSelect the biggest airlines             
        2\tSelect a specific airline
        enter answer (1/2): """)
        
        if choice_airlines == '1':
            print('You chose to plot the biggest airlines')
            map_number_airlines = int(input('How many of the biggest airlines do you want to plot? (1 to 15) '))
            
            if 1 <= map_number_airlines <= 15:
                print(f'You chose to plot the top {map_number_airlines} biggest airlines')
                
                airline_table = setair.airline_table(dataframe)
                
                airline_table_name = setair.airline_table_name(dataframe)
                
                dataframe = setair.take_nairlines(dataframe, airline_table, map_number_airlines)
                
                top_table = airline_table_name[:map_number_airlines]
                inspect.barplot_from_df(top_table, x="name airline" , y="flight_routes_nr" , ylabel="flight routes")
                

            else:
                print('\nSorry, this is not an option, we will use the default setting: all airports and airlines') 

                
        elif choice_airlines == '2':   
            print('You chose to plot a specific airline based on name')
            dataframe = setair.define_airline_through_user_input(dataframe)
          
        else:
            print('\nSorry, this is not an option, we will use the default setting: all airports and airlines') 
        
        
    elif map_amount == '3':
        print('You chose to plot specific airports')
        choice_airports = input("""What do you want to do?
        1\tSelect the biggest airports             
        2\tSelect a specific airports
        enter answer (1/2): """)  
        
        if choice_airports == '1':
            print('You chose to plot the biggest airports')
            map_number_airports = int(input('How many of the biggest airports do you want to plot? (1 to 15) '))
            if 1 <= map_number_airports <= 15:
                
                hub_nr = map_number_airports
                print(f'You chose to plot the top {hub_nr} biggest airports')
            
                hub_table = setair.find_hubs_in_df(dataframe, hub_nr)
            
                dataframe = setair.hub_network_df(dataframe, hub_table)
            
                inspect.barplot_from_df(hub_table, x="airport" , y="degree", ylabel="flight routes")
            else:
                print('\nSorry, this is not an option, we will use the default setting: all airports and airlines') 
                
        elif choice_airports == '2':
            print('You chose to plot a specific airport based on name')
            hub_nr = 1
            
            dataframe = setair.define_airport_through_user_input(dataframe)

    else:
        print('\nSorry, this is not an option, we will use the default setting: all airports and airlines') 



    map_edges = input("""What do you want to do?
    1\tMake an undirected network              
    2\tMake a directed network
    enter answer (1/2): """)
    
    if map_edges == '1':
        print(f'You chose to create an undirected network')
        
    elif map_edges == '2':
        print(f'You chose to create a directed network')
        directionality = nx.DiGraph()
        
    else:
        print('\nSorry, this is not an option, we will use the default setting: an undirected network')   
    

    size_airport = input("""What do you want to do?
    1\tDisplay all airports with the same size             
    2\tDisplay size of airport depending on how many flight routes it has (degree)
    enter answer (1/2): """)
    
    if size_airport == '1':
        print('You chose to display all airports with the same size')
        
    elif size_airport == '2':
        print('You chose to display airport size dependent on degree')
        graph = create_graph_object(dataframe, nx.Graph())

        node_size = node_size_degree(graph)
        
    else:
        print('\nSorry, this is not an option, we will use the default setting: all same size ')
    
    visualize_on_worldmap(dataframe, directionality, node_size, hub_nr)



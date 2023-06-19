import base_preprocessing as bpp
import networkx as nx
import operator
import pandas as pd

def create_graph_object(df):
    graph = nx.from_pandas_edgelist(df, source = 'source airport', \
                                 target = 'destination airport')
    return graph


def degree_of_nodes(graph):
    
    degree = dict(graph.degree())
    degree_sorted = sorted(degree.items(), key = operator.itemgetter(1), reverse=True)
    degree_nodes = pd.DataFrame(degree_sorted, columns=["airport", "degree"])

    return degree_nodes



def find_hubs_in_df(df, hubs_nr):
    
    graph = create_graph_object(df)
    degree_nodes = degree_of_nodes(graph)
    hub_table = degree_nodes[:hubs_nr]
    
    return hub_table
    

def hub_network_df(df, hub_table):
 
    hublist = hub_table["airport"].tolist()
    hub_df_source = df[df["source airport"].isin(hublist)]
    
    hub_df_dest = df[df["destination airport"].isin(hublist)]
    
    df_hubnetwork = pd.concat([hub_df_source, hub_df_dest], axis=0)
    df_hubnetwork_clean = bpp.clean_dataframe(df_hubnetwork)
    
    return df_hubnetwork_clean


def specific_airport_df(df, airport):
    
    hub_df_source = df[df["source airport"]==airport]
    hub_df_dest = df[df["destination airport"]==airport]
    df_specific_airport = pd.concat([hub_df_source, hub_df_dest], axis=0)
    df_specific_airport_clean = bpp.clean_dataframe(df_specific_airport)
    
    return df_specific_airport_clean



    
def airline_table(dataframe):
    
    df_top_airlines = dataframe['airline IATA code'].value_counts().reset_index()
    df_top_airlines.rename(columns= {'airline IATA code':'flight_routes_nr'}, inplace=True)
    df_top_airlines.rename(columns= {'index':'airline IATA code'}, inplace=True)
    
    return df_top_airlines


def airline_table_name(dataframe):

    df_top_airlines = dataframe['name airline'].value_counts().reset_index()
    df_top_airlines.rename(columns= {'name airline':'flight_routes_nr'}, inplace=True)
    df_top_airlines.rename(columns= {'index':'name airline'}, inplace=True)
    
    return df_top_airlines


def take_airlines(dataframe, sel_airline):
    
    dataframe = dataframe[dataframe['airline IATA code'] == (sel_airline)]
    dataframe_clean = bpp.clean_dataframe(dataframe)

    return dataframe_clean


def take_nairlines(dataframe, airline_table, number):
    
    df_airlines = airline_table[:number]
    airl_list = df_airlines['airline IATA code'].tolist()
    dataframe = dataframe.loc[dataframe['airline IATA code'].isin(airl_list)]
    dataframe_clean = bpp.clean_dataframe(dataframe)
    
    return dataframe_clean 




def define_airline_through_user_input(df):

    unique_airlines_list = df["airline IATA code"].drop_duplicates().tolist()
    input_airline = False
    while input_airline == False:
        
        airline = input("""
        Which airline do you want to visualise? Enter the 2-letter IATA code in 
        capital letters.
        
        For inspiration see the 10 airlines with the most flight routes: 
                        
        FR\tRyanair
        AA\tAmerican Airlines
        UA\tUnited Airlines
        DL\tDelta Air Lines
        US\tUS Airways
        CZ\tChina Southern Airlines
        MU\tChina Eastern Airlines
        CA\tAir China
        WN\tSouthwest Airlines
        U2\teasyJet
        
        Enter your answer here: """)

        if airline in unique_airlines_list:   
            
            df_airline = take_airlines(df, airline)
            
            input_airline == True
            
            return df_airline 
        else: 
            print("This is not a valid input, try again")
    
    
    
    
    
def define_airport_through_user_input(df):
    
    unique_airport_list = df["source airport"].drop_duplicates().tolist()
    input_airport = False
    
    while input_airport == False:
    
        airport = input("""
        Which airport do you want to visualise? Enter the 3-letter IATA code in 
        capital letters.
        
        For inspiration see the 10 airports with the most flight routes: 
                        
        AMS\tAmsterdam Airport Schiphol
        FRA\tFrankfurt am Main International Airport
        CDG\tCharles de Gaulle International Airport
        IST\tAtatürk International Airport
        ATL\tHartsfield Jackson Atlanta International Airport
        PEK\tBeijing Capital International Airport
        ORD\tChicago O'Hare International Airport
        MUC\tMunich International Airport
        DME\tDomodedovo International Airport
        DFW\tDallas Fort Worth International Airport
        
        Enter your answer here: """)
        
        if airport in unique_airport_list:   
            
            df_airport = specific_airport_df(df, airport)
            
            input_airport == True
            
            return df_airport
        
        else: 
            print("This is not a valid input, try again")
    
    
    


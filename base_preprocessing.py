import pandas as pd

def load_data_routes_from_file(file):
    
    df_routes = pd.read_csv(file, sep=',')
    
    df_routes.rename(columns= {"airline":"airline IATA code"}, inplace=True)
    df_routes.rename(columns= {" source airport":"source airport"}, inplace=True)
    df_routes.rename(columns= {" source airport id":"source airport ID"}, inplace=True)
    df_routes.rename(columns= {" destination apirport":"destination airport"}, inplace=True) 
    df_routes.rename(columns= {" destination airport id":"destination airport ID"}, inplace=True)
    df_routes.rename(columns= {" codeshare":"codshare"}, inplace=True)
    df_routes.rename(columns= {" stops":"stops"}, inplace=True)
    df_routes.rename(columns= {" equipment":"equipment"}, inplace=True)

    df_routes = df_routes.reindex(columns=["airline IATA code", "airline ID", "source airport", "source airport ID", "destination airport", "destination airport ID"])

    df_routes = df_routes[(df_routes["source airport ID"]!="\\N") & (df_routes["destination airport ID"]!="\\N")]
    
    df_routes = df_routes[df_routes["airline ID"]!="\\N"]
    
    df_routes["source airport ID"] = df_routes["source airport ID"].astype(int)
    df_routes["destination airport ID"] = df_routes["destination airport ID"].astype(int)
    df_routes["airline ID"] = df_routes["airline ID"]
        
    return df_routes


def load_data_airports_from_file(file):

    df_airports = pd.read_csv(file, sep=',', header=None)
    header = ["source airport ID", "airport name", "airport city", "airport country", "IATA", "ICAO", "latitude", "longitude", "altitude", "timezone", "DST", "Tz Olson format", "type", "source"]
    df_airports.columns = header
    
    df_airports = df_airports.reindex(columns=["source airport ID", "airport name", "airport city", "airport country", "latitude", "longitude"])

    return df_airports  


def load_data_airlines_from_file(file):
    
    df_airlines = pd.read_csv(file, sep=',', header=None)
    
    header = ["airline ID", "name airline", "alias", "IATA", "ICAO", "callsign", "country airline", "active"]
    df_airlines.columns = header
    
    df_airlines = df_airlines.reindex(columns=["airline ID", "name airline", "country airline"])

    return df_airlines



def left_merge_dataframes(df_left, df_right, on):
    
    df_merged = pd.merge(df_left, df_right, on=on, how= "left") 

    return df_merged    



 
def clean_dataframe(df):
    
    while True:
        
        airports_to_remove = []
    
        source_airport_ID_list = df["source airport ID"].tolist()
        
        for ID in df["destination airport ID"]:
            if ID not in source_airport_ID_list:
                airports_to_remove += [ID]
                
 
        if airports_to_remove == []:

            return df
            break
        
        else:

            df = df[~df["destination airport ID"].isin(airports_to_remove)]
              

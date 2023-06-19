import base_preprocessing as bpp
import module_visualization as worldmap
import module_inspect_data as inspect
import module_comparison_airlines as comp_air


filename_routes = "routes.csv"
filename_airports = "airports-extended.csv"
filename_airlines = "airlines.csv"

try:
    df_routes = bpp.load_data_routes_from_file(filename_routes)
except FileNotFoundError:
    print("file not found, please check filename_routes and current directory")
except Exception as err: 
    print("Something went wrong")
    print(err)

try:
    df_airports = bpp.load_data_airports_from_file(filename_airports)
except FileNotFoundError:
    print("file not found, please check filename_routes and current directory")
except Exception as err: 
    print("Something went wrong")
    print(err)   
    
try:    
    df_airlines = bpp.load_data_airlines_from_file(filename_airlines)
except FileNotFoundError:
    print("file not found, please check filename_routes and current directory")
except Exception as err: 
    print("Something went wrong")
    print(err) 
    
    
df_merge_airlines_info = bpp.left_merge_dataframes(df_routes, df_airlines, on="airline ID")


df_merged = bpp.left_merge_dataframes(df_merge_airlines_info, df_airports, "source airport ID")

df_merged = df_merged.reindex(columns=["airline IATA code", "airline ID", "name airline", "country airline", "source airport", "source airport ID", "destination airport", "destination airport ID", "airport name", "airport city", "airport country", "latitude", "longitude"])

df_merged = bpp.clean_dataframe(df_merged)   

print("---------------------------------------------------------------------")
print("|                     Flight Network Analysis                       |")
print("|                By: Viraj Bhat, Vinayak Dubey, S Harsh             |")
print("---------------------------------------------------------------------")
print("This project will answer the following questions: ")
print("1) What is the biggest (most connected) airport on earth? ")
print("2) Which airlines has the most flights? ")
print("3) How do airlines differ from each other based on graph metrics?\n")
print("----------------------------------------------------------------------")

while True:   
    choice = input("""What do you want to do?
    0\tSee demo visualization of the flight network.
    1\tInspect the dataframes               
    2\tVisualise flight network with self-chosen parameters.
    3\tCompare airlines.
    4\tExit program.
    enter answer (0/1/2/3/4): """)
    
    if choice == "0": 
        
        worldmap.demo_program(df_merged)


    elif choice == "1": 

        inspect.inspect_data(df_routes, df_airports, df_merged)
    
    
    elif choice == "2": 
        
        worldmap.visualisation_worldmap_program(df_merged)

            
    elif choice == "3": 
        
        comp_air.compare_airlines_program(df_merged)

    elif choice == "4":  
        break 
    
    else:
        print("Choice not recognized. Try again.")
        
        

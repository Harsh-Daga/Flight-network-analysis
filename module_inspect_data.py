import module_settings_airlines_airports as setair
import matplotlib.pyplot as plt



def inspect_columns(specific_df):
    print('\nVariables in the dataframe: \n')
    print(specific_df.columns.tolist())
    

def inspect_unique_values(specific_df):
    print('\nUnique values per variable \n')
    for column in specific_df.columns:
        print(f'{column} = {len(specific_df[column].unique())}')
     

def inspect_most_flights_airports(df):
    test = df['source airport'].value_counts()[:10].reset_index()
    test.plot.bar(x = "index", y = "source airport", legend=False)
    plt.ylabel("flight routes")
    plt.show()
    
def barplot_from_df(table, x, y, ylabel = None):
    table.plot.bar(x, y, legend=False)
    plt.ylabel(ylabel)
    plt.show()    
    

def inspect_data(routes, airports, merged):
    inspect_option = input("""What do you want to do?
    1\tInspect the variables of the used dataframe          
    2\tInspect unique values of the used dataframe
    3\tShow biggest airports/airlines/countries
    enter answer (1/2/3): """)
    
    if inspect_option == '1':
        columns_dataframe = input("""Which dataframe?
        1\tThe routes dataframe          
        2\tThe airports dataframe
        3\tThe merged dataframe 
        enter answer (1/2/3): """)
        
        if columns_dataframe == '1':
            inspect_columns(routes)
            
        elif columns_dataframe == '2':
            inspect_columns(airports)
            
        elif columns_dataframe == '3':
            inspect_columns(merged)
            
        else:
            print('\nSorry, this is not an option, we will return to the main program') 
            
    elif inspect_option == '2':
        unique_dataframe = input("""Which dataframe?
        1\tThe routes dataframe          
        2\tThe airports dataframe
        3\tThe merged dataframe 
        enter answer (1/2/3): """)
        
        if unique_dataframe == '1':
            inspect_unique_values(routes)
            
        elif unique_dataframe == '2':
            inspect_unique_values(airports)
            
        elif unique_dataframe == '3':
            inspect_unique_values(merged)
            
        else:
            print('\nSorry, this is not an option, we will return to the main program') 
            
    elif inspect_option == '3':
        extra_options = input("""What would you want to do?
        1\tShow in which countries most airports are located          
        2\tShow 10 biggest airports based on number of incoming flights
        3\tShow 10 biggest airports based on degree (most connected)
        4\tShow 10 biggest airlines
        enter answer (1/2/3/4): """)
        
        if extra_options == '1':
            print('\nThe 10 countries with most airports: \n')
            merged['airport country'].value_counts()[0:10].plot.pie()
            plt.show()
            
        elif extra_options == '2':
            print('\nThe 10 biggest airports based on number of incoming flights: \n')
            inspect_most_flights_airports(merged)
            
        elif extra_options == '3': 
            print('\nThe 10 biggest airports based on degree (most connected): \n')
            hub_table = setair.find_hubs_in_df(merged, 10)
            
            barplot_from_df(hub_table, x="airport" , y="degree", ylabel="flight routes")
            
        elif extra_options == '4':
            print('\nThe 10 biggest airlines: \n')
            df_table_airlines = setair.airline_table_name(merged)[:10]
            barplot_from_df(df_table_airlines, x="name airline" , y="flight_routes_nr" , ylabel="flight routes")
        else:
            print('\nSorry, this is not an option, we will return to the main program')
    else:
        print('\nSorry, this is not an option, we will return to the main program')
        
        
        

import pandas as pd
import os
# Ignore pandas warnings
pd.options.mode.chained_assignment = None

IMPORTANT_COLUMNS=["Name","Level","Cost gold-coin-icon","Build Time","Town hall Level Required",
                   "Research time","Available at",
                   "Cost dark-elixir-icon","Cost elixir-icon","Unlocks",
                   "Capacity dark-elixir-icon","Storage Capacity dark-elixir-icon",
                   "Production Rate elixir-icon","Capacity elixir-icon",
                   "Storage Capacity elixir-icon","Production Rate gold-coin-icon","Capacity gold-coin-icon",
                   "Storage Capacity gold-coin-icon"]

def clean_columns(df):
    df.drop(columns=[col for col in df.columns if col not in IMPORTANT_COLUMNS], inplace=True)
    return df

# def repeat_row(df, name, times, max_level):
#     print("name: "+name+" times: "+str(times)+" max_level: "+str(max_level))
#     resources = pd.read_csv("resources/"+name+".csv")
#     resources = clean_columns(resources)
    
#     return df
    
def read_dir(dir, townhall_level):
    print("------------------- TOWNHALL LEVEL: "+str(townhall_level)+" -------------------")
    # Read all files in directory
    files = os.listdir(dir)
    # Create a list of dataframes
    df_list = []
    # Loop through all files
    for file in files:
        file_name = file.split(".")[0]
        #print(file_name)
        if file_name == "Town_Hall":
            continue
        # Read the file
        df = pd.read_csv(dir+file)
        quantity = 1
        existe = False
        try:
            df2 = pd.read_csv("available/"+file)
            if townhall_level > 1:
                last_quantity = df2[" townhall townhall"+str(townhall_level-1)][0]
                #print("Last Quantity: "+str(last_quantity))
            df2 = df2[[" townhall townhall"+str(townhall_level)]]
            quantity = df2[" townhall townhall"+str(townhall_level)][0]
            #print("Current Quantity: "+str(quantity))
            if last_quantity == "-":
                last_quantity = 0
            if quantity == "-":
                quantity = 0
            difference = int(quantity) - int(last_quantity)
            existe = True
        except:
            pass
        # Remove all rows that are not the townhall level established in the column "Town hall Level Required" or "Available at"
        try:
            df.drop(df[df["Town hall Level Required"] != " townhall townhall"+str(townhall_level)].index, inplace=True)
        except:
            df.drop(df[df["Available at"] != " townhall townhall"+str(townhall_level)].index, inplace=True)
        
        # Cleaning columns with only IMPORTANT_COLUMNS
        try:
            df = clean_columns(df)
        except:
            print("Error cleaning columns")
        
        # Append the dataframe to the list
        df_list.append(df)
        # Add name filename column at the beginning of the dataframe
        df.insert(0, "Name", file_name)
        # Max level of the building
        # max_level = df["Level"].max()
        # print(file_name)
        # try:
        #     if existe:
        #         if difference > 0:
        #             print("difference: "+str(difference) + " max_level: "+str(max_level))
        #             df = repeat_row(df, file_name, difference, int(max_level))
        # except:
        #     pass
        # Add column quantity (quantity) to the dataframe
        df.insert(1, "Quantity", quantity)
        

    df = pd.concat(df_list)
    return df

if __name__ == "__main__":
    for townhall_level in range(1, 16):
        df = read_dir("resources/", townhall_level)
        df.to_csv("townhall/"+str(townhall_level)+".csv", index=False)
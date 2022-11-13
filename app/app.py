import pandas as pd
import os
# Read directory
def read_dir(dir, townhall_level):
    # Read all files in directory
    files = os.listdir(dir)
    # Create a list of dataframes
    df_list = []
    # Loop through all files
    for file in files:
        file_name = file.split(".")[0]
        # Read the file
        df = pd.read_csv(dir+file)
        # Remove all rows that are not the townhall level established in the column "Town hall Level Required" or "Available at"
        if file_name != "Town_Hall":
            try:
                df.drop(df[df["Town hall Level Required"] != " townhall townhall"+str(townhall_level)].index, inplace=True)
            except:
                df.drop(df[df["Available at"] != " townhall townhall"+str(townhall_level)].index, inplace=True)
        # Append the dataframe to the list
        df_list.append(df)
        # Add name filename column at the beginning of the dataframe
        df.insert(0, "Name", file_name)
        

    df = pd.concat(df_list)
    return df

if __name__ == "__main__":
    for townhall_level in range(1, 16):
        df = read_dir("resources/", townhall_level)
        df.to_csv("townhall/"+str(townhall_level)+".csv", index=False)
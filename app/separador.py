import pandas as pd
import os
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)


def remove_columns_that_contains(df, string):
    '''Remove all columns that contains a string'''
    columns = df.columns
    for column in columns:
        if string in column:
            df.drop(column, axis=1, inplace=True)

def rename_columns(df, old_name, new_name):
    '''Rename a column in a dataframe'''
    df.rename(columns={old_name: new_name}, inplace=True)


def rename_rows(df, old_name, new_name):
    '''Rename a row in a dataframe'''
    df.rename(index={old_name: new_name}, inplace=True)


def exist_column(df, column):
    '''Check if a column exists in a dataframe'''
    return column in df.columns


def get_cost(structure, nivel):
    # Read the file
    dir = "./resources/"
    if "#" in structure:
        structure = structure.split("#")[0]
    file = structure+".csv"
    df = pd.read_csv(dir+file, index_col=0)
    costo, tipo = 0, ""
    rename_rows(df, "gold-coin-icon", "")
    rename_rows(df, "elixir-icon", "")
    if exist_column(df, "Gold Cost"):
        costo = df["Gold Cost"][nivel]
        tipo = "Gold"
    elif exist_column(df, "Elixir Cost"):
        costo = df["Elixir Cost"][nivel]
        tipo = "Elixir"
    # Remove the text of "costo" if exists
    if " " in str(costo):
        costo = costo.split(" ")[0]
    return {"costo": costo, "tipo": tipo}

def get_time(structure, level):
    # Read the file
    dir = "./resources/"
    if "#" in structure:
        structure = structure.split("#")[0]
    file = structure+".csv"
    df = pd.read_csv(dir+file, index_col=0)
    time = df["Build Time"][level]
    return text_to_seconds(time)

def text_to_seconds(text):
    '''Convert a text to seconds'''
    seconds = 0
    possible_values = ["days", "day",
                       "hours", "hour",
                       "minutes", "minute",
                       "seconds", "second"]
    if text == "Instant" or type(text) == float:
        return 0
    for value in possible_values:
        if value in text:
            # Generate tuple of text (ej: 1 day 30 minutes = (1, day, 30, minutes))
            text = text.split(" ")
            if "days" in text or "day" in text:
                days = int(text[0])
                seconds += days * 24 * 60 * 60
                # Remove the first two elements
                text = text[2:]
            if "hours" in text or "hour" in text:
                hours = int(text[0])
                seconds += hours * 60 * 60
                # Remove the first two elements
                text = text[2:]
            if "minutes" in text or "minute" in text:
                minutes = int(text[0])
                seconds += minutes * 60
                # Remove the first two elements
                text = text[2:]
    return seconds

def availability(structure, townhall_level):
    # Read the file
    dir = "./available/"
    file = structure+".csv"
    df = pd.read_csv(dir+file)
    # Read columns and print the values of column that contains townhall_level
    columns = df.columns
    previous_column = ""
    for column in columns:
        if townhall_level > 1:
            if str(townhall_level) in column:
                if df[previous_column][0] == "-":
                    return {"previous": 0, "current": df[column][0]}
                return {"previous": df[previous_column][0], "current": df[column][0]}
        previous_column = column


def separador(townhall, output):
    # Read the file
    dir = "./townhall/"
    file = townhall+".csv"
    df = pd.read_csv(dir+file, index_col=False)
    df = df[df.Name != "Wall"]
    df_gold = pd.DataFrame()
    df_elixir = pd.DataFrame()
    time = pd.DataFrame()
    for index, dict in df.iterrows():
        name = dict["Name"]
        level = dict["Level"]
        data = get_cost(name, level)
        dict["Cost"] = data["costo"]
        dict["Build Time"] = text_to_seconds(dict["Build Time"])

        if data["tipo"] == "Gold":
            df_gold = df_gold.append(dict, ignore_index=True)
            remove_columns_that_contains(df_gold, "Town hall Level Required")
        elif data["tipo"] == "Elixir":
            df_elixir = df_elixir.append(dict, ignore_index=True)
            remove_columns_that_contains(df_elixir, "Town hall Level Required")
        else:
            print("Error: ", name, level)   

    # Obtain the max level of each structure
    max_level = {}
    for index, dict in df_gold.iterrows():
        if dict["Name"] in max_level:
            if dict["Level"] > max_level[dict["Name"]]:
                max_level[dict["Name"]] = dict["Level"]
        else:
            max_level[dict["Name"]] = dict["Level"]
    for index, dict in df_elixir.iterrows():
        if dict["Name"] in max_level:
            if dict["Level"] > max_level[dict["Name"]]:
                max_level[dict["Name"]] = dict["Level"]
        else:
            max_level[dict["Name"]] = dict["Level"]
    
    # Obtain the min level of each structure
    min_level = {}
    for index, dict in df_gold.iterrows():
        if dict["Name"] in min_level:
            if dict["Level"] < min_level[dict["Name"]]:
                min_level[dict["Name"]] = dict["Level"]
        else:
            min_level[dict["Name"]] = dict["Level"]
    for index, dict in df_elixir.iterrows():
        if dict["Name"] in min_level:
            if dict["Level"] < min_level[dict["Name"]]:
                min_level[dict["Name"]] = dict["Level"]
        else:
            min_level[dict["Name"]] = dict["Level"]

    quantity = {}
    for index, dict in df_gold.iterrows():
        quantity[dict["Name"]] = dict["Quantity"]
    for index, dict in df_elixir.iterrows():
        quantity[dict["Name"]] = dict["Quantity"]

    # Make "Name" the index
    df_gold.set_index("Name", inplace=True)
    df_elixir.set_index("Name", inplace=True)

    # Rotate the dataframe
    df_gold = df_gold.T
    df_elixir = df_elixir.T

    # Make a row from 1 to max level, if the row doesn't exist in the dataframe add a NaN
    max_possible_level = max(max_level.values())
    print(max_possible_level)
    # If max possible level is greater than quantity of rows, add empty rows
    if max_possible_level > len(df_gold):
        for i in range(len(df_gold), max_possible_level):
            df_gold.loc[i] = "None"
    if max_possible_level > len(df_elixir):
        for i in range(len(df_elixir), max_possible_level):
            df_elixir.loc[i] = "None"

    # Read all rows
    for index, dict in df_gold.iterrows():
        # Set row value to 0 if it's not "None"
        for key, value in dict.items():
            if value != "None":
                df_gold = df_gold.replace(value, "None")
    for index, dict in df_elixir.iterrows():
        # Set row value to 0 if it's not "None"
        for key, value in dict.items():
            if value != "None":
                df_elixir = df_elixir.replace(value, "None")

    # Add the column "Level"
    df_gold["Level"] = [i for i in range(1, max_possible_level+1)]
    df_elixir["Level"] = [i for i in range(1, max_possible_level+1)]

    # Put the column "Level" at the beginning of the dataframe
    cols_gold = df_gold.columns.tolist()
    cols_gold = cols_gold[-1:] + cols_gold[:-1]
    df_gold = df_gold[cols_gold]
    cols_elixir = df_elixir.columns.tolist()
    cols_elixir = cols_elixir[-1:] + cols_elixir[:-1]
    df_elixir = df_elixir[cols_elixir]

    # Reset the index
    df_gold.reset_index(drop=True, inplace=True)
    df_elixir.reset_index(drop=True, inplace=True)
    
    # Remove the repeated columns
    df_gold = df_gold.loc[:,~df_gold.columns.duplicated()]
    df_elixir = df_elixir.loc[:,~df_elixir.columns.duplicated()]

    # Add columns called structure+quantity, (ex: Cannon_0, Cannon_1, etc)
    for index, column in df_gold.iteritems():
        if index != "Level":
            for i in range(0, quantity[index]):
                df_gold[index+"#"+str(i)] = column
            # Remove the original column
            df_gold.drop(index, axis=1, inplace=True)

    # For each level, if the value is "None", replace it with the value of the cost of the structure
    for index, column in df_gold.iteritems():
        if index != "Level":
            for i in range(0, len(column)):
                current = index.split("#")[1] if "#" in index else 0
                if i+1 > max_level[index.split("#")[0]]:
                    break
                if column[i] == "None":
                    available = availability(index.split("#")[0], int(townhall))
                    min_current = min_level[index.split("#")[0]]
                    dif = available["current"]-available["previous"]
                    if dif == 0:
                        if i+1 >= min_current:
                            df_gold.at[i, index] = get_cost(index, i+1)["costo"]
                        else:
                            df_gold.at[i, index] = "None"
                    else:
                        for diferente in range(0, dif):
                            if current == str(diferente):
                                df_gold.at[i, index] = get_cost(index, i+1)["costo"]
                        for diferente in range(dif,available["current"] ):
                            if current == str(diferente):
                                if i+1 >= min_current:
                                    df_gold.at[i, index] = get_cost(index, i+1)["costo"]
                                else:
                                    df_gold.at[i, index] = "None"

    for index, column in df_elixir.iteritems():
        if index != "Level":
            for i in range(0, len(column)):
                current = index.split("#")[1] if "#" in index else 0
                if i+1 > max_level[index.split("#")[0]]:
                    break
                if column[i] == "None":
                    available = availability(index.split("#")[0], int(townhall))
                    min_current = min_level[index.split("#")[0]]
                    dif = available["current"]-available["previous"]
                    if dif == 0:
                        if i+1 >= min_current:
                            df_elixir.at[i, index] = get_cost(index, i+1)["costo"]
                        else:
                            df_elixir.at[i, index] = "None"
                    else:
                        for diferente in range(0, dif):
                            if current == str(diferente):
                                df_elixir.at[i, index] = get_cost(index, i+1)["costo"]
                        for diferente in range(dif,available["current"] ):
                            if current == str(diferente):
                                if i+1 >= min_current:
                                    df_elixir.at[i, index] = get_cost(index, i+1)["costo"]
                                else:
                                    df_elixir.at[i, index] = "None"

    df_time = pd.concat([df_gold, df_elixir], axis=1)
    df_time = df_time.loc[:,~df_time.columns.duplicated()]
    for index, column in df_time.iteritems():
        if index != "Level":
            for i in range(0, len(column)):
                if column[i] != "None":
                    tiempo = get_time(index, i+1)
                    df_time.at[i, index] = tiempo

    df_gold.to_csv(output+"/"+townhall+"_gold.csv", index=False)
    df_elixir.to_csv(output+"/"+townhall+"_elixir.csv", index=False)
    df_time.to_csv(output+"/"+townhall+"_time.csv", index=False)


def main():
    separador("1","test")


if __name__ == "__main__":
    main()

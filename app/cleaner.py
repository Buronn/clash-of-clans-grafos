import pandas as pd
import os


def remove_troops_and_spells(dir):
    '''Read all files and remove all troops and spells'''
    df_list = []
    for file in os.listdir(dir):
        file_name = file.split(".")[0]
        df = pd.read_csv(dir+file)
        df_list.append(df)
        # Read columns
        columns = df.columns
        # Remove all columns that contains "Research Cost"
        for column in columns:
            if "Research Cost" in column:
                a = input("Desea borrar el archivo "+file+"? (s/n)")
                if "s" in a:
                    os.remove(dir+file)
                    print("Archivo borrado")
                else:
                    print("Archivo no borrado")
                break


def clean_structures(dir):
    '''Read all files and clean the columns'''
    df_list = []
    for file in os.listdir(dir):
        file_name = file.split(".")[0]
        df = pd.read_csv(dir+file)
        df_list.append(df)
        # If column contains "gold-coin-icon" rename it to "gold"
        columns = df.columns
        for column in columns:
            if "gold-coin-icon" in column:
                rename_columns(df, "Cost gold-coin-icon", "Gold Cost")
                rename_columns(df, "Production Rate gold-coin-icon", "Gold Production Rate")
                rename_columns(df, "Capacity gold-coin-icon", "Gold Capacity")
                rename_columns(df, "Storage Capacity gold-coin-icon", "Gold Storage Capacity")
            # If column contains "elixir-icon" rename it to "elixir"
            if "elixir-icon" in column:
                rename_columns(df, "Cost elixir-icon", "Elixir Cost")
                rename_columns(df, "Production Rate elixir-icon", "Elixir Production Rate")
                rename_columns(df, "Capacity elixir-icon", "Elixir Capacity")
                rename_columns(df, "Storage Capacity elixir-icon", "Elixir Storage Capacity")
                rename_columns(df, "Load Cost elixir-icon", "Elixir Load Cost")
            # If column contains "dark-elixir-icon" rename it to "dark elixir"
            if "dark-elixir-icon" in column:
                rename_columns(df, "Cost dark-elixir-icon", "Dark Elixir Cost")
                rename_columns(df, "Production Rate dark-elixir-icon", "Dark Elixir Production Rate")
                rename_columns(df, "Capacity dark-elixir-icon", "Dark Elixir Capacity")
                rename_columns(df, "Storage Capacity dark-elixir-icon", "Dark Elixir Storage Capacity")
                rename_columns(df, "Load Cost dark-elixir-icon", "Dark Elixir Load Cost")

            if "Re-Arm" in column:
                remove_columns_that_contains(df, "Re-Arm")
            
            if "Hitpoints" in column:
                remove_columns_that_contains(df, "Hitpoints")

            if "Damage" in column:
                remove_columns_that_contains(df, "Damage")

            if "Push Strength" in column:
                remove_columns_that_contains(df, "Push Strength")

            if "Dark Elixir" in column:
                remove_columns_that_contains(df, "Dark Elixir")

            if "Unit Queue Length" in column:
                remove_columns_that_contains(df, "Unit Queue Length")

            if "Spawned Units" in column:
                remove_columns_that_contains(df, "Spawned Units")

            if "Troop Capacity" in column:
                remove_columns_that_contains(df, "Troop Capacity")

            if "Unlocks" in column:
                remove_columns_that_contains(df, "Unlocks")

        # Rewrite the file
        df.to_csv(dir+file, index=False)
            
def remove_columns_that_contains(df, string):
    '''Remove all columns that contains a string'''
    columns = df.columns
    for column in columns:
        if string in column:
            df.drop(column, axis=1, inplace=True)


def rename_columns(df, old_name, new_name):
    '''Rename a column in a dataframe'''
    df.rename(columns={old_name: new_name}, inplace=True)


def main():
    # Clean structures
    clean_structures("resources/")

if __name__ == "__main__":
    main()

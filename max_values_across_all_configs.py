import pandas as pd, glob


file_paths = glob.glob("<name_of_file_path>/*.csv")
dfs = [pd.read_csv(file) for file in file_paths]

combined_df = pd.concat(dfs)
combined_df = combined_df.sort_values(by="X_Values")

# find max values per each unique value of MHz
max_values = combined_df.groupby("X_Values")["Y_Values"].max().reset_index()

# export to csv
max_values.to_csv("max_values.csv", index=False)
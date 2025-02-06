import pandas as pd

def get_nutrition_df(food_df, folder_path, file_name ='fped_1720.csv'):
    """
    Returns a dataframe with added nutritional information for each row of food data.
    """
    # sum on sequence number to create unique sequence number

    # Group by 'sequence_number' and sum the values for each groug before
    # Merging data
    # obtain and merge FPED
    fped_df = pd.read_csv(folder_path + file_name)

    fped_df = fped_df.rename(columns={'FOODCODE': 'food_code'})

    fped_df[fped_df.columns[2:]] = fped_df[fped_df.columns[2:]].apply(pd.to_numeric)

    # merge food bank data and nutrition data
    nutrition_df_ = pd.merge(fped_df, food_df,  on='food_code')
    nutrition_df_ = nutrition_df_[nutrition_df_.columns[2:]] # After merging remove the food_code and description
    # get columns from the dfs to reoder ad put sequence_number in the beginning 
    food_df_columns = food_df.columns.to_list()
    food_df_columns.pop(1)
    
    nutrition_df_ = nutrition_df_.loc[:,food_df_columns + fped_df.columns.to_list()[2:] ] # Reoder the columns to have sequence_number as 1st columns
    nutrition_df = nutrition_df_.groupby('sequence_number', as_index=False).sum() # aggregate nutrients using sequence number

    # nutrition_df[nutrition_df.columns[2:]]  = nutrition_df[nutrition_df.columns[2:]].apply(pd.to_numeric,  axis=1)
    # renaming columns
    nutrition_df = nutrition_df.rename(columns={'F_TOTAL (cup eq)': 'total_fruits_cup',
                                                'G_WHOLE (oz eq)': 'whole_grains_oz',
                                                'G_REFINED (oz eq)': 'refined_grains_oz',
                                                'D_TOTAL (cup eq)': 'dairy_cup',
                                                'ADD_SUGARS (tsp eq)': 'added_sugars_tsp'
                                                })

    # calculate HEI component columns
   
    nutrition_df['whole_fruits_cup'] = nutrition_df['F_OTHER (cup eq)'] + nutrition_df['F_CITMLB (cup eq)']
    nutrition_df['total_vegetables_cup'] = nutrition_df['V_TOTAL (cup eq)'] + nutrition_df['V_LEGUMES (cup eq)']
    nutrition_df['greens_and_beans_cup'] = nutrition_df['V_DRKGR (cup eq)'] + nutrition_df['V_LEGUMES (cup eq)']
   
    nutrition_df['total_protein_foods_oz'] = (nutrition_df['PF_MPS_TOTAL (oz eq)'] +
                                              nutrition_df['PF_EGGS (oz eq)']	+
                                              nutrition_df['PF_SOY (oz eq)']	+
                                              nutrition_df['PF_NUTSDS (oz eq)'] +
                                              nutrition_df['PF_LEGUMES (oz eq)'])
    
    nutrition_df['seafood_and_plant_proteins_oz'] = (nutrition_df['PF_SEAFD_HI (oz eq)'] +
                                                     nutrition_df['PF_SEAFD_LOW (oz eq)'] +
                                                     nutrition_df['PF_SOY (oz eq)'] +
                                                     nutrition_df['PF_NUTSDS (oz eq)'] +
                                                     nutrition_df['PF_LEGUMES (oz eq)'])
    
    nutrition_df['sodium_g'] = nutrition_df['sodium_mg'] / 1000 # Convert to grams


    return nutrition_df
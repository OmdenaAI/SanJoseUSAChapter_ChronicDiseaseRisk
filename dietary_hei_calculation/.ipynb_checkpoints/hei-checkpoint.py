import pandas as pd
import numpy as np


hei_categories = ['total_fruits',
                  'whole_fruits',
                  'total_vegetables',
                  'greens_and_beans',
                  'whole_grains',
                  'dairy',
                  'total_protein_foods',
                  'seafood_and_plant_proteins',
                  'fatty_acids',
                  'refined_grains',
                  'added_sugars',
                  'sodium',
                  'saturated_fats']

def get_hei_df(df):
    """Returns a dataframe with columns for overall and component HEI scores."""

    # calculate HEI density ratios to be used in scoring
    # these categories have a density ratio per 1000 kcal.
    df['total_fruits'] = df['total_fruits_cup'] / (df['energy_kcal'] / 1000)
    df['whole_fruits'] = df['whole_fruits_cup'] / (df['energy_kcal'] / 1000)
    df['total_vegetables'] = df['total_vegetables_cup'] / (df['energy_kcal'] / 1000)
    df['greens_and_beans'] = df['greens_and_beans_cup'] / (df['energy_kcal'] / 1000)
    df['whole_grains'] = df['whole_grains_oz'] / (df['energy_kcal'] / 1000)
    df['dairy'] = df['dairy_cup'] / (df['energy_kcal'] / 1000)
    df['total_protein_foods'] = df['total_protein_foods_oz'] / (df['energy_kcal'] / 1000)
    df['seafood_and_plant_proteins'] = df['seafood_and_plant_proteins_oz'] / (df['energy_kcal'] / 1000)
    df['refined_grains'] = df['refined_grains_oz'] / (1000 * df['energy_kcal'])
    df['sodium'] = df['sodium_g'] / (1000 * df['energy_kcal'])
    # these categories have a density ratio based on percentage of energy
    df['added_sugars'] = (df['added_sugars_tsp'] * 16) / (df['energy_kcal'])
    df['saturated_fats'] = (df['saturated_fats_g'] * 9) / (df['energy_kcal'])
    # this category has a density ratio based on various fatty acid types
    df['fatty_acids'] = (df['monounsaturated_fats_g'] + df['polyunsaturated_fats_g']) / df['saturated_fats_g']

    # convert HEI density ratios to HEI scores
    # these scores all have a minimum of 0, and a higher score is more desirable
    df['total_fruits'] = (df['total_fruits'] / 0.8) * 5
    df['whole_fruits'] = (df['whole_fruits'] / 0.4) * 5
    df['total_vegetables'] = (df['total_vegetables'] / 1.1) * 5
    df['greens_and_beans'] = (df['greens_and_beans'] / 0.2) * 5
    df['whole_grains'] = (df['whole_grains'] / 1.5) * 10
    df['dairy'] = (df['dairy'] / 1.3) * 10
    df['total_protein_foods'] = (df['total_protein_foods'] / 2.5) * 5
    df['seafood_and_plant_proteins'] = (df['seafood_and_plant_proteins'] / 0.8) * 5
    
    # these scores have nonzero minimums, and a lower score is more desirable
    df['refined_grains'] = ((4.3 - df['refined_grains']) / 2.5) * 10
    df['added_sugars'] = ((26 - df['added_sugars']) / 9.5) * 10
    df['sodium'] = ((2 - df['sodium']) / 0.9) * 10
    df['saturated_fats'] = ((16 - df['saturated_fats']) / 8) * 10
    # this score has a nonzero minimum, and a higher score is more desirable
    df['fatty_acids'] = ((df['fatty_acids'] - 1.2) / 1.3) * 10

    # round down if HEI category score is more than maximum allowed
    df.loc[df['total_fruits'] > 5, 'total_fruits'] = 5
    df.loc[df['whole_fruits'] > 5, 'whole_fruits'] = 5
    df.loc[df['total_vegetables'] > 5, 'total_vegetables'] = 5
    df.loc[df['greens_and_beans'] > 5, 'greens_and_beans'] = 5
    df.loc[df['whole_grains'] > 10, 'whole_grains'] = 10
    df.loc[df['dairy'] > 10, 'dairy'] = 10
    df.loc[df['total_protein_foods'] > 5, 'total_protein_foods'] = 5
    df.loc[df['seafood_and_plant_proteins'] > 5, 'seafood_and_plant_proteins'] = 5
    df.loc[df['refined_grains'] > 10, 'refined_grains'] = 10
    df.loc[df['added_sugars'] > 10, 'added_sugars'] = 10
    df.loc[df['sodium'] > 10, 'sodium'] = 10
    df.loc[df['saturated_fats'] > 10, 'saturated_fats'] = 10
    df.loc[df['fatty_acids'] > 10, 'fatty_acids'] = 10

    # round up if HEI category score is less than minimum
    df.loc[df['total_fruits'] < 0, 'total_fruits'] = 0
    df.loc[df['whole_fruits'] < 0, 'whole_fruits'] = 0
    df.loc[df['total_vegetables'] < 0, 'total_vegetables'] = 0
    df.loc[df['greens_and_beans'] < 0, 'greens_and_beans'] = 0
    df.loc[df['whole_grains'] < 0, 'whole_grains'] = 0
    df.loc[df['dairy'] < 0, 'dairy'] = 0
    df.loc[df['total_protein_foods'] < 0, 'total_protein_foods'] = 0
    df.loc[df['seafood_and_plant_proteins'] < 0, 'seafood_and_plant_proteins'] = 0
    df.loc[df['refined_grains'] < 0, 'refined_grains'] = 0
    df.loc[df['added_sugars'] < 0, 'added_sugars'] = 0
    df.loc[df['sodium'] < 0, 'sodium'] = 0
    df.loc[df['saturated_fats'] < 0, 'saturated_fats'] = 0
    df.loc[df['fatty_acids'] < 0, 'fatty_acids'] = 0

    # sum all HEI category scores to calculate total HEI score
    df['hei_score'] = df[hei_categories].sum(axis=1)

    return df

import os
from utils.url_cleaning import shorten_url
from utils.lists_dictionaries import group_mapping, correct_spelling_colors, correct_spelling_scents, remove_words
from utils.helper_functions import set_display_options, map_color_to_family, extract_unique
from utils.gender_analysis_functions import extrapolate_gender, recalculate_counters, create_combined_counts, \
    plot_gender_distribution, calculate_counts, prepare_summary_table

import pandas as pd

set_display_options()


# Load the data, drop anything that doesn't have a URL
dpath = '../RandomThings/data_imports/Assignment 2 Data'
cleaned_combined_data = pd.read_csv('../RandomThings/data_imports/combined_data.csv')

cleaned_combined_data = cleaned_combined_data.dropna(subset=['URL'])
cleaned_combined_data['Gender*Sex'] = cleaned_combined_data['Gender*Sex'].replace('Any', '')
combined_data = cleaned_combined_data.copy()


# fix URL screw up and shorten what can be shortened
combined_data['URL'] = combined_data['URL'].str.replace(',', '/').str.replace(' ', '')
combined_data['URL'] = combined_data['URL'].apply(shorten_url)


# regroup product families
group_data = []

for filename in os.listdir(dpath):
    if filename.endswith('.csv'):
        group_number = filename.split()[0]

        file_path = os.path.join(dpath, filename)
        data = pd.read_csv(file_path)

        if 'Link to image of product' in data.columns:
            data.rename(columns={'Link to image of product': 'URL'}, inplace=True)

        data['Group'] = group_number

        group_data.append(data)

group_data_df = pd.concat(group_data)
filtered_combined_data = combined_data[combined_data['URL'].isin(group_data_df['URL'])]
result = pd.merge(filtered_combined_data, group_data_df[['URL', 'Group']], on='URL', how='inner')
result['Group'] = result['Group'].map(group_mapping)

# grouped_results = pd.read_csv('path/to/where/you/saved/the/file/named/grouped_results.csv')
# result = grouped_results.copy()

result = result[result['Group'].isin(['hair care', 'deodorants'])]

# print(result['Group'].unique())


# clean up formatting
result['Colors'] = result['Colors'].str.replace('.', '', regex=False)
result['Colors'] = result['Colors'].str.strip().str.lower()


# Remove unwanted words, correct spelling, separate color strings to independent strings,
# check for color family problems
for word in remove_words:
    result['Colors'] = result['Colors'].str.replace(word, '', regex=False)

for wrong, right in correct_spelling_colors.items():
    result['Colors'] = result['Colors'].str.replace(wrong, right, regex=False)

result['Colors'] = result['Colors'].apply(
    lambda x: ', '.join([color.strip().lower() for color in x.split(',')]) if pd.notna(x) else x)

result['Colors'] = result['Colors'].apply(lambda x: ','.join(color.strip() for color in x.split(',')))

unique_colors = extract_unique(result, 'Colors')
result['Family'] = result['Colors'].apply(map_color_to_family)
unknown_families = result[result['Family'].str.contains('Unknown')]


# repeat cleaning process for scents and get unique results
result['Scent'] = result['Scent'].str.replace('.', '', regex=False)
result['Scent'] = result['Scent'].str.strip().str.lower()

for wrong, right in correct_spelling_scents.items():
    result['Scent'] = result['Scent'].str.replace(wrong, right, regex=False)

unique_scents = extract_unique(result, 'Scent')


# Filter records with specified gender*sex to build data subset for analysis
filtered_result = result[result['Gender*Sex'].isin(['Male', 'Female'])]


# Initialize counters for color & scent distribution for records with specified gender*sex in order to build a model
male_colors_counter, female_colors_counter, _, _, male_scents_counter, female_scents_counter = recalculate_counters(
    result)

print("Initial Male Colors Counter:\n", male_colors_counter)
print("Initial Female Colors Counter:\n", female_colors_counter)
print("Initial Male Scents Counter:\n", male_scents_counter)
print("Initial Female Scents Counter:\n", female_scents_counter)


# Use the color & scent distributions for known gender*sex to extrapolate gender*sex on unspecified records,
# then recalculate the color & scent distribution and make dataframes for analysis and visualization
extrapolate_gender(result, male_colors_counter, female_colors_counter, male_scents_counter, female_scents_counter)

result.loc[~result['Gender*Sex'].isin(['Male', 'Female']), 'Gender*Sex'] = result['Extrapolated Gender']

# print(result[['Gender*Sex', 'Extrapolated Gender']].head())

male_colors_counter, female_colors_counter, male_families_counter, female_families_counter, male_scents_counter, female_scents_counter = recalculate_counters(
    result)

combined_color_counts = create_combined_counts(male_colors_counter, female_colors_counter, 'Color')
combined_family_counts = create_combined_counts(male_families_counter, female_families_counter, 'Family')
combined_scent_counts = create_combined_counts(male_scents_counter, female_scents_counter, 'Scent')


# Summarize the findings in tables
total_records_before = cleaned_combined_data.shape[0]
total_records_after = result.shape[0]

color_counts_before = calculate_counts(cleaned_combined_data, 'Gender*Sex', 'Colors')
scent_counts_before = calculate_counts(cleaned_combined_data, 'Gender*Sex', 'Scent')
color_counts_after = calculate_counts(result, 'Gender*Sex', 'Colors')
scent_counts_after = calculate_counts(result, 'Gender*Sex', 'Scent')

color_counts_before = color_counts_before.loc[(color_counts_before != 0).any(axis=1)]
scent_counts_before = scent_counts_before.loc[(scent_counts_before != 0).any(axis=1)]
color_counts_after = color_counts_after.loc[(color_counts_after != 0).any(axis=1)]
scent_counts_after = scent_counts_after.loc[(scent_counts_after != 0).any(axis=1)]

summary_colors = pd.concat([color_counts_before, color_counts_after], axis=1, keys=['Before', 'After']).fillna(0).astype(int)
summary_scents = pd.concat([scent_counts_before, scent_counts_after], axis=1, keys=['Before', 'After']).fillna(0).astype(int)

# print("Summary Colors:\n", summary_colors)
# print("\nSummary Scents:\n", summary_scents)


# Visualize the results
plot_gender_distribution(combined_color_counts, 'Distribution of Colors by Gender', 'Color')
plot_gender_distribution(combined_family_counts, 'Distribution of Families by Gender', 'Family')
plot_gender_distribution(combined_scent_counts, 'Distribution of Scents by Gender', 'Scent')


# Export to file
result.to_csv('../RandomThings/data_exports/final_gender_sex_data.csv', index=False)
summary_colors.to_csv('../RandomThings/data_exports/summary_colors.csv')
summary_scents.to_csv('../RandomThings/data_exports/summary_scents.csv')

from collections import Counter
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def extrapolate_gender(df: pd.DataFrame, male_colors_counter: Counter, female_colors_counter: Counter,
                       male_scents_counter: Counter, female_scents_counter: Counter) -> None:
    unknown_gender_result = df[~df['Gender*Sex'].isin(['Male', 'Female'])].copy()

    def extrapolate(row):
        color_items = row['Colors'].split(',')
        scent_items = row['Scent'].split(',') if pd.notna(row['Scent']) else []

        color_items = [color.strip().lower() for color in color_items]
        scent_items = [scent.strip().lower() for scent in scent_items]

        male_score = sum([male_colors_counter.get(color, 0) for color in color_items]) + sum(
            [male_scents_counter.get(scent, 0) for scent in scent_items])
        female_score = sum([female_colors_counter.get(color, 0) for color in color_items]) + sum(
            [female_scents_counter.get(scent, 0) for scent in scent_items])

        return 'Male' if male_score > female_score else 'Female'

    unknown_gender_result['Extrapolated Gender'] = unknown_gender_result.apply(extrapolate, axis=1)

    df.loc[~df['Gender*Sex'].isin(['Male', 'Female']), 'Extrapolated Gender'] = unknown_gender_result[
        'Extrapolated Gender']
    df.loc[~df['Gender*Sex'].isin(['Male', 'Female']), 'Gender*Sex'] = df['Extrapolated Gender']


def recalculate_counters(df: pd.DataFrame) -> tuple:
    filtered_result = df[df['Gender*Sex'].isin(['Male', 'Female'])]

    male_colors_counter = Counter()
    female_colors_counter = Counter()
    male_families_counter = Counter()
    female_families_counter = Counter()
    male_scents_counter = Counter()
    female_scents_counter = Counter()

    for _, row in filtered_result.iterrows():
        color_items = row['Colors'].split(',')
        family_items = row['Family'].split(',')
        scent_items = row['Scent'].split(',') if pd.notna(row['Scent']) else []

        color_items = [color.strip().lower() for color in color_items]
        family_items = [family.strip().lower() for family in family_items]
        scent_items = [scent.strip().lower() for scent in scent_items]

        if row['Gender*Sex'] == 'Male':
            male_colors_counter.update(color_items)
            male_families_counter.update(family_items)
            male_scents_counter.update(scent_items)
        elif row['Gender*Sex'] == 'Female':
            female_colors_counter.update(color_items)
            female_families_counter.update(family_items)
            female_scents_counter.update(scent_items)

    return male_colors_counter, female_colors_counter, male_families_counter, female_families_counter, male_scents_counter, female_scents_counter


def create_combined_counts(male_counter: Counter, female_counter: Counter, col_name: str) -> pd.DataFrame:
    male_counts = pd.DataFrame(male_counter.items(), columns=[col_name, 'Male']).sort_values(by='Male', ascending=False)
    female_counts = pd.DataFrame(female_counter.items(), columns=[col_name, 'Female']).sort_values(by='Female',
                                                                                                   ascending=False)

    combined_counts = pd.merge(male_counts, female_counts, on=col_name, how='outer').fillna(0)
    combined_counts['Male'] = combined_counts['Male'].astype(int)
    combined_counts['Female'] = combined_counts['Female'].astype(int)
    combined_counts = combined_counts.sort_values(by=['Male', 'Female'], ascending=False)
    return combined_counts


# Set plot style
sns.set(style="whitegrid")


def filter_counts(combined_counts: pd.DataFrame) -> pd.DataFrame:
    # Filter out rows where both Male and Female counts are less than 2
    filtered = combined_counts[(combined_counts['Male'] >= 2) | (combined_counts['Female'] >= 2)]
    return filtered


def plot_gender_distribution(combined_counts: pd.DataFrame, title: str, col_name: str):
    combined_counts = filter_counts(combined_counts)
    print(f"Filtered {col_name} Counts:\n", combined_counts)  # Debugging line

    plt.figure(figsize=(14, 8))
    bar_width = 0.35
    indices = range(len(combined_counts))

    plt.bar(indices, combined_counts['Male'], bar_width, label='Male', color='#65cee0')
    plt.bar([i + bar_width for i in indices], combined_counts['Female'], bar_width, label='Female', color='#a4c639')

    plt.title(title)
    plt.xlabel(col_name)
    plt.ylabel('Count')
    plt.xticks([i + bar_width / 2 for i in indices], combined_counts[col_name], rotation=90)
    plt.legend(title="gender*sex", loc="upper right")
    plt.show()


def calculate_counts(df: pd.DataFrame, group_col: str, count_col: str) -> pd.DataFrame:
    return (df.groupby(group_col)[count_col]
            .apply(lambda x: x.str.split(',').explode().value_counts())
            .unstack(fill_value=0)
            .astype(int))


def sum_counts(df: pd.DataFrame) -> int:
    return df.sum().sum()


def prepare_summary_table(counts: pd.DataFrame, label: str) -> pd.DataFrame:
    summary = counts.T
    summary['Data total'] = summary.sum(axis=1)
    summary = summary.loc[:, (summary != 0).any(axis=0)]
    summary.index.name = label
    return summary


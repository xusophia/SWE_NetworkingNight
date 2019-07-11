# Analyze the data created
# Analysis of results

import pandas as pd
from matplotlib import pyplot as plt
from NetworkingNight import Merge
from pprint import pprint
def analyze_preferences(preference_dessert_dict, preference_entree_dict):
    # Analyze the preference number people got
    analysis = Merge(preference_entree_dict,preference_dessert_dict)
    analysis_df = pd.DataFrame(analysis)
    analysis_df.hist(column = ['Dessert Preference', 'Entree Preference'])
    plt.savefig('preferences.png')

def analyze_major_dist(assignments_df, results_df):

    # Analyze the distribution of majors
    assignments_df[['Major:']].apply(pd.value_counts).plot(kind = 'bar')
    plt.yticks(fontsize = 10)
    plt.xticks(fontsize=4, rotation = 35)
    plt.title('Successful Assignments: Major Distribution')
    plt.savefig('Major_Distribution.png', dpi = 1000)
    results_df[['Major:']].apply(pd.value_counts).plot(kind = 'bar')
    plt.xticks(fontsize = 6)
    plt.title('ALL: Major Distribution')
    plt.gcf().subplots_adjust(bottom = 0.35)
    plt.savefig('Major_Distribution_ALL.png', dpi = 1000)
    # Analyze the distribution of years
    assignments_df[['Year:']].apply(pd.value_counts).plot(kind='bar')
    pprint(assignments_df[['Year:']].apply(pd.value_counts))
    pprint(results_df[['Year:']].apply(pd.value_counts))
    plt.xticks(fontsize = 9, rotation = 25)
    plt.title('Successful Assignments: Year Distribution')
    plt.savefig('Year_Distribution.png', dpi = 1000)
    #Need to analyze the distribution of years of the succesful assignments vs total
    results_df[['Year:']].apply(pd.value_counts).plot(kind = 'bar')
    plt.xticks(fontsize = 6, rotation = 45)
    plt.title('All: Year Distribution')
    plt.savefig('Year_Distribution_ALL.png', dpi = 1000)

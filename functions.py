import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# set default parameters for graphs
sns.set_style('darkgrid')
plt.rcParams['font.size'] = 12

def format_population_data(pop):
    '''
    Take the population dataset and reformat it to match the production dataset.
    This includes creating columns for each year from 1961 to 2013, will observations
    being the unique country names. Years 2013 to 108 will be dropped in this function.
    
    Rows with missing years will be filled with NaN values to match production dataset.
    This function returns a new dataframe.
    '''
    years = np.arange(1961,2014) # 1961 - 2013
    countries = pop.Area.unique() # Alphabetical list of each country name
    pop_df = pd.DataFrame() # Create new dataframe
    
    pop_df['Area'] = countries # set countries as first column
    pop_df.loc[:, 'Unit'] = '1000 persons' # set unit as second column

    for year in years: # Iterate through each year
        pop_vals = []
        for country in countries: # Iterate through each country
            if ((pop.Area == country) & (pop.Year == year)).any(): # See if the country and year combination exists
                yearly_pop = pop[(pop.Area == country) & (pop.Year == year)]['Value'].values[0]
            else: # If combination doesn't exist, set to NaN (matches production format)
                yearly_pop = float('NaN')
            pop_vals.append(yearly_pop) # Add 245 values to column

        col_name = 'Y'+ str(year) #  Create column name to match production dataset
        pop_df[col_name] = pop_vals # Create new column in our dataframe
    
    return pop_df



def plot_top_20_countries(data):
    '''
    Create a barplot of the top 20 producing countries over the last 50 years. 
    '''
    prod_by_country = {}
    for country in data.Area.unique(): # create dictionary with country and total production (all food items)
        prod_by_country[country] = data[data.Area == country]['TotalProd'].values.sum()
    
    prod_df = pd.DataFrame(list(prod_by_country.items()), columns=['Country', 'Production'])
    sorted_prod = prod_df.sort_values(by='Production', ascending=False).iloc[:20, :] # top 20 rows
    
    plt.figure(figsize=(12,8))
    sns.barplot(x='Production', y='Country', data=sorted_prod)
    plt.title('Top 20 Producing Countries')
    plt.xlabel('Production (in 1000 tonnes)')
    plt.show();
    
    prod_df = None # clear temporary dataframe
    sorted_prod = None # clear temporary dataframe
    return None



def plot_yearly_prod(data):
    '''
    Plot the top 3 countries production trend over the last 50 years. The country
    names are hard coded into the function and will need to be changed if needed.
    '''
    top_3 = ['China, mainland', 'United States of America', 'India']

    top_3_df = pd.DataFrame()
    top_3_df['Index'] = data.columns[5:-1].values

    for country in top_3:
        top_3_df[country] = data[data.Area == country].iloc[:, 5:-1].sum(axis=0).values

    top_3_df.set_index('Index', inplace=True)
    top_3_df = top_3_df.T  
    
    colors = ['red', 'orange', 'green']
    plt.figure(figsize=(16,8))
    x = np.arange(1,54)
    for i in range(3):
        sns.lineplot(x=top_3_df.columns.values, y=top_3_df.values[i], color=colors[i])
    plt.legend(top_3_df.index.values)
    plt.xticks(rotation='vertical')
    plt.title('Top 3 Producing Countries from 1961 to 2013')
    plt.ylabel('Production (in 1000 tonnes)')
    plt.show();
    
    return None



def top_20_feed_food(feed, food):   
    '''
    Create two plots, showing the top 20 produced food items for both human
    and livestock consumption.
    '''
    top_feed_prod = {}
    top_food_prod = {}

    for item in feed.Item.unique(): # Iterate through feed items
        top_feed_prod[item] = feed[feed.Item == item]['TotalProd'].sum()

    for item in food.Item.unique(): # Iterate through food items
        top_food_prod[item] = food[food.Item == item]['TotalProd'].sum()

    # Create feed dataframe, sort by descending, and select the top 20 rows
    feed_df = pd.DataFrame(list(top_feed_prod.items()), columns=['Item', 'Production'])
    feed_sorted = feed_df.sort_values(by='Production', ascending=False).iloc[:20, :] # top 20 rows

    # Create food dataframe, sort by descending, and select the top 20 rows
    food_df = pd.DataFrame(list(top_food_prod.items()), columns=['Item', 'Production'])
    food_sorted = food_df.sort_values(by='Production', ascending=False).iloc[:20, :] # top 20 rows

    # Plot both figures as subplots to compare
    plt.figure(figsize=(15,6))
    ax1 = plt.subplot(1,2,1)
    ax1.title.set_text('Top 20 Feed (Livestock) Products')
    sns.barplot(x='Production', y='Item', data=feed_sorted)
    plt.xlabel('Production (in 1000 tonnes)')
    plt.ylabel(' ') # remove y label

    ax2 = plt.subplot(1,2,2)
    ax2.title.set_text('Top 20 Food (Human) Products')
    sns.barplot(x='Production', y='Item', data=food_sorted)
    plt.xlabel('Production (in 1000 tonnes)')
    plt.ylabel(' ') # remove y label

    plt.tight_layout()

    # Clear dataframes for memory purposes (not sure if necessary but good for practice)
    feed_df = food_df = feed_sorted = food_sorted = None
    
    return None








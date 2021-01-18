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
    # Get top 20 producing countries    
    prod_df = pd.DataFrame(data.groupby('Area')['TotalProd'].agg('sum').sort_values(ascending=False))[:20]
    
    plt.figure(figsize=(12,8))
    sns.barplot(x=prod_df.TotalProd, y=prod_df.index)
    plt.title('Top 20 Producing Countries')
    plt.xlabel('Production (in 1000 tonnes)')
    plt.show();
    
    prod_df = None # clear temporary dataframes
    return None



def plot_yearly_prod(data):
    '''
    Plot the top 10 countries production trends over the last 50 years.
    '''
    top_10 = data.groupby('Area')['TotalProd'].agg('sum').sort_values(ascending=False).index[:10].values

    top_10_df = pd.DataFrame()
    top_10_df['Index'] = data.columns[5:-1].values

    for country in top_10:
        top_10_df[country] = data[data.Area == country].iloc[:, 5:-1].sum(axis=0).values

    top_10_df.set_index('Index', inplace=True)
    top_10_df = top_10_df.T  
    
    plt.figure(figsize=(16,8))
    x = np.arange(1,54)
    for i in range(10):
        sns.lineplot(x=top_10_df.columns.values, y=top_10_df.values[i], color=sns.color_palette("hls", 10)[i])
    plt.legend(top_10_df.index.values)
    plt.xticks(rotation='vertical')
    plt.title('Top 10 Producing Countries from 1961 to 2013')
    plt.ylabel('Production (in 1000 tonnes)')
    plt.show();
    
    top_10_df = None # clear temporary dataframe
    
    return None



def plot_top_20_food(data):
    '''
    Create a barplot of the top 20 produced items over the last 50 years.
    '''
    # Get top 20 products by quantity produced    
    prod_df = pd.DataFrame(data.groupby('Item')['TotalProd'].agg('sum').sort_values(ascending=False))[:20]
    
    # Get top 20 products by counts
    count_df = pd.DataFrame(data.groupby("Item")["Element"].agg("count").sort_values(ascending=False))[:20]
    
    # Plot both figures
    plt.figure(figsize=(12,10))
    ax1 = plt.subplot(2,1,1)
    sns.barplot(x=prod_df.TotalProd, y=prod_df.index)
    ax1.title.set_text('Top 20 Produced Items (by total quantity)')
    plt.xlabel('Production (in 1000 tonnes)')
    plt.ylabel(' ')
    
    ax2 = plt.subplot(2,1,2)
    sns.barplot(x=count_df.Element, y=count_df.index)
    ax2.title.set_text('Top 20 Produced Items (by occurance)')
    plt.xlabel('Occurance in Data')
    plt.ylabel(' ')
    
    plt.tight_layout()
    plt.show();
    
    prod_df = count_df = None # clear temporary dataframes
    return None



def top_20_feed_food(feed, food):   
    '''
    Create two plots, showing the top 20 produced food items for both human
    and livestock consumption.
    '''
    # Create feed dataframe, sort by descending, and select the top 20 rows
    feed_df = pd.DataFrame(feed.groupby('Item')['TotalProd'].agg('sum').sort_values(ascending=False))[:20]

    # Create food dataframe, sort by descending, and select the top 20 rows
    food_df = pd.DataFrame(food.groupby('Item')['TotalProd'].agg('sum').sort_values(ascending=False))[:20]

    # Plot both figures as subplots to compare
    plt.figure(figsize=(12,10))
    ax1 = plt.subplot(2,1,1)
    ax1.title.set_text('Top 20 Feed (Livestock) Products')
    sns.barplot(x=feed_df.TotalProd, y=feed_df.index)
    plt.xlabel('Production (in 1000 tonnes)')
    plt.ylabel(' ') # remove y label

    ax2 = plt.subplot(2,1,2)
    ax2.title.set_text('Top 20 Food (Human) Products')
    sns.barplot(x=food_df.TotalProd, y=food_df.index)
    plt.xlabel('Production (in 1000 tonnes)')
    plt.ylabel(' ') # remove y label

    plt.tight_layout()

    # Clear dataframes for memory purposes (not sure if necessary but good for practice)
    feed_df = food_df = None
    
    return None








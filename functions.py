import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def format_population_data(pop, name='pop_formatted.csv'):
    '''
    Take the population dataset and reformat it to match the production dataset.
    This includes creating columns for each year from 1961 to 2013, with observations
    being the unique country names. Years 2013 to 2018 will be dropped in this function.
    
    Rows with missing years will be filled with NaN values to match production dataset.
    This function saves a new dataframe to the current directory as a given name.
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
    
    # Drop China since it is broken down into subareas
    idx = pop_df.index[pop_df.Area == 'China'].values[0]
    pop_df.drop(44, axis=0, inplace=True)
    
    pop_df.to_csv(name, index=False)
    pop_df = None # clear temp memory
    
    return None



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



def plot_yearly_country(data):
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



def top_10_producers(data):
    '''
    Plot the top 10 producers for the top 10 products for a given dataset.
    '''
    # Get the top 4 product names from the dataset
    products = pd.DataFrame(data.groupby('Item')['TotalProd'].agg('sum').sort_values(ascending=False))[:4].index.values
    
    for product in products:
        df = None # clear previous dataframe
        df = pd.DataFrame(data[data.Item == product].groupby('Area')
                          ['TotalProd'].agg('sum').sort_values(ascending=False))[:10].T
        df.rename(index={'TotalProd':' '}, inplace=True)
        
        df.plot.barh(stacked=True, figsize=(12,1), color=sns.color_palette("hls", 10))
        plt.title(f'Top 10 Producers of {product}')
        plt.xlabel('Production (in 1000 tonnes) per country')
        plt.legend(loc='center left', bbox_to_anchor=(1.0, 0.5))
    
    plt.show();
    df = None # clear any remaining data
    return None    



def plot_yearly_product(data, title):
    '''
    Plot the top 10 products trend over the last 50 years.
    '''
    top_10 = data.groupby('Item')['TotalProd'].agg('sum').sort_values(ascending=False).index[:10].values

    top_10_df = pd.DataFrame()
    top_10_df['Index'] = data.columns[5:-1].values

    for product in top_10:
        top_10_df[product] = data[data.Item == product].iloc[:, 5:-1].sum(axis=0).values

    top_10_df.set_index('Index', inplace=True)
    top_10_df = top_10_df.T
    
    plt.figure(figsize=(16,8))
    x = np.arange(1,54)
    for i in range(10):
        sns.lineplot(x=top_10_df.columns.values, y=top_10_df.values[i], color=sns.color_palette("husl", 10)[i])
    plt.legend(top_10_df.index.values)
    plt.xticks(rotation='vertical')
    plt.title(f'Top 10 {title} Products from 1961 to 2013')
    plt.ylabel('Production (in 1000 tonnes)')
    plt.show();
    
    top_10_df = None # clear temporary dataframe
    
    return None



def yearly_pop_with_line(data):
    '''
    Plot the yearly population from 1961 to 2013. Add a straight line from starting
    to ending population to compare linear correlation.
    '''
    yearly_pop = data.iloc[:, 2:].sum(axis=0)
    
    # Make a line using the beggining and endpoints
    x = [0, len(yearly_pop)-1]
    y = [yearly_pop[0], yearly_pop[-1]]
    line = pd.DataFrame({'x':x, 'y':y})
    
    # Plot data and estimated line
    plt.figure(figsize=(14,8))
    sns.lineplot(x='x', y='y', data=line, color='red', label='Linear Estimation', alpha=0.6, linewidth=2)
    sns.scatterplot(x=yearly_pop.index, y=yearly_pop.values, s=90, color='green', label='Population Data')
    plt.legend()
    plt.xticks(rotation='vertical')
    plt.title('Global Population (Estimated)')
    plt.ylabel('Population (in 1000 persons)')
    plt.xlabel(' ')
    plt.show();
    
    line = None # clear temp data
    return None



def pop_vs_prod(data, pop):
    '''
    Plot the global popluation (independent variable) against the global food
    production (dependent variable). We also plot a straight line through the 
    data, as well as an estimated linear regression model with 95% confidence.
    '''
    yearly_pop = pop.iloc[:, 2:].sum(axis=0).values # x (independent) variable
    yearly_prod = data.iloc[:, 5:-1].sum(axis=0).values # y (dependent) variable

    x = [yearly_pop[0], yearly_pop[-1]]
    y = [yearly_prod[0], yearly_prod[-1]]
    line = pd.DataFrame({'x':x, 'y':y})

    plt.figure(figsize=(14,8))
    sns.regplot(x=yearly_pop, y=yearly_prod, order=2, scatter=False, ci=95, color='green', label='Estimated Regressor (95% CI)')
    sns.lineplot(x='x', y='y', data=line, color='red', alpha=0.6, linewidth=2, label='Linear Line')
    sns.scatterplot(x=yearly_pop, y=yearly_prod, s=100, color='purple', label='True Points')
    plt.title('Global Population vs Global Production (per year)')
    plt.ylabel('Production (in 1000 tonnes)')
    plt.xlabel('Population (in 1000 persons)')
    plt.legend()
    plt.show();
    
    yearly_pop = yearly_prod = line = None # clear memory
    return None



def plot_20_pop(data):
    '''
    Plot the top 20 countries for population density in 2013.
    '''
    pop_count = data[['Area', 'Y2013']].sort_values(by ='Y2013', ascending=False)[:20]

    plt.figure(figsize=(12,8))
    sns.barplot(x='Y2013', y='Area', data=pop_count)
    plt.title('Top 20 Populated Countries (2013 Estimates)')
    plt.xlabel('Population (in 1000 persons)')
    plt.ylabel(' ')
    plt.show();

    pop_count = None
    return None



def plot_top_prod_vs_pop(data, pop):
    '''
    Plot two graphs:
    1) Top 3 countries yearly production
    2) Top 3 countries yearly population
    '''
    top_3 = data.groupby('Area')['TotalProd'].agg('sum').sort_values(ascending=False).index[:3].values
    prod_df = pd.DataFrame(data=data.columns[5:-1].values, columns=['Years'])

    for country in top_3:
        prod_df[country] = data[data.Area == country].iloc[:, 5:-1].sum(axis=0).values

    prod_df.set_index('Years', inplace=True)
    prod_df = prod_df.T  

    pop_df = pop.drop('Unit', axis=1).sort_values(by ='Y2013', ascending=False)[0:3]
    pop_df.set_index('Area', inplace=True)

    plt.figure(figsize=(12,10))
    # Plot production for top 3 countries
    ax1 = plt.subplot(2,1,1)
    for i in range(3):
        sns.lineplot(x=prod_df.columns.values, y=prod_df.values[i], color=sns.color_palette("hls", 3)[i])
    plt.legend(prod_df.index.values)
    plt.xticks(rotation='vertical')
    plt.title('Top 3 Yearly Production from 1961 to 2013')
    plt.ylabel('Production (in 1000 tonnes)')
    
    # keep same color order for second plot
    colors = sns.color_palette("hls", 3)
    colors_ordered = [colors[0], colors[2], colors[1]]
    
    # Plot population for top 3 countries
    ax2 = plt.subplot(2,1,2)
    for i in range(3):
        sns.lineplot(x=pop_df.columns.values, y=pop_df.values[i], color=colors_ordered[i])
    plt.legend(pop_df.index.values)
    plt.xticks(rotation='vertical')
    plt.title('Top 3 Yearly Population from 1961 to 2013')
    plt.ylabel('Population (in 1000 persons)')

    plt.tight_layout()
    plt.show();
    
    top_3 = prod_df = pop_df = None # clear memory
    return None














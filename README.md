# Global Food Production Analysis

<img src="/header/header.jpg" width="700">

---

*Note: refer to `proposal.pdf` for the full in-depth project outline.*

*Note: refer to `project_report.pdf` for the full in-depth project findings and conclusion.*

---
## Project Overview & Goals
The current world population is nearly 7.8 billion people, and this number is estimated to rise to around 9.7 billion in the year 2050. This means within the next 30 years, we will need to feed two billion more people without sacrificing the planet. This means we will need to increase our crop production in order to feed that growing population. Agriculture is one of the greatest contributors of global warming, with farming consuming immense amounts of our water supplies and leaving major pollutants as its byproduct from fertilizer runoff. This leads to the question, how do we supply the necessary amount of food for a growing world population without sacrificing the climate of our planet?

The overall goal for the project is to explore the Food Balance Sheet in order to determine the most produced food items and the use case for them, whether it is for human or livestock consumption. We want to have an understanding of where the food we are producing is going, as well as clustering country's based on their production amount to understand which countries are responsible for a majority of food production. Using the population dataset, we want to explore the idea of using a regression model that can estimate the total food production for a given year, with total population being the independent variable and total food production being the dependent varaible. This will allow us to see what the necessary production would be to support a given population number (test using the 2050 population estimate of 9.7 billion).

---

## Data
Two different datasets will be used in the analysis, one coming from [Kaggle](https://www.kaggle.com/dorbicycle/world-foodfeed-production) and one coming from [FAO](http://www.fao.org/faostat/en/#data/OA) (the Food and Agriculture Organization of the United Nations). The use cases for each dataset is as follows:
- The Kaggle dataset will be used in analyzing food production, seeing which countries produce the most and if it is for human or livestock consumption. This data will also be used to cluster countries together based on their production levels, ideally separating high and low producing countries. 
- The FAO dataset will be used to compare the global population to the yearly total food production, as well as further analyzing the highest producing countries to see if they have the largest/fastest increasing populations.

---

## Modeling
### Regression model
An initial simple linear model was fit using first degree features. The model had an RMSE of around 405,000 and did not fit he production/population data well. In order to tune this, we created polynomial features for a range of degrees (1 to 8) and selected the top 4based on minimizing the RMSE values. Below are those RMSE values as well as their fit models plotted against our data.

<img src="/result_imgs/poly_rmse.jpg" width="600"> <img src="/result_imgs/poly_models.jpg" width="900">

From the [World Resources Institute](https://www.wri.org/blog/2018/12/how-sustainably-feed-10-billion-people-2050-21-charts), we know that we need an increase of around 56% in production from 2010 to 2050. The 2010 global production, from our dataset, was 11,445,072 (in 1000 tonnes). Following this idea, that means we need to produce 17,854,312.32 (in 1000 tonnes) total for the 2050 population. This seems to follow the degree 4 polynomial model, which estimated a production of 17,341,906.93 (in 1000 tonnes).

However, from the [United Nations](https://www.un.org/press/en/2009/gaef3242.doc.htm#:~:text=Food%20production%20must%20double%20by%202050%20to%20meet%20the%20demand,a%20panel%20discussion%20on%20%E2%80%9CNew), we have also inferred that global food production must double in order to support the global population. Given that the article was written in 2009, with a global production of 11,211,891 (in 1000 tonnes) for out dataset, this means we need to produce 22,423,782 (in 1000 tonnes) for the year 2050. This idea follows the degree 2 model (almost exactly) with an estimated production of 22,463,820.97 (in 1000 tonnes).

Despite not being the lowest RMSE for the models, these 2 most accurately depict what has been estimated by professionals. Choosing which model is correct will be more of a challenge, since there is no real way to determine what the actual growth will be in the future (global events, pandemics, food supply, etc.). However, these two models are good indicators of a possible future that we could see.

### Clustering
We also wanted to cluster countries based on their yearly production values (all of which were normalized). In order to do this, we needed to select the number of clusters using two different methods:

<img src="/result_imgs/cluster_select.jpg" width="700">

Using the elbow method for the inertia graph, it seemed that 2 is the ideal cluster number (but 3 and 4 could also be considered). We also used a silhouette score to determine help determine the number of clusters, which helps determine the distance between the resulting clusters, and we want a value of as close to 1 as possible. Using both of there, it seems that 2 clusters wass ideal since this is where the elbow occurs and also has the highest silhouette score (besides 1 which is not considered in this case). After fitting a KMeans model using 2 clusters, our model predicted the following:

<img src="/result_imgs/cluster_result.jpg" width="600">

As expected, using 2 clusters separated the top 3 producers from the remaining countries. This means the clusters are based on high vs low production, since from the DataExploration notebook we saw that the top 3 countries were responsible for over 40% of the global production. The next closest country (Brazil) produced less than 1/3 the amount that the United States or India does and around 1/6 the amount of China. These clusters seem to be accurate in separating our data in correct clusters, and helps us visual how much more the top 3 countries produced compared to the remaining countries.

---

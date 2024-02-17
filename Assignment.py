# %%
import pandas as pd 
import numpy as np
import matplotlib as mp 
import seaborn as sb 
import plotly as plt 


# %% [markdown]
# # Metadata Review
# 
# 1. What organization publishes this dataset?
# Shelter, Support & Housing Administration
# 
# 2. How frequently is the dataset updated?
# Daily
# 
# 3. What metadata is available (e.g., column names, data types, descriptions)?
# Column name and description of each column is provided under a rolldown menu " Data features". 
# 
# 4. Is there documentation about who or what produces the data? About who collects it? Through what processes?
# yes
# 
# 5. Is there documentation about limitations of the data, such as possible sources of error or omission?
# yes
# 
# 6. Are there any restrictions concerning data access or use? (e.g.,registraton required or non-commercial use only)
# no

# %% [markdown]
# ## Getting Started

# %%
pd.set_option("display.max_columns", None) # to display all columns in a dataset

# 1. Load the data to a single DataFrame
data = pd.read_csv('Daily shelter overnight occupancy.csv')
data

# %% [markdown]
# 

# %%
#2 profile the dataframe

# 2.a finding the column names
data.columns

# %%
# 2.b finding the columns data types
data.dtypes

# %%
#can use info to get all previous data profiling info, like column names, dtype, Naan, shape, etc. 
data.info(max_cols=None)



# %%
# I couldn't see all columns even after changing pandas settings, so I printed the info output to a file
with open('dataframe_info.txt', 'w') as f:
    data.info(buf=f)

# %%
# The occupancy_date column should be changed from object to date. Which i will do in a later step
#  OCCUPANCY_DATE          4035 non-null   object 
# change ID columns from int to string


# %%
# 2.c finding the Naans in each column.

nan_counts = data.isna().sum()
print(nan_counts)

nan_counts.to_csv('nan_counts.csv')


# %%
# 2.d shape of dataframe
data.shape

# %%
# 3. a) generate some summary stats for the data
# For numeric columns: the default for describe is for numerical values..
data.describe()

#unexpected results: program ID and location ID, etc should be treated as strings not as floats, which require type change.

# %%
# 3. b) For text columns: What is the most common value? How many unique values are there?

data.describe(exclude= [np.number])

# %%
# 4. rename one or more columns in the dataframe
data = data.rename(columns = {'UNAVAILABLE_ROOMS' : 'UA_ROOMs'})
 
print(list(data))

# %%
# 5. select a single column and find its unique values
data['SHELTER_GROUP'].unique()

# %%
data['SECTOR'].unique()


# %%
#6. Select a single text/categorical column and find the counts of its values.

data['SECTOR'].value_counts()

# %%
# 7. Convert the data type of at least one of the columns. If all columns are typed correctly, convert one to str and back.

data['SECTOR'] = data['SECTOR'].astype('category')
data['SECTOR']

# %%
# 7. Convert the data type of at least one of the columns. If all columns are typed correctly, convert one to str and back.

data['OCCUPANCY_DATE'] = pd.to_datetime(data['OCCUPANCY_DATE'])
data['OCCUPANCY_DATE'] 

# %%
#7. convert the data type of multiple columns

data.columns


# %%
data[['_id', 'ORGANIZATION_ID', 'SHELTER_ID', 'LOCATION_ID', 'PROGRAM_ID']] = data[['_id', 'ORGANIZATION_ID', 'SHELTER_ID', 'LOCATION_ID', 'PROGRAM_ID']].astype(str)



# %%
data.info()

# %%
#changing column names to lowercase
data= data.rename(columns=str.lower)

data.columns

# %%
# 8. Write the DataFrame to a different file format than the original.
data.to_excel('profiled_shelter_data.xlsx', index = False)

# %% [markdown]
# ## More Data wrangling, filtering

# %%
data

# %%
# 1. Create a column derived from an existing one. Some possibilities:
#Bin a continuous variable
#Extract a date or time part (e.g. hour, month, day of week)
#Assign a value based on the value in another column (e.g. TTC line number based on line values in the subway delay data)
#Replace text in a column (e.g. replacing occurrences of "Street" with "St.")

# this code didn't work for some reason
#data['weekends'] = data['occupancy_date'].dt.weekday.isin([4,5,6])
#data['weekends'] = np.where(data['occupancy_date'].dt.weekday.isin([4,5,6]),'yes','no')
#data['weekends'].head(20)

data['location_address2'] = data['location_address'].str.replace('Road', 'Rd')

data['location_address2']

# %%
#2. Remove one or more columns from the dataset.
data = data.drop(columns= 'location_province')

data.columns

# %%
#3. Extract a subset of columns and rows to a new DataFrame
#with .loc[]
subset_data = data.loc[:, ['capacity_actual_bed', 'organization_name', 'shelter_group', 'location_name']]
subset_data

# %%
#3 with the .query() method and column selecting [[colnames]]
data.query('capacity_actual_bed.isna()')[['organization_name','shelter_group','location_name', 'capacity_actual_bed']]

# %%
#4. Investigate null values
#Create and describe a DataFrame containing records with NaNs in any column
nan_data = data.isna()
nan_data
#Create and describe a DataFrame containing records with NaNs in a subset of columns
#If it makes sense to drop records with NaNs in certain columns from the original DataFrame, do so.

# %%
#Create and describe a DataFrame containing records with NaNs in a subset of columns

data_without_bed_capcity_nan = data.loc[data['capacity_actual_bed'].isna(),
                                    ['organization_name','shelter_group','location_name', 'capacity_actual_bed']]
data_without_bed_capcity_nan

# %%
# I'm not going to drop any Nans, but this is how it can be done
# Cleaned_data = data.dropna('columns names')


# %% [markdown]
# ## Grouping and aggregating

# %%
#1. Use groupby() to split your data into groups based on one of the columns.
sector_groups = data.groupby('sector')

sector_groups['occupancy_rate_beds'].mean()

# %%
# 2. #Use agg() to apply multiple functions on different columns and create a summary table. Calculating group sums or standardizing data are two examples of possible functions that you can use.
occupancy_summary = (data.groupby('sector')
                     .agg(bed_occupancy_sum = ('occupied_beds', 'sum'),
                         bed_mean_occupancy_rate = ('occupancy_rate_beds', 'mean'),
                         room_occupancy_sum = ('occupied_rooms', 'sum'),
                         room_mean_occupancy_rate = ('occupancy_rate_rooms', 'mean')))

occupancy_summary.head()

# %% [markdown]
# ## Plot

# %%
#1 Plot two or more columns in your data using matplotlib, seaborn, or plotly. Make sure that your plot has labels, a title, a grid, and a legend.
summary_plot = occupancy_summary.reset_index()




# %%
summary_plot

# %%
#%matplotlib inline 
import matplotlib.pyplot as mplt

fig, ax = mplt.subplots()


beds = ax.bar(summary_plot['sector'], summary_plot['bed_occupancy_sum'])
#rooms = ax.bar(summary_plot['sector'], summary_plot['room_occupancy_sum'])
ax.set_title('cumulative number of occupied beds for Jan 2024')
ax.set_xlabel('Sector')
ax.set_ylabel('Number of Occupied Beds')
ax.set_axisbelow(True)

ax.grid(alpha = 0.5)
ax.legend([beds], ['Beds'],
          bbox_to_anchor = (0,1),
          loc = 'upper left')

mplt.savefig('occupied_shelter_beds1.png')


# %%
modefig, (ax1, ax2) = mplt.subplots(nrows=1, ncols=2, sharey=True)

ax1.bar(summary_plot['sector'],
            summary_plot['bed_occupancy_sum'])
ax2.bar(summary_plot['sector'],
            summary_plot['room_occupancy_sum'])
ax1.set_title('Beds')
ax2.set_title('Rooms')

# Rotate the x-axis labels for better readability and adjust their alignment
ax1.set_xticklabels(summary_plot['sector'], rotation=45, ha="right")
ax2.set_xticklabels(summary_plot['sector'], rotation=45, ha="right")

modefig
mplt.savefig('occupied_shelter_beds2.png')

# %%
#%matplotlib inline 
import matplotlib.pyplot as mplt

fig, ax = mplt.subplots()

# Setting the width of the bars
bar_width = 0.35

# Setting the positions of the bars on the x-axis
indices = np.arange(len(summary_plot['sector']))

beds = ax.bar(indices - bar_width/2, summary_plot['bed_occupancy_sum'], bar_width, label='Bed Occupancy')
rooms = ax.bar(indices + bar_width/2, summary_plot['room_occupancy_sum'], bar_width, label='Room Occupancy')
ax.set_title('cumulative number of occupied beds/rooms for Jan 2024')
ax.set_xlabel('Sector')
ax.set_ylabel('Number of Occupied Beds/Rooms')
ax.set_xticks(indices)
ax.set_xticklabels(summary_plot['sector'])
ax.set_axisbelow(True)
ax.grid(alpha=0.5)
ax.legend()

fig
mplt.savefig('occupied_shelter_beds3.png')


# %%



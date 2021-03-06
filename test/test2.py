#from pandas import DataFrame, read_excel

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy.random as np
import sys
import matplotlib

#%matplotlib inline

print('Python version ' + sys.version)
print('Pandas version: ' + pd.__version__)
print('Matplotlib version ' + matplotlib.__version__)

# set seed
np.seed(111)


# Function to generate test data
def CreateDataSet(Number=1):
    Output = []

    for i in range(Number):
        # Create a weekly (mondays) date range
        rng = pd.date_range(start='1/1/2009', end='12/31/2012', freq='W-MON')

        # Create random data
        data = np.randint(low=25, high=1000, size=len(rng))

        # Status pool
        status = [1, 2, 3]

        # Make a random list of statuses
        random_status = [status[np.randint(low=0, high=len(status))] for i in range(len(rng))]

        # State pool
        states = ['GA', 'FL', 'fl', 'NY', 'NJ', 'TX']

        # Make a random list of states
        random_states = [states[np.randint(low=0, high=len(states))] for i in range(len(rng))]

        Output.extend(zip(random_states, random_status, data, rng))

    return Output

dataset = CreateDataSet(4)
df = pd.DataFrame(data=dataset, columns=['State','Status','CustomerCount','StatusDate'])
print(df.info())

print df.head()


# Save results to excel
df.to_excel('Lesson3.xlsx', index=False)
print('Done')

pd.read_excel

# Location of file
Location = r'C:\Users\steven.mitchell\PycharmProjects\test\Lesson3.xlsx'

# Parse a specific sheet
df = pd.read_excel(Location, 0, index_col='StatusDate')
print df.dtypes

print df.index

print  df.head()

print df['State'].unique()

# Clean State Column, convert to upper case
df['State'] = df.State.apply(lambda x: x.upper())

print df['State'].unique()

# Only grab where Status == 1
mask = df['Status'] == 1
df = df[mask]

# Convert NJ to NY
mask = df.State == 'NJ'
df['State'][mask] = 'NY'

print df['State'].unique()


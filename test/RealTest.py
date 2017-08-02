#from pandas import DataFrame, read_excel

# Import libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy.random as np
import sys
import matplotlib

import os, sys

Location1 = r'C:\Users\steven.mitchell\PycharmProjects\test\sys_processor_dev.xls'
#df = pd.read_excel(Location1, 0,names =['Name','Active','Created','Created by','Updated','Updated by'])
df1 = pd.read_excel(Location1)
#print(df1.info())

Sorted1 = df1.sort_values(['Name'], ascending=True)
#print Sorted1.head(1)

#df.to_excel('testingWrite.xlsx', index=False)

Location2 = r'C:\Users\steven.mitchell\PycharmProjects\test\sys_processor_test.xls'

df2 = pd.read_excel(Location1)
#print(df2.info())

Sorted2 = df2.sort_values(['Name'], ascending=True)
#print Sorted2.head(1)

difference = df1[df1!=df2]
print difference

#difference.to_excel('testingOutput.xlsx',index = False)
print('Done')

#for f in os.listdir("C:\Users\steven.mitchell\PycharmProjects\\test\\"):
 #   print(f)
a = os.listdir("C:\Users\steven.mitchell\PycharmProjects\\test\\")
print a
from pandas import  DataFrame

df1 = DataFrame({'col1':[1,2,3], 'col2':[2,3,4]})
df2 = DataFrame({'col1':[4,2,5], 'col2':[6,3,5]})
print df1
print df2
print df2[~df2.isin(df1).all(1)]
print df2[(df2!=df1)].dropna(how='all')
print df2[~(df2==df1)].dropna(how='all')
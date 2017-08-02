import pandas as pd
import numpy as np


# devFolderLocation = "C:\Users\steven.mitchell\Desktop\Dev_Docs"
# testFolderLocation = "C:\Users\steven.mitchell\Desktop\Test_Docs"
# # Define the diff function to show the changes in each field
# filenameDev= raw_input("Enter the name of the DEV file:\n")
# print filenameDev
# filenameDev = folderLocation + filenameDev
# print filenameDev
# filenameTest = raw_input("Enter the name of the TEST file:\n")
# print filenameTest

def report_diff(x):
    return x[0] if x[0] == x[1] else '{} ---> {}'.format(*x)

# We want to be able to easily tell which rows have changes
def has_change(row):
    if "--->" in row.to_string():
        return "Y"
    else:
        return "N"

Location1 = r'C:\Users\steven.mitchell\PycharmProjects\test\sys_processor_dev.xls'
Location2 = r'C:\Users\steven.mitchell\PycharmProjects\test\sys_processor_test.xls'


# Read in both excel files
df1 = pd.read_excel(Location1)
df2 = pd.read_excel(Location2)

# comments
# print "printing head"
# print df1.head(0)
# df1.head()
# print "done with head"

# Make sure we order by account number so the comparisons work
df1 = df1.sort_values(['Name'], ascending=True)
df1=df1.reindex()
df2 = df2.sort_values(['Name'], ascending=True)
df2=df2.reindex()

print "columns"
print list(df2)
print ''.join(list(df2.columns[0]))

print "done"


# Create a panel of the two dataframes
diff_panel = pd.Panel(dict(df1=df1,df2=df2))
#print "printing panel"
# diff_panel.to_excel('my-diff-5.1.xlsx',index = False)


#Apply the diff function
diff_output = diff_panel.apply(report_diff, axis=0)

# Flag all the changes
diff_output['has_change'] = diff_output.apply(has_change, axis=1)

#Save the changes to excel but only include the columns we care about
#print diff_output
#print diff_output.info()
#diff_output[(diff_output.has_change == 'Y')].to_excel('my-diff-1.xlsx',na_rep="NaN",index=False)


diff_output.to_excel('my-diff-3.xlsx',index = False)
print('Done')
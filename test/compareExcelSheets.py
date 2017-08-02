import pandas as pd
import numpy as np
import os, sys



# Define the diff function to show the changes in each field
def report_diff(x):
    return x[0] if x[0] == x[1] else '{} ---> {}'.format(*x)

# We want to be able to easily tell which rows have changes
def has_change(row):
    if "--->" in row.to_string():
        return "Y"
    else:
        return "N"

def compareDevAndTest(devFile, testFile):
    #sc_maintain_category.xls
    devPath = "C:\Users\steven.mitchell\Desktop\Dev_Docs\\"
    testPath = "C:\Users\steven.mitchell\Desktop\Test_Docs\\"

    devFile1 = devPath + devFile
    testFile1 = testPath + testFile

    # Read in both excel files
    df1 = pd.read_excel(devFile1)
    df2 = pd.read_excel(testFile1)

    # # Make sure we order by account number so the comparisons work
    # df1 = df1.sort_values(['Name'], ascending=True)
    # df1 = df1.reindex()
    # df2 = df2.sort_values(['Name'], ascending=True)
    # df2 = df2.reindex()

    # Create a panel of the two dataframes
    diff_panel = pd.Panel(dict(df1=df1, df2=df2))
    # print "printing panel"
    # print diff_panel

    # Apply the diff function
    diff_output = diff_panel.apply(report_diff, axis=0)

    # Flag all the changes
    diff_output['has_change'] = diff_output.apply(has_change, axis=1)

    # Save the changes to excel but only include the columns we care about
    # print diff_output
    name = "C:\Users\steven.mitchell\Desktop\\Compare_Of_Folder\\"+"Compare_Of_"+devFile + "x"
    # print name
    diff_output.to_excel(name ,index=False)
    print('Done with:', devFile, ' comparison')

devPath = "C:\Users\steven.mitchell\Desktop\Dev_Docs\\"
devDirectory = os.listdir(devPath)
testPath = "C:\Users\steven.mitchell\Desktop\Test_Docs\\"
testDirectory = os.listdir(testPath)

for devFile, testFile in zip(devDirectory,testDirectory):
    # print devFile, testFile
    compareDevAndTest(devFile,testFile)
    # print "Done with 1 interation"


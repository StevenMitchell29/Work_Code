import pandas as pd
import numpy as np
import os, sys


# Define the diff function to show the changes in each field
def report_diff(x):
    return x[0] if x[0] == x[1] else '{} ---> {}'.format(*x)

def compareDevAndTest(devFile, testFile):
    #sc_maintain_category.xls
    # devPath = "C:\Users\steven.mitchell\Desktop\Dev_Docs\\"
    # testPath = "C:\Users\steven.mitchell\Desktop\Test_Docs\\"#
    devPath = "C:\Users\steven.mitchell\Desktop\Dev_Diction\\"
    testPath = "C:\Users\steven.mitchell\Desktop\Test_Diction\\"

    devFile1 = devPath + devFile
    testFile1 = testPath + testFile

    # Read in both excel files
    dev = pd.read_excel(devFile1)
    test = pd.read_excel(testFile1)
    dev['version'] = "dev"
    test['version'] = "test"

    firstColumn = ''.join(list(dev.columns[0]))
    secondColumn = ''.join(list(dev.columns[1]))
    createdColumn = ''.join(list(dev.columns[-4]))
    # firstTwo = list(dev.columns[:2])
    # print firstTwo
    # print secondColumn

    columnList = list(dev.columns[:-1])
    # print columnList

    #Join all the data together and ignore indexes so it all gets added
    full_set = pd.concat([test,dev],ignore_index=True)

    # Let's see what changes in the main columns we care about
    changes = full_set.drop_duplicates(subset=columnList)

    #We want to know where the duplicates are --> changes or duplicate named records
    # dupe_accts = changes.set_index('Name').index.get_duplicates()
    dupe_accts = changes.set_index(firstColumn,createdColumn).index.get_duplicates()

    #Get all the duplicate rows
    # dupes = changes[changes[secondColumn].isin(dupe_accts)]
    dupes = changes[(changes[firstColumn].isin(dupe_accts))] #& changes[secondColumn].isin(dupe_accts))]

    dupes = dupes.sort_values([firstColumn], ascending=True)
    dupes = dupes.reindex()

    #Flag all duplicated names
    findAdditionAndDeletions=changes[firstColumn].isin(dupe_accts)

    #Identify the records that did not make it to test
    removed_accounts = changes[(findAdditionAndDeletions == False) & (changes["version"] == "dev")]

    # added_test_set = full_set.drop_duplicates(subset=columnList,keep='last')
    # dupe_accts2 = added_test_set.set_index(firstColumn).index.get_duplicates()
    #
    # # Flag all duplicated names
    # findAdditions = added_test_set[firstColumn].isin(dupe_accts2)
    # added_accounts = added_test_set[(findAdditions == False) & (changes["version"] == "test")]

    #Identify added accounts
    unchanged = changes[(findAdditionAndDeletions == False) & (changes["version"] == "test")]
    # unchanged = unchanged[~unchanged.isin(added_accounts).all(1)]

    # print unchanged -added_accounts

    #Save the changes to excel but only include the columns we care about
    # Save the changes to excel but only include the columns we care about
    # print diff_output
    # name = "C:\Users\steven.mitchell\Desktop\\Compare_Of_Folder\\" + "Compare_Of_" + devFile# + "x"
    name = "C:\Users\steven.mitchell\Desktop\\Diction_Compare\\" + "Compare_Of_" + devFile# + "x"

    # print name
    writer = pd.ExcelWriter(name)
    dupes.to_excel(writer, "Edited or Duplicated Name", index=False)
    removed_accounts.to_excel(writer, "Deleted", index=False)
    # added_accounts.to_excel(writer, "Only Test", index=False)
    unchanged.to_excel(writer, "Unchanged and Added", index=False)
    writer.save()
    print('Done with:', devFile, ' comparison')


# devPath = "C:\Users\steven.mitchell\Desktop\Dev_Docs\\"
devPath = "C:\Users\steven.mitchell\Desktop\Dev_Diction\\"
devDirectory = os.listdir(devPath)
# testPath = "C:\Users\steven.mitchell\Desktop\Test_Docs\\"
testPath = "C:\Users\steven.mitchell\Desktop\Test_Diction\\"

testDirectory = os.listdir(testPath)

for devFile, testFile in zip(devDirectory,testDirectory):
    # print devFile, testFile
    compareDevAndTest(devFile,testFile)
    # print "Done with 1 interation"
import pandas as pd
import numpy as np
import os, sys


# Define the diff function to show the changes in each field
def report_diff(x):
    return x[0] if x[0] == x[1] else '{} ---> {}'.format(*x)

def compareDevAndTest(devFile, testFile):
    #sc_maintain_category.xls
    devPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Dev_Docs\\"
    testPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Test_Docs\\"#
    # devPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Dev_Diction\\"
    # testPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Test_Diction\\"

    devFile1 = devPath + devFile
    testFile1 = testPath + testFile

    # Read in both excel files
    dev = pd.read_excel(devFile1)
    test = pd.read_excel(testFile1)
    dev['version'] = "dev"
    test['version'] = "test"

    firstColumn = ''.join(list(dev.columns[0]))
    createdColumn = ''.join(list(dev.columns[-4]))

    # Get all columns except for the version
    columnList = list(dev.columns[:-1])

    #Join all the data together and ignore indexes so it all gets added
    full_set = pd.concat([test,dev],ignore_index=True)

    # Drop all the duplicates, but keep the test version if so
    changes = full_set.drop_duplicates(subset=columnList)
    # drop all the duplicates, but keep the dev version if so
    changes2 = full_set.drop_duplicates(subset=columnList,keep='last')

    # merge the sets together
    full_Unchanged = pd.merge(changes,changes2, how='inner',on=columnList)
    # full_Unchanged.to_excel('full_Unchanged.xlsx', index=False)

    # and find all of the records that were unchanged from dev to test
    unchanged = full_Unchanged[(full_Unchanged.version_x=="test") & (full_Unchanged.version_y=="dev")]
    # get all the duplicate names and creation dates that appear in both
    # TODO this may not catch all records that are the same if they do not have the same creation date
    duplicate_Names = full_Unchanged.set_index(firstColumn, createdColumn).index.get_duplicates()
    # Get all the duplicate or edited rows
    duplicate = full_Unchanged[(full_Unchanged[firstColumn].isin(duplicate_Names))]
    # TODO this might work
    duplicate = duplicate[(duplicate.version_x=="test") & (duplicate.version_y=="test") |(duplicate.version_x=="dev") & (duplicate.version_y=="dev")]

    duplicate = duplicate.sort_values([firstColumn], ascending=True)
    duplicate = duplicate.reindex()
    # duplicate.to_excel('duplicate.xlsx', index=False)

    # remove all the entries from unchaged so they only appear in duplicates
    unchanged = unchanged[-unchanged.isin(duplicate_Names)]
    unchanged.dropna(subset=[firstColumn], inplace=True)
    # test_only.to_excel('test_only2.xlsx', index=False)

    # get all the entries that appear in test only and not in duplicate
    # test_only = full_Unchanged[(full_Unchanged.version_x == "test") & (full_Unchanged.version_y == "test")]
    # test_only.to_excel('test_only1.xlsx', index=False)
    # test_only = test_only[-test_only.isin(duplicate_Names)]
    # test_only.dropna(subset=[firstColumn], inplace=True)
    # test_only.to_excel('test_only2.xlsx', index=False)

    # get all records that appear in dev only
    # dev_only = full_Unchanged[(full_Unchanged.version_x=="dev") & (full_Unchanged.version_y=="dev")]
    # test_only.to_excel('test_only1.xlsx', index=False)
    # dev_only = dev_only[-dev_only.isin(duplicate_Names)]
    # dev_only.dropna(subset=[firstColumn], inplace=True)
    # dev_only.to_excel('dev_only.xlsx', index=False)
    print('Done with:', devFile, ' comparison')
    return duplicate


devPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Dev_Docs\\"
# devPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Dev_Diction\\"
devDirectory = os.listdir(devPath)
testPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Test_Docs\\"
# testPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Test_Diction\\"
testDirectory = os.listdir(testPath)

name = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\\Compare_Of_Folder2\\" + "Only comparisons" + ".xlsx"
    # name = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\\Diction_Compare\\" + "Compare_Of_" + devFile# + "x"

writer = pd.ExcelWriter(name)
for devFile, testFile in zip(devDirectory,testDirectory):
    # print devFile, testFile
    print('Starting:', devFile, ' comparison')
    compareDevAndTest(devFile,testFile).to_excel(writer, devFile, index=False)

writer.save()
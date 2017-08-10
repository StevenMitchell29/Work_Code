import pandas as pd
import numpy as np
import os, sys


# Define the diff function to show the changes in each field
def report_diff(x):
    return x[0] if x[0] == x[1] else '{} ---> {}'.format(*x)

def compareDevAndTest(devFile, testFile):
    #sc_maintain_category.xls
    # devPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Dev_Docs\\"
    # testPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Test_Docs\\"#
    devPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Dev_Diction\\"
    testPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Test_Diction\\"

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
    full_Unchanged = full_Unchanged[-full_Unchanged.isin(unchanged[firstColumn])]
    full_Unchanged[firstColumn].replace('', np.nan, inplace=True)
    full_Unchanged.dropna(subset=[firstColumn], inplace=True)
    # full_Unchanged.to_excel('full_Unchanged.xlsx', index=False)

    # Get all records that are duplicates for everything except updated and updated by--> most likely upgrades
    test = full_Unchanged.duplicated(subset=columnList[:-2])

    # get all the dev versions first
    dev_edited = full_Unchanged[test]
    # dev_edited.to_excel('full_Unchanged2.xlsx', index=False)
    # make sure that no test records are randomly mixed within
    dev_edited = dev_edited[(dev_edited.version_x == "dev") & (dev_edited.version_y =="dev")]
    # edit the version columns
    dev_edited = dev_edited.drop(['version_x'], axis=1)
    dev_edited = dev_edited.drop(['version_y'], axis=1)
    dev_edited['version'] = "dev"
    # dev_edited.to_excel('full_Unchanged2.xlsx', index=False)

    # get all the test versions now
    test2 = full_Unchanged.duplicated(subset=columnList[:-2],keep='last')
    test_edited = full_Unchanged[test2]
    # make sure no dev records are randomly mixed within
    test_edited = test_edited[(test_edited.version_x == "test") & (test_edited.version_y =="test")]
    test_edited = test_edited.drop(['version_x'], axis=1)
    test_edited = test_edited.drop(['version_y'], axis=1)
    test_edited['version'] = "test"

    # merge the two sheets together for an 'intersection' on the same columns
    prelim_merge = pd.merge(dev_edited,test_edited, how='inner',on=columnList[:-2])
    # prelim_merge.to_excel('full_Unchanged4.xlsx', index=False)

    # sort
    prelim_merge = prelim_merge.sort_values([firstColumn], ascending=True)
    prelim_merge = prelim_merge.reindex()

    # sort
    full_Unchanged = full_Unchanged.sort_values([firstColumn], ascending=True)
    full_Unchanged = full_Unchanged.reindex()

    # find all records that are in only test
    test_only = full_Unchanged[(full_Unchanged.version_x == "test") & (full_Unchanged.version_y == "test")]
    test_only = pd.concat([test_only,test_edited])
    # remove all records that are found in test_edited
    test_only = test_only.drop_duplicates(subset=columnList[:-2],keep=False)
    test_only = test_only[columnList]
    test_only['version'] = "test"
    test_only.to_excel('test_only1.xlsx', index=False)

    # get all records that appear in dev only
    dev_only = full_Unchanged[(full_Unchanged.version_x == "dev") & (full_Unchanged.version_y == "dev")]
    dev_only = pd.concat([dev_only, dev_edited])
    dev_only = dev_only.drop_duplicates(subset=columnList, keep=False)
    dev_only = dev_only[columnList]
    dev_only['version'] = "dev"
    dev_only.to_excel('dev_only.xlsx', index=False)

    # name = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\\Compare_Of_Folder\\" + "Compare_Of_" + devFile  # + "x"
    name = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\\Diction_Compare\\" + "Compare_Of_" + devFile# + "x"

    writer = pd.ExcelWriter(name)
    prelim_merge.to_excel(writer, "Edited", index=False)
    dev_only.to_excel(writer, "Only Dev", index=False)
    test_only.to_excel(writer, "Only Test", index=False)
    unchanged.to_excel(writer, "Unchanged from Dev to Test", index=False)
    writer.save()
    print('Done with:', devFile, ' comparison')


# devPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Dev_Docs\\"
devPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Dev_Diction\\"
devDirectory = os.listdir(devPath)
# testPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Test_Docs\\"
testPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Test_Diction\\"
testDirectory = os.listdir(testPath)

for devFile, testFile in zip(devDirectory,testDirectory):
    # print devFile, testFile
    print('Starting:', devFile, ' comparison')
    compareDevAndTest(devFile,testFile)


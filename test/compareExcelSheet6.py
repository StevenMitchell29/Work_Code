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
    full_Unchanged = full_Unchanged[-full_Unchanged.isin(unchanged[firstColumn])]
    full_Unchanged[firstColumn].replace('', np.nan, inplace=True)
    full_Unchanged.dropna(subset=[firstColumn], inplace=True)
    # full_Unchanged.to_excel('full_Unchanged.xlsx', index=False)

    # Get all records that are duplicates for everything except updated and updated by
    test = full_Unchanged.duplicated(subset=columnList[:-2])

    # get all the dev versions first
    dev_edited = full_Unchanged[test]
    # edit all the columns
    # make sure that no test records are randomly mixed within
    dev_edited.to_excel('full_Unchanged2.xlsx', index=False)

    dev_edited = dev_edited[(dev_edited.version_x == "dev") & (dev_edited.version_y =="dev")]
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
    # test_edited.to_excel('full_Unchanged3.xlsx', index=False)

    # testing = pd.merge(test_edited,dev_edited, how='outer',on=columnList)
    # testing = testing.drop_duplicates(subset=columnList[:-2],keep=False)

    # testing.to_excel('full_Unchanged_.xlsx',index=False)
    # bleh
    prelim_merge = pd.merge(dev_edited,test_edited, how='inner',on=columnList[:-2])
    prelim_merge.to_excel('full_Unchanged4.xlsx', index=False)
    # TODO so now testing looks good you just have to remove all files with conditions dev dev or test test
    # the 2 lines below look redundant
    # upgraded_set = prelim_merge[((prelim_merge.version_x=="test") & (prelim_merge.version_y=="test") |(prelim_merge.version_x=="dev") & (prelim_merge.version_y=="dev"))]
    # upgraded_set.to_excel('full_Unchanged5.xlsx', index=False)


    prelim_merge = prelim_merge.sort_values([firstColumn], ascending=True)
    prelim_merge = prelim_merge.reindex()

    full_Unchanged = full_Unchanged.sort_values([firstColumn], ascending=True)
    full_Unchanged = full_Unchanged.reindex()

    # full_Unchanged2 = full_Unchanged
    # for row in prelim_merge.itertuples():
    #     for row2 in full_Unchanged.itertuples():
    #         if row[firstColumn] == row2[firstColumn]:
            # if row[1:8] == row2[1:8]:
                # print row2[1:8]
                # full_Unchanged2 = full_Unchanged2[row2[1]]
                # dev_and_test_only  = dev_and_test_only.concat([dev_and_test_only,row2],ignore_index=True)#,ignore_index=True)

    # full_Unchanged2.to_excel('full_Unchanged_.xlsx', index=False)
    # testing = pd.concat([full_Unchanged,prelim_merge])
    # testing = testing[columnList]
    # testing.to_excel('full_Unchanged_.xlsx', index=False)
    # TODO So what am I trying to do.  I am trying to remove all records from one data frame from another
    # TODO if they appear there.  If the records has the same values up to a certain point then delte
    # testing.drop_duplicates(keep=False)
    # testing = testing.sort_values([firstColumn], ascending=True)
    # testing = testing.reindex()
    # testing.to_excel('full_Unchanged_.xlsx', index=False)


    # bleh
    # testing = full_Unchanged[(full_Unchanged.version_x == "test") & (full_Unchanged.version_y == "test")]  # (prelim_merge[firstColumn])]
    #
    # testing = testing[-testing.isin(prelim_merge[firstColumn])]
    # testing.dropna(subset=[firstColumn], inplace=True)
    # testing.to_excel('full_Unchanged.xlsx', index=False)

    # full_Unchanged.dropna(subset=[firstColumn], inplace=True)

    # bleh
    # get all the duplicate names and creation dates that appear in both
    # duplicate_Names = full_Unchanged.set_index(firstColumn).index.get_duplicates()
    # Get all the duplicate or edited rows
    # duplicate = full_Unchanged[(full_Unchanged[firstColumn].isin(duplicate_Names))]
    # duplicate = duplicate[(duplicate.version_x=="test") & (duplicate.version_y=="test") |(duplicate.version_x=="dev") & (duplicate.version_y=="dev")]

    # get a list of all the names in this updated set
    # get_names = duplicate.set_index(firstColumn,createdColumn).index.get_duplicates()

    # duplicate = duplicate.sort_values([firstColumn], ascending=True)
    # duplicate = duplicate.reindex()
    # duplicate.to_excel('duplicate.xlsx', index=False)

    # remove all the entries from unchanged so they only appear in duplicates
    # unchanged = unchanged[-unchanged.isin(get_names)]
    # unchanged.dropna(subset=[firstColumn], inplace=True)
    # test_only.to_excel('test_only2.xlsx', index=False)

    # get all the entries that appear in test only and not in duplicate
    # testing = pd.concat([full_Unchanged, prelim_merge])
    # testing = testing[columnList]
    # testing.to_excel('full_Unchanged_.xlsx', index=False)
    # TODO So what am I trying to do.  I am trying to remove all records from one data frame from another
    # TODO if they appear there.  If the records has the same values up to a certain point then delte
    # testing.drop_duplicates(keep=False)
    # testing = testing.sort_values([firstColumn], ascending=True)
    # testing = testing.reindex()
    # testing.to_excel('full_Unchanged_.xlsx', index=False)

    test_only = full_Unchanged[(full_Unchanged.version_x == "test") & (full_Unchanged.version_y == "test")]
    test_only = pd.concat([test_only,test_edited])
    test_only = test_only.drop_duplicates(subset=columnList,keep=False)
    test_only = test_only[columnList]
    test_only['version'] = "test"
    test_only.to_excel('test_only.xlsx', index=False)

    # testing = pd.merge(test_edited,dev_edited, how='outer',on=columnList)
    # testing = testing.drop_duplicates(subset=columnList[:-2],keep=False)

    # test_only.to_excel('test_only1.xlsx', index=False)
    # test_only = test_only[-test_only.isin(get_names)]#duplicate_Names)]
    # test_only.dropna(subset=[firstColumn], inplace=True)
    # test_only.to_excel('test_only2.xlsx', index=False)

    # get all records that appear in dev only
    dev_only = full_Unchanged[(full_Unchanged.version_x == "dev") & (full_Unchanged.version_y == "dev")]
    dev_only = pd.concat([dev_only, dev_edited])
    dev_only = dev_only.drop_duplicates(subset=columnList, keep=False)
    dev_only = dev_only[columnList]
    dev_only['version'] = "dev"
    dev_only.to_excel('dev_only.xlsx', index=False)

    # dev_only = full_Unchanged[(full_Unchanged.version_x=="dev") & (full_Unchanged.version_y=="dev")]
    # test_only.to_excel('test_only1.xlsx', index=False)
    # dev_only = dev_only[-dev_only.isin(get_names)]#duplicate_Names)]
    # dev_only.dropna(subset=[firstColumn], inplace=True)
    # dev_only.to_excel('dev_only.xlsx', index=False)

    name = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\\Compare_Of_Folder\\" + "Compare_Of_" + devFile  # + "x"
    # name = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\\Diction_Compare\\" + "Compare_Of_" + devFile# + "x"

    writer = pd.ExcelWriter(name)
    prelim_merge.to_excel(writer, "Edited", index=False)
    dev_only.to_excel(writer, "Only Dev", index=False)
    test_only.to_excel(writer, "Only Test", index=False)
    unchanged.to_excel(writer, "Unchanged from Dev to Test", index=False)
    writer.save()
    print('Done with:', devFile, ' comparison')


devPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Dev_Docs\\"
# devPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Dev_Diction\\"
devDirectory = os.listdir(devPath)
testPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Test_Docs\\"
# testPath = "C:\Users\steven.mitchell\OneDrive - Accenture Federal Services\Abrams\Upgrade Validation\Test_Diction\\"
testDirectory = os.listdir(testPath)

for devFile, testFile in zip(devDirectory,testDirectory):
    # print devFile, testFile
    print('Starting:', devFile, ' comparison')
    compareDevAndTest(devFile,testFile)


import pandas as pd
import numpy as np

# Define the diff function to show the changes in each field
def report_diff(x):
    return x[0] if x[0] == x[1] else '{} ---> {}'.format(*x)

# Read in the two files but call the data old and new and create columns to track
Location1 = r'C:\Users\steven.mitchell\PycharmProjects\test\sys_processor_dev.xls'
Location2 = r'C:\Users\steven.mitchell\PycharmProjects\test\sys_processor_test.xls'
dev = pd.read_excel(Location1)
test = pd.read_excel(Location2)
dev['version'] = "dev"
test['version'] = "test"

#Join all the data together and ignore indexes so it all gets added
full_set = pd.concat([dev,test],ignore_index=True)
# full_set.to_excel('my-diff-2.2.xlsx',index = False)

# Let's see what changes in the main columns we care about
changes = full_set.drop_duplicates(subset=['Name','Active','Created','Created by', 'Updated', "Updated by"])
# changes.to_excel('my-diff-2.3.xlsx',index = False)

#We want to know where the duplicate account numbers are, that means there have been changes
dupe_accts = changes.set_index('Name').index.get_duplicates()
# print dupe_accts

#Get all the duplicate rows
dupes = changes[changes["Name"].isin(dupe_accts)]
dupes = dupes.sort_values(['Name'], ascending=True)
dupes= dupes.reindex()
# TODO Export with the "improvements"
# dupes.to_excel('my-diff-2.4.xlsx',index = False)


#Flag all duplicated account numbers
findAdditionAndDeletions=changes["Name"].isin(dupe_accts)

#Identify non-duplicated items that are dev and not in test
removed_accounts = changes[(findAdditionAndDeletions == False) & (changes["version"] == "dev")]
# removed_accounts.to_excel('my-diff-2.5.xlsx',index = False)

#Drop duplicates but keep the first item instead of the last
# new_account_set = full_set.drop_duplicates(subset=['Name','Active','Created','Created by', 'Updated', "Updated by"])

#Identify dupes in this new dataframe
# new_account_set_Duplicate=new_account_set["Name"].isin(dupe_accts)

#Identify added accounts
added_accounts = changes[(findAdditionAndDeletions == False) & (changes["version"] == "test")]
# added_accounts.to_excel('my-diff-2.6.xlsx',index = False)

#Save the changes to excel but only include the columns we care about
writer = pd.ExcelWriter("my-diff-2.xlsx")
dupes.to_excel(writer,"Edited")
removed_accounts.to_excel(writer,"Kept",index=False)#,columns=['Name','Active','Created','Created by', 'Updated', "Updated by","Version"])
added_accounts.to_excel(writer,"Added",index=False)#,columns=['Name','Active','Created','Created by', 'Updated', "Updated by","Version"])
writer.save()
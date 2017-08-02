import pandas as pd
import numpy as np

# Define the diff function to show the changes in each field
def report_diff(x):
    return x[0] if x[0] == x[1] else '{} ---> {}'.format(*x)

# Read in the two files but call the data old and new and create columns to track
old = pd.read_excel('sample-address-old.xlsx')
new = pd.read_excel('sample-address-new.xlsx')
old['version'] = "old"
new['version'] = "new"

#Join all the data together and ignore indexes so it all gets added
full_set = pd.concat([old,new],ignore_index=True)

# Let's see what changes in the main columns we care about
changes = full_set.drop_duplicates(subset=["account number","name","street","city","state","postal code"])

# changes.to_excel('my-diff-3.xlsx',index = False)

#We want to know where the duplicate account numbers are, that means there have been changes
dupe_accts = changes.set_index('account number').index.get_duplicates()


#Get all the duplicate rows
dupes = changes[changes["account number"].isin(dupe_accts)]
# dupes.to_excel('my-diff-4.xlsx',index = False)

#Pull out the old and new data into separate dataframes
change_new = dupes[(dupes["version"] == "new")]
change_old = dupes[(dupes["version"] == "old")]

#Drop the temp columns - we don't need them now
change_new = change_new.drop(['version'], axis=1)
change_old = change_old.drop(['version'], axis=1)

#Index on the account numbers
# change_new.set_index('account number',inplace=True)
# change_old.set_index('account number',inplace=True)
change_new = change_new.sort_values(['account number'], ascending=True)
change_new = change_new.reindex()
change_old = change_old.sort_values(['account number'], ascending=True)
change_old = change_old.reindex()

print "change new"
print change_new
print "done"
print "change old"
print change_old
print "done"
print type(change_old)

#Now we can diff because we have two data sets of the same size with the same index
diff_panel = pd.Panel(dict(df1=change_old,df2=change_new))
# diff_panel.to_excel('my-diff-5.xlsx')

# diff_output = diff_panel.apply(report_diff)
diff_output = diff_panel.apply(report_diff, axis=0)
# diff_output.to_excel('my-diff-6.xlsx',index = False)

#Diff'ing is done, we need to get a list of removed items

#Flag all duplicated account numbers
changes['duplicate']=changes["account number"].isin(dupe_accts)

#Identify non-duplicated items that are in the old version and did not show in the new version
removed_accounts = changes[(changes["duplicate"] == False) & (changes["version"] == "old")]

# We have the old and diff, we need to figure out which ones are new

#Drop duplicates but keep the first item instead of the last
new_account_set = full_set.drop_duplicates(subset=["account number","name","street","city","state","postal code"])
# print new_account_set
# print "done"
#Identify dupes in this new dataframe
new_account_set['duplicate']=new_account_set["account number"].isin(dupe_accts)

#Identify added accounts
added_accounts = new_account_set[(new_account_set["duplicate"] == False) & (new_account_set["version"] == "new")]

#Save the changes to excel but only include the columns we care about
writer = pd.ExcelWriter("my-diff-2.xlsx")
diff_output.to_excel(writer,"changed")
removed_accounts.to_excel(writer,"removed",index=False,columns=["account number",
                                         "name","street","city","state","postal code"])
added_accounts.to_excel(writer,"added",index=False,columns=["account number",
                                         "name","street","city","state","postal code"])
writer.save()
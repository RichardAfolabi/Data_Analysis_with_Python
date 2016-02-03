#%%
import os
import operator
import numpy as np
import scipy.stats as scp
import pandas as pd
from lxml import objectify
from collections import Counter
import matplotlib.pyplot as plt
from xml.etree import ElementTree as ET


#%%  What fraction of posts contain the 5th most popular tag?
post_xlspath = "Posts.xlsx"
user_xlspath = "Users.xlsx"
cmnt_xlspath = "Comments.xlsx"
user_records = pd.read_excel(user_xlspath, header=1  )
post_records = pd.read_excel(post_xlspath)
comnt_records = pd.read_excel(cmnt_xlspath, header=1)

#%% What is the Pearson's correlation between a user's reputation and total score from posts (for valid users)?

def tagvalue_extractor(path, tagstring):
    """ Extract tags/data from xml files"""
    
    xmlfile = ET.parse(path)
    root = xmlfile.getroot()
    root_rows = root.findall("./row")
    
    alltags = []
    for k in root_rows:
        raw_entry = k.get(tagstring)
        # Clean posts with missing entry
        if raw_entry == None:
            raw_entry = 'Missing'
        alltags.append(raw_entry)
    return alltags
    
    
userpath = "Users.xml"
postpath = "Posts.xml"


pscr = tagvalue_extractor(postpath, "Score")
post_score = np.array([int(rep) for rep in pscr])
post_userid = tagvalue_extractor(postpath, "OwnerUserId")

non_unique = [(post_userid[k],post_score[k]) for k in range(len(post_score))]
#print(non_unique[:8])
#print(len(non_unique))

raw_usrrep = tagvalue_extractor(userpath, "Reputation")
user_rep = np.array([int(rep) for rep in raw_usrrep])
usrId = tagvalue_extractor(userpath, "AccountId")

unique = [(usrId[k],user_rep[k]) for k in range(len(user_rep) )]
#print(unique[:8])
#print(len(unique))

#%%
valid_users = {key:0 for (key,value) in unique}


for (key, value) in non_unique:
    if key in valid_users.keys():
        valid_users[key] += value

# check 
#vd = {key:value for (key, value) in valid_users.items() if value>0}

# Pearson test using scipy module
valid_users_score = np.array([value for value in valid_users.values()])


prsnr_test = scp.stats.pearsonr(user_rep, valid_users_score)

#
print("(p-corr, p-signf) = ", prsnr_test)

print("Pearson corr test : %.8f" %prsnr_test[0])

#%%
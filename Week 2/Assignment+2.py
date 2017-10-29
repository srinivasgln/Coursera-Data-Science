
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.2** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning. 
# 
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

# In[10]:

import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
    if col[:2]=='01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    if col[:2]=='02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    if col[:2]=='03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
    if col[:1]=='№':
        df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index) 
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()


# ### Question 0 (Example)
# 
# What is the first country in df?
# 
# *This function should return a Series.*

# In[11]:

# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_one():
    # This function returns the row for Afghanistan, which is a Series object. The assignment
    # question description will tell you the general format the autograder is expecting
   return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_one() 



# ### Question 1
# Which country has won the most gold medals in summer games?
# 
# *This function should return a single string value.*

# In[88]:

def answer_one():
    Most_GM=df.loc[df['Gold'].argmax()].name
    return Most_GM
                  
answer_one()
                  


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
# 
# *This function should return a single string value.*

# In[89]:

def answer_two():
    return df.loc[(df['Gold']-df['Gold.1']).argmax()].name
answer_two()


# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count? 
# 
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
# 
# Only include countries that have won at least 1 gold in both summer and winter.
# 
# *This function should return a single string value.*

# In[142]:

def answer_three():
    rG=df.loc[(df['Gold']>=1)&(df['Gold.1']>=1)]
    rG['rgn']=(rG['Gold']-rG['Gold.1'])/(rG['Gold.2'])
    rgn_1=rG.sort_values(['rgn'],ascending=False).head(1)
    rgn=rgn_1.index[0]
    return rgn
answer_three()


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created.
# 
# *This function should return a Series named `Points` of length 146*

# In[43]:

def answer_four():
    Points=pd.Series((df['Gold.2']*3)+(df['Silver.2']*2+(df['Bronze.2']*1)))
    
    return Points

answer_four()


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov/popest/data/counties/totals/2015/CO-EST2015-alldata.html). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](http://www.census.gov/popest/data/counties/totals/2015/files/CO-EST2015-alldata.pdf) for a description of the variable names.
# 
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
# 
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
# 
# *This function should return a single string value.*

# In[1]:

import pandas as pd
import numpy as np
census_df = pd.read_csv('census.csv')
census_df.head()

        


# In[2]:

def answer_five():
    us_states=dict()
    county=census_df['CTYNAME'].tolist()
    #print('total number of county is',len(county) )
    state=dict()
    count=0
    dic_c=0
    ls=None
    st=None
    for r,cod,st in zip(census_df.CTYNAME,census_df.COUNTY,census_df.STATE):
        count=count+1
        for j in census_df.loc[(census_df['CTYNAME']==r)&(census_df['COUNTY']==cod)&
                (census_df['STATE']==st)]['STNAME']:

            us_states[j]=us_states.get(j,0)+1
            dic_c=dic_c+1
    for state,count in us_states.items():
        if ls is None or count>ls:
            st=state
            ls=count
    return st
answer_five()


# ### Question 6
# Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
# 
# *This function should return a list of string values.*

# In[3]:

def answer_six():
    for i in census_df['STNAME'].unique():
        simp=census_df[(census_df.STNAME==i)&(census_df.SUMLEV==50)].sort_values(['CENSUS2010POP']
          ,ascending=False).head(3)
        try:
            ls=pd.concat([ls,simp],axis=0)
        except:
            ls=pd.concat([simp],axis=1)
    StateTotal=ls.groupby('STNAME').CENSUS2010POP.sum().sort_values(ascending=False).head(3)
    lst_st=StateTotal.index.tolist()
    print(ls.shape)
    
    #print(census_df.shape,len(census_df['STNAME'].unique()),simp.shape,ls.shape,StateTotal.shape)
    return lst_st
answer_six()


# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
# 
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
# 
# *This function should return a single string value.*

# In[37]:

def answer_seven():
    pd.options.mode.chained_assignment = None
    '''to avoid the error messages f or using chained assignment'''
    rf=census_df.copy()
    zf=rf[(rf.SUMLEV==50)]
    zf.shape
    zf['m_and_m']=zf[zf.columns[9:15]].apply(np.max,axis=1)-zf[zf.columns[9:15]].apply(np.min,axis=1)
    #max_cty=zf.loc[zf['m_and_m'].argmax()]['CTYNAME']
    #type(max_cty)
    return zf.loc[zf['m_and_m'].argmax()]['CTYNAME']
answer_seven()



# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column. 
# 
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
# 
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[41]:

def answer_eight():
    rf=census_df.copy()
    #dresult=rf[(rf.CTYNAME.str.startswith('Washington')&(rf.SUMLEV==50)&(rf.POPESTIMATE2015>rf.POPESTIMATE2014)&((rf.REGION==1)|(rf.REGION==2)))][['REGION','STNAME','CTYNAME','POPESTIMATE2015','POPESTIMATE2014']]
    dresult=rf[(rf.CTYNAME.str.startswith('Washington')&(rf.SUMLEV==50)&(rf.POPESTIMATE2015>rf.POPESTIMATE2014)&((rf.REGION==1)|(rf.REGION==2)))][['STNAME','CTYNAME']]
    #print(dresult)
    return dresult
answer_eight()


# In[ ]:




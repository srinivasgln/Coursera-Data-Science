
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[2]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[3]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}


# In[2]:

import re 
import pandas as pd
def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the university_towns.txt list. The format of the DataFrame should be: DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], columns=["State", "RegionName"] )
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    States_RegionN = list()

    with open('university_towns.txt') as File:
        for line in File:
            finding_st = re.match('(.+)\[edit\]',line) 
            if finding_st:
                state=(finding_st).group(1)
            else:
                RegionName = line.split('(')[0].strip()
                States_RegionN.append([state,RegionName])


    Result = pd.DataFrame(States_RegionN,columns=["State","RegionName"])
    return Result
get_list_of_university_towns()


# 

# In[5]:

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    GDP = pd.read_excel('gdplev.xls',skiprows=219,headers=None,usecols=range(4,7))
    GDP.columns=[['Season','GDP_Current_$','GDP_2009_$']]
    
    #A recession is defined as starting with two consecutive quarters of GDP decline,
    # and ending with two consecutive quarters of GDP growth.
    for i in range(2,len(GDP)):
        
        if (GDP.iloc[i][1]<GDP.iloc[i-1][1]) and (GDP.iloc[i-1][1]<GDP.iloc[i-2][1]):
            #print('The recession starts at',GDP.iloc[i-2][0])
            return GDP.iloc[i-2][0]
    #print(GDP)
      
get_recession_start()


# In[6]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
    GDP = pd.read_excel('gdplev.xls',skiprows=219,headers=None,usecols=range(4,7))
    GDP.columns=[['Season','GDP_Current_$','GDP_2009_$']]
    Recession_start=get_recession_start()
    rs=GDP.loc[GDP['Season']==Recession_start].index[0]
    GDP_E=GDP.iloc[rs:]
    for i in range(2,len(GDP_E)):
        if (GDP_E.iloc[i][1]>GDP_E.iloc[i-1][1]) and (GDP_E.iloc[i-1][1]>GDP_E.iloc[i-2][1]):
            #print('The recession ended at',GDP_E.iloc[i][0])
            return GDP_E.iloc[i][0]
    
get_recession_end()     
    


# In[7]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3
    A recession bottom is the quarter within a recession which had the lowest GDP.'''
    GDP = pd.read_excel('gdplev.xls',skiprows=219,headers=None,usecols=range(4,7))
    GDP.columns=[['Season','GDP_Current_$','GDP_2009_$']]
    Recession_start=get_recession_start()
    rs=GDP.loc[GDP['Season']==Recession_start].index[0]
    Recession_end=get_recession_end()  
    re=GDP.loc[GDP['Season']==Recession_end].index[0]
    
    Recc_Timeline=GDP.iloc[rs:re+1]
    Rec_Bottom=Recc_Timeline['GDP_Current_$'].min()
    RB_Quarter=Recc_Timeline.loc[Recc_Timeline['GDP_Current_$']==Rec_Bottom].index[0]
    #print('The recession bottom is at',GDP.iloc[RB_Quarter]['Season'])    
    bottom=GDP.iloc[RB_Quarter]['Season']
    return bottom
    
get_recession_bottom()


# In[3]:

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    HousingData=pd.read_csv('City_Zhvi_AllHomes.csv')
    HousingData.drop(['Metro','CountyName','RegionID','SizeRank'],axis=1,inplace=True)
    states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
    Seasons=list()
    for year in range(2000,2017):
        for q in ['q1','q2','q3','q4']:
            Seasons.append((str(year)+q))
    
    #print(Seasons)
    #HousingData['State'] = HousingData.replace({'State':states})
    HousingData['State'] = HousingData['State'].map(states)
    HousingData.set_index(['State','RegionName'],inplace=True)
    #Drop Data before 2000s i.e first 45 columns
    HousingData.drop(list(HousingData.columns)[0:45],axis=1,inplace=True)
    
    Qtrs=list()
    for i in range(0, len(list(HousingData.columns)), 3):
        qt=HousingData.columns[i:i+3].tolist()
        Qtrs.append(qt)
    #Qtrs = [list(HousingData.columns)[x:x+3] for x in range(0, len(list(HousingData.columns)), 3)]
    Seasons=Seasons[:67]
    for col,q in zip(Seasons,Qtrs):
        HousingData[col] = HousingData[q].mean(axis=1)
    FinalData = HousingData[Seasons]
    #print(FinalData.loc["Texas"].loc["Austin"].loc["2010q3"])
    

    
    
    #print(len(Qtrs),len(Seasons))
    #print(FinalData.shape)
    #print(len(Seasons))
    return FinalData
convert_housing_data_to_quarters()


# In[10]:


def run_ttest():
    from scipy.stats import ttest_ind
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    CollegeTowns= get_list_of_university_towns()['RegionName']
    #CollegeTowns=CollegeTowns['RegionName']
    #print(CollegeTowns)
    lst_ut=set(CollegeTowns)
    #RStart=get_recession_start() '2008q3'
    #REnd=get_recession_end()
    #RBottom=get_recession_bottom() '2009q2'
    Hdata = convert_housing_data_to_quarters()
    
    Hdata = Hdata.loc[:,'2008q3':'2009q2']
    #Hdata = Hdata.loc[:,RStart:RBottom]
    Hdata.reset_index(inplace=True)
    def PR(x):
        return (x['2008q3'] - x['2009q2'])/x['2008q3']
    Hdata['PriceRatio'] = Hdata.apply(PR,axis=1)
    Hdata['Univ_town']=0
    
    for i in Hdata['RegionName']:
        if i in lst_ut:
            Hdata.loc[Hdata['RegionName']==i,['Univ_town']]=1
        else:
            continue
    #Hdata['up&down']=(Hdata['2008q3'] - Hdata['2009q2'])/Hdata['2008q3']
    #print(Hdata)
    
    not_univ_town = Hdata[Hdata['Univ_town']==0].loc[:,'PriceRatio'].dropna()
    Univ_town = Hdata[Hdata['Univ_town']==1].loc[:,'PriceRatio'].dropna()
    def better():
        if not_univ_town.mean() < Univ_town.mean():
            return 'non-university town'
        else:
            return 'university town'
    p_val = list(ttest_ind(not_univ_town,Univ_town))[1]
    result = (True,p_val,better())
    return result
    
    '''Hdata=Hdata[RecPeriod]
    Hdata = Hdata.loc[:,RStart:RBottom]
    Hdata.sort_index(inplace=True)
    df_ut=pd.merge(CollegeTowns,Hdata,how='inner',right_index=True , 
                   left_on=['State','RegionName']).set_index(['State','RegionName'])
    df_Nut = Hdata.loc[~Hdata.index.isin(df_ut.index)]
    df_ut['PriceRatio']= df_ut[RStart]/df_ut[RBottom]
    df_Nut['PriceRatio']= df_Nut[RStart]/df_Nut[RBottom]
    s,p=(ttest_ind(df_ut.dropna()['PriceRatio'],df_Nut.dropna()['PriceRatio']))
    
    hypothesis = False
    if p < 0.01:
        
        hypothesis = True
    print(hypothesis,p)
        
    
    
    #return (result,p_value,test())'''

    
run_ttest()


# In[ ]:




# In[ ]:




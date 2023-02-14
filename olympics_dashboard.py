# -*- coding: utf-8 -*-
"""
Created on Thu Feb  9 12:31:01 2023

@author: Zeeshan Waseem - CDA - Karachi AI
"""



## Importing necessary libraries

import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Setting app to use a wide layout 
st.set_page_config(layout = "wide")

# Reading datasets from local repo

df = pd.read_csv('athlete_events.csv')
df_noc = pd.read_csv('noc_regions.csv')

# ========================================================================
#               Data Pre=processing (Cleaning/Conversion) 
# ========================================================================
'''
# 1.  The column types are Ok. Only Age can be converted into int64 however the net result is same so we don't go for typecasting overhead
#      I confirmed that age dimesion can safely be converted since no age is in fractions using following command
#       df[(df['Age']-round(df['Age']))>0]

# 2.  As part of data cleaning, we check out NULL values and found many 
#     The most null value were from Medal column, but that's alright since not every participant wins medal 
#     the other missing attributes were age , height and weight. I checked the total number of missing values where
#     medals were won too so those were in good number too. Moreover, the assignment requirement doesn't cater/emphaisizes
#     on these dimensions' values hence we can't just drop these missing value however we jsut 
#     replace them with suitable ones

'''

#           ** Methodology: Step 1 **
### Firstly we'll check that if 0, 0, 0 and "NM" (No Medal) are not already assigned to age, height, weight and medal respectively  

print(df[df['Age'] == 0].count())
print(df[df['Height'] == 0].count())
print(df[df['Weight'] == 0].count())
print(df[df['Medal'] == 'NM'].count())



###             Methodology: Step 2

# Secondly, we'll assign following values to null corresponding values of mentioned below columns:-
#  Age: null --> 0
#  Height: null --> 0
#  Weight: null --> 0 
#  Medal: null --> "NM" 


# Setting/Replacing Null values of Age dimesion with 0 and verifying the result
df['Age'].fillna(0, inplace = True)
print(df[df['Age'].isna()])

# Setting/Replacing Null values of Medal dimesion with "NM"and verifying the result
df['Medal'].fillna("NM", inplace = True)
print(df[df['Medal'].isna()])

# Setting/Replacing Null values of Height dimesion with 0 and verifying the result
df['Height'].fillna(0, inplace = True)
print(df[df['Height'].isna()])

# Setting/Replacing Null values of Weight dimesion with 0 and verifying the result
df['Weight'].fillna(0, inplace = True)
print(df[df['Weight'].isna()])



##              Duplication Check  
#   After manual inspection of data set, it is clear that no dimension is unique since each dimension can have same value 
#   over the length of data. Even ID column is bind to Name of athelete and can be duplicated However, no two
#   rows should be same so we check for duplication by all columns.

# first we sort data by ID and then by index 
df=df.sort_values(by='ID')
df= df.sort_index(ascending=True)

df[df.duplicated()].shape


# So we have 1385 duplicated values as confirmed by manual inspection as well. So we drop them
df_clean=df.drop_duplicates()

# After duplucation removal we have 269731 records available. Our data is free from Nan/Null and duplicated values
df_clean.shape


##                     *** Dealing with NOC Data ***
## Generating  a new dimension "country" based on region and notes(if any). Afterwards, dropping unnecesssary column "notes, region" 
## and merging NOC table with athletes so as to get country/region names. We couldn't 
## use Team name as country name b/c on manual inspection it was revealed that some of the Team were quite different  like 
## "GyoshuII, New York Athletic Club #2-4, Large boat etc"

df_noc["country"] = df_noc["region"].str.cat(df_noc["notes"], sep = " - ")
df_noc['country']=df_noc['country'].fillna(df_noc['region'])
df_noc['country']=df_noc['country'].fillna(df_noc['notes'])


df_noc=df_noc.drop(['notes', 'region'], axis=1)
data = pd.merge(df_clean, df_noc, on='NOC', how='left')

 
# ========================================================================
##                       Setting up layout and display 
##                        (Data is READY to be USED)
# ========================================================================




# Setting css style for title and sub-title usinf custom functions

def title(url):
     st.markdown(f'<p style="background-color:#00bfff;color:#2B547E;font-family: Lucida Bright;font-size:42px;border: 1px solid #2B547E;border-radius:3%;padding: 0px;text-align:center;">{url}</p>', unsafe_allow_html=True)

def info(url):
     st.markdown(f'<p style="background-color:#2B547E;color:#FFFFFF;font-family:Goudy Old Style;font-size:22px;border-radius:8%;padding: 8px;text-align:center;">{url}</p>', unsafe_allow_html=True)

title("Olympic History Dashboard")
info("Created by: Zeeshan Waseem")

# This container will be displayed below the text above
def selectbox(url, url1):
    st.markdown(" div[role=“listbox”] ul { ** background-color: #99cfdd;**};div[data-baseweb=“select”] > div {background-color: #99cfdd;} div[data-baseweb=“input”] > div {background-color: #99cfdd;**} ")



## ------------------------- CONATINER ! (Select box - Country) -----------------
# This container will be displayed below the first one
with st.container():
    col1, col2, col3 = st.columns((1,98,1))

    with col2:
       
        countries=data['country'].sort_values(ascending=True).unique()
        selected_country=col2.selectbox("",countries)
        
        ## Calculating Total number of participants and total number of Gold,
        ## Silver and Bronze medal won pertaning to the seleceted country
        
        tot_participant=data[data['country']==selected_country]['ID'].count()
        bronze=data[(data['country']==selected_country) & (data['Medal']=='Bronze')].count()[0]
        gold=data[(data['country']==selected_country) & (data['Medal']=='Gold')].count()[0]
        silver=data[(data['country']==selected_country) & (data['Medal']=='Silver')].count()[0]

##----------------------------------------------------------------------------------

## ------------------------- CONATINER 2 (Misc: Metrics) ---------------------------

with st.container():
    col1, col2, col3, col4 = st.columns((25,25,25,25))

    with col1:
        # Customized heading for metric contents
        def header(url):
            st.markdown(f'<p style="color:#007C80;font-family:Hoefler Text;font-size:29px;border-bottom: 2px solid #007C80;border-radius:1%;padding: 3px;font-weight:bold;">{url}</p>', unsafe_allow_html=True)
        
        header("Total Participants")
        st.metric("Total:",tot_participant,label_visibility="collapsed")
      
  
    with col2:
        # Customized heading for metric contents
        def header(url):
            st.markdown(f'<p style="color:#FBB117;font-family:Hoefler Text;font-size:29px;border-bottom: 2px solid #FBB117;border-radius:1%;padding: 3px;font-weight:bold;">{url}</p>', unsafe_allow_html=True)
        header("Gold Medals")
        st.metric("Gold:",gold,label_visibility="collapsed")

    with col3:
        # Customized heading for metric contents
        def header(url):
            st.markdown(f'<p style="color:#A9A9A9;font-family:Hoefler Text;font-size:29px;border-bottom: 2px solid grey;border-radius:1%;padding: 3px;font-weight:bold;">{url}</p>', unsafe_allow_html=True)
        header("Silver Medals")
        st.metric("Silver:",silver, label_visibility="collapsed")

    with col4:
        # Customized heading for metric contents
        def header(url):
            st.markdown(f'<p style="color:#804A00;font-family:Hoefler Text;font-size:29px;border-bottom: 2px solid #804A00;border-radius:1%;padding: 3px;font-weight:bold;">{url}</p>', unsafe_allow_html=True)
        header("Bronze Medals")
        st.metric("Bronze:",bronze,label_visibility="collapsed")

##----------------------------------------------------------------------------------              

##               Container 3 - Data Collection Queries & Customization

## ----------------------------------------------------------------------------------


# 1. Line Plot Data - Getting selected country's Medal won over the period of olympics time

year_wises_medal_count=data[(data['country']==selected_country) & (data['Medal']!='NM')].groupby(['Medal','Year'])['Medal'].count().unstack(0)
type_of_medals=year_wises_medal_count.count().shape[0]

# Setting customized pallete colors
if type_of_medals==1:
    selected_palette=['green']
elif type_of_medals==2:
    selected_palette=['red', 'blue']
else:
    selected_palette=['green', 'red', 'blue']
    
    
# 2. Top athelet Data

top_athlete_data=data[(data['country']==selected_country) & (data['Medal']!='NM')]

top_athlete_order = data[(data['country']==selected_country) & (data['Medal']!='NM')]['Name'].value_counts().head(5).index


# 3. Top Sports Data

subset_sport=data[(data['country']==selected_country) & (data['Medal']!='NM')].groupby(['Sport'])['Medal'].count().nlargest(5)


## -------------------CONATINER 3 (1. Line Plot, 2. Bar Plot, 3. Data Frame) ---------------------------

with st.container():
    col1, col2, col3 = st.columns((33,33,33))
    
    ##### Line Plot: Dsiplaying plot for slected country's Medal Won over years
    with col1:
        # Customized heading for metric contents
        def header(url):
            st.markdown(f'<p style="background-color:#007C80;color:#FFFFFF;font-family:Hoefler Text;font-size:25px;border-radius:2%;padding: 8px;text-align:center;">{url}</p>', unsafe_allow_html=True)
        header("Medal Won Over Years") 
        
        # Exception handling for EMPTY dataframes 
        if not(year_wises_medal_count.empty):
            top_plot = plt.figure()
            sns.lineplot(data=year_wises_medal_count, palette=selected_palette)
            plt.title('Total Medals Over Years')
            plt.xlabel('Year')
            plt.ylabel('Medal Count')
            st.pyplot(top_plot)
        else:
            st.warning('Sorry! '+selected_country+'  did not won any medal in any year', icon="⚠️")
        
        
    ##### Bar plot: showing top 5 athelete with most medal won - overall
    with col2:
        # Customized heading for metric contents
        def header(url):
            st.markdown(f'<p style="background-color:#FFA500;color:#FFFFFF;font-family:Hoefler Text;font-size:25px;border-radius:2%;padding: 8px;text-align:center;">{url}</p>', unsafe_allow_html=True)
            
        header("  Top 5 Athelets")
        
        # Exception handling for EMPTY dataframes 
        if not(top_athlete_data.empty):
            top_plot = plt.figure()
            sns.countplot(data=top_athlete_data, y='Name', order=top_athlete_order)
            #plt.title('Top5 5 Athletes with Most Medals')
            plt.xlabel('No. of awrded medals')
            plt.ylabel('Athlete Name')
            sns.set(rc={'figure.figsize':(6,8)})
            st.pyplot(top_plot)
        else:
            st.warning('Sorry! No Athlete won any medal for '+selected_country, icon="⚠️")
        
        
    ##### DataFrame: showing top 5 Sportshaving most of the medals - overall    
    with col3:
        # Customized heading for metric contents
        def header(url):
            st.markdown(f'<p style="background-color:#6F4E37;color:#FFFFFF;font-family:Hoefler Text;font-size:25px;border-radius:2%;padding: 8px;text-align:center;">{url}</p>', unsafe_allow_html=True)
        def dataFrame(url,url1):
            st.markdown(f'<p style="background-color:#6F4E37;color:#FFFFFF;font-family:Hoefler Text;font-size:25px;border-radius:2%;padding: 8px;text-align:center;">{url}</p>', unsafe_allow_html=True)
        
        header("  Top 5 Sports")
        
        # Exception handling for EMPTY dataframes 
        if not(subset_sport.empty):
            col3.dataframe(subset_sport,use_container_width=True)
        else:
            st.warning('Sorry! No sports won any medal for '+selected_country, icon="⚠️")
          
        
##----------------------------------------------------------------------------------              

##               Container 4 - Data Collection Queries & Customization

## ----------------------------------------------------------------------------------

# 1. Histogram Data - Getting data for distributoin of medlas as per age
medals_hist=data[(data['country']==selected_country) & (data['Medal']!='NM') & (data['Age']!=0) ]

# 2. Pie Chart Data - Number of medals as per Sex
medals_gender_wise=data[(data['country']==selected_country) & (data['Medal'].isin(['Gold','Silver','Bronze']))].groupby(['Sex','Medal'])['Sex'].count()


# 3. Vetical Bar Chart Data - Filtering out out dataframe to get right number of medals w.r.t Season
medals_season=data[(data['country']==selected_country) & (data['Medal']!='NM')]

#======================================================================================

## -------------------CONATINER 4 (1. Histogram, 2. Pie Chart, 3. Grouped Bar Chart) ---------------------------

with st.container():
    col1, col2, col3 = st.columns((33,33,33))
    
    ##### Histogram: showing medal won distribution age-wise
    with col1:
        # Customized heading for metric contents
        def header(url):
            st.markdown(f'<p style="background-color:#008000;color:#FFFFFF;font-family:Hoefler Text;font-size:25px;border-radius:2%;padding: 8px;text-align:center;">{url}</p>', unsafe_allow_html=True)
       
        header("Medals Won Age-wise")
        
        # Exception handling for EMPTY dataframes 
        if not(medals_hist.empty):
            hist_plot = plt.figure()
            sns.histplot(data=medals_hist, x="Age", bins=10)
            #plt.title('Medal Count Age-wise')
            plt.xlabel('Age of Athlete')
            plt.ylabel('Medals Won')
            sns.set(rc={'figure.figsize':(6,4)})
            st.pyplot(hist_plot)
        else:
            st.warning('Sorry! No medals, for any age group, were found for '+selected_country, icon="⚠️")
          
        
    ##### Pie Chart: showing Summarized number of Medals bifurcated by Gender
    with col2:
        # Customized heading for metric contents
        def header(url):
            st.markdown(f'<p style="background-color:#5865F2;color:#FFFFFF;font-family:Hoefler Text;font-size:25px;border-radius:2%;padding: 8px;text-align:center;">{url}</p>', unsafe_allow_html=True)

        header("Medals Gender-wise")
        
        # Exception handling for EMPTY dataframes
        if not(medals_gender_wise.empty):
            fig1, ax1 = plt.subplots()
            wedges=ax1.pie(medals_gender_wise, labels=medals_gender_wise.index, autopct='%1.1f%%')
            st.pyplot(fig1)
        else:
            st.warning('Sorry! No medals, for any gender, were found for '+selected_country, icon="⚠️")
          
     
    ##### Vertical Bar Chart: showing number of medals received in each season
    with col3:
        # Customized heading for metric contents
        def header(url):
            st.markdown(f'<p style="background-color:#E4287C;color:#FFFFFF;font-family:Hoefler Text;font-size:25px;border-radius:2%;padding: 8px;text-align:center;">{url}</p>', unsafe_allow_html=True)

        header("Medals Season-wise")
        
        # Exception handling for EMPTY dataframes
        if not(medals_season.empty):
            fig=sns.catplot(data=medals_season,kind='count',x='Season',hue='Medal')
            st.pyplot(fig)
        else:
            st.warning('Sorry! No medals, in any season, were found for '+selected_country, icon="⚠️")
           

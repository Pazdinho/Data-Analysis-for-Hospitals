# write your code here
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests

#loading data set and concatenation
def stage1():
    pd.set_option('display.max_columns', 8)
    sport = pd.read_csv('test/sports.csv')
    gen = pd.read_csv('test/general.csv')
    pren = pd.read_csv('test/prenatal.csv')

    sport.columns = gen.columns
    pren.columns = gen.columns
    #concatenatation
    hospital = pd.concat([gen, pren, sport], ignore_index=True)
    #dropping unnamed column
    hospital.drop(columns = ['Unnamed: 0'], inplace=True)
    return hospital

#cleaning dataset
def stage2(hospital):
    #deleteing all rows that are fully empty
    hospital.dropna(axis=0, how='all',inplace=True)
    #reconciliation of nomenclature
    hospital.gender.replace({'man': 'm', 'male': 'm', 'woman': 'f', 'female': 'f'}, inplace = True)
    #getting rid of NaN
    hospital.gender.fillna('f',inplace = True)
    list = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
    for i in list:
        hospital[i].fillna(0,inplace = True)
    return hospital

#looking for answers
def stage3(hospital):
    #Which hospital has the highest number of patients?
    print(hospital.hospital.value_counts()[0])

    #What share of the patients in the general hospital suffers from stomach-related issues?
    print(round(len((hospital.diagnosis[(hospital.diagnosis == 'stomach') & (hospital.hospital == 'general')]))/len(hospital[hospital.hospital == 'general']),3))

    #What share of the patients in the sports hospital suffers from dislocation-related issues?
    print(round(len((hospital.diagnosis[(hospital.diagnosis == 'dislocation') & (hospital.hospital == 'sports')]))/len(hospital[hospital.hospital == 'sports']),3))

    #What is the difference in the median ages of the patients in the general and sports hospitals?
    h = hospital.groupby('hospital').agg({'age':'median'}).to_dict()
    print(h['age']['general']-h['age']['sports'])

    # In which hospital the blood test was taken the most often
    print(hospital[hospital.blood_test == 't'].groupby('hospital').agg({'hospital': ['count']}).to_dict()['hospital', 'count']['prenatal'])

#plotting
def stage4(hospital):

    hospital.age.plot(kind='hist')
    plt.show()
    hospital['diagnosis'].value_counts().plot(kind='pie',autopct='%1.0f%%',subplots=True)
    plt.show()
    plt.violinplot(dataset = [hospital[hospital.hospital =='general']['height'].values,
                                hospital[hospital.hospital =='prenatal']['height'].values,
                                hospital[hospital.hospital =='sports']['height'].values])
    plt.show()

    # based on plots its possible to answer questions below
    #What is the most common age of a patient among all hospitals? Based on histogram
    print('The answer to the 1st question: 15-35')
    #What is the most common diagnosis among patients in all hospitals?  Based on pie chart
    print('The answer to the 2nd question: pregnancy')
    #What is the main reason for the gap in values? Based on violin plot
    print("The answer to the 3rd question: It's because height in sport hospital was measured in feet")

stage1()
stage2(stage1())
#stage3(stage2(stage1()))
stage4(stage2(stage1()))

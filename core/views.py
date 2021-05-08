"""
Created on Thu May  6 22:11:47 2021

@author: Aishwarya Ganesh
"""


from django.shortcuts import render
import json
from rest_framework.response import Response
from rest_framework.views import APIView
import pandas as pd
import numpy as np
from datetime import datetime

class TestView(APIView):
    def get(self,request,*args,**kwargs):
        # Read the Team Information and Project requirement files
        Employee = pd.read_excel (r'./teamInfo.xlsx')
        Project = pd.read_excel (r'./Project.xlsx')
        # Combine the skillset of each employee into a single column
        Employee['Skills'] = Employee[['Skill 1', 'Skill 2', 'Skill 3', 'Skill 4', 'Skill 5']].apply(lambda x: ','.join(x[x.notnull()]), axis = 1)
        # Tokenize the skillset of employees and Skills required by the project
        tokenized_Skills = [e.split(',') for e in Employee['Skills']]
        tokenized_Req = [e.split(',') for e in Project['Skills']]
        m = len(tokenized_Req)
        n = len(tokenized_Skills)
        i=0
        j=0
        # Create a m*n matrix to store the similarity distance between each project and employee
        allocation = [[-1 for x in range(n)] for y in range(m)]
        # Use the Jaccard formula to populate the matrix 
        for proj in tokenized_Req:
           for emp in tokenized_Skills:
               if (Project['Location'][i] == Employee['Prod Build Location'][j]) and (Project['Role Level'][i] == Employee['Role Level'][j]) and (Project['Role'][i] == Employee['Role'][j]):
                   intersection = len(list(set(proj).intersection(emp)))
                   union = (len(proj) + len(emp)) - intersection
                   allocation[i][j] = 1 - (float(intersection)/union)
               j = j+1
           i = i+1
           j=0
        i=0
        j=0
        for proj in tokenized_Req:
           for emp in tokenized_Skills:
               if (allocation[i][j] != -1):
                   allocation[i][j] = allocation[i][j] + (((Employee['resource product end date'][j]).date())-((Project['start_date'][i]).date())).days
               j=j+1
           i=i+1
           j=0
        i=0
        j=0
        for proj in tokenized_Req:
           for emp in tokenized_Skills:
               if (allocation[i][j] == -1):
                   allocation[i][j] = np.nan
               j=j+1
           i=i+1
           j=0
           
        Mapping = [['' for x in range(2)] for y in range(m)]
        i=0
        while i<m:
            Mapping[i][0]=Project['Project'][i]
            i = i+1
        i=0
        for proj in tokenized_Req:
            res= np.where(allocation[i] == np.nanmin(allocation[i]))
            x=min(res[0])
            Mapping[i][1] = Employee['Name'][x]
            j=i+1
            while j < m:
                allocation[j][x] = np.nan
                j = j+1
            i = i+1
        
        i=0
        Project['Resource']=Project['Project']
        while i<m:
            Project['Resource'][i] = Mapping[i][1]
            i = i+1
        
        now = datetime.now()
        file_name = r'Project_Output_' + now.strftime("%m-%d-%Y_%H-%M-%S") + r'.xlsx'
        Project.to_excel(file_name,index=False,sheet_name='Sheet1')
        json = Project.to_json()
        data = {
            'data':'dasd',
            'dasd':'dsdsd'
        }
        return Response(json)
        # return(json)
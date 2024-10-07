from functions import *

group1= ["Hideo Kojima"]
group2= ["game"]

#When groupNot="", it does not add an exclusion criteria.  
groupNot=["Splinter Cell"]

#"COMP", "ENGI", "ARTS", "MATH", "NEUR", "PSYC"
#For more info, visit: https://dev.elsevier.com/sc_search_tips.html
#When subjectAreas is [], it gets from all disciplines.  
subjectAreas= []

#When year="", it gets all the papers ignoring the year.  


#Example 1: You can get up to 5000 papers in a single csv file from 1980 up to present.
"""
q1=Query("testQuery1",[group1, group2], subjectAreas,">",1980, groupNot,"")
getPapers(q1)
"""

#Example 2: You can get up to 5000 papers per year from 2021 to 2023. A csv file for each year with results. 
"""
for year in range(2023, 2020, -1):
   q2=Query("testQuery2",[group1, group2], subjectAreas,"=",year,"","")
   getPapers(q2)
"""

#Example 3: You can use a prequery
"""
prequery='TITLE("game*") OR TITLE("videogame*") AND '
q3=Query("testQuery3",[group1, group2], subjectAreas,">",1980, groupNot,prequery)
"""

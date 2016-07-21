import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
Voterdata = pd.read_csv('SocialCopsChallengeFullyCompleted.csv', index_col = 0, encoding = 'utf-8')
#Voterdata.groupby(['Gender']).Age.value_counts()
#Voterdata.head()
Voterdata.pivot_table(values = 'Serial Number', index = 'Age',columns = 'Gender', aggfunc = 'count')
Voterdata['clean_age'] = Voterdata['Age'].fillna(0)
Voterdata['clean_gender'] = Voterdata['Gender'].fillna('U')
#Voterdata.head()
Voterdata['extra_use_of_age'] = Voterdata['clean_age']
table = Voterdata.pivot_table(values = 'extra_use_of_age', index = 'clean_age', columns = 'clean_gender', aggfunc = 'count')
#Voterdata.head()
#Voterdata.plot()
#plt.show()
table.plot(title = 'Total Voters of Faizabad by sex and Age')
plt.xlabel('Age of the voters')
plt.ylabel('Number of voters')
plt.grid(True)
plt.legend()
plt.savefig('Plotting_Voters_According_To_Their_Ages_And_Gender.jpg', dpi = 200)
plt.show()

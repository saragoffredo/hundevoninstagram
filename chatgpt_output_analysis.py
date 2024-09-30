import pandas as pd

# Set the paths to the ChatGPT output files
ChatGPT_output_run1 = ''
ChatGPT_output_run2 = ''
ChatGPT_output_run3 = ''
OUTPUT_SAVE_PATH = ''


#______________________________________________________________________________________________________________________
df_full1 = pd.read_excel(ChatGPT_output_run1)
df_full2 = pd.read_excel(ChatGPT_output_run2)
df_full3 = pd.read_excel(ChatGPT_output_run3)

dicts = []; dict_per_caption = {}
for j,df_full in enumerate([df_full1, df_full2, df_full3]):
    for i,act in enumerate(df_full['activities']):
        # "act" is supposed to be a string containing a dictionary with the activities and sentiments
        dicts.append(eval(act))
        dict_per_caption.update({i: temp})
        temp = {}
    
    
# count the number of occurrences of each key in the dictionaries
from collections import Counter
bodypart = Counter()
for i in dicts:
    if len(i)==0:
        continue
    if len(i['1']) == 0:
        continue
    bodypart.update(i['1'])
accessory = Counter()
for i in dicts:
    if len(i)==0:
        continue
    if len(i['2']) == 0:
        continue
    accessory.update(i['2'])
activity = Counter()
for i in dicts:
    if len(i)==0:
        continue
    if len(i['3']) == 0:
        continue
    activity.update(i['3'])
location = Counter()
for i in dicts:
    if len(i)==0:
        continue
    if len(i['4']) == 0:
        continue
    location.update(i['4'])
sentiment = Counter()
for i in dicts:
    if len(i)==0:
        continue
    if len(i['5']) == 0:
        continue
    sentiment.update(i['5'])
people = Counter()
for i in dicts:
    if len(i)==0:
        continue
    if len(i['6']) == 0:
        continue
    people.update(i['6'])
print(f'Body part: {bodypart.most_common()}')
print(f'Accessory: {accessory.most_common()}')
print(f'Activity: {activity.most_common()}')
print(f'Location: {location.most_common()}')
print(f'Sentiment: {sentiment.most_common()}')
print(f'People: {people.most_common()}')

# here we check the percentage of the rows in "dict_per_caption" which have a length of >0 in the "bodypart" field, i.e. 1 key
tot_rows = len(dict_per_caption);
rows_with_bodypart = len([1 for x in dict_per_caption.keys() if len(dict_per_caption[x].get('1',''))>0])
print(f'Percentage of rows with a bodypart: {rows_with_bodypart/tot_rows*100}%')
rows_with_accessory = len([1 for x in dict_per_caption.keys() if len(dict_per_caption[x].get('2',''))>0])
print(f'Percentage of rows with an accessory: {rows_with_accessory/tot_rows*100}%')
rows_with_activity = len([1 for x in dict_per_caption.keys() if len(dict_per_caption[x].get('3',''))>0])
print(f'Percentage of rows with an activity: {rows_with_activity/tot_rows*100}%')
rows_with_location = len([1 for x in dict_per_caption.keys() if len(dict_per_caption[x].get('4',''))>0])
print(f'Percentage of rows with a location: {rows_with_location/tot_rows*100}%')
rows_with_sentiment = len([1 for x in dict_per_caption.keys() if len(dict_per_caption[x].get('5',''))>0])
print(f'Percentage of rows with a sentiment: {rows_with_sentiment/tot_rows*100}%')
rows_with_people = len([1 for x in dict_per_caption.keys() if len(dict_per_caption[x].get('6',''))>0])
print(f'Percentage of rows with people: {rows_with_people/tot_rows*100}%')


# make a excel file with the results
bodypart_df = pd.DataFrame(bodypart.items(), columns=['Body Part', 'Count'])
accessory_df = pd.DataFrame(accessory.items(), columns=['Accessory', 'Count'])
activity_df = pd.DataFrame(activity.items(), columns=['Activity', 'Count'])
location_df = pd.DataFrame(location.items(), columns=['Location', 'Count'])
sentiment_df = pd.DataFrame(sentiment.items(), columns=['Sentiment', 'Count'])
people_df = pd.DataFrame(people.items(), columns=['People', 'Count'])

#normalize the second row of each dataframe by dividing by 3 each value
bodypart_df['Count'] = bodypart_df['Count']/3
accessory_df['Count'] = accessory_df['Count']/3
activity_df['Count'] = activity_df['Count']/3
location_df['Count'] = location_df['Count']/3
sentiment_df['Count'] = sentiment_df['Count']/3
people_df['Count'] = people_df['Count']/3

# lets add percentages
bodypart_df['Percentage'] = bodypart_df['Count']/rows_with_bodypart*100
accessory_df['Percentage'] = accessory_df['Count']/rows_with_accessory*100
activity_df['Percentage'] = activity_df['Count']/rows_with_activity*100
location_df['Percentage'] = location_df['Count']/rows_with_location*100
sentiment_df['Percentage'] = sentiment_df['Count']/rows_with_sentiment*100
people_df['Percentage'] = people_df['Count']/rows_with_people*100

# order the values by count
bodypart_df = bodypart_df.sort_values(by='Count', ascending=False)
accessory_df = accessory_df.sort_values(by='Count', ascending=False)
activity_df = activity_df.sort_values(by='Count', ascending=False)
location_df = location_df.sort_values(by='Count', ascending=False)
sentiment_df = sentiment_df.sort_values(by='Count', ascending=False)
people_df = people_df.sort_values(by='Count', ascending=False)



# remove fields where the column has length 0
bodypart_df = bodypart_df[bodypart_df['Body Part'].apply(lambda x: len(x)>0)]
accessory_df = accessory_df[accessory_df['Accessory'].apply(lambda x: len(x)>0)]
activity_df = activity_df[activity_df['Activity'].apply(lambda x: len(x)>0)]
location_df = location_df[location_df['Location'].apply(lambda x: len(x)>0)]
sentiment_df = sentiment_df[sentiment_df['Sentiment'].apply(lambda x: len(x)>0)]
people_df = people_df[people_df['People'].apply(lambda x: len(x)>0)]

# Creating a dictionary of dataframes
dfs = {
    'Body Part': bodypart_df,
    'Accessory': accessory_df,
    'Activity': activity_df,
    'Location': location_df,
    'Sentiment': sentiment_df,
    'People': people_df
}

# Saving the dataframes to an Excel file with each dataframe on a separate sheet
with pd.ExcelWriter(OUTPUT_SAVE_PATH) as writer:
    for sheet_name, df in dfs.items():
        df.to_excel(writer, sheet_name=sheet_name, index=False)



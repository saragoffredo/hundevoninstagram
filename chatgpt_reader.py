import pandas as pd
from collections import Counter
from openai import OpenAI # pip install openai
import os

SAVE_FILE_PATH = ''
PATH_FILE_XLSX_WITH_INSTAGRAM_DATA = ''
gpt_key ='YOUR_CHAT_GPT_SECRET_KEY'

# _________________________________________________________________________________________
# Excel files with columns: 'hashtag', 'number', 'link', 'caption'
df_full = pd.read_excel(PATH_FILE_XLSX_WITH_INSTAGRAM_DATA) 


# total words in captions:
counter = 0
err = 0
for caption in df_full['caption']:
    try:
        counter += len(caption.split())
    except:
        err += 1
print('Total words in captions: ', counter)

# add an empty column to df_full
if 'activities' not in df_full.columns:
    df_full['activities'] = ''


client = OpenAI(api_key=gpt_key)



CHAT_GPT_PROMPT = '''Analysiere die folgenden Captions aus dem Sozialnetzwerk Instagram. Es handelt sich um Captions, bei denen einige Frauen um den eigenen Hund schreiben, als wäre er das eigene Kind, oder um Caption, bei denen der Hund fiktiv über das eigene Frauchen (Mutter bzw. Mama) oder die eigene Familie spricht. 
Untersuche in den Texten folgende Aspekte und liste sie mit Keywords auf: 
1.	Aussehen oder explizit benannte Körperteile des Hundes. Wähle ein Wort aus der Liste aus. Wenn du nichts findest, dann schreib, welcher Körperteil explizit im Text benannt wird. Liste: [Pfote, Ohr, Nase, Maul]. Achtung: Der Körperteil muss ausschließlich im Text erscheinen und nicht bei den Hashtags. Wenn du keine Information zum Aussehen oder zu den Körperteilen im Text findest, dann lass das Feld leer. 
2.	Accessoires, die der Hund trägt, oder Frisur des Hundes. Wähle das Wort ausschließlich aus der Liste aus. Liste: [Accessoire, Kleidungsstück, Frisur]. Wenn keine Accessoires bzw. Frisur im Text erwähnt werden, bleibt das Feld leer. Achtung: Wenn im Text ein Pulli, eine Jacke oder ein Mäntelchen benannt wird, dann musst du dich für ‚Kleidungsstück‘ entscheiden, aus der vorgegebenen Liste. Sei also nicht zu spezifisch bei den 3 Kategorien der Liste. 
3.	Im Post beschriebene Aktivität. Wähle ein Wort aus der Liste aus, aber wenn du nichts findest, schreibe du die im Text beschriebene Aktivität [spielen, spazieren, essen, schlafen, kuscheln, fernsehen]. Wenn keine Aktivität im Text erwähnt wird, bleibt das Feld leer. 
4.	Ort, an dem die beschriebene Aktivität stattfindet. Wähle einen Ort aus der Liste aus oder schreibe du den Ort, den du im Text gefunden hast [Haus, Natur, Schule]. Wenn kein Ort im Text erwähnt wird, bleibt das Feld leer.
5.	Im Text beschriebene Emotion bzw. beschriebenes Gefühl. Wähle das Wort ausschließlich aus der folgenden Liste aus. Liste: [Freude, Scham, Traurigkeit, Angst, Eckel, Liebe, Überraschung, Stolz]. Wenn du nichts finden kannst, lass das Feld leer. 
6.	Menschen bzw. Akteuren, die im Text erwähnt werden. Berücksichtige hauptsächlich die Wörter auf der Liste, wenn du das Wort nicht findest, ergänze du das Wort vom Text. Benutze ein Wort aus der Liste, wenn du ein Synonym findest. Liste: [Mutter, Vater, Onkel, Opa, Freund]. Wenn keine Menschen bzw. Figuren im Text erwähnt wird, bleibt das Feld leer.
Keine Interpretationen. 
Schreibe die Ergebnisse in einem python dictionary, bei dem der Schlüssel der analysierte Aspekt und der Wert eine Liste von Schlüsselwörtern ist. Stelle sicher, dass das dictionary den Kriterien entspricht, die python versteht und lesen kann. Pass auf die Gänsefüßchen auf, zum Beispiel: 
{'1': ['Pfote', 'Maul'], 
'1a': # hier schreibe eine Erklärung, warum du dich für das Wort entschieden hast.
'2': ['Accessoire'],
'2a': # hier schreibe das Wort, dank dem du verstanden hast, um welchen Oberbegriff sich handelt. 
'3': ['essen', 'spazieren'], 
'3a': # hier kommentiere die ausgewählte Aktivität, z.B.: "das habe ich abgeleitet, denn der Hundebesitzer/-in darüber schreibt, dass er bzw. sie mit dem Hund Gassi gegangen ist und ihm gefüttert hat"
'4': ['Haus'],
'4a': # hier kommentiere mit einer Erklärung des ausgewählten Orts, z.B.: "das habe ich abgeleitet, denn der Hundebesitzer/-in darüber schreibt, dass er bzw. sie mit dem Hund einen Film auf dem Sofa schaut"
'5': ['Liebe', 'Freude'],
'5a': # hier erkläre die ausgewählte Emotion, z.B.: "das habe ich abgeleitet, denn das Frauchen darüber schreibt, dass der Hund sich wohl und geliebt in der Familie fühlt"
'6': ['Oma'],
'6a': # hier erkläre die ausgewählte Figur, z.B.: "das habe ich abgeleitet, denn der Hundebesitzer/-in darüber schreibt, dass er bzw. sie zusammen mit dem Hund die Oma besucht hat"
}
'''



begin = 0 # 0 is first item of the excel file, 1 is the second item, etc.
end = 10000000000 # 10 è l'undicesimo post, 11 è il dodicesimo post, ecc.

try:
    for i,text in enumerate(df_full.iloc[:, -2]):
        if pd.isna(df_full.iloc[i, -1]) and i>=begin and i<end and str(text)!='nan':
            stream = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": CHAT_GPT_PROMPT  +text}],
                stream=True,
            )
            print(f'Post number {i+1}, caption: {text}\n CHAT GPT - ANSWER: ')
            answer = ""
            for chunk in stream:
                print(chunk.choices[0].delta.content or "", end="")
                answer += chunk.choices[0].delta.content or ""
            print('\n')
            print('\n')
            df_full.iloc[i, -1] = answer
except Exception as e:
    print('\n')
    print('\n')
    print(e)
    print('Error at post number: ', i+1)
    print('Caption: ', text)


df_full.to_excel(SAVE_FILE_PATH, index=False)
 
print('Done!')

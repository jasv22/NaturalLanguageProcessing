#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pyttsx3
from bs4 import BeautifulSoup 
import requests
from googlesearch import search
import webbrowser
import speech_recognition as sr
from tkinter import *
from tkinter.messagebox import showinfo, showerror
import csv
import time

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

#speak("what is your query?\n")
def main():
    query=""
    ans=""
    def google(name):
        nonlocal ans
        name2 = name.replace(" ","+")
        try:
            res = requests.get(f'https://www.google.com/search?q={name2}&oq={name2}&aqs=chrome..69i57j46j69i59j35i39j0j46j0l2.4948j0j7&sourceid=chrome&ie=UTF-8',headers=headers)
            soup = BeautifulSoup(res.text,'html.parser')
        except:
            speak("Error occured!")
            speak("Make sure you have a internet connection..!")
        try:
            try:
                ans = soup.select('.RqBzHd')[0].getText().strip()
            
            except:
                try:
                    title=soup.select('.AZCkJd')[0].getText().strip()
                    try:
                        ans=soup.select('.e24Kjd')[0].getText().strip()
                    except:
                        ans=""
                    ans=f'{title}\n{ans}'
                    
                except:
                    try:
                        ans=soup.select('.hgKElc')[0].getText().strip()
                    except:
                        ans=soup.select('.kno-rdesc span')[0].getText().strip()
        
        except:
            import re
            from nltk.tokenize import sent_tokenize,word_tokenize
            import heapq
            from nltk.corpus import stopwords

            data = ""

            for i in search(query, num=1, stop=3, pause=2): 
                link = i
                #webbrowser.open(f"{link}")
                res = requests.get(link,headers=headers)
                soup = BeautifulSoup(res.text,"html.parser")
                content = soup.findAll("p")
                #print(link)
                for texts in content :
                    data +=texts.text
            print(data)
            data2 = data
            def clean(data2):
                text = data2
                text = re.sub(r"\[[0-9]*\]"," ",text)
                text = text.lower()
                text = re.sub(r'\s+'," ",text)
                text = re.sub(r","," ",text)
                text = re.sub("\s\s+"," ",text)

                return text
            summary = clean(data2)
            #print(cleandata)
            #print(summary)

            ##Tokenixing
            sent_tokens = sent_tokenize(summary)

            summary = re.sub(r"[^a-zA-z]"," ",summary)
            word_tokens = word_tokenize(summary)
            ## Removing Stop words

            word_frequency = {}
            stopwords =  set(stopwords.words("english"))

            for word in word_tokens:
                if word not in stopwords:
                    if word not in word_frequency.keys():
                        word_frequency[word]=1
                    else:
                        word_frequency[word] +=1
            maximum_frequency = max(word_frequency.values())
            #print(maximum_frequency)          
            for word in word_frequency.keys():
                word_frequency[word] = (word_frequency[word]/maximum_frequency)
            #print(word_frequency)
            sentences_score = {}
            for sentence in sent_tokens:
                for word in word_tokenize(sentence):
                    if word in word_frequency.keys():
                        if (len(sentence.split(" "))) <30:
                            if sentence not in sentences_score.keys():
                                sentences_score[sentence] = word_frequency[word]
                            else:
                                sentences_score[sentence] += word_frequency[word]
                                
            def get_key(val): 
                for key, value in sentences_score.items(): 
                    if val == value: 
                        return key 
            #key = get_key(max(sentences_score.values()))
            #print(key+"\n")
            #print(sentences_score)
            summary = heapq.nlargest(5,sentences_score,key=sentences_score.get)
            #print(" ".join(summary))
            ans = " ".join(summary)
        return ans
    
    def text():
        nonlocal query,ans
        print("Ask something: \n")
        #query=textF.get()
        query=input()
        ans=google(query)
        print(ans)
        #text.insert(END, f"{ans}\n\n")
        #textF.delete(0,END)

    def voice():
        nonlocal query,ans
        r = sr.Recognizer()
        with sr.Microphone() as source:
            speak("I am now Listening...! Speak..!")
            time.sleep(1)
            audio=r.listen(source)
        try:    
            query = r.recognize_google(audio)
            print(f"user:{query}")
            #textF.insert(0,f"{query}")
            time.sleep(2)
        except:
            speak(" I can't understand what you are saying..! Please Type..")
            #query=textF.get()
            query=input()
            
        ans=google(query)
        speak("Here's what i found..!")
        speak(ans)
        print(ans)
        #text.insert(END, f"{ans}\n\n")
        #textF.delete(0,END)
 
    if __name__ == "__main__":
        voice()
        main()
        

    with open('data.csv', 'a', newline='\n') as file:
        writer = csv.writer(file)
        if ans == "" :
            pass
        else:
            writer.writerow([f"{query}", f"{ans}"])

main()


# In[ ]:





# Text-Summarizer
Text summarization refers to the technique of shortening long pieces of text. The intention is to create a coherent and fluent summary having only the main points outlined in the document.
The extractive text summarization technique involves pulling keyphrases from the source document and combining them to make a summary. The extraction is made according to the defined metric without making any changes to the texts.



CODE:
#importing the libraries required 
import nltk
import heapq  
import bs4 as bs  
import urllib.request  
import re
from gtts import gTTS  
import os
import tkinter
from tkinter import *
from pygame import mixer

#function to show the summary of the text/article 
def display(summary):
    #creating object of tkinter.tk() class for the window that can be shown to the user
    summary_window = Tk()  
    #giving title to window
    summary_window.title('Your summarized text is ready!!') 
    #widget function used to display multiline text
    sVar = Message(summary_window, text = summary) 
    sVar.config(bg='white') 
    #function to display the widget
    sVar.pack( )
    #making button widget 
    playButton= Button(summary_window, height=1, width=30, text="Play Audio of Summary", command=lambda: audio(summary)) 
    playButton.pack() 
    stopButton=Button(summary_window, height=1,  width=10, text="Stop ,command= lambda: stop())
    stopButton.pack()
    #function to make the window displayed until the user closes it
    summary_window.mainloop() 



#function to make the voice assistant read out the summary 

def audio_function(summary):
    text_to_speak = summary
    #defining the language 
    language = 'en'
    myspeak = gTTS(text=text_to_speak, lang=language, slow=False) 
    #saving the file as summary.mp3
    myspeak.save("summary.mp3") 
    #mpg321 is a cmd-line mp3 player to play the music
    os.system("mpg321 summary.mp3")
    #pygame module for loading and playing music
    mixer.init()
    mixer.music.load("summary.mp3")
    mixer.music.play()

#function to make the voice assistant stop from reading out the summary 

def stop():
    mixer.music.stop()

#function to create the summary of the article present in the provided URL

def summarization(source):
     #opening the source/URL  passed to the function as a parameter
    data = urllib.request.urlopen(source)  
    article_from_web = data.read()
    #scrapping the data using bs4 
    parsed_article = bs.BeautifulSoup(article_from_web,'lxml')
    #fetching all p tags in the scrapped data
    paragraphs = parsed_article.find_all('p')
    article_text = ""
    
    #now from each p tag fetching the text present in it 
    for p in paragraphs:  
        article_text += p.text
    
    # Removing Square Brackets, numbers inside the square brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  
    article_text = re.sub(r'\s+', ' ', article_text)  
    
    ## Removing any kind of text other than alphabets and again removing extra spaces
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)  
    
    #making the list of sentences 
    sentences = nltk.sent_tokenize(article_text) 
    
    #making a list of stopwords(a,an ,the it, between,etc.)
    stopwords = nltk.corpus.stopwords.words('english')
    
    #making the word frequency dictionary i.e. key=word and value=number of occurrences of   that word
    word_freq = {}  
    for word in nltk.word_tokenize(formatted_article_text):  
        if word not in stopwords:
            if word not in word_freq.keys():
                word_freq[word] = 1
            else:
                word_freq[word] += 1
    
    #getting maximum frequency            
    max_freq = max(word_freq.values())
    
    #normalising the frequencies
    for word in word_freq.keys():  
        word_freq[word] = (word_freq[word]/max_freq)
    
    #calculating scores of the sentences 
    sentence_scores = {}  
    for sent in sentences:  
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_freq.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_freq[word]
                    else:
                        sentence_scores[sent] += word_freq[word]
   
    
    #picking top 8 sentences for summary                      
    summary_sentences = heapq.nlargest(8, sentence_scores, key=sentence_scores.get)
    
    #joining different sentences
    summary = ' '.join(summary_sentences)
    
    #calling display and audio functions  
    display(summary)
    audio_function(summary)


#function to fetch the URL from tkinter window and calling summarization() function 
def fetch_input():
    global source 
    source = source_field.get("1.0","end-1c")
    summarization(source)

#main window making that will be displayed at first 
root = Tk()
root.title('Enter URL for summary')
source_field = Text(root, height=1, width=50)
source_field.pack()
button1= Button(root, height=1, width=12, text="SUBMIT", command=lambda: fetch_input())
button1.pack() 
root.mainloop()

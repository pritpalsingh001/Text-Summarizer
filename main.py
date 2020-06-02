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


def display(summary):
    summary_window = Tk()
    summary_window.title('Your summarized text is ready!!')
    sVar = Message(summary_window, text = summary) 
    sVar.config(bg='white') 
    sVar.pack( )
    playButton= Button(summary_window, height=1, width=30, text="Play Audio of Summary", command=lambda: audio(summary))
    playButton.pack()
    stopButton= Button(summary_window, height=1, width=10, text="Stop", command=lambda: stop())
    stopButton.pack()
    summary_window.mainloop()


def audio_function(summary):
    text_to_speak = summary
    language = 'en'
    myobj = gTTS(text=text_to_speak, lang=language, slow=False) 
    myobj.save("summary.mp3") 
    os.system("mpg321 summary1.mp3")
    mixer.init()
    mixer.music.load("summary.mp3")
    mixer.music.play()


def stop():
    mixer.music.stop()


def summarization(source):
    data = urllib.request.urlopen(source)  
    article_from_web = data.read()
    parsed_article = bs.BeautifulSoup(article_from_web,'lxml')
    paragraphs = parsed_article.find_all('p')
    article_text = ""
    for p in paragraphs:  
        article_text += p.text
    
    # Removing Square Brackets and Extra Spaces
    article_text = re.sub(r'\[[0-9]*\]', ' ', article_text)  
    article_text = re.sub(r'\s+', ' ', article_text)  
    
    formatted_article_text = re.sub('[^a-zA-Z]', ' ', article_text )  
    formatted_article_text = re.sub(r'\s+', ' ', formatted_article_text)  
    
    sentences = nltk.sent_tokenize(article_text) 
    
    stopwords = nltk.corpus.stopwords.words('english')
    
    word_freq = {}  
    for word in nltk.word_tokenize(formatted_article_text):  
        if word not in stopwords:
            if word not in word_freq.keys():
                word_freq[word] = 1
            else:
                word_freq[word] += 1
                
    max_freq = max(word_freq.values())
    
    for word in word_freq.keys():  
        word_freq[word] = (word_freq[word]/max_freq)
    
    sentence_scores = {}  
    for sent in sentences:  
        for word in nltk.word_tokenize(sent.lower()):
            if word in word_freq.keys():
                if len(sent.split(' ')) < 30:
                    if sent not in sentence_scores.keys():
                        sentence_scores[sent] = word_freq[word]
                    else:
                        sentence_scores[sent] += word_freq[word]
                         
    summary_sentences = heapq.nlargest(8, sentence_scores, key=sentence_scores.get)
    
    summary = ' '.join(summary_sentences)  
    display(summary)
    audio_function(summary)
  
def fetch_input():
    global source 
    source = source_field.get("1.0","end-1c")
    summarization(source)

root = Tk()
root.title('Enter URL for summary')

source_field = Text(root, height=1, width=50)
source_field.pack()


button1= Button(root, height=1, width=12, text="SUBMIT", command=lambda: fetch_input())
button1.pack() 
root.mainloop()

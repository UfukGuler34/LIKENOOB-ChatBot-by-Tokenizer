import speech_recognition as sr
import os
from translate import Translator
from gtts import gTTS
import datetime
import feedparser

def hava():
    parse = feedparser.parse("http://rss.accuweather.com/rss/liveweather_rss.asp?metric=1&locCode=EUR|TR|20020|DENİZLİ|")
    parse = parse["entries"][0]["summary"]
    parse = parse.split()
    aa=("Bugün"+" "+str(parse[2])+" "+str(parse[4])+" "+"Derece"+" bekleniyor")
    return(str(aa))
def konusma(metin):
    tts= gTTS(text=metin ,lang='tr')
    tts.save("aaa.mp3")
    os.system("mpg321 aaa.mp3")
    
def trTranslate(text):
    sonuc =Translator(str(text),'en','tr')
    return sonuc

def enTranslate(text):
    sonuc =Translator(str(text),'tr','en')
    return sonuc

def anlama():
    with sr.Microphone() as kaynak:
         ses = r.listen(kaynak,timeout = None)
         text = r.recognize_google(ses,language="tr-TR")
         print(text)
         return text
     
def tarih ():
    an= datetime.datetime.today()
    tam=str(an.day)+" "+trTranslate(str(datetime.datetime.strftime(an, '%B')))+" "+str(an.year)+" "+trTranslate(str(datetime.datetime.strftime(an, '%A')))
    print(str(tam))
    return(str(tam))
def saat():
    an= datetime.datetime.today()
    hr="saat"+" "+str(an.hour)+" "+str(an.minute)
    print(hr)
    return(str(hr))

r= sr.Recognizer()   
with sr.Microphone() as kaynak:   
     print("Please wait. Calibrating microphone...")   
     # listen for 5 seconds and calculate the ambient noise energy level   
     r.adjust_for_ambient_noise(kaynak, duration=1)
     konusma('kalibrasyon tamamlandi')

def wakeword():     
    print('konuşmak için bana seslenin')
    trueOrFalse= True
    while trueOrFalse:
        try:
            ses = anlama()
            if str(ses)=="destek":
                trueOrFalse= False
            if str(ses)=="dostek":
                trueOrFalse= False
            elif str(ses)=="Hey Dostek":
                trueOrFalse= False
            elif str(ses)=="Merhaba Dostek":
                trueOrFalse= False
            elif str(ses)=="Selamünaleyküm Dostek":
                trueOrFalse= False
        except sr.UnknownValueError:
                 print("Anlamadim.")
    
        except sr.RequestError:
                 print("Bad Request")
        
def dongu() :
            try:
                 print('dinliyorum')
                 sorgu= anlama()  
                 if (str(sorgu))=="Bugünün tarihi ne":
                     konusma(tarih())
                 elif (str(sorgu))=="güle güle":
                     wakeword()
                 elif (str(sorgu))=="görüşürüz":
                     wakeword()
                 elif (str(sorgu))=="saat kaç":
                     konusma(saat())
                 elif (str(sorgu))== "hava nasıl":
                     konusma(hava())
                 elif (str(sorgu))=='soru eklemek istiyorum':
                     ekleme()
                 else:
                     response = str(sorucevap(sorgu))
                     if response==('bu sorunun cevabı henüz eklenmedi eklemek ister misiniz'):
                         cevap=anlama()
                         if cevap == 'evet ':
                             ekleme()
                         else :
                             dongu()
                     print(str(response))
                     konusma(str(response))                   
            except sr.UnknownValueError:
                 print("Anlamadim.")
            except sr.RequestError:
                 print("Bad Request")
def ekleme():
    pswd='No 25'
    konusma('Yönetici şifresini söyleyiniz')
    sifre = anlama()
    print(sifre)
    if sifre == pswd:
        konusma('eklemek istediğiniz soruyu söyleyiniz')
        soru = anlama()
        konusma(str('sorunuz ' + soru))
        konusma('sorunun cevabını söyleyiniz')
        cevap=anlama()
        konusma(str('cevabınız '+ cevap))
        konusma('onaylıyor musunuz')
        onaylama= anlama()
        if onaylama=='Evet':
           with open("sorular.txt", "a") as f:
               f.write('\n')
               f.write(str(soru))
           with open("cevaplar.txt", "a") as f:
               f.write('\n')     
               f.write(str(cevap))
        else:
            konusma('işlem tekrar ediliyor')
            ekleme()
    elif sifre==('iptal et'):
        wakeword()
    else:
        konusma('sifre yanlış')
        ekleme()
def muslum():
    os.system("mpg321 muslum.mp3")
    
def sorucevap(sorucuk):
    soru = sorucuk
    sorulist = soru.split()
    
    sorularlist = list()
    with open("sorular.txt") as f:
      for line in f:
        sorularlist.append(line)
    
    #indices = [i for i, s in enumerate(sorularlist) if 'renk' in s]
    
    indices = []
    for i, elem in enumerate(sorularlist):
        for j,elemk in enumerate(sorulist):
            if elemk in elem:
                indices.append(i)
                
    def most_common(lst):
        max12 = max(set(lst), key=lst.count)
        return max12
    
    cevaplarlist = list()
    with open("cevaplar.txt") as c:
      for line in c:
        cevaplarlist.append(line)

    if(indices != []):
        quesindex = most_common(indices)
        print(most_common(indices))
        answer = cevaplarlist[quesindex]
        print(answer)
    else:
        quesindex = 1000
        answer = 'bu sorunun cevabı henüz eklenmedi eklemek ister misiniz'
        print(answer)
    return answer
  
wakeword()
konusma('Sizi dinliyorum')        

while True:
    dongu()

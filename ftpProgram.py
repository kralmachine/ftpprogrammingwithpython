
# ABDULLAH AVŞAR 141180501  21 MART 2018 ÇARŞAMBA
#BM402 BİLGİSAYAR AĞLARI ÖDEV - 3


from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
import os
import ftplib

say=0
def girisYap():
     global say
     say=0
     if(hostname.get()!='' and userName.get()!='' and passWord.get()!=''):
         ftp=ftplib.FTP(hostname.get())         #Host ismi giriliyor örnek 192.168.0.23 veya ftp.python.org
         ftp.login(userName.get(),passWord.get()) #host kullanıcı adı ve şifre giriliyor
         print(ftp.getwelcome())                #host a girdikten sonra bir mesaj veriliyor
         print('Current Directory',ftp.pwd())   #güncel dosya yolu gösteriliyor
         ftp.dir()                              #güncel dosya ve klasör listelerini çekiyoruz
         gelenServerDosyalar.insert(END,ftp.getwelcome()) #ftp giriş kısmını yazdırma işlemi yapma
         gelenServerDosyalar.insert(END,'Current Directory'+ftp.pwd()) #güncel klasör yolunu belirtme
         for direc in ftp.nlst():           #güncel dosyaları foreach döngüsü yaparak onları ekleme işlemi yapıyoruz
            gelenServerDosyalar.insert(END,direc)
         gelenServerDosyalar.insert(END,'-----------------------------')
         gelenServerDosyalar.pack(side=RIGHT)
         say=1
     else:
         print('Lütfen Verileri Doldurun')
         
def dosyaSec():
     directory=filedialog.askdirectory()        #client için dosya açma işlemi
     print (directory)
     for roots,dirs,files in os.walk(directory):    #dosya işleminden gelen dosyaları , klasörleri ekleme işlemi yapılır
        for file in files:
            print('File =%s' % file)
            gelenClientDosyalar.insert(END,file)
        for direc in dirs:
            print('Direc =%s' % direc)
            gelenClientDosyalar.insert(END,direc)
     gelenClientDosyalar.insert(END,'-----------------------------')
     gelenClientDosyalar.pack(side=LEFT)
     
def cikisYap():
    mGUI.destroy()      #form dan çıkış yapmak ram'den yok ediyoruz object i
    mGUI.quit()         #formu kapatma
    
def komutCalistir():
     command=komutIslem.get()       #gelen komut u command değişkenine atma
     print(command)                 
     commands=command.split()       #command dan gelen değerleri parçalama işlemi yaparak onları kullanacağız
     for i in commands:
         print(i)
     print(say,command)
     if(say==1 and command!=''):        #giriş işlemi yapıldımı kontrol ediyor.
         ftp=ftplib.FTP(hostname.get())
         ftp.login(userName.get(),passWord.get())
            
         if commands[0]=='cd': #kalsör değiştirme işlemi yapar.
            try:
                ftp.cwd(commands[1])
                print('Directory of ',ftp.pwd())
                gelenServerDosyalar.insert(END,'Directory of '+ftp.pwd())
                ftp.dir()
                for direc in ftp.nlst():
                    gelenServerDosyalar.insert(END,direc)
                print('Current Diretory',ftp.pwd())
                gelenServerDosyalar.insert(END,'Directory of '+ftp.pwd())
                gelenServerDosyalar.insert(END,'----------------------------------')
            except ftplib.error_perm as e: #handle 550 (not found / no permission error)
                error_code=str(e).split(None,1)
                if error_code[0]=='550':
                    print(error_code[1],'Directory may not exits or you may not have permission to view it')
                    gelenServerDosyalar.insert(END,error_code[1]+'Directory may not exits or you may not have permission to view it')
                    gelenServerDosyalar.insert(END,'----------------------------------')
                
            
         elif commands[0]=='get': #Dosya indirme işlemi yapar
               try:
                 ftp.retrbinary('RETR '+commands[2], open(commands[1]+commands[2],'wb').write) #dosya yı yazdırma işlemi yapar ve istenilen yere indirme yapar
                 print('File successful download')
                 gelenServerDosyalar.insert(END,'File successful download')
                 gelenServerDosyalar.insert(END,'----------------------------------')
               except ftplib.error_perm as e: #handle 550 (not found / no permission error)
                     error_code=str(e).split(None,1)
                     if error_code[0]=='550':
                        print(error_code[1],'File may not exits or you may not have permission to view it')
                        gelenServerDosyalar.insert(END,error_code[1]+' File may not exits or you may not have permission to view it')
                        gelenServerDosyalar.insert(END,'----------------------------------')
            
         elif commands[0]=='fup': #dosya upload işlemi yapar
                 try:
                    ftp.storlines('STOR '+commands[2],open(commands[1]+commands[2],'rb')) #istenilen dosyayı istenilen yere upload işlemi sağlar
                    print('File successful upload')
                    gelenServerDosyalar.insert(END,'File successful upload')
                    gelenServerDosyalar.insert(END,'----------------------------------')
                 except ftplib.error_perm as e: #handle 550 (not found / no permission error)
                     error_code=str(e).split(None,1)
                     if error_code[0]=='550':
                        print(error_code[1],'File may not exits or you may not have permission to view it')
                        gelenServerDosyalar.insert(END,error_code[1]+'File may not exits or you may not have permission to view it')
                        gelenServerDosyalar.insert(END,'----------------------------------')
            
         elif commands[0]=='ls': #Dosyaları yazdırma işlemi yapar
                 print('Directory of',ftp.pwd())
                 ftp.dir()
                 gelenServerDosyalar.insert(END,'Directory of',ftp.pwd())
                 for direc in ftp.nlst():
                     gelenServerDosyalar.insert(END,direc)
                 gelenServerDosyalar.insert(END,'----------------------------------')
                 
         elif commands[0]=='mkd': #Dosya oluşturma işlemi yapar
                 ftp.mkd('/'+commands[1])
                 print('Successful create a directory')
                 print('Directory of',ftp.pwd())
                 gelenServerDosyalar.insert(END,'Successful create a directory')
                 gelenServerDosyalar.insert(END,'Directory of'+ftp.pwd())
                 ftp.dir()
                 for direc in ftp.nlst():
                     gelenServerDosyalar.insert(END,direc)
                 gelenServerDosyalar.insert(END,'----------------------------------')
                 
         elif commands[0]=='rn': #Dosya adı değiştirme işlemi yapar
                 ftp.rename('/'+commands[1],'/'+commands[2])
                 print('Successful rename a directory')
                 print('Directory of',ftp.pwd())
                 gelenServerDosyalar.insert(END,'Successful rename a directory')
                 gelenServerDosyalar.insert(END,'Directory of'+ftp.pwd())
                 ftp.dir()
                 for direc in ftp.nlst():
                     gelenServerDosyalar.insert(END,direc)
                 gelenServerDosyalar.insert(END,'----------------------------------')
                 
         elif commands[0]=='delete': #Dosya silme işlemi yapar
                 ftp.delete('/'+commands[1])
                 print('Successful remove a file')
                 print('Directory of',ftp.pwd())
                 gelenServerDosyalar.insert(END,'Successful remove a file')
                 gelenServerDosyalar.insert(END,'Directory of'+ftp.pwd())
                 ftp.dir()
                 for direc in ftp.nlst():
                     gelenServerDosyalar.insert(END,direc)
                 gelenServerDosyalar.insert(END,'----------------------------------')
                 
         elif commands[0]=='rmd': # Klasör silme işlemi yapar
                 ftp.rmd('/'+commands[1])
                 print('Successful remove a directory')
                 print('Directory of',ftp.pwd())
                 gelenServerDosyalar.insert(END,'Successful remove a directory')
                 gelenServerDosyalar.insert(END,'Directory of'+ftp.pwd())
                 ftp.dir()
                 for direc in ftp.nlst():
                     gelenServerDosyalar.insert(END,direc)
                 gelenServerDosyalar.insert(END,'----------------------------------')
                 
         elif commands[0]=='exit': #ftp den çıkma işlemi yapar
                ftp.quit()
                print('İyi Günler FTP Kapatmıştır')
                gelenServerDosyalar.insert(END,'İyi Günler FTP Kapatmıştır')
                gelenServerDosyalar.insert(END,'----------------------------------')
                
         else: #belirlediğimiz komutlar kullanılmıyorsa invalid hatası vermesi için else işlemi yapıyoruz.
                print('Invalid command try again (vali options cd/get/ls/mkd/rn/delete/rmd/exit)')
                gelenServerDosyalar.insert(END,'Invalid command try again (vali options cd/get/ls/mkd/rn/delete/rmd/exit)')
                gelenServerDosyalar.insert(END,'---------------------------------------')
     else:  #eğer giriş işlemi yapılmadıysa hata mesajı çıkacak.
         messagebox.showerror('Hata','Lütfen Host Girişi Yapınız\nveya\nKomut Satırını Boş Geçmeyiniz.')
        
            
mGUI=Tk() #tkinter yani GUI için nesne türetme
mGUI.title('FTP PROGRAM') #GUI için başlık ekleme
mGUI.geometry('1000x650+200+50')    #GUI için boyut ayarlama

hostname=StringVar() #Entry component i için bir string değişken tanımlama
userName=StringVar() #Entry component i için bir string değişken tanımlama
passWord=StringVar() #Entry component i için bir string değişken tanımlama
komutIslem=StringVar() #Entry component i için bir string değişken tanımlama

#Kullanıcı şifre host tasarim
lblGirisYazi=Label(mGUI,text='FTP PROGRAMINA HOŞ GELDİNİZ\nLÜTFEN GİRİŞ İŞLEMLERİNİ YAPINIZ',fg='Red').pack()
hostName=Entry(mGUI,textvariable=hostname,width=20).pack()  #hostname girişi
kulAd=Entry(mGUI,textvariable=userName,width=20).pack()     #hostname kullanıcı adı girişi
kulSifre=Entry(mGUI,textvariable=passWord,width=20).pack()      #hostname şifre girişi
btnGiris=Button(mGUI,text='Giriş Yapınız',command=girisYap,fg='Black').pack() #Giriş İşlemi

#Clien Server Tasarım
#Client
btnDosyaSec=Button(mGUI,text='ClientDosya Seç',fg='Black',command=dosyaSec).pack()
gelenClientDosyalar=Listbox(mGUI,width=60,height=30)

#Server
gelenServerDosyalar=Listbox(mGUI,width=60,height=30)
btnGiris=Button(mGUI,text='Çıkış Yapınız',command=cikisYap,fg='Black').pack()

#Komut Girişi ve Komut Çalıştırma
lblGirisYazi=Label(mGUI,text='FTP KOMUT ÇALIŞTIRMA EKRANI (cd,get,fup,ls,mkd,rn,delete,rmd,exit)',fg='Red').pack()
komutCalistirma=Entry(mGUI,textvariable=komutIslem,width=80).pack() #komut çalıştırma için bir entry tanımlanmıştır.
btnGiris=Button(mGUI,text='Komut Çalıştır',command=komutCalistir,fg='Black').pack()
lblBilgilendirme=Label(mGUI,fg='red',text='cd,get,fup,ls,mkd,rn,delete,rmd,exit komutları vardır.\nBunlar şöyledir\ncd komutu klasör erişi için örn (cd dosya)\nget download için örn (get C:\\Users\\aAa\\Desktop\\ deneme.txt)\nfup upload için örn (fup C:\\Users\\aAa\\Desktop\\ deneme.txt)\nls komutu listeleme yapar örn (ls)\nmkd komutu bir klasöt oluşturur örn (mkd deneme)\nrn komutu dosya ismi değiştirme yapar örn (rn deneme dene)\ndelete işlemi dosya siler örn (delete deneme.txt)\nrmd işlemi klasör siler örn (rmd deneme)\nexit işlemi ftp kapatır örn (exit)')
lblBilgilendirme.pack()



mGUI.mainloop()         #GUI ekranda tutması için gereken kod
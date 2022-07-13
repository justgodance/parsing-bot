#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import time
import pickle
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import csv
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
import sched, time
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import telegram_send


# In[2]:


#arrays for garantex data
price=[]
price = [0 for i in range(50)]
volume=[]
volume = [0 for i in range(50)]
#arrays for binance data
price_b=[0 for i in range(50)]
volume_b=[0 for i in range(50)]
volume_b_min=[0 for i in range(50)]
#global urlbinance
global data_gg
global update1


# In[3]:


if os.path.exists('conf.txt')==False:
    telegram_send.configure(conf ='conf.txt' , channel=False, group=False, fm_integration=False)
telegram_send.send(messages=["Вы успешно подключились к боту"],conf='conf.txt')


# In[4]:


def start():
    garant=Tk()
    def start_driver():
        options = Options()
        options.add_argument('user-data-dir=\\chromedriver_win32\\UserData') #changeable
        options.add_argument('--disable-site-isolation-trials')
        options.w3c = True
        driver = webdriver.Chrome(r'chromedriver_win32\\chromedriver.exe', options=options) #changeable r'C:\\Users\\StolekKk\\Documents\\bot\\
        driver.maximize_window()
        driver.implicitly_wait(1)
        time.sleep(1)
        return(driver)   
    ##disabling popups
    def disabler(driver):
    #cookie alert
        try:
            driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
        except NoSuchElementException:
            pass
        time.sleep(2)
    #cheating alert
        try:
            svgObject = driver.find_element(By.XPATH, "//div[@class='css-1fs3b8h']//div[@class='css-b41z7l']//*[name()='svg']");
            action = ActionChains(driver)
            action.click(svgObject).perform();
            driver.find_element(By.CLASS_NAME, "css-gyhchg").click()
        except NoSuchElementException:
            pass
        time.sleep(2)
    #training alert
        try:
            svgObject = driver.find_element(By.XPATH, '//div[@class="css-ebuj64"]//*[name()="svg"]');
            action = ActionChains(driver)
            action.click(svgObject).perform();
        except NoSuchElementException:
            pass
        time.sleep(2)
        try:
            driver.find_element(By.CLASS_NAME, "css-md8x5t").click()
        except NoSuchElementException:
            pass
#time.sleep(10)
   #alert
    def showMessage(): #may be better
        garant.attributes('-topmost', 1)              
        garant.attributes('-topmost', 0)              
        messagebox.showinfo("ALERT", "You should pass the captcha test and fill your mobile/email codes, then close two windows")
    #first time login
    def first_login():
        if os.path.exists('chromedriver_win32\\UserData') == False:
            os.mkdir('chromedriver_win32\\UserData') #creating user data
        driver = start_driver()
        driver.get(urlbinance) #changeable
        time.sleep(4)
        disabler(driver)
        time.sleep(1)
        driver.find_element(By.ID, "header_login").click()
        time.sleep(3)
        driver.find_element(By.CLASS_NAME, "css-1cahv52").click()
        Webelement = driver.find_element(By.NAME,'email')
        Webelement.send_keys(log1) #changeable
        Webelement2 = driver.find_element(By.NAME, 'password')
        Webelement2.send_keys(pas1) #changeable
        garant.after(3000, showMessage)       
        garant.mainloop()
        driver.get("https://p2p.binance.com/ru/trade/Tinkoff/USDT?fiat=RUB")
        pickle.dump(driver.get_cookies() , open("cookies.pkl","wb"))
        return(driver)
    #openning binance url
    #openning binance url
    def binance_url(driver):
        driver.get(urlbinance) #changeable
        disabler(driver)
        cookies = pickle.load(open("cookies.pkl", "rb"))
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        window_before = driver.window_handles[0]
        time.sleep(3)
        disabler(driver)
        driver.find_element(By.CLASS_NAME, "css-qev57u").click()
        driver.find_element(By.XPATH, '//*[@id="__APP"]/div[2]/main/div[4]/div/div[6]/div/div[2]/div/div[2]').click()
        return(window_before, driver)


    #openning garantex url
    def garantex_url(driver):
        driver.execute_script("window.open('about:blank', 'tab2');")
        window_after = driver.window_handles[1] #window_after = garantex
        driver.switch_to.window(window_after)
        time.sleep(1)
        driver.get('https://garantex.io/trading/usdtrub')
    #time.sleep(10)
        return(window_after)
    def garantex(driver):   #collecting data from garantex
        driver.switch_to.window(window_after)
        driver.refresh()
    #ddos alert
        try:
            timeout = 5
            element_present = EC.presence_of_element_located((By.XPATH,'//*[@id="order_book_holder"]/div[2]/div[2]'))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            telegram_send.send(messages=["Нужно пройти капчу"],conf='conf.txt')
            messagebox.showinfo("Пройдите проверку и нажмите ок")
        soup_g = BeautifulSoup(driver.page_source, "xml")
        table = soup_g.find_all('td',{'class':"price col-xs-6 overflow-aut"})#course table
        table2 = soup_g.find_all('td',{'class':"amount col-xs-6 overflow-aut"})#volume table
        i=150
        while i < 200:
            price[i-150]=table[i].text
            volume[i-150]=table2[i].text
            i+=1
        resultprice = [float(item) for item in price]
        resultvolume = [int(item) for item in volume]
        driver.switch_to.window(window_before)
        return(resultprice, resultvolume)


    def binance(driver, data_g, update):  #collecting data from binance
        while(1):
            path = "/html/body/div[1]/div[2]/main/div[5]/div/div[2]/div[1]/div[1]/div[5]/div/button" #path to buy button
            path2 = "/html/body/div[1]/div[2]/main/div[5]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div[1]/div[2]/input" #path to value
            path3 = "/html/body/div[1]/div[2]/main/div[5]/div/div[2]/div[1]/div/div/div[2]/div/div[2]/div/button[2]" #path to second buy button
#waiting for page to load
            try:
                timeout = 10 #may be less
                element_present = EC.presence_of_element_located((By.XPATH,"//*[@id='C2CofferBuy__btn']"))
                WebDriverWait(driver, timeout).until(element_present)
            except TimeoutException:
                binance()
#parsing beginning 
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            course = soup.find_all('div',{'class':'css-1m1f8hn'})[:5]
            maximum = soup.find_all('div',{'class':'css-4cffwv'})[131:141]
#finding values
            i=0
            for item in course:
                price_b[i]=float(item.text)
                i+=1
            p=0 #for volume demarcation
            i=0
            for item in maximum:
                if item.text[0] == '₽' and p%2 == 1:
                    volume_b[i]=float(item.text[1:].replace(",",""))
                if item.text[0] == '₽' and p%2 == 0:
                    volume_b_min[i]=float(item.text[1:].replace(",",""))
                    i+=1
                p+=1
#comparison
#compare user and parsing data
            for i in range(5):
                if(vol1<data_g[1][i]):
                    r=i
                    break
            for i in range(5):
                if data_g[0][r]-price_b[i]>kurs1 and volume_b[i+1]<data_g[1][r] and vol1>volume_b_min[i] and volume_b[i+1]>vol1:
                    path_button = path[:52] + str(i+1) + path[53:]
                    path_buy = path2[:52] + str(i+1) + path2[53:]
                    path_button2 = path3[:52] + str(i+1) + path3[53:]
                    driver.find_element(By.XPATH, path_button).click()      #buying(uncomment when finished)
                    Webelement = driver.find_element(By.XPATH, path_buy)
                    if vol1<volume_b[i+1]:
                        Webelement.send_keys(vol1)
                    else:
                        Webelement.send_keys(volume_b[i+1])
                    driver.find_element(By.XPATH, path_button2).click()
                    telegram_send.send(messages=["Забрал ордер, проверьте Binance"],conf='conf.txt')
                    break
                #for client awareness
                elif data_g[0][r]-price_b[i]<0.2 and data_g[0][r]-price_b[i]>0.1 and vol1>volume_b_min[i] and volume_b[i+1]>vol1:
                    kurs = data_g[0][r]-price_b[i]
                    telegram_send.send(messages=["Разница в курсе:"+str(kurs)],conf='conf.txt')
                elif data_g[0][r]-price_b[i]<0.3 and data_g[0][r]-price_b[i]>0.2 and vol1>volume_b_min[i] and volume_b[i+1]>vol1:
                    kurs = data_g[0][r]-price_b[i]
                    telegram_send.send(messages=["Разница в курсе:"+str(kurs)],conf='conf.txt')
                elif data_g[0][r]-price_b[i]<0.4 and data_g[0][r]-price_b[i]>0.3 and vol1>volume_b_min[i] and volume_b[i+1]>vol1:
                    kurs = data_g[0][r]-price_b[i]
                    telegram_send.send(messages=["Разница в курсе:"+str(kurs)],conf='conf.txt')
                elif data_g[0][r]-price_b[i]<0.5 and data_g[0][r]-price_b[i]>0.4 and vol1>volume_b_min[i] and volume_b[i+1]>vol1:
                    kurs = data_g[0][r]-price_b[i]
                    telegram_send.send(messages=["Разница в курсе:"+str(kurs)],conf='conf.txt')
                elif data_g[0][r]-price_b[i]<0.6 and data_g[0][r]-price_b[i]>0.7 and vol1>volume_b_min[i] and volume_b[i+1]>vol1:
                    kurs = data_g[0][r]-price_b[i]
                    telegram_send.send(messages=["Разница в курсе:"+str(kurs)],conf='conf.txt')                    
#updating garantex data
            update+=1
            if update == 100: #may be bigger
                data_g=garantex(driver)
                update = 0

   #main function
    if __name__ == '__main__':
        check=1
        if os.path.exists('cookies.pkl')==True: #usual start
            driver=start_driver()
        if os.path.exists('cookies.pkl')==False: #first start
            driver=first_login()
        rem = binance_url(driver) #for binance_url data
    #check for outdated cookies 
        try:
            timeout = 15
            element_present = EC.presence_of_element_located((By.XPATH,"//body/div[@id='__APP']/div[@class='layout__Container-sc-1v4mjny-0 hFTMle scroll-container']/header[@class='css-6qqx1f']/div[3]/div[1]//*[name()='svg']"))
            WebDriverWait(driver, timeout).until(element_present)
        except TimeoutException:
            os.remove("cookies.pkl")
            driver.quit()
            driver=first_login()
            rem = binance_url(driver)
        window_before = rem[0] #binance window
        driver = rem[1]
        window_after = garantex_url(driver) #garantex window
        driver.switch_to.window(window_before) 
        data_gg=garantex(driver)
        disabler(driver)
        update1 = 0
        binance(driver, data_gg, update1)


# In[5]:


#interface
def checkKey():
    key = keyentry.get()
    if (str(key)=='R2ks-ldIE'):
        def callbackFunc(event):
            global urlbinance
            url1 = comboExample.get()
            if(url1 == "ABank"):  
               
                urlbinance = "https://p2p.binance.com/ru/trade/ABank/USDT?fiat=RUB"
            if(url1 == "Tinkoff"):  
                urlbinance = "https://p2p.binance.com/ru/trade/Tinkoff/USDT?fiat=RUB"
            if(url1 == "Rosbank"):  
                urlbinance = "https://p2p.binance.com/ru/trade/RosBank/USDT?fiat=RUB"
            if(url1 == "RaiffeisenBank"):  
                urlbinance = "https://p2p.binance.com/ru/trade/RaiffeisenBankRussia/USDT?fiat=RUB"
            print(urlbinance)
        def kurs():
            key3 = keyentry3.get()
            global kurs1 
            kurs1 = float(key3)
            print(kurs1)
            return kurs1
        def log():
            key1 = keyentry1.get()
            global log1 
            log1= key1
            print(log1)
            return log1
        def pas():
            key2= keyentry2.get()
            global pas1 
            pas1 = key2
            print(pas1)
            return pas1
        def vol():
            key4 = keyentry4.get()
            global vol1 
            vol1 = float(key4)
            print(vol1)
            return vol1
        messagebox.showinfo("Спасибо что воспользовались нашими услугами, доступ открыт")
        root.destroy()
        pars = tk.Tk()
        pars.geometry('1000x1000')
        pars.title('Программа для арбитража')
        title = Label(pars, text='Программа для арбитража', font='Arial 40')
        
        text = Label(pars, text='Введите логин')
        text.pack()
#
        keyentry1 = Entry()
        keyentry1.pack()
        
        keylog = Button(pars, text="клик", command = lambda: log())
        keylog.pack()
        
        text = Label(pars, text='Введите пароль')
        text.pack()
#
        
        keyentry2= Entry()
        keyentry2.pack()
        keypas = Button(pars, text="клик", command = lambda: pas())
        keypas.pack()
                
        text = Label(pars, text='Введите мин разницу курса')
        text.pack()
#
        keyentry3= Entry()
        keyentry3.pack()
        
        keykurs = Button(pars, text="клик", command = lambda: kurs())
        keykurs.pack()
                
        text = Label(pars, text='Введите объем покупки')
        text.pack()
#
        keyentry4= Entry()
        keyentry4.pack()
        
        keyvol = Button(pars, text="клик", command = lambda: vol())
        keyvol.pack()
        
       
        
        
        labelTop = tk.Label(pars,
                    text = "Каким Банком пользуетесь")
        labelTop.pack()
        comboExample = ttk.Combobox(pars, 
                            values=[
                                    "Tinkoff", 
                                    "Rosbank",
                                    "RaiffeisenBank",
                                    "ABank"],state="readonly")
        comboExample.pack()
        comboExample.bind("<<ComboboxSelected>>", callbackFunc)
        
        text = Label(pars, text='Старт')
        text.pack()
        keyentry5= Entry()
        
        keystart = Button(pars, text="клик", command = lambda: start())
        keystart.pack()

        pars.mainloop()
       
    else:
        messagebox.showinfo("Ключ введен неверено")


# In[ ]:


root = Tk()
root.geometry('400x500')
root.title('Проверка ключа активации')
title = Label(root, text='Проверка ключа активации', font='Arial 40')
text = Label(root, text='Введите ключ в поле ввода')
text.pack()

keyentry = Entry()
keyentry.pack()
keybutton = Button(root, text="Проверить ключ", command = lambda: checkKey())
keybutton.pack()




root.mainloop()


# In[ ]:





# In[ ]:





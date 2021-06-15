import ctypes
import os
import threading
import time

from tkinter import (END, INSERT, Button, Canvas, Checkbutton, Entry, IntVar,
                     Label, OptionMenu, PhotoImage, Scale, StringVar, Text,
                     Toplevel, mainloop, messagebox, ttk)
from idlelib.tooltip import Hovertip
from mttkinter import mtTkinter as tk
from pygame import mixer
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# SPLASH SCREEN

ctypes.windll.shcore.SetProcessDpiAwareness(1)
splash_root = tk.Tk()
splash_root.title("SPLASH SCREEN")
splash_root.geometry('555x480+680+255')
splash_root.resizable(False, False)
splash_root.overrideredirect(1)


# SPLASH IMAGE
splash_logo = PhotoImage(file="img\\splash.png")
splash_label = Label(splash_root, image=splash_logo)
splash_label.place(x=0, y=0, relwidth=1, relheight=1)


# PROGRESS BAR STYLE

style = ttk.Style()
style.theme_use('clam')
style.configure("red.Horizontal.TProgressbar", foreground='red', background='black')
bar = ttk.Progressbar(splash_root, style="red.Horizontal.TProgressbar", orient="horizontal",
                      length=200, mode="determinate", value=0)



# MAIN WINDOW !!!

def main_window():

    splash_root.destroy()
    root = tk.Tk()
    root.title("Opinaika bot v. 1.9.9")
    root.geometry('1072x772+450+75')
    root.iconbitmap('img\\lain_favicon.ico')
    root.resizable(False, False)
    root.focus_force()

    # CHROME

    def chrome_script():


        swe_sanasto = "http://www.opinaika.fi/opinaika/so.cfm?s=aihioselaus&va=62416"
        eng_sanasto = "https://www.opinaika.fi/opinaika/so.cfm?s=aihioselaus&va=59994"
        ger_sanasto = "https://www.opinaika.fi/opinaika/so.cfm?s=aihioselaus&va=64625"
        spa_sanasto = "https://www.opinaika.fi/opinaika/so.cfm?s=aihioselaus&va=56267"
        rus_sanasto = "https://www.opinaika.fi/opinaika/so.cfm?s=aihioselaus&va=36509"
        fre_sanasto = "https://www.opinaika.fi/opinaika/so.cfm?s=aihioselaus&va=66922"
        ita_sanasto = "https://www.opinaika.fi/opinaika/so.cfm?s=aihioselaus&va=108152"
        custom_sanasto = url_entry_var.get()

        chrome_path = "img\\chromedriver.exe"
        driver = webdriver.Chrome(chrome_path, options=Options())

        if url_check_var.get() == 1 and custom_sanasto != "":
                global user_sanasto
                user_sanasto = custom_sanasto
        else: 
            if url_check_var.get() == 1:
                write("Url field empty!\nUsing selected language sanasto")
            user_sanasto = lang_variable.get()

        if user_sanasto == str(custom_sanasto): 
            driver.get(str(custom_sanasto))

        elif user_sanasto == "Swedish": 
            driver.get(swe_sanasto)
        
        elif user_sanasto == "English": 
            driver.get(eng_sanasto)
                
        elif user_sanasto == "German": 
            driver.get(ger_sanasto)
                    
        elif user_sanasto == "Spanish": 
            driver.get(spa_sanasto)
                    
        elif user_sanasto == "Russian": 
            driver.get(rus_sanasto)
                    
        elif user_sanasto == "French": 
            driver.get(fre_sanasto)
                    
        elif user_sanasto == "Italian": 
            driver.get(ita_sanasto)

        
        print(user_sanasto)
        write(user_sanasto)

        human_state = human_var.get() 

        if human_state == 1:
            print("Humanlike behaviour enabled")
            write("Humanlike behaviour enabled")
        
        driver.maximize_window()


        time.sleep(0.2)
        
        # HUMALIKE BEHAVIOUR
        
        global piste_threshold_reached
        piste_threshold_reached = False
        
        def human_behaviour():
            
            piste_threshold = human_scale.get()
            tehtyja_kohtia = driver.find_element_by_xpath('//*[@id="divKohtiaTehty"]').text
            
            if len(tehtyja_kohtia) < 10: 
                pisteet = 0
            else:
                pisteet = tehtyja_kohtia.split("Pisteet: ", 1)[1].split(".", 1)[0]
                print(pisteet + " points")
                write(pisteet + " points")                
                    
                if int(pisteet) >= int(piste_threshold): 
                    time.sleep(0.5)
                    global piste_threshold_reached
                    piste_threshold_reached = True
                    return


        # ABORT HUMAN
        def abort():
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)
            driver.find_element_by_xpath('//*[@id="divAihioHarjoittelu"]/center/div').click()
            time.sleep(0.2)



        # END OF EXERCISE

        def end_of_exercise():
                
            if str(url_type_var.get()) == "Kurssitehtävät" and custom_sanasto != "": driver.execute_script("window.history.go(-1)")
            else:
                if len(driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")) > 0:
                    (driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")[0]).click()
                    
                else: driver.find_element_by_class_name("selainpalaa.loppupalautenavigointi").click()
            
            global piste_threshold_reached
            piste_threshold_reached = False 
                        
        # LOGIN #

        username_input = username.get()
        password_input = password.get()

        def login():
            username = driver.find_element_by_xpath('/html/body/center/table/tbody/tr[3]/td/center/form/table/tbody/tr[2]/td[2]/input')
            password = driver.find_element_by_xpath('/html/body/center/table/tbody/tr[3]/td/center/form/table/tbody/tr[3]/td[2]/input')    
            login_button = driver.find_element_by_xpath('/html/body/center/table/tbody/tr[3]/td/center/form/table/tbody/tr[4]/td[2]/input')
            username.click()
            username.clear()
            username.send_keys(username_input)
            time.sleep(0.2)
            password.click()
            password.clear()
            password.send_keys(password_input)

            time.sleep(0.2)

            login_button.click()


        login()
        time.sleep(1.5)



        # TUTUSTUMINEN

        def tutustuminen():
            
            driver.execute_script("window.scrollTo(0, 250);")
            time.sleep(0.2)
            tutut = driver.find_elements_by_class_name("painettava.tutustumisrivioletus.perussanasto")
            for i in range(len(tutut)):
                (tutut[i]).click()

            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            end_of_exercise()
            
            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")


        # SANASANELU

        def sanasanelu():
            
            sanat = driver.find_elements_by_class_name("harjoituskohta.kirjoitettava.playsoundonfocus")
            
            for i in range(len(sanat)):
                
                if human_state == 1 and piste_threshold_reached == True: 
                    abort()
                    break
                elif human_state == 1 and piste_threshold_reached == False:
                        human_behaviour()
                        if piste_threshold_reached == True:
                            abort()
                            break
                        

                sanelu_oikea_vastaus = (sanat[i]).get_attribute("data-oikeatvastaukset").split('"text":"', 1)[1].split('"}', 1)[0]
                print(sanelu_oikea_vastaus)
                write(sanelu_oikea_vastaus)
                (sanat[i]).send_keys(sanelu_oikea_vastaus)
                (sanat[i]).send_keys(Keys.ENTER)
                    
            
            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            end_of_exercise()

            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")


        # AUKKOLAUSE

        def aukkolause():
            
            lauseet = driver.find_elements_by_class_name("harjoituskohta.kirjoitettava.painettava")
            
            for i in range(len(lauseet)):

                if human_state == 1 and piste_threshold_reached == True: 
                    abort()
                    break
                elif human_state == 1 and piste_threshold_reached == False:
                    human_behaviour()
                    if piste_threshold_reached == True: 
                        abort()
                        break

                aukkolause_oikea_vastaus = (lauseet[i]).get_attribute("data-oikeatvastaukset").split('"text":"', 1)[1].split('"}', 1)[0]
                print(aukkolause_oikea_vastaus)
                write(aukkolause_oikea_vastaus)
                (lauseet[i]).send_keys(aukkolause_oikea_vastaus)
                (lauseet[i]).send_keys(Keys.ENTER)

            
            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            end_of_exercise()

            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")


        # AUKKOSANA

        def aukkosana():
            
            aukot = driver.find_elements_by_class_name("harjoituskohta.kirjoitettava")
            
            for i in range(len(aukot)):
                
                if human_state == 1 and piste_threshold_reached == True: 
                    abort()
                    break
                elif human_state == 1 and piste_threshold_reached == False:
                    human_behaviour()
                    if piste_threshold_reached == True: 
                        abort()
                        break
                
                aukkosana_oikea_vastaus = (aukot[i]).get_attribute("data-oikeatvastaukset").split('"text":"', 1)[1].split('"}]}', 1)[0]
                print(aukkosana_oikea_vastaus)
                write(aukkosana_oikea_vastaus)
                (aukot[i]).send_keys(aukkosana_oikea_vastaus)
                (aukot[i]).send_keys(Keys.ENTER)

            
            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            end_of_exercise()
            
            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")


        # KUVAVALINTA

        def kuvavalinta():
            
            driver.execute_script("window.scrollTo(0, 180);")
            kuvat = driver.find_elements_by_xpath("//*[@data-ratkaisupainallus='1']")
            for i in range(len(kuvat)):
                
                if human_state == 1 and piste_threshold_reached == True: 
                    abort()
                    break
                elif human_state == 1 and piste_threshold_reached == False:
                    human_behaviour()
                    if piste_threshold_reached == True: 
                        abort()
                        break
                
                (kuvat[i]).click()
                time.sleep(5)


            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            end_of_exercise()
            
            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")


        # RISTIKKO

        def ristikko():
            
            driver.execute_script("window.scrollTo(0, 509);")
            ristit = driver.find_elements_by_class_name("harjoituskohta.merkkikirjoitus.vrr")
            risti = driver.find_elements_by_class_name("harjoituskohta.merkkikirjoitus.prr")

            # PYSTY
            for i in range(len(risti)):
                ristikko_oikea_vastaus_2 = (risti[i]).get_attribute("data-oikeamerkki")
                (risti[i]).send_keys(ristikko_oikea_vastaus_2)

            time.sleep(0.2)

            # VAAKA
            for i in range(len(ristit)):
                
                if human_state == 1 and piste_threshold_reached == True: 
                    abort()
                    break
                elif human_state == 1 and piste_threshold_reached == False:
                    human_behaviour()
                    if piste_threshold_reached == True: 
                        abort()
                        break
                
                ristikko_oikea_vastaus = (ristit[i]).get_attribute("data-oikeamerkki")
                (ristit[i]).send_keys(ristikko_oikea_vastaus)
                    



            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            end_of_exercise()
            
            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")


        # PIILOSANA

        def piilosana(): 

            piilot = driver.find_elements_by_class_name('painettava.valittavaruutu.ratkaisematonpsruutu')
    
            pysty_alku = []
            pysty_loppu = []
    
            vaaka_alku = []
            vaaka_loppu = []

            for i in piilot:
                p_a_value = int((i).get_attribute('data-pystysananalku'))
                if p_a_value > -1:
                    vaaka_alku.append(i)

            for i in piilot:
                p_l_value = int((i).get_attribute('data-pystysananloppu'))
                if p_l_value > -1:
                    vaaka_loppu.append(i)
    
            for i in piilot:
                v_a_value = int((i).get_attribute('data-vaakasananalku'))
                if v_a_value > -1:
                    pysty_alku.append(i)

            for i in piilot:
                v_l_value = int((i).get_attribute('data-vaakasananloppu'))
                if v_l_value > -1:
                    pysty_loppu.append(i)

    
            # ACTUALLY WORKS NOW
    
            while len(driver.find_elements_by_class_name('painettava.ratkaisematonpsruutu')) >= 2:
        
                time.sleep(0.3)
        
                for i in pysty_alku:
                    
                    if human_state == 1 and piste_threshold_reached == True: 
                        abort()
                        break
                    elif human_state == 1 and piste_threshold_reached == False:
                        human_behaviour()
                        if piste_threshold_reached == True: 
                            abort()
                            break
                    
                    driver.execute_script("arguments[0].click();", i)
                    time.sleep(0.1)

                for i in pysty_loppu:
                    
                    driver.execute_script("arguments[0].click();", i)
                    time.sleep(0.1)
        
                time.sleep(0.3)

                for i in vaaka_alku:

                    if human_state == 1 and piste_threshold_reached == True: 
                        abort()
                        break
                    elif human_state == 1 and piste_threshold_reached == False:
                        human_behaviour()
                        if piste_threshold_reached == True: 
                            abort()
                            break          
              
                    driver.execute_script("arguments[0].click();", i)
                    time.sleep(0.2)

                            
                    for i in vaaka_loppu:
                        driver.execute_script("arguments[0].click();", i)
                        time.sleep(0.2)
        
            time.sleep(1)


            time.sleep(12)   
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            end_of_exercise()

            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")


        # MONIVALINTA

        def monivalinta():
            
            time.sleep(0.5)
            driver.execute_script("window.scrollTo(0, 220);")
            time.sleep(0.5)
            monit = driver.find_elements_by_xpath("//*[@data-oikeaarvo]")

            for i in range(len(monit)):
                
                if human_state == 1 and piste_threshold_reached == True: 
                    abort()
                    break
                elif human_state == 1 and piste_threshold_reached == False:
                    human_behaviour()
                    if piste_threshold_reached == True: 
                        abort()
                        break                
                
                moni_oikea_vastaus = (monit[i]).get_attribute('data-lopputeksti')
                time.sleep(0.1)
                (monit[i]).click()
                time.sleep(0.1)
                driver.find_element_by_xpath('//div[text()="%s"]' % moni_oikea_vastaus).click()
                print(moni_oikea_vastaus)
                write(moni_oikea_vastaus)

            

            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            end_of_exercise()
            
            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")


        # YHDISTELY

        def yhdistely():
            
            time.sleep(0.2)            
            driver.execute_script("window.scrollTo(0, 490);")
            time.sleep(0.2)

            yhdit = driver.find_elements_by_class_name("yhdistettava.yhdistettava_kohde.tekstiyhdistely_kohde")

            for i in range(len(yhdit)):
                
                if human_state == 1 and piste_threshold_reached == True: 
                    abort()
                    break
                elif human_state == 1 and piste_threshold_reached == False:
                    human_behaviour()
                    if piste_threshold_reached == True: 
                        abort()
                        break  
                    
                yhdistely_oikea_vastaus = (yhdit[i]).get_attribute('data-oikeaarvo')
                (yhdit[i]).click()
                time.sleep(0.2)
                yhdisteet = driver.find_elements_by_class_name('sekoitettava.harjoituskohta.toggleoncorrect.yhdistettava.yhdistettava_lahde.tekstiyhdistely_lahde')
                for i in range(len(yhdisteet)):
                    if str((yhdisteet[i]).text) == str(yhdistely_oikea_vastaus):
                        print(yhdistely_oikea_vastaus)
                        write(yhdistely_oikea_vastaus)
                        time.sleep(0.2)
                        (yhdisteet[i]).click()

                    
                    time.sleep(0.2)

            
            time.sleep(12)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            end_of_exercise()
            
            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")

        
        # AUKKO

        def aukko():
            
            aukko = driver.find_elements_by_class_name("harjoituskohta.kirjoitettava.painettava")
            
            for i in range(len(aukko)):
                
                if human_state == 1 and piste_threshold_reached == True: 
                    abort()
                    break
                elif human_state == 1 and piste_threshold_reached == False:
                    human_behaviour()
                    if piste_threshold_reached == True: 
                        abort()
                        break 

                aukko_oikea_vastaus = (aukko[i]).get_attribute("data-oikeatvastaukset").split('"text":"', 1)[1].split('"', 1)[0].strip("/")
                print(aukko_oikea_vastaus)
                write(aukko_oikea_vastaus)
                (aukko[i]).send_keys(aukko_oikea_vastaus)
                (aukko[i]).send_keys(Keys.ENTER)

            
            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)
            
            end_of_exercise()
            
            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")

        # TEORIA

        def teoria():

            time.sleep(0.5)
            driver.execute_script("window.history.go(-1)")
            time.sleep(1)
            print("Exercise done!")
            write("Exercise done!")


        # KUULLUN YMMÄRTÄMINEN

        def kuullun_ymmärtäminen():

            print("lul")
            print("still under development :trol:")
            time.sleep(0.5)
            driver.execute_script("window.history.go(-1)")


        # SANASTO MENU

        all_the_elems =  ('//*[@id="divValikkoItemit"]/div[1]'
        , '//*[@id="divValikkoItemit"]/div[2]', '//*[@id="divValikkoItemit"]/div[3]'
        , '//*[@id="divValikkoItemit"]/div[4]', '//*[@id="divValikkoItemit"]/div[5]'
        , '//*[@id="divValikkoItemit"]/div[6]', '//*[@id="divValikkoItemit"]/div[7]'
        , '//*[@id="divValikkoItemit"]/div[8]', '//*[@id="divValikkoItemit"]/div[9]'
        , '//*[@id="divValikkoItemit"]/div[10]', '//*[@id="divValikkoItemit"]/div[11]'
        , '//*[@id="divValikkoItemit"]/div[12]', '//*[@id="divValikkoItemit"]/div[13]'
        , '//*[@id="divValikkoItemit"]/div[14]', '//*[@id="divValikkoItemit"]/div[15]'
        ,'//*[@id="divValikkoItemit"]/div[16]', '//*[@id="divValikkoItemit"]/div[17]')


        # FINAL FINISHED FUNCTION

        def omg(): 
            for i in range(len(driver.find_elements_by_class_name("selausvalikko.vaihdaosoite"))):
                driver.find_element_by_xpath(all_the_elems[i]).click()
                time.sleep(0.3)
                sub_menu()
                print("Section completed!")
                write("Section completed")
                time.sleep(0.5)
                driver.find_element_by_class_name("vaihdaosoite.ohjelmapaluupainike").click()

        # SUB MENU

        def sub_menu():
            for i in range(len(driver.find_elements_by_class_name("selausvalikko.vaihdaosoite"))):
                driver.find_element_by_xpath(all_the_elems[i]).click()
                time.sleep(0.3)
                sub_sub_menu()
                time.sleep(0.3)
                driver.find_element_by_class_name("vaihdaosoite.ohjelmapaluupainike").click()


        # SUB SUB MENU

        def sub_sub_menu():
            for i in range(len(driver.find_elements_by_class_name("selausvalikko.vaihdaosoite"))):
                (driver.find_elements_by_class_name("selausvalikko.vaihdaosoite")[i]).click()
                time.sleep(0.3)

                exercises()

                time.sleep(0.3)
                driver.find_element_by_class_name("vaihdaosoite.ohjelmapaluupainike").click()



        # EXERCISES

        def exercises():

            for i in range(len(driver.find_elements_by_class_name('selausaihio_aladivi'))):
                
                exercise = (driver.find_elements_by_class_name('selausaihio_aladivi')[i]).get_attribute('innerText').partition('\n')[0][4:]
                print(exercise)
                write(exercise)
                
                exercise_score = (driver.find_elements_by_class_name('selausaihio_aladivi')[i]).get_attribute('innerText').partition('\n')[2].strip()
                
                if exercise_score == '':
                    exercise_score = "0"
                    print(exercise_score)
                    write(exercise_score)               
                else:
                    print(exercise_score)
                    write(exercise_score)

                skip_check = skip_var.get()
                skip_threshold = skip_scale_var.get()

                if skip_check == 1 and int(exercise_score) > skip_threshold:
                    print(exercise + " " + "already completed")
                    write(exercise + " " + "already completed")
                else:
                    (driver.find_elements_by_class_name('selausaihio_aladivi')[i]).click()
                    time.sleep(0.5)
                    if exercise == "Tutustuminen":
                        tutustuminen()
                    elif exercise == "Aukkolause":
                        aukkolause()
                    elif exercise == "Aukkosana":
                        aukkosana()
                    elif exercise == "Kuvavalinta":
                        kuvavalinta()
                    elif exercise == "Monivalinta":
                        monivalinta()
                    elif exercise == "Ristikko":
                        ristikko()
                    elif exercise == "Piilosana":
                        piilosana()        
                    elif exercise == "Sanasanelu":
                        sanasanelu()
                    elif exercise == "Yhdistely":
                        yhdistely()
                    elif exercise == "Aukko":
                        aukko()                    
                    elif exercise == "Teoria":
                        teoria()   
                    else:
                        kurssi_exercises()

        # FINAL FUNCTION FOR KURSSITEHTÄVÄT

        def kurssi_omg():
            
            # TOP LEVEL (MENU)
            
            kurssi_list = ["//*[@id='divKurssinTehtavat']/table/tbody/tr[2]/td[1]/div", "//*[@id='divKurssinTehtavat']/table/tbody/tr[3]/td[1]/div",
                            "//*[@id='divKurssinTehtavat']/table/tbody/tr[4]/td[1]/div", "//*[@id='divKurssinTehtavat']/table/tbody/tr[5]/td[1]/div",
                            "//*[@id='divKurssinTehtavat']/table/tbody/tr[6]/td[1]/div", "//*[@id='divKurssinTehtavat']/table/tbody/tr[7]/td[1]/div",
                            "//*[@id='divKurssinTehtavat']/table/tbody/tr[8]/td[1]/div", "//*[@id='divKurssinTehtavat']/table/tbody/tr[9]/td[1]/div",
                            "//*[@id='divKurssinTehtavat']/table/tbody/tr[10]/td[1]/div", "//*[@id='divKurssinTehtavat']/table/tbody/tr[11]/td[1]/div",
                            "//*[@id='divKurssinTehtavat']/table/tbody/tr[12]/td[1]/div"]


            kurssi_table = driver.find_element_by_xpath('//*[@id="divKurssinTehtavat"]/table')
            kurssit = kurssi_table.find_elements_by_class_name("avaakurssitehtava.ikonipainike")
            for i in range(len(kurssit)):
                kurssi_nimi = driver.find_element_by_xpath((kurssi_list[i])).text
                print(kurssi_nimi)
                write(kurssi_nimi)
                kurssi_harjoitus = driver.find_element_by_xpath((kurssi_list[i]))
                kurssi_harjoitus.click()
                time.sleep(0.3)
                kurssi_menu()
                time.sleep(0.3)
                siirry_kurssiin = driver.find_element_by_xpath('//*[@id="divYPlisatoiminnot"]/div')
                siirry_kurssiin.click()
                print("Section compledted!")
                write("Section compledted!")
                time.sleep(0.5)


       # KURSSI MENU
        
        def kurssi_menu():
            

            otsikko_list = ["//*[@id='divTehtavakohdat']/div/table/tbody/tr[2]/td[2]/div", "//*[@id='divTehtavakohdat']/div/table/tbody/tr[3]/td[2]/div",
                            "//*[@id='divTehtavakohdat']/div/table/tbody/tr[4]/td[2]/div", "//*[@id='divTehtavakohdat']/div/table/tbody/tr[5]/td[2]/div",
                            "//*[@id='divTehtavakohdat']/div/table/tbody/tr[6]/td[2]/div", "//*[@id='divTehtavakohdat']/div/table/tbody/tr[7]/td[2]/div",
                            "//*[@id='divTehtavakohdat']/div/table/tbody/tr[8]/td[2]/div"]
            
            piste_list = ["//*[@id='divTehtavakohdat']/div/table/tbody/tr[2]/td[3]", "//*[@id='divTehtavakohdat']/div/table/tbody/tr[3]/td[3]",
                          "//*[@id='divTehtavakohdat']/div/table/tbody/tr[4]/td[3]", "//*[@id='divTehtavakohdat']/div/table/tbody/tr[5]/td[3]",
                          "//*[@id='divTehtavakohdat']/div/table/tbody/tr[6]/td[3]", "//*[@id='divTehtavakohdat']/div/table/tbody/tr[7]/td[3]",
                          "//*[@id='divTehtavakohdat']/div/table/tbody/tr[8]/td[3]"]
            
            exercise_list = ["//*[@id='divTehtavakohdat']/div/table/tbody/tr[2]/td[4]/div", "//*[@id='divTehtavakohdat']/div/table/tbody/tr[3]/td[4]/div",
                           "//*[@id='divTehtavakohdat']/div/table/tbody/tr[4]/td[4]/div", "//*[@id='divTehtavakohdat']/div/table/tbody/tr[5]/td[4]/div",
                           "//*[@id='divTehtavakohdat']/div/table/tbody/tr[6]/td[4]/div", "//*[@id='divTehtavakohdat']/div/table/tbody/tr[7]/td[4]/div",
                           "//*[@id='divTehtavakohdat']/div/table/tbody/tr[8]/td[4]/div"]

            time.sleep(0.2)
            table = driver.find_element_by_xpath('//*[@id="divTehtavakohdat"]/div/table')
            otsikot = table.find_elements(By.CLASS_NAME, "kurssitehtavakohtaotsikko")


            for i in range(len(otsikot)):
                
                global kurssi_otsikko
                kurssi_otsikko = driver.find_element_by_xpath((otsikko_list[i])).text
                print(kurssi_otsikko)
                write(kurssi_otsikko)
                
                global kurssi_pisteet
                kurssi_pisteet = driver.find_element_by_xpath((piste_list[i])).text
                print(kurssi_pisteet)
                write(kurssi_pisteet)
                
                time.sleep(0.2)
                kurssi_harjoitus = driver.find_element_by_xpath((exercise_list[i]))
                 
                if str(kurssi_pisteet) == 'Avattu':
                    kurssi_pisteet = "0"
                
                elif str(kurssi_pisteet) == '-':
                    kurssi_pisteet = "0"
                
                skip_check = skip_var.get()
                skip_threshold = skip_scale_var.get()
                
                if skip_check == 1 and int(kurssi_pisteet) > skip_threshold:
                    print(kurssi_otsikko + " " + "already completed")
                    write(kurssi_otsikko + " " + "already completed")

                else:    
                    kurssi_harjoitus.click()
                    time.sleep(0.2)
                    kurssi_exercises()
                    
                
        # KURSSI EXERCISES

        def kurssi_exercises():
            
            exercise_dict = {'tutustuminen': tutustuminen, 'aukkolause': aukkolause, 'aukkosana': aukkosana, 'kuvavalinta': kuvavalinta,
                             'monivalinta': monivalinta, 'ristikko': ristikko, 'piilosana': piilosana, 'yhdistely': yhdistely, 'aukko': aukko,
                             'teoria': teoria, 'kuullunymmärtäminen': kuullun_ymmärtäminen}

            time.sleep(0.5)
            aihiokoodi = driver.find_element_by_xpath('//*[@id="divYPnimilaatikko"]/span[1]')
            aihiokoodi.click()
            time.sleep(0.8)
            aihiokoodi_table = driver.find_element_by_xpath('//*[@id="divAihioPopup"]/div/table[2]')
            aihiokoodi_row = aihiokoodi_table.find_elements(By.TAG_NAME, "tr")[1]
            exercise = str(aihiokoodi_row.find_elements(By.TAG_NAME, "td")[1].text.split("(", 1)[1].strip(")").strip().lower())
            print(exercise)
            write(exercise)
            sulje_aihiokoodi = driver.find_element_by_id('divSuljeAihioKortti')
            time.sleep(0.2)
            sulje_aihiokoodi.click()
            time.sleep(0.5)

            exercise_dict[exercise]()
            

        # WHICH FUNCTION SELECT
        
        if str(url_type_var.get()) == "Kurssitehtävät":
            if custom_sanasto != "":
                kurssi_omg()
            else:
                omg()
        
        else:
            omg()
        
        print("Automation ended!")
        write("Automation ended!")
        time.sleep(5)
        driver.quit()
 

    # COLOR HEX

    navy = '#343647'
    gray = '#CCCCCC'
    baby_blue = '#99ccff'
    light_blue = '#899cf0'
    light_purple = '#c2c4f5'


    # BACKGROUND IMAGE
    
    background = PhotoImage(file="img\\bg.png")
    bg_label = Label(root, image=background)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = background

    # STASTUS BAR

    status_bar = Canvas(root, bg=gray, width=1072, height=31, borderwidth=0)
    status_bar.place(x=0, y=0)

    # BUTTONS

    # SETTINGS WINDOW
    
    def settings_window():
        if settings_root.state() != "normal": 
            settings_root.deiconify()
        else:
            settings_root.withdraw()
    

    settings_root = Toplevel()
    settings_root.title("Settings")
    settings_root.iconbitmap('img\\settings.ico')
    settings_root.geometry('585x645+1150+260')
    settings_root.resizable(False, False)

    # SETTINGS BACKGROUND IMAGE
    
    settings_background = PhotoImage(file="img\\settings_bg.png")
    settings_bg_label = Label(settings_root, image=settings_background)
    settings_bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    settings_bg_label.image = settings_background    

    
    # ACTUAL SETTINGS #

    # NUMBER SCALES #

    # SKIP SCALE
    
    skip_scale_var = IntVar()
    skip_scale = Scale(settings_root, bg=gray, resolution=5, variable=skip_scale_var, from_ = 0, to = 100, orient = "horizontal", 
    width=20, sliderlength=40, length=450, label="Change the minimium score for skipping an exercise")  
    
    skip_scale.set(70)
    skip_scale.place(x=70, y=220)
    skip_scale.lower()

    close_skip = Button(settings_root, bg=gray, height=1, width=5, text="ok")
    
    def hide_skip_scale():
        global popup_open
        popup_open = 0
        write("Skip threshold set to " + str(skip_scale_var.get()) + " points")
        human_check.config(state='normal')
        url_check.config(state='normal')
        skip_scale.lower()
        close_skip.lower()
    
    close_skip['command'] = hide_skip_scale
    close_skip.place(x=255, y=320)
    close_skip.lower()

    # HUMAN SCALE 
    
    human_scale_var = IntVar()
    human_scale = Scale(settings_root, bg=gray, resolution=5, variable=human_scale_var, from_ = 0, to = 100, orient = "horizontal", 
    width=20, sliderlength=40, length=450, label="Change the minimium score to finish an exercise")  
    
    human_scale.set(90)
    human_scale.place(x=70, y=220)
    human_scale.lower()

    close_human = Button(settings_root, bg=gray, height=1, width=5, text="ok")
    
    def hide_human_scale():
        global popup_open
        popup_open = 0
        write("Human threshold set to " + str(human_scale_var.get()) + " points")
        skip_check.config(state='normal')
        url_check.config(state='normal')
        human_scale.lower()
        close_human.lower()
    
    close_human['command'] = hide_human_scale
    close_human.place(x=255, y=320)
    close_human.lower()

    # CUSTOM URL ENTRY

    url_label = Label(settings_root, bg=gray, fg="black", width=45, height=3, text="Enter your own URL for opinaika", anchor="n")
    url_label.place(x=70, y=220)
    url_label.lower()

    url_entry_var = StringVar(value="")
    url_entry = Entry(settings_root, bg=navy, fg="white", width=45, textvariable=url_entry_var)
    url_entry.place(x=71, y=274)
    url_entry.lower()

    url_OPTIONS = [
    "Kurssitehtävät",
    "Sanasto+",
    ] 

    url_type_var = StringVar(root)
    url_type_var.set(url_OPTIONS[0])

    url_type_menu = OptionMenu(settings_root, url_type_var, *url_OPTIONS)
    url_type_menu.place(x=70, y=175)
    url_type_menu.config(bg=gray)
    url_type_menu["menu"].config(bg=gray)
    url_type_menu.lower()
    Hovertip(url_type_menu, "Select the exercise type")    
    
    close_url = Button(settings_root, bg=gray, height=1, width=5, text="ok")
    
    def hide_url_entry():
        global popup_open
        popup_open = 0
        write('Opinaika url set to "' + str(url_entry_var.get()) + '"')
        skip_check.config(state='normal')
        human_check.config(state='normal')
        url_entry.lower()
        close_url.lower()
        url_label.lower()
        url_type_menu.lower()
    
    close_url['command'] = hide_url_entry
    close_url.place(x=255, y=320)
    close_url.lower()

    # SKIP CHECKBOX
    
    popup_open = 0

    skip_var = IntVar(value=1)
    
    def show_skip_scale():
        global popup_open
        if skip_var.get() == 1:
            popup_open = 1
            if popup_open == 1:
                human_check.config(state='disabled')
                url_check.config(state='disabled')
                skip_scale.lift()
                close_skip.lift()
            else:
                human_check.config(state='normal')
                url_check.config(state='normal')
            skip_scale.lift()
            close_skip.lift()
        else:
            popup_open = 0
            if popup_open == 1:
                human_check.config(state='disabled')
                url_check.config(state='disabled')
                skip_scale.lift()
                close_skip.lift()
            else:
                human_check.config(state='normal')
                url_check.config(state='normal')
            skip_scale.lower()
            close_skip.lower()

    skip_check = Checkbutton(settings_root, bg=gray, height=1, text="Skip completed exercises", variable=skip_var, command=show_skip_scale)
    skip_check.place(x=10, y=15)
    Hovertip(skip_check, "Skip the exercise if the score is 70p or higher")    
    
    # HUMANLIKE BEHAVIOUR CHECKBOX
    
    human_var = IntVar(value=0)
    
    def show_human_scale():
        global popup_open
        if human_var.get() == 1:
            popup_open = 1
            if popup_open == 1:
                url_check.config(state='disabled')
                skip_check.config(state='disabled')
            else:
                url_check.config(state='normal')
                skip_check.config(state='normal')
            human_scale.lift()
            close_human.lift()
        else:
            popup_open = 0
            if popup_open == 1:
                url_check.config(state='disabled')
                skip_check.config(state='disabled')
            else:
                url_check.config(state='normal')
                skip_check.config(state='normal')
            human_scale.lower()
            close_human.lower()
    
    human_check = Checkbutton(settings_root, bg=gray, height=1, text="Humanlike behaviour", variable=human_var, command=show_human_scale)
    human_check.place(x=10, y=60)
    Hovertip(human_check, "Exit the exercise when 90p reached") 

    # CUSTOM URL GIVEN BY USER
  
    url_check_var = IntVar(value=0)
    
    def show_url_entry():
        global popup_open
        if url_check_var.get() == 1:
            popup_open = 1
            if popup_open == 1:
                human_check.config(state='disabled')
                skip_check.config(state='disabled')
            else:
                human_check.config(state='normal')
                skip_check.config(state='normal')
            url_label.lift()
            url_entry.lift()
            close_url.lift()
            url_type_menu.lift()
        else:
            popup_open = 0
            if popup_open == 1:
                human_check.config(state='disabled')
                skip_check.config(state='disabled')
            else:
                human_check.config(state='normal')
                skip_check.config(state='normal')
            url_label.lower()
            url_entry.lower()
            close_url.lower()
            url_type_menu.lower()

    
    url_check = Checkbutton(settings_root, bg=gray, height=1, text="Custom URL", variable=url_check_var, command=show_url_entry)
    url_check.place(x=10, y=105)
    Hovertip(url_check, "Use custom opinaika URL given by user")




    # SAVE SETTINGS BUTTON
    
    def save_settings():
        
        if str(skip_check['state']) != 'disabled':
            write("Settings saved")
        
        settings_root.withdraw()
    
    save = Button(settings_root, bg=gray, width=6, height=1, text="save", command=save_settings)
    save.place(x=10, y=590)


    settings_root.withdraw()

    def on_closing():
        settings_root.withdraw()

    settings_root.protocol("WM_DELETE_WINDOW", on_closing)
    
    

    # SETTINGS BUTTON

    settings_img = PhotoImage(file="img\\set.png")
    settings_button = Button(root, image=settings_img, command=settings_window, borderwidth=0, bg=gray)
    settings_button.image = settings_img
    settings_button.place(x=1030, y=2)
    

    # ENTRIES
    
    username_text = StringVar(root)
    password_text = StringVar(root)
    
    username = Entry(root, bg=navy, fg="white", textvariable=username_text, width=23)
    username.place(x=30, y=95, relwidth=0.36, relheight=0.045)

    password = Entry(root, bg=navy, fg="white", textvariable=password_text, show="*", width=23)
    password.place(x=30, y=140, relwidth=0.36, relheight=0.045)
    

    # NOW PLAYING TEXT

    now_playing = Label(status_bar, bg=gray, text=" ", width=75)
    now_playing.place(x=150, y=2)

    
    # MUSIC

    def menu_music():
        
        
        mixer.init()
        lists_of_songs = os.listdir("img/music")

        for song in lists_of_songs:
            if song.endswith(".mp3"):
                file_path = "img/music/" + song
                mixer.music.load(str(file_path))
                mixer.music.play()
                print("Playing::::: " + song[:-4])
                now_playing.config(text="Now playing ::: " + " " + str(song[:-4]))
                
                while mixer.music.get_busy() == True:
                    continue

    music_thread = threading.Thread(target=menu_music)
    music_thread.daemon = True
    music_thread.start()
    




    # TERMINAL THING

    terminal = Text(root, bg=navy, fg="white", height=9, width=38)
    terminal.place(x=0, y=575)
    terminal.tag_config("green", background=navy, foreground="green")
    terminal.tag_config("baby_blue", background=navy, foreground=baby_blue)
    terminal.tag_config("light_blue", background=navy, foreground=light_blue)
    terminal.tag_config("light_purple", background=navy, foreground=light_purple)
    

    terminal.insert(END, "Dirty my life, I clean for you\nI dream of life, it might come true\nI need a break, can I live?\nI need to change something quick\nI pay the price for the sin\nI'm at the gate, let me in\nI take my life for the risk\nI roll a dice, need a six\n", 'baby_blue')
    terminal.config(state='disabled')
    
    # TEXT INTO TERMINAL

    def write(*message, end = "\n", sep = " "):
        terminal.config(state='normal')
        text = ""
        for i in message:
            text += "{}".format(i)
            text += sep
        text += end
        terminal.insert(INSERT, text, "light_purple")
        terminal.see(END)
        terminal.config(state='disabled')
    

    def lock():
        username.config(state='disabled')
        password.config(state='disabled')
        dropdown_menu.config(state='disabled')
        login.config(state='disabled')
        skip_check.config(state='disabled')
        terminal.config(state='disabled')
        human_check.config(state='disabled')
        url_check.config(state='disabled')


    def lock_and_run_chrome():
        
        if str(username.get()) == "":
            print("Invalid email/pass")
            write("Invalid email/pass")
        
        elif str(password.get()) == "":
            print("Invalid email/pass")
            write("Invalid email/pass")
        
        else:
            write("\n")
            lock()
            chrome_thread = threading.Thread(target=chrome_script)
            chrome_thread.daemon = True
            chrome_thread.start()


    # LOGIN BUTTON

    login = Button(root, bg=gray, width=6, text="login", command=lock_and_run_chrome)
    login.place(x=175, y=200)
    
    # DROPDOWN MENU FOR ENGLISH/SWEDISH MODE
    
    lang_OPTIONS = [
    "Swedish",
    "English",
    "German",
    "Spanish",
    "Russian",
    "French",
    "Italian"] 

    lang_variable = StringVar(root)
    lang_variable.set(lang_OPTIONS[0])

    dropdown_menu = OptionMenu(root, lang_variable, *lang_OPTIONS)
    dropdown_menu.place(x=0, y=0)
    dropdown_menu.config(bg=gray)
    dropdown_menu["menu"].config(bg=gray)


    # INFO POPUP

    lines = ['Please read the instructions in readme.nfo', ' ', ' ', ' ', ' ', ' ', ' ', 
    'Made by Arrow', ' ', '©2021 A Dream of Life All rights reserved']
    
    messagebox.showinfo(' Bliss Fields', "\n".join(lines))


# PROGRESS BAR FUNCTION

bar.start(16)

def stop_progressbar():
    bar.stop()
    bar['value'] = 100
    splash_root.after(650)
    main_window()


splash_root.after(1950, stop_progressbar)

bar.place(x=12, y=449, relwidth=0.95, relheight=0.042)



mainloop()

from mttkinter import mtTkinter as tk
from tkinter import Entry, Button, PhotoImage, Label, Canvas, mainloop, ttk, INSERT, messagebox, StringVar, OptionMenu, Checkbutton, IntVar, Text, END, Checkbutton
from pygame import mixer
import os
import time
import threading

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys


# SPLASH SCREEN

splash_root = tk.Tk()
splash_root.title("SPLASH SCREEN")
splash_root.geometry('370x320+430+160')
splash_canvas = Canvas(splash_root, bg="blue", height=280, width=350)
splash_root.resizable(False, False)
splash_root.overrideredirect(1)


# SPLASH IMAGE
splash_logo = PhotoImage(file="img\\5.png")
splash_label = Label(splash_root, image=splash_logo)
splash_label.place(x=0, y=0, relwidth=1, relheight=1)


# PROGRESS BAR STYLE

s = ttk.Style()
s.theme_use('clam')
s.configure("red.Horizontal.TProgressbar", foreground='red', background='black')

bar = ttk.Progressbar(splash_root, style="red.Horizontal.TProgressbar", orient="horizontal",
                      length=200, mode="determinate", value=0)



# MAIN WINDOW !!!

def main_window():

    splash_root.destroy()
    root = tk.Tk()
    root.title("Opinaika bot v. 1.1.1")
    root.geometry('715x515+300+50')
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

        chrome_path = "img\\chromedriver.exe"
        driver = webdriver.Chrome(chrome_path, options=Options())

        user_sanasto = lang_variable.get()        

        if user_sanasto == "Swedish": 
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
        
        print (user_sanasto)
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
            
            if human_state == 1:
                piste_threshold = 90
                tehtyja_kohtia = driver.find_element_by_xpath('//*[@id="divKohtiaTehty"]').text
            
                if len(tehtyja_kohtia) < 10:
                    pisteet = 0
                else:
                    pisteet = tehtyja_kohtia.split("Pisteet: ", 1)[1].split(".", 1)[0]
                    print(pisteet + " points")
                    write(pisteet + " points")                
                        
                    if int(pisteet) >= int(piste_threshold): 
                        time.sleep(0.5)
                        driver.execute_script("window.scrollTo(0, 1080);")
                        time.sleep(0.5)
                        driver.find_element_by_class_name('divlopetaaihio.lopetaaihio').click()
                        global piste_threshold_reached
                        piste_threshold_reached = True
                        return

                    


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
        time.sleep(2)

        # TUTUSTUMINEN

        def tutustuminen():
            
            driver.execute_script("window.scrollTo(0, 560);")
            time.sleep(1)
            elems = driver.find_elements_by_class_name("painettava.tutustumisrivioletus.perussanasto")
            for i in range(len(elems)):
                (elems[i]).click()

            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            if len(driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")) > 0:
                (driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")[0]).click()

            else:
                driver.find_element_by_class_name("selainpalaa.loppupalautenavigointi").click() 
            

            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")

        # SANASANELU

        def sanasanelu():
            sanat = driver.find_elements_by_class_name("harjoituskohta.kirjoitettava.playsoundonfocus")
            
            for i in range(len(sanat)):
                
                if piste_threshold_reached == True:
                    break
                else:
                    if human_state == 1:
                        human_behaviour()
                    
                    sanelu_oikea_vastaus = (sanat[i]).get_attribute("data-oikeatvastaukset").split('"text":"', 1)[1].split('"}', 1)[0]
                    print(sanelu_oikea_vastaus)
                    write(sanelu_oikea_vastaus)
                    (sanat[i]).send_keys(sanelu_oikea_vastaus)
                    (sanat[i]).send_keys(Keys.ENTER)
                    
            
            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            if len(driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")) > 0:
                (driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")[0]).click()

            else:
                driver.find_element_by_class_name("selainpalaa.loppupalautenavigointi").click() 
            

            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")


        # AUKKOLAUSE

        def aukkolause():
            
            lauseet = driver.find_elements_by_class_name("harjoituskohta.kirjoitettava.painettava")
            
            for i in range(len(lauseet)):
                
                if piste_threshold_reached == True:
                    break
                else:
                    if human_state == 1:
                        human_behaviour()

                    aukkolause_oikea_vastaus = (lauseet[i]).get_attribute("data-oikeatvastaukset").split('"text":"', 1)[1].split('"}]}', 1)[0]
                    print(aukkolause_oikea_vastaus)
                    write(aukkolause_oikea_vastaus)
                    (lauseet[i]).send_keys(aukkolause_oikea_vastaus)
                    (lauseet[i]).send_keys(Keys.ENTER)

            
            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            if len(driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")) > 0:
                (driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")[0]).click()

            else:
                driver.find_element_by_class_name("selainpalaa.loppupalautenavigointi").click() 
            

            time.sleep(0.5)
            print("Exercise done!")


        # AUKKOSANA

        def aukkosana():
            
            aukot = driver.find_elements_by_class_name("harjoituskohta.kirjoitettava")
            
            for i in range(len(aukot)):
                
                if piste_threshold_reached == True:
                    break
                else:
                    if human_state == 1:
                        human_behaviour()
                
                    aukkosana_oikea_vastaus = (aukot[i]).get_attribute("data-oikeatvastaukset").split('"text":"', 1)[1].split('"}]}', 1)[0]
                    print(aukkosana_oikea_vastaus)
                    write(aukkosana_oikea_vastaus)
                    (aukot[i]).send_keys(aukkosana_oikea_vastaus)
                    (aukot[i]).send_keys(Keys.ENTER)

            
            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            if len(driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")) > 0:
                (driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")[0]).click()

            else:
                driver.find_element_by_class_name("selainpalaa.loppupalautenavigointi").click() 
            

            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")


        # KUVAVALINTA

        def kuvavalinta():
            
            driver.execute_script("window.scrollTo(0, 180);")
            kuvat = driver.find_elements_by_xpath("//*[@data-ratkaisupainallus='1']")
            for i in range(len(kuvat)):
                
                if piste_threshold_reached == True:
                    break
                else:
                    if human_state == 1:                    
                        human_behaviour()
                
                    (kuvat[i]).click()
                    time.sleep(5)


            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            if len(driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")) > 0:
                (driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")[0]).click()

            else:
                driver.find_element_by_class_name("selainpalaa.loppupalautenavigointi").click() 
            

            time.sleep(0.5)
            print("Exercise done!")


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
                
                if piste_threshold_reached == True:
                    break
                else:
                    if human_state == 1:                    
                        human_behaviour() 
                
                    ristikko_oikea_vastaus = (ristit[i]).get_attribute("data-oikeamerkki")
                    (ristit[i]).send_keys(ristikko_oikea_vastaus)
                    



            time.sleep(10)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            if len(driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")) > 0:
                (driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")[0]).click()

            else:
                driver.find_element_by_class_name("selainpalaa.loppupalautenavigointi").click() 
            
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
        
                time.sleep(1)
        
                for i in pysty_alku:
                    driver.execute_script("arguments[0].click();", i)
                    time.sleep(0.2)

                    for i in pysty_loppu:
                        driver.execute_script("arguments[0].click();", i)
                        time.sleep(0.2)
        
                time.sleep(0.5)

                for i in vaaka_alku:

                    if piste_threshold_reached == True:
                        break
                    else:
                        if human_state == 1:                    
                            human_behaviour()                 
              
                        driver.execute_script("arguments[0].click();", i)
                        time.sleep(0.2)

                            
                        for i in vaaka_loppu:
                            driver.execute_script("arguments[0].click();", i)
                            time.sleep(0.2)
        
            time.sleep(1)


            time.sleep(12)   
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            if len(driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")) > 0:
                (driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")[0]).click()

            else:
                driver.find_element_by_class_name("selainpalaa.loppupalautenavigointi").click() 
    

            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")


        # MONIVALINTA

        def monivalinta():
            
            monit = driver.find_elements_by_xpath("//*[@data-oikeaarvo]")

            for i in range(len(monit)):
                
                if piste_threshold_reached == True:
                    break
                else:
                    if human_state == 1:                    
                        human_behaviour()                
                
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

            if len(driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")) > 0:
                (driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")[0]).click()

            else:
                driver.find_element_by_class_name("selainpalaa.loppupalautenavigointi").click() 
            

            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")


        # YHDISTELY

        def yhdistely():
            
            yhdit = driver.find_elements_by_xpath("//*[@data-oikeaarvo]")

            for i in range(len(yhdit)):
                
                if piste_threshold_reached == True:
                    break
                else:
                    if human_state == 1:                    
                        human_behaviour()                 
                
                    yhdistely_oikea_vastaus = (yhdit[i]).get_attribute('data-oikeaarvo')
                    (yhdit[i]).click()
                    driver.find_element_by_xpath('//div[text()="%s"]' % yhdistely_oikea_vastaus).click()
                    print(yhdistely_oikea_vastaus)
                    write(yhdistely_oikea_vastaus)

            
            time.sleep(12)
            driver.execute_script("window.scrollTo(0, 1080);")
            time.sleep(0.5)

            if len(driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")) > 0:
                (driver.find_elements_by_class_name("vaihdaosoite.loppupalautenavigointi")[0]).click()

            else:
                driver.find_element_by_class_name("selainpalaa.loppupalautenavigointi").click() 
            

            time.sleep(0.5)
            print("Exercise done!")
            write("Exercise done!")





        # SANASTO MENU

        all_the_elems =  ('//*[@id="divValikkoItemit"]/div[1]'
        , '//*[@id="divValikkoItemit"]/div[2]', '//*[@id="divValikkoItemit"]/div[3]'
        , '//*[@id="divValikkoItemit"]/div[4]', '//*[@id="divValikkoItemit"]/div[5]'
        , '//*[@id="divValikkoItemit"]/div[6]', '//*[@id="divValikkoItemit"]/div[7]'
        , '//*[@id="divValikkoItemit"]/div[8]', '//*[@id="divValikkoItemit"]/div[9]'
        , '//*[@id="divValikkoItemit"]/div[10]', '//*[@id="divValikkoItemit"]/div[11]'
        , '//*[@id="divValikkoItemit"]/div[12]', '//*[@id="divValikkoItemit"]/div[13]'
        , '//*[@id="divValikkoItemit"]/div[14]', '//*[@id="divValikkoItemit"]/div[15]')


        # FINAL FINISHED FUNCTION

        def omg(): 
            for i in range(len(driver.find_elements_by_class_name("selausvalikko.vaihdaosoite"))):
                driver.find_element_by_xpath(all_the_elems[i]).click()
                time.sleep(0.5)
                sub_menu()
                print("Section completed!")
                write("Section completed")
                time.sleep(1)
                driver.find_element_by_class_name("vaihdaosoite.ohjelmapaluupainike").click()

        # SUB MENU FOR LOOP FUNCTION

        def sub_menu():
            for i in range(len(driver.find_elements_by_class_name("selausvalikko.vaihdaosoite"))):
                driver.find_element_by_xpath(all_the_elems[i]).click()
                time.sleep(0.5)
                sub_sub_menu()
                time.sleep(0.5)
                driver.find_element_by_class_name("vaihdaosoite.ohjelmapaluupainike").click()


        # SUB SUB MENU FOR LOOP FUNCTION

        def sub_sub_menu():
            for i in range(len(driver.find_elements_by_class_name("selausvalikko.vaihdaosoite"))):
                (driver.find_elements_by_class_name("selausvalikko.vaihdaosoite")[i]).click()
                time.sleep(0.5)
                
                skip_check = skip_var.get()
                if skip_check == 1:
                    exercises_skip_enabled()
                else: 
                    exercises()


                time.sleep(0.5)
                driver.find_element_by_class_name("vaihdaosoite.ohjelmapaluupainike").click()

        
        # EXERCISES FUNCTION

        def exercises():

            for i in range(len(driver.find_elements_by_class_name('selausaihio_aladivi'))):
                
                exercise = (driver.find_elements_by_class_name('selausaihio_aladivi')[i]).get_attribute('innerText').partition('\n')[0][4:]
                print(exercise)
                write(exercise)
                
                exercise_score = (driver.find_elements_by_xpath('//*[@title="Paras aihiosta saamasi tulos"]')[i]).get_attribute('innerText')
                
                try:
                    print(exercise_score)
                    write(exercise_score)
                
                except NoSuchElementException:
                    
                    exercise_score = "0"
                    print("0")
                    write("0")

                (driver.find_elements_by_class_name("selausaihio_aladivi")[i]).click()
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
                else:
                    print("Unable to indentify exercise! \nSkipping...")
                    write("Unable to indentify exercise! \nSkipping...")
                    continue


        # EXERCISES FUNCTION WITH "SKIP COMPLETED" ENABLED

        def exercises_skip_enabled():

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

                if int(exercise_score) > 70:
                    
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
                    else:
                        print("Unable to indentify exercise! \nSkipping...")
                        write("Unable to indentify exercise! \nSkipping...")
                        continue


        omg()
        
        print("Automation finished")
        write("Automation finished!")
        time.sleep(5)
        driver.quit()



    # COLOR HEX

    navy = '#343647'
    gray = '#CCCCCC'


    # BACKGROUND IMAGE
    
    background = PhotoImage(file="img\\bot_bg_2.png")
    bg_label = Label(root, image=background)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)
    bg_label.image = background

    # BUTTONS

    # SKIP CHECKBOX
    skip_var = IntVar(value=1)
    skip_check = Checkbutton(root, bg=gray, height=1, text="Skip completed exercises", variable=skip_var)
    skip_check.place(x=12, y=55)
    
    # HUMANLIKE BEHAVIOUR CHECKBOX
    human_var = IntVar(value=0)
    human_check = Checkbutton(root, bg=gray, height=1, text="Humanlike behaviour", variable=human_var)
    human_check.place(x=12, y=80)

    # ENTRIES
    
    username_text = StringVar(root)
    password_text = StringVar(root)
    
    username = Entry(root, bg=navy, fg="white", textvariable=username_text, width=25)
    username.place(x=380, y=46, relwidth=0.33, relheight=0.047)

    password = Entry(root, bg=navy, fg="white", textvariable=password_text, show="*", width=25)
    password.place(x=380, y=80, relwidth=0.33, relheight=0.047)
    

    # NOW PLAYING TEXT

    now_playing = Label(root, bg=gray, text=" ")
    now_playing.place(x=150, y=0)

    
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
    music_thread.start()
    




    # TERMINAL THING

    terminal = Text(root, bg=navy, fg="white", height=9, width=42)
    terminal.place(x=374, y=367)
    terminal.insert(END, "I dream of life, it might come true")
    terminal.config(state='disabled')
    
    # TEXT INTO TERMINAL

    def write(*message, end = "\n", sep = " "):
        terminal.config(state='normal')
        text = ""
        for i in message:
            text += "{}".format(i)
            text += sep
        text += end
        terminal.insert(INSERT, text)
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


    def lock_and_run_chrome():
        terminal.config(state='normal')
        terminal.delete('1.0', END)
        lock()
        chrome_thread = threading.Thread(target=chrome_script)
        chrome_thread.start()


    # LOGIN BUTTON

    login = Button(root, bg=gray, width=6, height=1, text="login", command=lock_and_run_chrome)
    login.place(x=465, y=130)
    
    # DROPDOWN MENU FOR ENGLISH/SWEDISH MODE
    
    OPTIONS = [
    "Swedish",
    "English",
    "German",
    "Spanish",
    "Russian",
    "French",
    "Italian"] 

    lang_variable = StringVar(root)
    lang_variable.set(OPTIONS[0])

    dropdown_menu = OptionMenu(root, lang_variable, *OPTIONS)
    dropdown_menu.place(x=12, y=12)
    dropdown_menu.config(bg=gray)
    dropdown_menu["menu"].config(bg=gray)


    # INFO POPUP

    lines = ['Opinaika bot', ' ', 'Please, read the instructions in readme.nfo ', ' ', ' ', ' ', ' ',
     ' ', ' ', 'Made by Arrow', ' ', '©2021 Eternal Bliss All rights reserved',  '']
    messagebox.showinfo(' A Dream of Life', "\n".join(lines))


# PROGRESS BAR FUNCTION

bar.start(16)

def stop_progressbar():
    bar.stop()
    bar['value'] = 100
    splash_root.after(650)
    main_window()


splash_root.after(1950, stop_progressbar)

bar.place(x=-2, y=307, relwidth=1, relheight=0.042)



mainloop()

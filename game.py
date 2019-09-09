import tkinter as tk
import random
from tkinter import simpledialog
import os.path
import time
from tkinter import ttk
import winsound as sound
import threading

class Start_page():
    def __init__(self, root, width, height):
        self.root = root
        self.root.title('ultimate driver v. 1.0')
        self.root.geometry('+200+50')
        self.root.resizable(False, False)
        self.widgets()
        self.username = ''
        self.toplevel=False
        global game
        game=False

    def widgets(self):
        thefont = 'Arial 24'
        self.f1 = tk.Frame(self.root)
        self.f1.pack(side='top',fill="both")
        self.canvas = tk.Canvas(self.f1, width=width, height=height, bg='lightyellow')
        self.canvas.pack()
        self.start_image = tk.PhotoImage(file='images/start_background.gif' )
        self.start_screen = self.canvas.create_image(0, 0, image=self.start_image, anchor='nw')
        self.f2 = tk.Frame(self.canvas)
        self.label = tk.Label(self.f2, text='username:',font='Arial 10 bold',bg="red",fg="white")
        self.label.pack(expand=0, fill='both')
        self.entry = tk.Entry(self.f2, font='Arial 19', width=10)  # το πλαίσιο εισαγωγής κειμένου
        self.entry.pack(fill='both', expand=1)
        self.entry.insert(0,"player")
        self.canvas.create_window(int(self.canvas['width']) / 2, int(self.canvas['height']) / 2-100, window=self.f2)
        self.f3=tk.Frame(self.canvas)
        self.label = tk.Label(self.f3, text='Choose level:',font='Arial 10 bold',bg="red",fg="white")
        self.label.pack(expand=0, fill='both')
        self.combo_level()
        self.canvas.create_window(int(self.canvas['width'])/2,int(self.canvas['height'])/2,window=self.f3)
        self.f4 = tk.Frame(self.canvas)
        self.label = tk.Label(self.f4, text='Choose car:',font='Arial 10 bold',bg="red",fg="white")
        self.label.pack(expand=0, fill='both')
        self.combo_car()
        self.canvas.create_window(int(self.canvas['width']) / 2, int(self.canvas['height']) / 2+100, window=self.f4)
        self.f5 = tk.Frame(self.canvas)
        self.button_start = tk.Button(self.f5, text=' New game ', font="Forte 24" ,command=self.new_game,width=10)
        self.button_start.pack(side='bottom', fill='y',expand=0)
        self.canvas.create_window(int(self.canvas['width']) / 2, int(self.canvas['height']) / 2 + 200, window=self.f5)
        self.f6 = tk.Frame(self.canvas)
        self.button_scores = tk.Button(self.f6, text=' High scores ',font=thefont,command=self.retrieve_sorted_scores,width=10)
        self.button_scores.pack(side='left', fill='y', expand=0)
        self.button_info = tk.Button(self.f6, text='[ i ]', font=thefont,command=self.info, width=3)
        self.button_info.pack(side='left', fill='y', expand=0)
        self.speaker_on = tk.PhotoImage(file='images/Speaker_Icon.gif')
        self.speaker_off = tk.PhotoImage(file='images/Mute_Icon.gif')
        if speaker:
            self.button_speaker = tk.Button(self.f6, image=self.speaker_on,command=self.sound_off)
            self.button_speaker.pack(side='left', fill='y', expand=0)
            sound.PlaySound("Racing-Menu", sound.SND_ASYNC | sound.SND_LOOP)
        else:
            self.button_speaker = tk.Button(self.f6, image=self.speaker_off, command=self.sound_on)
            self.button_speaker.pack(side='left', fill='y', expand=0)
            sound.PlaySound(None, sound.SND_PURGE)
        self.canvas.create_window(int(self.canvas['width']), int(self.canvas['height']), window=self.f6,anchor="se")

    def new_game(self):
        self.username=self.entry.get()
        if not self.username:self.username="player"
        self.car_color = self.box_car.get()
        self.car=tk.PhotoImage(file='images/'+self.car_color+'.gif')
        self.value_of_combo_level = self.box_level.get()
        self.box_level.destroy()
        self.box_car.destroy()
        self.canvas.delete('all')
        if self.value_of_combo_level == "easy":
            self.road_name = "road"
            self.side_ground_name = "gravel"
            Level(self.root,self.car,self.f1,self.canvas,self.username,self.road_name,self.side_ground_name,1)
        elif self.value_of_combo_level == "normal":
            self.road_name = "roadway"
            self.side_ground_name = "ground"
            Level(self.root,self.car,self.f1,self.canvas,self.username,self.road_name,self.side_ground_name,2)
        elif self.value_of_combo_level == "hard":
            self.road_name = "highway"
            self.side_ground_name = "grass"
            Level(self.root,self.car,self.f1,self.canvas,self.username,self.road_name,self.side_ground_name,3)

    def retrieve_sorted_scores(self):
        the_famous = []
        message = '\n\nSo far the highest scores are:\n'
        if not self.toplevel:
            self.t = tk.Toplevel()
            self.t.geometry('+200+50')
            self.toplevel=True
            self.t.protocol("WM_DELETE_WINDOW", self.exit)
            self.t.title("ultimate driver v. 1.0 High scores")
            self.confirm = tk.Button(self.t,text='OK',command=self.exit,font="Arial 12", width=10).pack(expand=0, fill='x',side='bottom')
            tk.Label(self.t, text=message, bg='lightyellow', font="Arial 12").pack(expand=1, fill='x', side="top")
            if os.path.isfile('ultimate driver.txt'):
                for line in open('ultimate driver.txt', 'r', encoding='utf-8'):
                    the_famous.append(line.strip().split(';'))
                for x in the_famous:  # reverse time in order to sort by multiple keys
                    x.append(- (int(x[2].split(':')[0]) * 60 + int(x[2].split(':')[1])))
                the_famous = sorted(the_famous, key=lambda x: (int(x[1]), x[3]), reverse=True)
                message1="Name"
                message2 = "Points"
                message3="Time"
                for n, f in enumerate(the_famous):
                    message1 += "\n"+f[0]
                    message2 += "\n"+f[1]
                    message3 += "\n"+f[2]
                    if n == 4: break
                tk.Label(self.t,text=message1,bg='lightyellow', font="Arial 12", justify="left").pack(expand=1,fill='both',side="left")
                tk.Label(self.t,text=message2,bg='lightyellow', font="Arial 12", justify="left").pack(expand=1,fill='both',side="left")
                tk.Label(self.t,text=message3,bg='lightyellow', font="Arial 12", justify="left").pack(expand=1,fill='both',side="left")
        else:
            self.t.lift()

    def exit(self):
        self.t.destroy()
        self.toplevel=False

    def info(self):
        message="Easy level:\nΠατήστε τα βελάκια για να κινήσετε το αμάξι.Καθώς ο χρόνος κυλάει η βενζίνη σας μειώνεται." \
                "Μαζέψτε όσα περισσότερα νομίσματα μπορείτε πριν ξεμείνετε απο βενζίνη ή φροντίστε να αναφοδιάζεστε " \
                "με μπιτόνια όταν αυτά εμφανίζονται για να συνεχίσετε το παιχνίδι.\nNormal level:\nΣε αυτό το επίπεδο" \
                " εκτός από τον κίνδυνο να ξεμείνετε από βενζίνη έχετε και τους βράχους που εμφανίζονται ξαφνικά και η" \
                " πρόσκρουση μαζί τους προκαλεί σοβαρές ζημιές στο αμάξι σας.Προσπαθήστε να μείνετε μακρυά τους και κρατήστε" \
                " το αμάξι σας αρκετό γερό για να συνεχίστε το ταξίδι σας.\nHard level:\nΈγινε ένα ατύχημα στην εθνική οδό" \
                " και ο δρόμος γέμισε γυαλιά.Προσπαθήστε να τα αποφύγετε γιατί δεν έχετε πολλές ρεζέρβες.\nΚαλή διασκέδαση!!"
        simpledialog.messagebox.showinfo("ultimate driver v. 1.0 Info", message)

    def sound_off(self):
        sound.PlaySound(None, sound.SND_PURGE)
        self.button_speaker.config(image=self.speaker_off,command=self.sound_on)
        global speaker
        speaker=False

    def sound_on(self):
        sound.PlaySound("Racing-Menu", sound.SND_ASYNC | sound.SND_LOOP)
        self.button_speaker.config(image=self.speaker_on, command=self.sound_off)
        global speaker
        speaker = True

    def combo_level(self):
        self.box_value_level = tk.StringVar()
        self.box_level= ttk.Combobox(self.f3, textvariable=self.box_value_level,state='readonly',values=('easy','normal','hard'))
        self.box_level.current(0)
        self.box_level.pack(expand=0, fill='both')

    def combo_car(self):
        self.box_value_car = tk.StringVar()
        self.box_car = ttk.Combobox(self.f4,textvariable=self.box_value_car, state='readonly',
                values=('red','yellow',"white",'blue','green','grey','pink',"lightblue","van",'police'))
        self.box_car.current(0)
        self.box_car.pack(expand=0, fill='both')

class Star():
    def __init__(self,canvas,car,road_width,side_ground_width):
        self.canvas = canvas
        self.road_width = road_width
        self.side_ground_width = side_ground_width
        self.thecar=car
        self.star = tk.PhotoImage(file='images/star.gif')
        self.create_star()

    def create_star(self):
        self.list = []
        while len(self.list) <20:
            while True:
                self.x = random.randint(self.side_ground_width + 10, self.side_ground_width + self.road_width - 50)
                self.y = random.randint(-8000, -5)
                self.thestar = self.canvas.create_image(self.x, self.y, image=self.star, anchor='nw')
                if not self.hit_object():break
                self.canvas.delete(self.thestar)
            self.list.append(self.thestar)

    def hit_object(self):  # έλεγχος αν χτύπησε άλλο αντικείμενο του καμβά
        overlapping_items = self.canvas.find_overlapping(*self.canvas.bbox(self.thestar))
        return False if len(overlapping_items) < 2 else True

    def move(self,speed):
        self.canvas.update()
        for i in self.list:
            self.canvas.move(i,0,speed)
            self.canvas.update()
            x = self.canvas.bbox(i)
            overlapping_items = self.canvas.find_overlapping(*x)
            detect_collision = True
            if len(overlapping_items) > 2:
                detect_collision = self.handlecollision(overlapping_items,i)
            if x[1]>int(self.canvas["height"]):
                self.list.remove(i)
            if len(self.list)==0:
                self.create_star()

    def handlecollision(self,t,i):
        if self.thecar in t:
            if speaker: sound.PlaySound("coin", sound.SND_ASYNC)
            self.list.remove(i)
            self.canvas.delete(i)
            self.update_points()

    def show_points(self):
        self.points=0
        self.p=self.canvas.create_text(int(self.canvas['width'])-65, int(self.canvas['height'])-30,
                                fill="yellow", text=self.points, font="Arial 20", anchor='se')

    def update_points(self):
        self.points+=1
        if self.points==100:
            self.canvas.delete(self.p)
            self.p = self.canvas.create_text(int(self.canvas['width']) - 60, int(self.canvas['height']) - 30,
                                             fill="yellow", text=self.points, font="Arial 20", anchor='se')
        self.canvas.itemconfig(self.p,text=self.points)

class Fuel():
    def __init__(self, canvas, car, road_width, side_ground_width):
        self.canvas = canvas
        self.road_width = road_width
        self.side_ground_width = side_ground_width
        self.thecar = car
        self.gas = tk.PhotoImage(file='images/gas.gif')
        self.active_blink=False
        self.color = "red"
        self.create_gas()

    def create_gas(self):
        self.list = []
        while len(self.list) <1:
            while True:
                self.x = random.randint(self.side_ground_width + 10, self.side_ground_width + self.road_width - 50)
                self.y = random.randint(-6000, -2000)
                self.thegas = self.canvas.create_image(self.x, self.y, image=self.gas, anchor='nw')
                if not self.hit_object():break
                self.canvas.delete(self.thegas)
            self.list.append(self.thegas)

    def hit_object(self):  # έλεγχος αν χτύπησε άλλο αντικείμενο του καμβά
        overlapping_items = self.canvas.find_overlapping(*self.canvas.bbox(self.thegas))
        return False if len(overlapping_items) <2 else True

    def move(self,speed):
        self.canvas.update()
        for i in self.list:
                self.canvas.move(i,0,speed)
                self.canvas.update()
                x = self.canvas.bbox(i)
                overlapping_items = self.canvas.find_overlapping(*x)
                detect_collision = True
                if len(overlapping_items) > 2:
                    detect_collision = self.handlecollision(overlapping_items,i)
                if x[1]>int(self.canvas["height"]):
                    self.list.remove(i)
                if len(self.list)==0:
                    self.create_gas()

    def handlecollision(self,t,i):
        if self.thecar in t:
            if speaker: sound.PlaySound("gas", sound.SND_ASYNC)
            self.list.remove(i)
            self.update_gas()
            self.canvas.delete(i)
            x = self.canvas.bbox(self.thecar)
            self.col_message = self.canvas.create_text(x[0] +10, x[1] - 50, text="+1%",fill="white", font="Arial 20", anchor='nw')
            self.canvas.update()
            self.canvas.after(150, self.canvas.delete(self.col_message))

    def show_fuel(self):
        self.fuel=100
        self.f=self.canvas.create_text(int(self.canvas['width'])-55, int(self.canvas['height'])-145,
                                fill="white", text=str(self.fuel)+"%", font="Arial 15", anchor='se')

    def update_gas(self):
        if self.fuel<100:
            self.fuel+=1
            if self.fuel<=9:
                self.canvas.itemconfig(self.f,text="Low!\n  "+str(self.fuel)+"%",fill="red")
                if not self.active_blink:
                    self.blink()
            else:
                if self.active_blink:
                    self.stop_blink()
                self.canvas.itemconfig(self.f,text=str(self.fuel)+"%",fill="white")

    def blink(self):
        self.active_blink = True
        self.color="black" if self.color=="red" else "red"
        self.canvas.itemconfig(self.f, fill=self.color)
        self.b = self.canvas.after(600, self.blink)

    def stop_blink(self):
        self.canvas.after_cancel(self.b)
        self.active_blink=False

class Rock():
    def __init__(self,root,canvas,car,road_width,side_ground_width):
        self.root=root
        self.canvas = canvas
        self.thecar=car
        self.road_width = road_width
        self.side_ground_width = side_ground_width
        self.rock = tk.PhotoImage(file='images/rock.gif')
        self.boom = tk.PhotoImage(file='images/boom.gif')
        self.smoke = tk.PhotoImage(file='images/smoke.gif')
        self.smoke_on=False
        self.create_rock()

    def create_rock(self):
        self.list = []
        while len(self.list) <1:
            while True:
                self.x = random.randint(self.side_ground_width + 10, self.side_ground_width + self.road_width - self.rock.width())
                self.y = random.randint(-6000, -2000)
                self.therock = self.canvas.create_image(self.x, self.y, image=self.rock, anchor='nw')
                if not self.hit_object():break
                self.canvas.delete(self.therock)
            self.list.append(self.therock)

    def hit_object(self):  # έλεγχος αν χτύπησε άλλο αντικείμενο του καμβά
        overlapping_items = self.canvas.find_overlapping(*self.canvas.bbox(self.therock))
        return False if len(overlapping_items) < 2 else True

    def move(self,speed):
        self.canvas.update()
        for i in self.list:
                self.canvas.move(i,0,speed)
                self.canvas.update()
                x = self.canvas.bbox(i)
                self.detect_collision = True
                overlapping_items = self.canvas.find_overlapping(*x)
                if len(overlapping_items) > 2:
                    self.detect_collision = self.handlecollision(overlapping_items,i)
                if x[1]>int(self.canvas["height"]):
                    self.list.remove(i)
                if len(self.list)==0:
                    self.create_rock()

    def handlecollision(self, t, i):
        if self.thecar in t:
            if speaker: sound.PlaySound("crash", sound.SND_ASYNC)
            x = self.canvas.bbox(self.thecar)
            self.theboom = self.canvas.create_image(x[0] - 95, x[1] - 50, image=self.boom, anchor='nw')
            self.col_message = self.canvas.create_text(x[0]-15 , x[1] + 45, text="-5%", font="Arial 45", anchor='nw')
            self.canvas.update()
            self.canvas.after(900, self.canvas.update())
            self.update_damage()
            self.canvas.delete(self.therock)
            self.canvas.delete(self.col_message)
            self.create_rock()
            self.canvas.delete(self.theboom)
            
    def show_damage(self):
        self.damage=100
        self.d=self.canvas.create_text(int(self.canvas['width'])-32, int(self.canvas['height'])-265,
                                fill="white", text=str(self.damage)+"%", font="Arial 15", anchor='se')

    def update_damage(self):
            self.damage-=5
            self.canvas.itemconfig(self.d,text=str(self.damage)+"%")
            if self.damage==40:
                x = self.canvas.bbox(self.thecar)
                self.thesmoke = self.canvas.create_image(x[0]-20, x[1]+15, image=self.smoke, anchor='nw')
                self.smoke_on=True

class Glass():
    def __init__(self,parent, root, canvas, car, road_width, side_ground_width):
        self.parent=parent
        self.root = root
        self.canvas = canvas
        self.thecar = car
        self.road_width = road_width
        self.side_ground_width = side_ground_width
        self.glass = tk.PhotoImage(file='images/glass.gif')
        self.speed=8
        self.flat_tire = False
        self.bar_on = False
        self.create_glass()

    def create_glass(self):
        self.list = []
        while len(self.list) <1:
            while True:
                self.x = random.randint(self.side_ground_width + 10,
                                        self.side_ground_width + self.road_width - self.glass.width())
                self.y = random.randint(-6000, -2000)
                self.theglass = self.canvas.create_image(self.x, self.y, image=self.glass, anchor='nw')
                if not self.hit_object(): break
                self.canvas.delete(self.theglass)
            self.list.append(self.theglass)

    def hit_object(self):  # έλεγχος αν χτύπησε άλλο αντικείμενο του καμβά
        overlapping_items = self.canvas.find_overlapping(*self.canvas.bbox(self.theglass))
        return False if len(overlapping_items) < 2 else True

    def move(self,speed):
        self.canvas.update()
        for i in self.list:
                self.canvas.move(i, 0, speed)
                self.canvas.update()
                x = self.canvas.bbox(i)
                self.detect_collision =False
                overlapping_items = self.canvas.find_overlapping(*x)
                if len(overlapping_items) > 2:
                    self.detect_collision = self.handlecollision(overlapping_items, i)
                if x[1] > int(self.canvas["height"]):
                    self.list.remove(i)
                if len(self.list) == 0:
                    self.create_glass()

    def handlecollision(self, t, i):
        if self.thecar in t:
            self.canvas.tag_raise(self.thecar)
            if self.flat_tire==False:
                if speaker: sound.PlaySound("glass", sound.SND_ASYNC)
                self.update_tires()
                self.slow_down()
                self.flat_tire=True

    def slow_down(self):
        self.speed-=0.05

    def start_car(self):
        self.speed+=0.05

    def change_tire(self):
        x = self.canvas.bbox(self.thecar)
        self.f1 = tk.Frame(self.canvas)
        self.mes = tk.StringVar()
        self.mes.set("change tire")
        change_tire = tk.Label(self.f1, fg='white', bg='black', font='Arial 15', textvariable=self.mes, width=10)
        change_tire.pack(side='top', fill='x', expand=False, pady=2, padx=2)
        self.progress = ttk.Progressbar(self.f1, orient="horizontal", length=100, mode='determinate')
        self.progress.pack(side="bottom",padx=5)
        self.w=self.canvas.create_window(x[0]-20,x[1]+100, window=self.f1, anchor='sw')
        self.parent.run = False
        self.progress_value=0
        self.bar_on=True
        self.bar()

    def bar(self):
        # Function responsible for the updation
        # of the progress bar value
        if self.progress_value < 100:
            self.progress_value += 20
            self.progress['value'] = self.progress_value
            root.update_idletasks()
            self.canvas.update()
            self.b = self.canvas.after(1000, self.bar)
        else:
            self.mes.set("completed")
            self.canvas.update()
            self.canvas.after(400, self.canvas.delete(self.w))
            self.bar_on = False
            self.flat_tire = False
            self.parent.run = True
            self.start_car()
            self.parent.moveup()

    def show_tires(self):
        self.tires = 5
        self.t = self.canvas.create_text(int(self.canvas['width']) - 52, int(self.canvas['height']) - 351,
                                         fill="white", text=str(self.tires) , font="Arial 20", anchor='se')

    def update_tires(self):
        self.tires -= 1
        if self.tires!=-1:self.canvas.itemconfig(self.t, text=str(self.tires) )

class Level():
    def __init__(self,root,car,f,canvas,username,road_name,side_ground_name,level):
        self.car=car
        self.f=f
        self.canvas=canvas
        self.root=root
        self.username=username
        self.road_name=road_name
        self.side_ground_name=side_ground_name
        self.level=level
        self._elapsedtime = 0.0
        self.run = False
        self.speed=0
        self.beginning=True
        self.root.protocol("WM_DELETE_WINDOW", self.exit)
        global game
        game=True
        self.widgets()

    def widgets(self):
        self.road = tk.PhotoImage(file='images/'+self.road_name+'.gif')
        self.road_height = self.road.height()
        self.road_width = self.road.width()
        self.side_ground = tk.PhotoImage(file='images/'+self.side_ground_name+'.gif')
        self.side_ground_height = self.side_ground.height()
        self.side_ground_width = self.side_ground.width()
        self.car_height = self.car.height()
        self.car_width = self.car.width()
        self.bag=tk.PhotoImage(file='images/bag.gif')
        self.bag_height = self.bag.height()
        self.bag_width = self.bag.width()
        self.pump = tk.PhotoImage(file='images/pump.gif')
        self.pump_height = self.pump.height()
        self.pump_width = self.pump.width()
        self.theroad1 = self.canvas.create_image(self.side_ground_width, 0, image=self.road, anchor='nw')
        self.theroad2 = self.canvas.create_image(self.side_ground_width,self.road_height , image=self.road, anchor='nw')
        self.theside_ground1 = self.canvas.create_image(0, 0, image=self.side_ground, anchor='nw')
        self.theside_ground2 = self.canvas.create_image(0,self.side_ground_height , image=self.side_ground, anchor='nw')
        self.theside_ground3 = self.canvas.create_image(self.side_ground_width+self.road_width,0 ,image=self.side_ground, anchor='nw')
        self.theside_ground4 = self.canvas.create_image( self.side_ground_width+self.road_width,self.side_ground_height,
                                                         image=self.side_ground, anchor='nw')
        self.thebag=self.canvas.create_image(int(self.canvas['width']), int(self.canvas['height']), image=self.bag, anchor='se')
        self.thepump = self.canvas.create_image(int(self.canvas['width']), int(self.canvas['height'])-self.bag_height,
                                                                                        image=self.pump,anchor='se')
        self.thecar = self.canvas.create_image(self.side_ground_width+self.road_width/2+130,
                                               int(self.canvas['height'])- self.car_height-20,image=self.car, anchor='nw')
        self.f1 = tk.Frame(self.canvas)
        self.save = tk.PhotoImage(file='images/save.gif')
        self.button_save_score = tk.Button(self.f1,image=self.save,command=self.save_score)
        self.button_save_score.pack(side='left', fill='both', expand=1)
        self.button_save_score.config(state="disable")
        self.button_pause = tk.Button(self.f1, text='| |', font="Arial 20", command=self.pause,width=3)
        self.button_pause.pack(side='left', fill='y', expand=0)
        self.button_pause.config(state="disable")
        self.canvas.create_window(0,0, window=self.f1, anchor="nw")
        self.stars=Star(self.canvas,self.thecar,self.road_width,self.side_ground_width)
        self.fuels=Fuel(self.canvas,self.thecar,self.road_width,self.side_ground_width)
        if self.level == 2 or self.level == 3:
            self.tool = tk.PhotoImage(file='images/tool.gif')
            self.thetool = self.canvas.create_image(int(self.canvas['width']),int(self.canvas['height'])-self.bag_height
                                                        -self.pump_height-10,image=self.tool, anchor='se')
            self.rocks = Rock(self.root,self.canvas, self.thecar, self.road_width, self.side_ground_width)
            self.rocks.show_damage()
        if self.level==3:
            self.tire=tk.PhotoImage(file='images/tire.gif')
            self.thetire = self.canvas.create_image(int(self.canvas['width'])-5,int(self.canvas['height']) - self.bag_height
                                                    - self.pump_height - self.tool.height()-15, image=self.tire, anchor='se')
            self.glasses = Glass(self,self.root, self.canvas, self.thecar, self.road_width, self.side_ground_width)
            self.glasses.show_tires()
        self.show_time()
        self.show_username()
        self.stars.show_points()
        self.fuels.show_fuel()
        self.my_message = self.canvas.create_text(int(self.canvas['width']) / 2, int(self.canvas['height']) / 2,
                                                  fill="black", text="", font="Arial 45", anchor='nw')
        self.canvas.update()
        if speaker:sound.PlaySound("countdown", sound.SND_ASYNC )
        time.sleep(1)
        self.count_down(3)
        self.start_game()

    def start_game(self):
        self.button_pause.config(state="normal")
        self.run=True
        self.distance=0
        self.start_timer()
        self.root.bind('<Left>', self.moveleft)
        self.root.bind('<Right>', self.moveright)
        if speaker:
            sound.PlaySound(None, sound.SND_PURGE)
        self.moveup()

    def update_fuel(self):
        self.fuels.fuel-=1
        if self.fuels.fuel == 0:
            self.game_over()
        elif self.fuels.fuel<=9:
            self.canvas.itemconfig(self.fuels.f,text="Low!\n  "+str(self.fuels.fuel)+"%",fill="red")
            if not self.fuels.active_blink :
                self.fuels.blink()
        else:
            if self.fuels.active_blink:
                self.fuels.stop_blink()
            self.canvas.itemconfig(self.fuels.f,text=str(self.fuels.fuel)+"%",fill="white")

    def game_over(self):
        if speaker: sound.PlaySound("Game-over", sound.SND_ASYNC)
        self.run = False
        self.stop_timer()
        if self.fuels.fuel<=9:
            self.fuels.stop_blink()
            self.canvas.itemconfig(self.fuels.f, text="Low!\n  " + str(self.fuels.fuel) + "%", fill="red")
        self.canvas.create_text(350,100,fill="red", text="game over", font="Arial 45", anchor='nw')
        self.button_save_score.config(state="normal")
        self.button_pause.config(state="disable")
        self.f2 = tk.Frame(self.canvas)
        self.button_play_again = tk.Button(self.f2, text=' play again ',command=self.play_again,font="Arial 20", width=10)
        self.button_play_again.pack(side='top', fill='y', expand=0)
        self.button_start_page = tk.Button(self.f2, text=' start page ', font="Arial 20", command=self.start_page,width=10)
        self.button_start_page.pack(side='top', fill='both', expand=0)
        self.button_quit = tk.Button(self.f2, text=' quit ', font="Arial 20", command=self.quit, width=10)
        self.button_quit.pack(side='top', fill='both', expand=0)
        self.canvas.create_window(400,200, window=self.f2, anchor="nw")

    def play_again(self):
        self.canvas.delete("all")
        Level(self.root,self.car,self.f,self.canvas,self.username,self.road_name,self.side_ground_name,self.level)

    def start_page(self):
        self.f.destroy()
        start = Start_page(root, width, height)

    def save_score(self):
        if self.username==None:self.username="player"
        the_famous=[]
        if os.path.isfile('ultimate driver.txt'):
            for line in open('ultimate driver.txt', 'r', encoding='utf-8'):
                the_famous.append(line.strip().split(';')[0])
        while self.username=="player" or self.username=="" or self.username in the_famous:
            if self.username=="player" or self.username=="":self.username = simpledialog.askstring("Save", "Add username")
            elif self.username in the_famous:
                self.username = simpledialog.askstring("Save", "This username is already taken.\nPlease use another.")
        try:
            openfile = 'a' if os.path.isfile('ultimate driver.txt') else 'w'
            with open('ultimate driver.txt', openfile, encoding='utf-8') as f:
                f.write(self.username + ';' + str(self.stars.points) + ';' + self._set_time(self._elapsedtime) + '\n')
            simpledialog.messagebox.showinfo("Save", "The save was successful!")
            self.button_save_score.configure(state='disabled')
        except:simpledialog.messagebox.showinfo("Save","The save was unsuccessful!")

    def pause(self):
        self.button_pause.config(state="disable")
        self.stop_timer()
        self._minutes = int(self.timestr.get().split(':')[0])
        self._seconds = int(self.timestr.get().split(':')[1])
        self.run=False
        if self.level==3:
            if self.glasses.bar_on:
                self.canvas.after_cancel(self.glasses.b)
        if self.fuels.fuel<=9:
            self.fuels.stop_blink()
            self.canvas.itemconfig(self.fuels.f, text="Low!\n  " + str(self.fuels.fuel) + "%", fill="red")
        self.f3 = tk.Frame(self.canvas)
        self.button_resume = tk.Button(self.f3, text=' resume', font="Arial 20", command=self.resume,width=10)
        self.button_resume.pack(side='top', fill='both', expand=0)
        self.button_start_page = tk.Button(self.f3, text=' start page ', font="Arial 20", command=self.start_page,width=10)
        self.button_start_page.pack(side='top', fill='both', expand=0)
        self.button_quit = tk.Button(self.f3, text=' quit ', font="Arial 20", command=self.quit, width=10)
        self.button_quit.pack(side='top', fill='both', expand=0)
        self.w=self.canvas.create_window(400, 200, window=self.f3, anchor="nw")

    def resume(self):
            self.canvas.delete(self.w)
            self.button_pause.config(state="normal")
            self._start = time.time() - self._minutes * 60 - self._seconds
            self._update_timer()
            if self.fuels.fuel<=9:
                self.fuels.blink()
            if self.level == 3 and self.glasses.bar_on:
                self.glasses.bar()
            else:
                self.run = True
                self.moveup()

    def quit(self):
        self.root.destroy()

    def moveright(self, event):
        if self.run:
            x = self.canvas.bbox(self.thecar)
            if x[2] <= int(self.canvas["width"])-self.side_ground_width and self.run:
                self.canvas.move(self.thecar, 40, 0)
                if self.level==2 or self.level==3:
                    if self.rocks.smoke_on:
                        self.canvas.move(self.rocks.thesmoke, 40, 0)

    def moveleft(self, event):
        if self.run:
            x = self.canvas.bbox(self.thecar)
            if x[0] > self.side_ground_width+20 and self.run:
                self.canvas.move(self.thecar, -40, 0)
                if self.level == 2 or self.level == 3:
                    if self.rocks.smoke_on:
                        self.canvas.move(self.rocks.thesmoke, -40, 0)

    def moveup(self):
        while self.run:
            if self.beginning and self.speed<8:
                self.speed+=0.03
            else:
                self.speed=8
                self.beginning=False
            if self.level==3 and not self.beginning:
                if self.glasses.speed<8 and self.glasses.speed>0:
                    if self.glasses.flat_tire:self.glasses.slow_down()
                    else:self.glasses.start_car()
                elif self.glasses.speed > 8:self.glasses.speed = 8
                elif self.glasses.speed<0:
                    self.glasses.speed=0
                    if self.glasses.tires == -1:
                        self.game_over()
                        break
                    self.glasses.change_tire()
                self.speed=self.glasses.speed
                self.glasses.move(self.speed)
            self.move_background(self.speed)
            self.stars.move(self.speed)
            self.fuels.move(self.speed)
            self.distance += 1
            if self.distance == 300 :
                self.update_fuel()
                self.distance = 0
            if self.level==2 or self.level == 3:
                self.rocks.move(self.speed)
                if self.rocks.damage==0:
                    self.game_over()

    def move_background(self,speed):
            self.canvas.move(self.theroad1, 0, speed)
            self.canvas.move(self.theroad2, 0, speed)
            self.canvas.move(self.theside_ground1, 0, speed)
            self.canvas.move(self.theside_ground2, 0, speed)
            self.canvas.move(self.theside_ground3, 0, speed)
            self.canvas.move(self.theside_ground4, 0, speed)
            coord1 = self.canvas.coords(self.theroad1)
            coord2 = self.canvas.coords(self.theroad2)
            coord3 = self.canvas.coords(self.theside_ground1)
            coord4 = self.canvas.coords(self.theside_ground2)
            if min(coord1[1], coord2[1]) >= 0:
                if coord1[1] < coord2[1]:
                    self.canvas.move(self.theroad2,0 ,-self.road_height * 2)
                else:
                     self.canvas.move(self.theroad1, 0 ,-self.road_height * 2)
            if min(coord3[1], coord4[1]) >= 0:
                if coord3[1] < coord4[1]:
                    self.canvas.move(self.theside_ground2, 0 ,-self.side_ground_height * 2)
                    self.canvas.move(self.theside_ground4, 0, -self.side_ground_height * 2)
                else:
                    self.canvas.move(self.theside_ground1, 0 ,-self.side_ground_height * 2)
                    self.canvas.move(self.theside_ground3, 0 ,-self.side_ground_height * 2)

    def count_down(self,num):
        self.num=num
        self.msg=str(self.num)
        if self.num >0:
            self.canvas.itemconfig(self.my_message,text=self.msg)
            self.num-=1
            self.msg=str(self.num)
            self.canvas.after(1000,self.canvas.update())
            self.count_down(self.num)
        else:
            self.canvas.itemconfig(self.my_message, text="go")
            self.canvas.after(1000, self.canvas.update())
            self.canvas.delete(self.my_message)

    def show_time(self):
        self.f1 = tk.Frame(self.canvas)
        self.timestr = tk.StringVar()
        time_display = tk.Label(self.f1, fg='green', bg='black', font='Arial 15', textvariable=self.timestr, width=10)
        self._set_time(self._elapsedtime)
        time_display.pack(side='left', fill='x', expand=False, pady=2, padx=2)
        self.canvas.create_window(5, int(self.canvas['height']), window=self.f1, anchor='sw')
        self.f1.update()

    def show_username(self):
        self.f2 = tk.Frame(self.canvas)
        username_display = tk.Label(self.f2, fg='white',bg='black',font='Arial 17',text=self.username)
        username_display.pack(side='left', fill='x', expand=True, pady=2, padx=2)
        self.canvas.create_window(5, int(self.canvas['height'])-40, window=self.f2, anchor='sw')

    def _set_time(self, elap):
        """ Όρισε με μορφή Minutes:Seconds το StringVar timestr """
        minutes = int(elap / 60)
        seconds = int(elap - minutes * 60.0)
        self.timestr.set('%02d:%02d' % (minutes, seconds))
        return '%02d:%02d' % (minutes, seconds)

    def _update_timer(self):
        """ Ανανέωσε το label with με τον χρόνο που έχει περάσει. """
        self._elapsedtime = time.time() - self._start
        self._set_time(self._elapsedtime)
        self._timer = self.root.after(200, self._update_timer)

    def start_timer(self):
        """ Ξεκίνησε τη μέτρηση του χρόνου """
        self._elapsedtime = 0.0
        self._start = time.time() - self._elapsedtime
        self._update_timer()

    def stop_timer(self):
        """ Σταμάτησε τη χρονομέτρηση """
        self.root.after_cancel(self._timer)
        self._elapsedtime = time.time() - self._start

    def exit(self):
        if not game:self.root.destroy()

if __name__ == '__main__':
    root = tk.Tk()
    padx, pady = 15, 15
    margin = 10
    width = 950
    height = 580
    global speaker
    speaker=True
    start = Start_page(root, width, height)
    root.mainloop()
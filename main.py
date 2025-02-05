import os, json

with open("data/shaders_lib.json", "r", encoding="utf-8") as f:
    shaders = json.load(f)  

class GameCreator():
    def __init__(self):
        
        path = input('Path: ')
        name = input('Name: ')
        
        self.game_path = path+name
        
        self.mechanics = {
         'None': None   
        }
        
        self.imports = []
        self.particles = []
        
        self.mechanics = False
        self.screen = False
        
        self.help = '''
         :q - quit
         :m - mechanics
         :c - compile
        '''
        
    def init_game(self):
        os.mkdir(self.game_path)
        os.mkdir(self.game_path+'/shaders')
        os.mkdir(self.game_path+'/scripts')
        os.mkdir(self.game_path+'/data')
        
        main = open(f"{self.game_path}/main.py", "w")
        for i in self.imports:
            main.write(i+'\n')
            
        if self.screen:
            vert_shader = open(f"{self.game_path}/shaders/shader.vert", "w")
            vert_shader.write(shaders['vert'])
            
            frag_shader = open(f"{self.game_path}/shaders/shader.frag", "w")
            frag_shader.write(shaders['frag'])
        
    def pick_mechanics(self):
        self.mechanics = True
        
        os.system('clear')
        print(''' 
            pick mechanics - 
            0 - back;
            1 - init Game Class;
            2(path) - add font;
            3(width=640, height=360) - add screen; zoom; screen_shake; scroll; zoom;
            4(path) - add anim;
            5(path) - add particles;
            6(level_name, path) - add tileset; tileset script;
            7(path) - add ui; ui script;
            8(name) - set caption;
            9 - add player; player script;
            10 - add fps;
            11 - add buff script;
            ''')
        
    def run(self):
        os.system('clear')
        
        while True:
            us_write = input(':')
            
            if self.mechanics:
                if us_write == '0':
                    os.system('clear')
                    self.mechanics = False
                    
                elif us_write == '1':
                    self.imports.append(
                        'import sys, pygame, random\nfrom scripts.utils import Animation, Tileset, load_image'
                    )
                    
                    print('Successfully added class added')
                
                elif us_write == '2':
                    print('Successfully font added')
                
                elif us_write == '3':
                    self.screen = True
                    print('Successfully added screen')
                    
                
                elif us_write == '4':
                    print('Successfully added class added')
                
                elif us_write == '5':
                    self.imports.append(
                        'from scripts.particles import Particle, load_particle_images'
                    )
                    
                    print('Successfully particles added')
                
                elif us_write == '6':
                    print('Successfully tileset added')
                
                elif us_write == '7':
                    self.imports.append(
                        'from scripts.ui import SkillsUI, BuffUI'
                    )
                    
                    print('Successfully ui added')
                
                elif us_write == '8':
                    print('Successfully caption setted')
                
                elif us_write == '9':
                    print('Successfully player added')
                
                elif us_write == '10':
                    print('Successfully fps added')
                
                elif us_write == '11':
                    print('Successfully buffs added')
                    
                else:
                    print('error')

            else:
                if us_write == 'q':
                    os.system('clear')
                    break
                
                elif us_write == 'm':
                    self.pick_mechanics()
                
                elif us_write == 'h':
                    print(self.help)
                    
                elif us_write == 'c':
                    self.init_game()
                
                else:
                    print('Unknow command -> write :h to help!')
        

GameCreator().run()
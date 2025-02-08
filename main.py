import os, json, re

with open("data/shaders_lib.json", "r", encoding="utf-8") as f:
    shaders = json.load(f)  
    
with open("data/base_lib.json", "r", encoding="utf-8") as f:
    cycle_parts = json.load(f)  

class GameCreator():
    def __init__(self):
        
        self.game = False
        
        path = input('Path: ')
        self.name = input('Name: ')
        
        self.game_path = path+self.name
        
        self.mechanics = {
         'None': None   
        }
        
        self.imports = []
        self.values = []
        
        self.functions = []
        
        self.core_loop = [[],[],[]]
                
        self.mechanics = False
        self.screen = False
        self.anim = []
        self.ui = []
        
        self.help = '''
         :q - quit
         :m - mechanics
         :c - compile
        '''
        
    def get_input_values(self, us_input):
        [(lambda x: int(x) if x.isdigit() else (x.lower() == "true" if x.lower() in ("true", "false") else x.strip('"')))(x) for x in us_input.group(1).split(', ')] if us_input else []
        
    def init_game(self):
        os.mkdir(self.game_path)
        os.mkdir(self.game_path+'/shaders')
        os.mkdir(self.game_path+'/scripts')
        os.mkdir(self.game_path+'/data')
        
        main = open(f"{self.game_path}/main.py", "w")
        for i in self.imports:
            main.write(i+'\n')
        
        main.write('\n')
            
        if self.game:
            main.write('class Game():\n    def __init__(self):\n        pygame.init()\n')
            
        for i in self.values:
            if isinstance(i, list):
                for j in i:
                    main.write(f'       {j}\n')
            else:
                main.write(f'       {i}\n')
        
        main.write('\n')
        
        main.write(f"pygame.display.set_caption('{self.name}')\n")
        
        main.write('\n')
        
        if len(self.anim) > 0:
            main.write("       self.animations = {\n")
            for i in self.anim:
                main.write(f'           {i[0]}: Animation({i[1]}, img_dur={i[2]}, loop={i[3]})\n')
            main.write("       }\n")
        
        buttons = []
        
        main.write('\n')
        
        if len(self.ui) > 0:
            main.write("       self.ui = {\n")
            for i in self.ui:
                buttons.append(i[0])
                main.write(f"           '{i[0]}': SkillsUI({i[1]},{i[2]}, load_image('{i[3]}'), {i[4]}, {i[5]}, {i[6]} , '{i[7]}')\n")
            main.write("       }\n")        
        
        main.write('\n')
        
        main.write("self.button_conditions = {" + ", ".join(f"'{btn}': False" for btn in buttons) + "}")
        
        main.write('\n')
        
        for func in self.functions:
            main.write(func)
        
        main.write('\n\n    def run(self):\n        while True:')
        
        for i in self.core_loop:
            for j in i:
                for l in j:
                    main.write('            '+j+'\n')
        
        if self.screen:
            vert_shader = open(f"{self.game_path}/shaders/shader.vert", "w")
            vert_shader.write(shaders['vert'])
            
            frag_shader = open(f"{self.game_path}/shaders/shader.frag", "w")
            frag_shader.write(shaders['frag'])
        
        if self.game:
            main.write('if __name__ == "__main__":\n    Game().run()')
        
        
    def pick_mechanics(self):
        self.mechanics = True
        
        os.system('clear')
        print(''' 
            pick mechanics - 
            0 - back;
            1 - init Game Class;
            2(path) - add font;
            3(width=640, height=360) - add screen; zoom; screen_shake; scroll; zoom;
            4(name, path, img_dur, loop) - add anim;
            5(path) - add particles;
            6(level_name, path) - add tileset; tileset script;
            7(name, width, height, img, x, y, kd, key) - add ui; ui script;
            8 - add player; player script;
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
                    self.game = True
                    self.imports.append(
                        'import sys, pygame, random\nfrom scripts.utils import Animation, Tileset, load_image'
                    )
                    
                    self.values.append(["self.clock = pygame.time.Clock()", "self.t = 0"])
                    
                    self.core_loop[0].append([
                        "           self.t += self.clock.get_time() / 1000",
                    ])
                    
                    self.core_loop[1].append([
                        "           for event in pygame.event.get():",
                        "               if event.type == pygame.QUIT:",
                        "                   pygame.quit()",
                        "                   sys.exit()",
                    ])

                    print('Successfully added class added')
                
                elif '2' in us_write:
                    match = re.search(r'\((.*?)\)', us_write)
                    
                    self.values.append(f"self.font = pygame.font.SysFont('{match.group(1)}'), 24)")
                    
                    print('Successfully font added')
                
                elif '3' in us_write:
                    self.screen = True
                    
                    width = 640
                    height = 360
                    
                    self.values.append([
                        f"self.screen = pygame.display.set_mode(({width}, {height}), pygame.OPENGL | pygame.DOUBLEBUF)",
                        "self.display_width, self.display_height = 320, 180",
                        "self.main_shader = Shader('shader', 'shader')",
                        "self.main_surf = pygame.Surface((self.display_width, self.display_height))",
                        "self.decoration_surf = pygame.Surface((self.display_width, self.display_height))",
                        f"self.ui_surf = pygame.Surface(({width}, {height}))",
                        "self.current_zoom = 1.0",
                        "self.target_zoom = 1.0",
                        "self.screen_shake = 0 "
                                        ])

                    self.core_loop[0].append([
                        "self.target_zoom = 1.0",
                        "self.current_zoom += (self.target_zoom - self.current_zoom) * 0.1\n",
                        "self.ui_surf.fill((0,0,255))",
                        "self.main_surf.fill((198, 183, 190))",
                        "self.decoration_surf.fill((0, 0, 0, 0))\n",
                        "self.scroll[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.scroll[0]) / 30",
                        "self.scroll[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.scroll[1]) / 30",
                        "render_scroll = (int(self.scroll[0]), int(self.scroll[1]))\n",
                        "if self.screen_shake > 0:",
                        "   self.screen_shake -= 1",
                        "   self.scroll[0] += random.randint((self.screen_shake//5) * -1, (self.screen_shake//5))",
                        "   self.scroll[1] += random.randint((self.screen_shake//5) * -1, (self.screen_shake//5))\n",
                        "display_mask = pygame.mask.from_surface(self.display)",
                        "display_sillhouette = display_mask.to_surface(setcolor=(0, 0, 0, 180), unsetcolor=(0, 0, 0, 0))\n",
                        "for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:",
                        "   self.display.blit(display_sillhouette, offset)\n",
                    ])
                    
                    self.core_loop[2].append([
                        "zoomed_size = (int(self.main_surf.get_width() * self.current_zoom), int(self.main_surf.get_height() * self.current_zoom))",
                        "offset_x = (self.main_surf.get_width() - zoomed_size[0]) // 2",
                        "offset_y = (self.main_surf.get_height() - zoomed_size[1]) // 2\n",
                        "zoomed_main_surf = pygame.transform.smoothscale(self.main_surf, zoomed_size)",
                        "self.display.blit(zoomed_main_surf, (offset_x, offset_y))\n",
                        "self.decoration_surf.set_colorkey((0, 0, 0))",
                        "zoomed_decoration_surf = pygame.transform.smoothscale(self.decoration_surf, zoomed_size)",
                        "self.display.blit(zoomed_decoration_surf, (offset_x, offset_y))\n",
                        "self.ui_surf.set_colorkey((0,0,255))\n",
                        "screen_surface = pygame.transform.scale(self.display, self.screen.get_size())",
                        "screen_surface.blit(self.ui_surf, (0,0))\n",
                        "self.main_shader.render(screen_surface, self.t)\n",
                        "pygame.display.flip()",
                        "self.clock.tick(60)"
                        
                    ])
                    
                    print('Successfully added screen')
                    
                
                elif '4' in us_write:

                    self.anim.append(self.get_input_values(us_write))
                    
                    print('Successfully anim added')
                
                elif '5' in us_write:
                    self.imports.append(
                        'from scripts.particles import Particle, load_particle_images'
                    )
                    
                    self.core_loop[0].append([
                        "for particle in self.particles[:]:",
                        "   particle.update(self.clock.get_time() / 45)\n",
                        "for particle in self.particles:",
                        "   particle.draw(self.main_surf, self.scroll)\n",
                    ])
                    
                    self.values.append(f"load_particle_images('f{self.get_input_values(us_write)[0]}')")
                    
                    print('Successfully particles added')
                
                elif '6' in us_write:
                    self.values.append([
                        f"self.tileset = Tileset('{self.get_input_values(us_write)[1]}', 16).load_tileset()",
                        "self.tilemap = Tilemap(self, tile_size=16)",
                        f"self.level = '{self.get_input_values(us_write)[0]}'",
                        "self.load_level(self.level)"
                                        ])
                    
                    self.core_loop[0].append([
                        "self.tilemap.render(",
                        "   self.main_surf,",
                        "   self.decoration_surf,",
                        "   self.tileset,",
                        "   offset=render_scroll,",
                        ")\n"
                    ])
                    
                    self.functions.append(cycle_parts['load_lvl'])
                    
                    print('Successfully tileset added')
                
                elif '7' in us_write:
                    self.imports.append(
                        'from scripts.ui import SkillsUI, BuffUI'
                    )
                    
                    self.ui.append(self.get_input_values(us_write))
                    
                    self.core_loop[2].append([
                        "for name, obj in self.ui.items():",
                        "   obj.render(self.ui_surf, state)\n"
                    ])
                    
                    print('Successfully ui added')
                
                elif us_write == '8':
                    
                    self.values.append([
                        "self.movement = [False, False]",
                        "self.player = Player(self, (50, 50), (8, 15))",
                    ])
                    
                    self.core_loop[0].append([
                        "self.player.update(self.tilemap, (self.movement[1] - self.movement[0], 0))",
                        "self.player.render(self.main_surf, offset=render_scroll)\n"
                    ])
                    
                    print('Successfully player added')
                    
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
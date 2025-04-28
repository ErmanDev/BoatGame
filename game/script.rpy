image river movie = Movie(play="images/river.ogv", size=(1920,1080))
image boat = "boat.png"
image btn_left = "left.png"
image btn_right = "right.png"
image btn_left_hover = "buttonarrowleft_hover.png"
image btn_right_hover = "buttonarrowright_hover.png"
image btn_settings = "settings.png"
image btn_settings_hover = "setting_hover.png"
image garbage1 = "obstacle_garbage.png"
image garbage2 = "obstacle_garbage2.png"
image heart_buff = "heart_buff.png"
image heart = "heart.png"
image no_heart = "no_heart.png"
image game_over_frame = "game_over_frame.png"
image pause_menu_frame = "paused_frame.png"
image btn_play_again_idle = "PlayAgain_idle.png"
image btn_play_again_hover = "PlayAgain_hover.png"
image btn_main_menu_idle = "Menu_idle.png"
image btn_main_menu_hover = "Menu_hover.png"
image btn_quit_idle = "Quit_idle.png"
image btn_quit_hover = "Quit_hover.png"
image btn_continue_idle = "Continue_idle.png"
image btn_continue_hover = "Continue_hover.png"
image btn_restart_idle =  "Restart_idle.png"
image btn_restart_hover = "Restart_hover.png"

init python:
    import random
    import time

    boat_xpos = 0.5
    health = 3
    score = 0
    garbage_items = []
    game_running = True
    show_hitboxes = False  
    
    last_spawn_time = time.time()
    spawn_interval = 2.0
    last_column = 2

    LEFT_BOUNDARY = 0.15
    RIGHT_BOUNDARY = 0.85

    BOAT_HITBOX_WIDTH = 0.08  
    BOAT_HITBOX_HEIGHT = 0.3  
    ITEM_HITBOX_WIDTH = 0.08 
    ITEM_HITBOX_HEIGHT = 0.1 
 
    BOAT_YPOS = 0.85
    BOAT_YANCHOR = 0.7

    def move_boat_left():
        global boat_xpos
        if not game_running:
            return
        boat_xpos = max(LEFT_BOUNDARY, boat_xpos - 0.05)
        renpy.show("boat", at_list=[Position(xpos=boat_xpos, ypos=BOAT_YPOS, xanchor=0.5, yanchor=BOAT_YANCHOR), Transform(zoom=1.5)])
        if show_hitboxes:
            renpy.show("boat_hitbox", at_list=[Position(xpos=boat_xpos, ypos=BOAT_YPOS, xanchor=0.5, yanchor=BOAT_YANCHOR)])

    def move_boat_right():
        global boat_xpos
        if not game_running:
            return
        boat_xpos = min(RIGHT_BOUNDARY, boat_xpos + 0.05)
        renpy.show("boat", at_list=[Position(xpos=boat_xpos, ypos=BOAT_YPOS, xanchor=0.5, yanchor=BOAT_YANCHOR), Transform(zoom=1.5)])
        if show_hitboxes:
            renpy.show("boat_hitbox", at_list=[Position(xpos=boat_xpos, ypos=BOAT_YPOS, xanchor=0.5, yanchor=BOAT_YANCHOR)])

    def reset_boat_position():
        global boat_xpos
        boat_xpos = 0.5  
        renpy.show("boat", at_list=[Position(xpos=boat_xpos, ypos=BOAT_YPOS, xanchor=0.5, yanchor=BOAT_YANCHOR), Transform(zoom=1.5)])
        if show_hitboxes:
            renpy.show("boat_hitbox", at_list=[Position(xpos=boat_xpos, ypos=BOAT_YPOS, xanchor=0.5, yanchor=BOAT_YANCHOR)])

    class RiverItem:
        def __init__(self, column):
            self.type = random.randint(1, 3)
            if column == 1:
                self.xpos = 0.25
            elif column == 2:
                self.xpos = 0.5
            else:
                self.xpos = 0.75
            self.ypos = -0.2
            self.active = True
            self.has_scored = False
            self.id = str(renpy.random.random())
            self.speed = random.uniform(0.025, 0.035)

            item_img = "garbage" + str(self.type) if self.type <= 2 else "heart_buff"
            item_zoom = 0.4 if self.type <= 2 else 0.35

            renpy.show(item_img + self.id, what=item_img, at_list=[Position(xpos=self.xpos, ypos=self.ypos, xanchor=0.5, yanchor=0.5), Transform(zoom=item_zoom)])

            if show_hitboxes:
                hitbox_color = "#FF000080" if self.type <= 2 else "#00FF0080"
                renpy.show("item_hitbox" + self.id, what=Solid(hitbox_color, xysize=(ITEM_HITBOX_WIDTH , ITEM_HITBOX_HEIGHT)), 
                         at_list=[Position(xpos=self.xpos, ypos=self.ypos, xanchor=0.5, yanchor=0.5)])

        def update(self):
            global game_running, score
            if not game_running or not self.active:
                return False

            self.ypos += self.speed
            item_img = "garbage" + str(self.type) if self.type <= 2 else "heart_buff"
            item_zoom = 0.4 if self.type <= 2 else 0.35

            renpy.show(item_img + self.id, what=item_img, at_list=[
                Position(xpos=self.xpos, ypos=self.ypos, xanchor=0.5, yanchor=0.5),
                Transform(zoom=item_zoom)
            ])

            if show_hitboxes:
                hitbox_color = "#FF000080" if self.type <= 2 else "#00FF0080"
                renpy.show("item_hitbox" + self.id, what=Solid(hitbox_color, xysize=(ITEM_HITBOX_WIDTH, ITEM_HITBOX_HEIGHT )), 
                         at_list=[Position(xpos=self.xpos, ypos=self.ypos, xanchor=0.5, yanchor=0.5)])

            if self.check_collision():
                self.active = False
                renpy.hide(item_img + self.id)
                if show_hitboxes:
                    renpy.hide("item_hitbox" + self.id)
                return False

            if self.active and not self.has_scored and self.ypos > 0.95:
                self.has_scored = True
                if self.type <=2:
                    score +=1
                    if score >= 5:
                        game_running = False
                        renpy.jump("next_scene")

            if self.ypos > 1.2:
                self.active = False
                renpy.hide(item_img + self.id)
                if show_hitboxes:
                    renpy.hide("item_hitbox" + self.id)
                return False

            return True


        def check_collision(self):
            global health, game_running

            if not self.active or not game_running:
                return False

            x_distance = abs(self.xpos - boat_xpos)
            y_distance = abs(self.ypos - BOAT_YPOS)
            
            x_overlap = x_distance < (BOAT_HITBOX_WIDTH + ITEM_HITBOX_WIDTH) / 2
            y_overlap = y_distance < (BOAT_HITBOX_HEIGHT + ITEM_HITBOX_HEIGHT) / 2
            
            if x_overlap and y_overlap:
                
                if self.type == 3:  
                    if health < 3:
                        health += 1
                else:  
                    health -= 1
                    if health <= 0:
                        game_running = False
                        stop_all_items()

                return True
            
            return False

    def stop_all_items():
        for item in garbage_items:
            if item.active:
                item.active = False
                item_img = "garbage" + str(item.type) if item.type <= 2 else "heart_buff"
                renpy.hide(item_img + item.id)
                if show_hitboxes:
                    renpy.hide("item_hitbox" + item.id)

    def clear_all_items():
        stop_all_items()
        global garbage_items
        garbage_items = []

    def restart_game():
        global health, score, garbage_items, game_running, last_spawn_time, last_column
        
        health = 3
        score = 0
        game_running = True
        last_spawn_time = time.time()
        last_column = 2
    
        clear_all_items()
        reset_boat_position()

    def spawn_items():
        global last_spawn_time, spawn_interval, game_running, last_column
        current_time = time.time()
        
        if game_running and (current_time - last_spawn_time) >= spawn_interval:
            last_column = last_column % 3 + 1
            
            new_item = RiverItem(last_column)
            garbage_items.append(new_item)
            last_spawn_time = current_time
            
            spawn_interval = 2.0

        if game_running:
            for item in list(garbage_items):
                if not item.update():
                    garbage_items.remove(item)

        renpy.restart_interaction()
        renpy.timeout(0.1)

    def toggle_hitboxes():
        global show_hitboxes
        show_hitboxes = not show_hitboxes
        
        if show_hitboxes:
            renpy.show("boat_hitbox", at_list=[Position(xpos=boat_xpos, ypos=BOAT_YPOS, xanchor=0.5, yanchor=BOAT_YANCHOR)])
        else:
            renpy.hide("boat_hitbox")
            
        for item in garbage_items:
            if item.active:
                if show_hitboxes:
                    hitbox_color = "#FF000080" if item.type <= 2 else "#00FF0080"
                    renpy.show("item_hitbox" + item.id, what=Solid(hitbox_color, xysize=(ITEM_HITBOX_WIDTH * 100, ITEM_HITBOX_HEIGHT * 100)), 
                             at_list=[Position(xpos=item.xpos, ypos=item.ypos, xanchor=0.5, yanchor=0.5)])
                else:
                    renpy.hide("item_hitbox" + item.id)


init:
    image boat_hitbox = Solid("#0000FF80", xysize=(BOAT_HITBOX_WIDTH, BOAT_HITBOX_HEIGHT))

screen river_game():
    key "K_LEFT" action Function(move_boat_left)
    key "K_RIGHT" action Function(move_boat_right)
    key "K_h" action Function(toggle_hitboxes) 
    key "K_p" action [SetVariable("game_running", False), Show("pause_menu")]

    imagebutton:
        idle "btn_left"
        hover "btn_left_hover"
        action Function(move_boat_left)
        align (0.1, 0.93)
        sensitive game_running
    imagebutton:
        idle "btn_right"
        hover "btn_right_hover"
        action Function(move_boat_right)
        align (0.9, 0.93)
        sensitive game_running
    imagebutton:
        idle "btn_settings"
        hover "btn_settings_hover"
        action [SetVariable("game_running", False), Show("pause_menu")]
        align (0.99, 0.02)
        sensitive (health > 0)

    text str(score) size 60 color "#FFFFFF" outlines [(2, "#000000", 0, 0)] xalign 0.5 yalign 0.05

    hbox:
        xalign 0.1
        yalign 0.05
        spacing 10
        for i in range(3):
            if i < health:
                add "heart" zoom 0.5
            else:
                add "no_heart" zoom 0.5

    textbutton "Hitboxes (H)":
        action Function(toggle_hitboxes)
        text_color "#FFFFFF"
        xalign 0.85
        yalign 0.14 
        text_size 20

    textbutton "Pause (P)":
        text_color "#FFFFFF"
        xalign 0.85
        yalign 0.05
        text_size 20

    textbutton  "Left (←)":
        text_color "#FFFFFF"
        xalign 0.85
        yalign 0.08
        text_size 20

    textbutton "Right (→)":
        text_color "#FFFFFF"
        xalign 0.85
        yalign 0.11
        text_size 20   

    if not game_running and health <= 0:
        add "game_over_frame.png" at Position(xalign=0.5, yalign=0.5)
        
        text "Final Score: [score]" size 40 color "#FFFFFF":
            xalign 0.5
            yalign 0.42 
            
        imagebutton:
            idle "btn_play_again_idle"
            hover "btn_play_again_hover"
            action Function(restart_game)
            xalign 0.5
            yalign 0.53  
            
        imagebutton:
            idle "btn_main_menu_idle"
            hover "btn_main_menu_hover"
            action MainMenu()
            xalign 0.5
            yalign 0.67  
                    
    timer 0.1 action Function(spawn_items) repeat True


screen pause_menu():
    modal True
    
    add "pause_menu_frame" at Position(xalign=0.5, yalign=0.5)

    text "Score: [score]" size 40 color "#FFFFFF":
        xalign 0.5
        yalign 0.35
            
    imagebutton:
        idle "btn_continue_idle"
        hover "btn_continue_hover"
        action [SetVariable("game_running", True), Hide("pause_menu")]
        xalign 0.5
        yalign 0.45

    imagebutton:
        idle "btn_restart_idle"
        hover "btn_restart_hover"
        action [Function(restart_game), Hide("pause_menu")]
        xalign 0.5
        yalign 0.60

    imagebutton:
        idle "btn_main_menu_idle"
        hover "btn_main_menu_hover"
        action MainMenu()
        xalign 0.5
        yalign 0.75

label start:
    $ health = 3
    $ score = 0
    $ garbage_items = []
    $ game_running = True
    $ last_spawn_time = time.time()
    $ spawn_interval = 2.0
    $ boat_xpos = 0.5
    $ last_column = 2

    show river movie
    show boat at Position(xpos=boat_xpos, ypos=BOAT_YPOS, xanchor=0.5, yanchor=BOAT_YANCHOR), Transform(zoom=1.5)

    if show_hitboxes:
        show boat_hitbox at Position(xpos=boat_xpos, ypos=BOAT_YPOS, xanchor=0.5, yanchor=BOAT_YANCHOR), Transform(zoom=0.1)

    call screen river_game

    return

label next_scene:
    scene black with fade
    


    centered "{size=100}Next Scene{/size}"
    

    
    pause 3.0
    
    return
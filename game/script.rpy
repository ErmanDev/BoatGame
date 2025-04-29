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
image question_textbox = "quiz_assets/question_textbox.png"
image answer_textbox =  "quiz_assets/answer_textbox.png"
image answer_textbox_hover = "quiz_assets/answer_textbox_hover.png"
image background_chapter_one =  "quiz_assets/bg_chap_1.png"
image background_chapter_two =  "quiz_assets/bg_chap_2.png"
image background_chapter_three =  "quiz_assets/bg_chap_3.png"
image game_summary_box =  "quiz_assets/game_summary.png" 
image display_one = "quiz_assets/1.png"
image display_two = "quiz_assets/2.png"
image display_three = "quiz_assets/3.png"
image display_four = "quiz_assets/4.png"
image display_five = "quiz_assets/5.png"



init python:
    import random
    import time

    boat_xpos = 0.5
    health = 3
    score = 0
    garbage_items = []
    game_running = True
    show_hitboxes = False  
    player_answers = []
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

    number_images = {
        1: "display_one",
        2: "display_two",
        3: "display_three",
        4: "display_four",
        5: "display_five",
    }

    

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
                    if score >= 1:
                        game_running = False
                        renpy.jump("chapter_one_intro")

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

label chapter_one_intro:
    scene black with fade
    show question_textbox at center:
        xalign 0.5
        yalign 0.5
    show text "{font=fonts/BBTMartiresFree-ExtraBold.otf}{color=#60301c}{size=180}Chapter 1{/size}" at truecenter
    pause 3
    hide text
    hide question_textbox
    jump chapter_one_quiz

label chapter_one_quiz:
    scene background_chapter_one
    call screen chapter_one_quiz_part_one
    return

screen chapter_one_quiz_part_one:
        
    $feedback_chapter_one_one = " Pinili mong kontrolin ang iyong 90%. Hindi mo hinayaang ang 10% na gulo ni Tatay ang magdikta sa iyong emosyon. Ipinakita mo ang malalim na self-control at kakayahan na pumili ng kapayapaan kaysa gulo. "

    $feedback_chapter_one_two = "Hinayaan mong ang 10% (pagkagalit ni Tatay) ay makahila sa iyo. Bagaman natural ang magalit, nagpakita ito ng kahinaan sa paggamit ng iyong 90% paramanatiling kalmado."

    $feedback_chapter_one_three = "Pinili mong ipahayag ang iyong nararamdaman. Bagama't totoo sa sarili, kailangang maging maingat, dahil maaaring ang iyong 90% na reaksyon ay magpalala ng 10% na problema."

    add "question_textbox" xalign 0.5 yalign 0.2
    text "{color=#60301c}{size=40}1. Sa kabila ng hindi ko makontrol ang pag-uugali ni Tatay, paano ko mapapanatili ang kontrol sa aking emosyon at magiging mas mahinahon sa sitwasyong ito?{/size}":
        xalign 0.5
        yalign 0.28
        xmaximum 1300
        slow_cps 30
        justify True

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_one_one]),
            Hide("chapter_one_quiz_part_one"),
            Show("chapter_one_quiz_part_two")
        ]
        align (0.5, 0.63)
    text "{size=29}Hihinga ako nang malalim at aalis sandali upang pakalmahin ang sarili.":
        xalign 0.5
        yalign 0.62

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_one_two]),
            Hide("chapter_one_quiz_part_one"),
            Show("chapter_one_quiz_part_two")
        ]
        align (0.5, 0.79)
    text "{size=29}Sasabayan ko siya sa pagtaas ng boses upang ipaglaban ang sarili kong punto.":
        xalign 0.5
        yalign 0.76

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_one_three]),
            Hide("chapter_one_quiz_part_one"),
            Show("chapter_one_quiz_part_two")
        ]
        align (0.5, 0.95)
    text "{size=29}Ipapakita ko ang aking galit upang malaman niyang nasasaktan ako.":
        xalign 0.5
        yalign 0.91


screen chapter_one_quiz_part_two:

    $ feedback_chapter_one_part_two_one = "Ginamit mo ang iyong 90% upang piliin ang lakas at pag-aaral sa sitwasyon, sa halip na maging biktima ng 10% na hindi mo kontrolado."
    $ feedback_chapter_one_part_two_two = "Pinili mong maging maingat upang hindi palakihin ang 10% na gulo. Isang indikasyon ng maturity — minsan, ang paggamit ng iyong 90% ay ang pag-iwas sa labanan."
    $ feedback_chapter_one_part_two_three = "Ipinaglaban mo ang iyong dangal, pinapakita na ang iyong 90% ay nakatuon sa pagpapanatili ng self-respect kahit mahirap."
    

    add "question_textbox" xalign 0.5 yalign 0.2
    text "{color=#60301c}{size=40}2. Ano ang magiging epekto sa akin kung pipiliin kong harapin si Tatay sa halip na tahimik na umalis? Alin ang mas makakabuti sa aking kinabukasan?{/size}":
        xalign 0.5
        yalign 0.28
        xmaximum 1300
        slow_cps 30
        justify True

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_one_part_two_one]),
            Hide("chapter_one_quiz_part_two"),
            Show("chapter_one_quiz_part_three")
        ]
        align (0.5, 0.63)
    text "{size=29}Matututo akong tumindig sa aking paninindigan at maging matatag.":
        xalign 0.5
        yalign 0.62

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_one_part_two_two]),
            Hide("chapter_one_quiz_part_two"),
            Show("chapter_one_quiz_part_three")
        ]
        align (0.5, 0.80)
    text "{size=29}Mas lalala ang sitwasyon at baka hindi na kami magkaayos.":
        xalign 0.5
        yalign 0.77

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_one_part_two_three]),
            Hide("chapter_one_quiz_part_two"),
            Show("chapter_one_quiz_part_three")
        ]
        align (0.5, 0.95)
    text "{size=29}Mawawala ang respeto ko sa sarili kung hindi ko siya haharapin.":
        xalign 0.5
        yalign 0.91


screen chapter_one_quiz_part_three:

    $ feedback_chapter_one_part_three_one = " Isang napakagandang paggalang sa 90/10 Principle — hindi mo hinayaan na ang 10% ng sakit ay magdikta ng iyong buhay. Ginamit mo ito para maging mas mabuting tao."

    $ feedback_chapter_one_part_three_two = "Ikaw ay nagsusumikap na maging matalino sa iyong mga karanasan, ngunit kailangan ng balanse para hindi maging bihag ng nakaraan — bahagi ng tamang paggamit ng 90%"

    $ feedback_chapter_one_part_three_three = " Pinili mong kalimutan ang 10% na negatibo. Isang paraan ng self-protection, pero dapat tiyakin na hindi ito magiging hadlang sa tunay na paglago."

    add "question_textbox" xalign 0.5 yalign 0.2
    text "{color=#60301c}{size=40}3. Paano ko magagamit ang aking mga karanasan upang bumuo ng mas positibong pananaw sa buhay, sa halip na hayaang pigilan ako ng aking nakaraan?{/size}":
        xalign 0.5
        yalign 0.28
        xmaximum 1200
        slow_cps 30
        justify True

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_one_part_three_one]),
            Hide("chapter_one_quiz_part_three"),
            Jump("chapter_two_intro")
        ]
        align (0.5, 0.63)
    text "{size=27}Gagawin kong inspirasyon ang aking mga pinagdaanan upang maging mas mabuting tao.":
        xalign 0.5
        yalign 0.62

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_one_part_three_two]),
            Hide("chapter_one_quiz_part_three"),
            Jump("chapter_two_intro")
        ]
        align (0.5, 0.80)
    text "{size=29}Palagi kong aalalahanin ang sakit ng nakaraan upang hindi makalimot.":
        xalign 0.5
        yalign 0.77

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_one_part_three_three]),
            Hide("chapter_one_quiz_part_three"),
            Jump("chapter_two_intro")
        ]
        align (0.5, 0.95)
    text "{size=29}Iwasan ko na lang isipin ang nakaraan at hayaan na lang itong makalimutan.":
        xalign 0.5
        yalign 0.91


label chapter_two_intro:
    scene black with  fade
    show question_textbox at center:
        xalign 0.5
        yalign 0.5
    show text "{font=fonts/BBTMartiresFree-ExtraBold.otf}{color=#60301c}{size=180}Chapter 2{/size}" at truecenter
    pause 3
    hide text
    hide question_textbox
    jump chapter_two_quiz

label chapter_two_quiz:
    scene background_chapter_two
    call screen chapter_two_quiz_part_one
    return

screen chapter_two_quiz_part_one:

    $ feedback_chapter_two_part_one_one = " Ayon sa teorya ng True vs False Self, pinili mong yakapin ang iyong \"True Self\" — na kayang harapin ang sakit at bumuo ng bagong kahulugan. Mula sa pananaw ni Mead, ito ay ang aktibong “I” — ang bahagi mong kumikilos batay sa sariling lakas-loob, hindi lang ayon sa hinihingi ng iba."

    $ feedback_chapter_two_part_one_two = "Pinili mong bitawan ang nakaraan para makapagpatuloy. Kung ito ay tunay na desisyon mula sa iyong puso, ito ay pagsasabuhay ng isang matatag na “Differentiated Self” — hindi ikinukulong ng nakaraan, ngunit hindi rin tinatakasan ang sarili."

    $ feedback_chapter_two_part_one_three = "Ipinapakita ng sagot mo ang pagyakap sa katotohanan ng Multiple Self — kinikilala mong may iba’t ibang bahagi ng sarili na parehong may halaga. Tulad ng sinabi sa handout, ang tao ay hindi iisang mukha lang kundi binubuo ng maraming dynamic selves."

        

    add "question_textbox" xalign 0.5 yalign 0.2
    text "{color=#60301c}{size=40}1. Mas matapang ba ang bumabalik sa nakaraan o ang sumusulong?{/size}":
        xalign 0.5
        yalign 0.28
        xmaximum 1300
        slow_cps 30
        justify True

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_two_part_one_one]),
            Hide("chapter_two_quiz_part_one"),
            Show("chapter_two_quiz_part_two")
        ]
        align (0.5, 0.63)
    text "{size=29}Mas matapang ang humaharap sa nakaraan.":
        xalign 0.5
        yalign 0.62

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_two_part_one_two]),
            Hide("chapter_two_quiz_part_one"),
            Show("chapter_two_quiz_part_two")
        ]
        align (0.5, 0.79)
    text "{size=29}Mas matapang ang sumusulong.":
        xalign 0.5
        yalign 0.76

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_two_part_one_three]),
            Hide("chapter_two_quiz_part_one"),
            Show("chapter_two_quiz_part_two")
        ]
        align (0.5, 0.95)
    text "{size=29}Pareho silang matapang.":
        xalign 0.5
        yalign 0.91


screen chapter_two_quiz_part_two:

    $ feedback_chapter_two_part_two_one =  "Kinikilala mo na ang hindi pagharap ay pagpapalakas ng iyong False Self. Isang mahalagang hakbang sa True Self ang pag-amin na ang takot ay kailangang harapin, hindi takasan."


    $ feedback_chapter_two_part_two_two = " Ito ay porma ng “False Freedom” — akala’y malaya, pero sa totoo'y nakakulong sa hindi natutunang aral. Ayon sa Emotion Convergence ng handout, hindi pagtanggap sa totoong emosyon ay nagdadala ng mas matagal na stress."


    $ feedback_chapter_two_part_two_three =  " Ipinakita mong may malalim kang self-awareness: batid mo na ang pagtakas ay panandalian lamang, at ang tunay na paglaya ay sa pagharap. Ito ay bahagi ng pagkakaroon ng Differentiated Self."
    

    add "question_textbox" xalign 0.5 yalign 0.2
    text "{color=#60301c}{size=40}2. Kung patuloy akong tatakbo palayo sa aking mga problema, magiging malaya ba talaga ako, o lalo lang akong magiging bihag ng sarili kong takot?{/size}":
        xalign 0.5
        yalign 0.28
        xmaximum 1300
        slow_cps 30
        justify True

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_two_part_two_one]),
            Hide("chapter_two_quiz_part_two"),
            Show("chapter_two_quiz_part_three")
        ]
        align (0.5, 0.63)
    text "{size=29}Magiging bihag ako ng takot dahil hindi ko ito hinaharap at natututo mula rito.":
        xalign 0.5
        yalign 0.62

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_two_part_two_two]),
            Hide("chapter_two_quiz_part_two"),
            Show("chapter_two_quiz_part_three")
        ]
        align (0.5, 0.80)
    text "{size=29}Oo, magiging malaya ako basta’t hindi ko na iniisip ang mga problema.":
        xalign 0.5
        yalign 0.77

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_two_part_two_three]),
            Hide("chapter_two_quiz_part_two"),
            Show("chapter_two_quiz_part_three")
        ]
        align (0.5, 0.95)
    text "{size=26}Pansamantala akong makakatakas, pero babalik din ang takot hangga’t hindi ko ito hinaharap.":
        xalign 0.5
        yalign 0.91


screen chapter_two_quiz_part_three:

    $ feedback_chapter_two_part_three_one =  " Ipinapakita nito ang pagsasanib ng iyong “True Self” (katapatan sa sarili) at high Openness to Experience ayon sa Big Five Traits. Ang ganitong attitude ay nagpapalalim sa tunay na pagkatao."

    $ feedback_chapter_two_part_three_two = " Isang uri ng pagtatanggol ng False Self — iniiwasan ang tukso, pero hindi pa lubusang napoproseso ang ugat ng dating ugali. Ang tunay na paglago ay hindi lamang pag-iwas, kundi pagharap na may bagong kamalayan."

    $ feedback_chapter_two_part_three_three =  "Isang malakas na indikasyon ng False Self dominance — kung saan ang sarili ay binabago hindi dahil sa totoong kagustuhan, kundi dahil sa takot sa paghusga ng iba. Ayon kay D.W. Winnicott, ito ang pinagmumulan ng \"poverty of inner life.\""

    add "question_textbox" xalign 0.5 yalign 0.2
    text "{color=#60301c}{size=40}3. Kung tinanggap ko ang aking personal na paglago, paano ko ito mapapanindigan? Paano ko maiiwasan ang pagbagsak sa parehong pagkakamali?{/size}":
        xalign 0.5
        yalign 0.28
        xmaximum 1200
        slow_cps 30
        justify True

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_two_part_three_one]),
            Hide("chapter_two_quiz_part_three"),
            Jump("chapter_three_intro")
        ]
        align (0.5, 0.63)
    text "{size=27}Patuloy kong sisikaping matuto sa bawat karanasan at palibutan ang sarili ng tamang tao.":
        xalign 0.5
        yalign 0.62

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_two_part_three_two]),
            Hide("chapter_two_quiz_part_three"),
            Jump("chapter_three_intro")
        ]
        align (0.5, 0.80)
    text "{size=29}Iwasan ko na lang ang sitwasyong maaaring magbalik sa dati kong ugali.":
        xalign 0.5
        yalign 0.77

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_two_part_three_three]),
            Hide("chapter_two_quiz_part_three"),
            Jump("chapter_three_intro")
        ]
        align (0.5, 0.95)
    text "{size=29}Magpanggap na lang akong nagbago para hindi husgahan ng iba.":
        xalign 0.5
        yalign 0.91


label chapter_three_intro:
    scene black with fade
    show question_textbox at center:
        xalign 0.5
        yalign 0.5
    show text "{font=fonts/BBTMartiresFree-ExtraBold.otf}{color=#60301c}{size=180}Chapter 3{/size}" at truecenter
    pause 3
    hide text
    hide question_textbox
    jump chapter_three_quiz

label chapter_three_quiz:
    scene background_chapter_three
    call screen chapter_three_quiz_part_one
    return

screen chapter_three_quiz_part_one:
    
    $ feedback_chapter_three_part_one_one =  " Pinapakita nito ang iyong pagpapahalaga sa relasyon, ngunit kailangan mong bantayan na hindi ma-kompromiso ang iyong sariling “I” (ang active self na nagsusulong ng sariling kagustuhan) para lamang sa \"Me\" (expectations ng ibang tao)."

    $ feedback_chapter_three_part_one_two = " Ipinapakita nito ang isang matatag na Real Self: ang kakayahan mong ituloy ang iyong personal na misyon kahit walang garantisadong suporta. Ito rin ay indikasyon ng mataas na Self-Determination."

    $ feedback_chapter_three_part_one_three =  " Ipinapakita mong nagsusumikap kang pagsamahin ang multiple selves mo—ang \"self as friend\" at ang \"self as individual\"—isang malusog na pagsasanib ayon sa Unified Self Model"

    add "question_textbox" xalign 0.5 yalign 0.2
    text "{color=#60301c}{size=40}1. Ano ang mas mahalaga sa akin ngayon—ang pagkakaroon ng tiwala at suporta mula sa isang kaibigan tulad ni Biboy, o ang pagsunod sa sarili kong landas kahit mahirap?{/size}":
        xalign 0.5
        yalign 0.28
        xmaximum 1200
        slow_cps 30
        justify True
    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_three_part_one_one]),
            Hide("chapter_three_quiz_part_one"),
            Show("chapter_three_quiz_part_two")
        ]
        align (0.5, 0.63)
    text "{size=28}Mas mahalaga ang tiwala at suporta ni Biboy dahil siya ang naging sandigan ko sa mga mahihirap na panahon.":
        xalign 0.5
        yalign 0.62
        xmaximum 1000
    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_three_part_one_two]),
            Hide("chapter_three_quiz_part_one"),
            Show("chapter_three_quiz_part_two")
        ]
        align (0.5, 0.79)
    text "{size=29}Mas mahalaga ang sarili kong landas dahil ito ang magdadala sa akin sa tunay kong layunin sa buhay.":
        xalign 0.5
        yalign 0.77
        xmaximum 1000

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_three_part_one_three]),
            Hide("chapter_three_quiz_part_one"),
            Show("chapter_three_quiz_part_two")
        ]
        align (0.5, 0.95)
    text "{size=29}Pareho silang mahalaga—ang suporta ng kaibigan ay inspirasyon, pero ang desisyon ay dapat manggaling sa sarili.":
        xalign 0.5
        yalign 0.92
        xmaximum 1000


screen chapter_three_quiz_part_two:

    $ feedback_chapter_three_part_two_one =  "Maaaring nagpapakita ito ng impulsivity o openness to experience, pero kailangan mong suriin kung ito ba ay nakaugat sa tunay mong prinsipyo o sa pressure ng Ideal Self na gusto ng mabilis na tagumpay."

    $ feedback_chapter_three_part_two_two = "Isang malakas na pagyakap sa Real Self. Ito ay pagsunod sa sarili mong inner compass kahit mahirap—isang marka ng mataas na Self-Integrity."

    $ feedback_chapter_three_part_two_three = " Ang pagpili ng reflection bago aksyon ay tanda ng mature na Differentiated Self — hindi padalos-dalos, at isinasaalang-alang ang kabuuan ng sarili."


    add "question_textbox" xalign 0.5 yalign 0.2
    text "{color=#60301c}{size=40}2. Tama bang pagbigyan ko ang alok ni Tom para sa mabilis na pag-angat, kahit na may panganib na malihis ako sa tamang landas? O dapat ko bang alalahanin ang mga aral ni Tatay Pilo?{/size}":
        xalign 0.5
        yalign 0.28
        xmaximum 1200
        slow_cps 30
        justify True
    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_three_part_two_one]),
            Hide("chapter_three_quiz_part_two"),
            Show("chapter_three_quiz_part_three")
        ]
        align (0.5, 0.63)
    text "{size=29}Oo, dapat kong subukan ang alok ni Tom dahil baka ito na ang pagkakataon kong umasenso.":
        xalign 0.5
        yalign 0.62
        xmaximum 1200

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_three_part_two_two]),
            Hide("chapter_three_quiz_part_two"),
            Show("chapter_three_quiz_part_three")
        ]
        align (0.5, 0.79)
    text "{size=29}Hindi, mas mahalagang manatili sa tamang prinsipyo gaya ng itinuro ni Tatay Pilo, kahit mabagal ang progreso.":
        xalign 0.5
        yalign 0.77
        xmaximum 1200

    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
            SetVariable("player_answers", player_answers + [feedback_chapter_three_part_two_three]),
            Hide("chapter_three_quiz_part_two"),
            Show("chapter_three_quiz_part_three")
        ]
        align (0.5, 0.95)
    text "{size=29}Dapat ko munang pag-isipan nang mabuti, timbangin ang mga panganib, at alalahanin ang mga aral na nakatulong sa akin noon.":
        xalign 0.5
        yalign 0.91
        xmaximum 1200

        

screen chapter_three_quiz_part_three:

    $ feedback_chapter_three_part_three_one =  "Ipinapakita nito ang struggle mo sa Ideal Self vs Real Self — ang pagdududa kung ikaw ba ay tumatayo sa sarili mong paa o umaasa sa iba para sa identity."

    $ feedback_chapter_three_part_three_two = " Isang tanda ng maturity at malalim na Real Self: batid mo na ang pagmamahal at koneksyon ay hindi pagsuko ng kalayaan kundi bahagi ng tunay na paglago."

    $ feedback_chapter_three_part_three_three = "Pinapakita mong may malalim kang awareness sa Multiple Self system: ang tamang desisyon ay nakasalalay hindi sa kilos kundi sa puso at layunin sa likod nito."

    add "question_textbox" xalign 0.5 yalign 0.2
    text "{color=#60301c}{size=38}3. Kung pipiliin ko si Tiya Mela at babalik sa aking pamilya, nangangahulugan ba ito na hindi ko kayang tumayo sa sarili kong mga paa? O ito ba ang tamang hakbang upang tunay na makapag-move on?{/size}":
        xalign 0.5
        yalign 0.28
        xmaximum 1200
        slow_cps 30
        justify True
    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
        SetVariable("player_answers", player_answers + [feedback_chapter_three_part_three_one]),
        Hide("chapter_three_quiz_part_three"),
        Show("chapter_three_quiz_part_four")
        ]
        align (0.5, 0.63)
    text "{size=27}Oo, baka nga ibig sabihin nito na hindi pa ako handang magsarili.":
        xalign 0.5
        yalign 0.62
    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
        SetVariable("player_answers", player_answers + [feedback_chapter_three_part_three_two]),
        Hide("chapter_three_quiz_part_three"),
        Show("chapter_three_quiz_part_four")
        ]
        align (0.5, 0.79)
    text "{size=29}Hindi, ang pagbabalik ay hindi kahinaan kundi isang paraan ng pagpapagaling at pagtanggap.":
        xalign 0.5
        yalign 0.77
        xmaximum 1200
    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
        SetVariable("player_answers", player_answers + [feedback_chapter_three_part_three_three]),
        Hide("chapter_three_quiz_part_three"),
        Show("chapter_three_quiz_part_four")]
        align (0.5, 0.95)
    text "{size=29}Depende ito sa intensyon—kung ito’y mula sa takot, baka hindi makakatulong; kung mula sa pagmamahal, baka ito ang tamang desisyon.":
        xalign 0.5
        yalign 0.92
        xmaximum 1200



screen chapter_three_quiz_part_four:

    $ feedback_chapter_three_part_four_one =  " Isang conscious act of Self-Discovery — ang pagsisikap mong tukuyin ang iyong \"True Self\" sa halip na magpa-dala sa expectations ng \"Generalized Other\" (Mead's theory)."

    $ feedback_chapter_three_part_four_two = "Panganib na mahulog sa \"False Self\" — sinusundan ang landas ng iba para lang maabot ang ideal image, hindi ang sariling katotohanan."

    $ feedback_chapter_three_part_four_three = "Pinapakita nito ang proseso ng conscious integration: pag-respeto sa iba't ibang pananaw habang pinipili ang tumutugma sa sariling Real Self."

    add "question_textbox" xalign 0.5 yalign 0.2
    text "{color=#60301c}{size=38}4. Ang bawat isa sa kanila ay may kanya-kanyang pananaw sa buhay—paano ko malalaman kung alin ang pinaka-angkop sa tunay kong pagkatao?{/size}":
        xalign 0.5
        yalign 0.28
        xmaximum 1200
        slow_cps 30
        justify True
    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
        SetVariable("player_answers", player_answers + [feedback_chapter_three_part_four_one]),
        Hide("chapter_three_quiz_part_four"),
        Show("chapter_three_quiz_part_five")]
        align (0.5, 0.63)
    text "{size=26}Sa pamamagitan ng pagninilay sa sarili at pagtukoy kung alin ang nagpapalalim sa aking pagkatao.Sa pamamagitan ng pagninilay sa sarili at pagtukoy kung alin ang nagpapalalim sa aking pagkatao.":
        xalign 0.5
        yalign 0.62
        xmaximum 1100
    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
        SetVariable("player_answers", player_answers + [feedback_chapter_three_part_four_two]),
        Hide("chapter_three_quiz_part_four"),
        Show("chapter_three_quiz_part_five")]
        align (0.5, 0.79)
    text "{size=29}Susubukan kong sundan ang pananaw ng pinakamatagumpay at titingnan kung ito ay babagay sa akin.":
        xalign 0.5
        yalign 0.77
        xmaximum 1100
    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
        SetVariable("player_answers", player_answers + [feedback_chapter_three_part_four_three]),
        Hide("chapter_three_quiz_part_four"),
        Show("chapter_three_quiz_part_five")]
        align (0.5, 0.95)
    text "{size=29}Papakinggan ko silang lahat, pero pipiliin ko ang landas na nagbibigay ng kapayapaan at saysay sa akin.":
        xalign 0.5
        yalign 0.92
        xmaximum 1200


screen chapter_three_quiz_part_five:

    $ feedback_chapter_three_part_five_one =  " Ipinapakita ang mataas na Self-Reflection at Conscientiousness—ang kakayahang isaalang-alang ang buong sarili bago kumilos."

    $ feedback_chapter_three_part_five_two = "Maaaring nagpapakita ng self-protection, pero panganib na mapalakas ang False Self kung puro practicality ang pinaiiral."

    $ feedback_chapter_three_part_five_three = " Isang tanda ng mature Integrated Self — pinapakita mong kaya mong pagsamahin ang puso, isip, at prinsipyo."


    add "question_textbox" xalign 0.5 yalign 0.2
    text "{color=#60301c}{size=38}5. Kung ako ang gagawa ng sarili kong desisyon, paano ko mapapanatili ang balanse sa pagitan ng pagiging praktikal, pagiging makatao, at pagsunod sa aking sariling mga prinsipyo?{/size}":
        xalign 0.5
        yalign 0.28
        xmaximum 1200
        slow_cps 30
        justify True
    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
        SetVariable("player_answers", player_answers + [feedback_chapter_three_part_five_one]),
        Hide("chapter_three_quiz_part_five"),
        Jump("game_summary")]
        align (0.5, 0.63)
    text "{size=28}Maglalaan ako ng oras sa bawat desisyon upang masiguro na hindi ako lumilihis sa aking mga pinaniniwalaan.":
        xalign 0.5
        yalign 0.62
        xmaximum 1000
    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
        SetVariable("player_answers", player_answers + [feedback_chapter_three_part_five_two]),
        Hide("chapter_three_quiz_part_five"), Jump("game_summary")]
        align (0.5, 0.79)
    text "{size=29}Uunahin ko ang praktikal na solusyon, kahit minsan ay isantabi ang emosyon at prinsipyo.":
        xalign 0.5
        yalign 0.77
        xmaximum 1000
    imagebutton:
        idle "answer_textbox"
        hover "answer_textbox_hover"
        action [
        SetVariable("player_answers", player_answers + [feedback_chapter_three_part_five_three]),
        Hide("chapter_three_quiz_part_five"),
        Jump("game_summary")]
        align (0.5, 0.95)
    text "{size=29} Hahanap ako ng gitnang daan kung saan may espasyo ang prinsipyo, puso, at realidad ng buhay.":
        xalign 0.5
        yalign 0.92
        xmaximum 1100

screen game_summary_components():

    

    add "game_summary_box":
        xalign 0.5
        yalign 0.5
        zoom 0.9

    text "{font=fonts/BBTMartiresFree-ExtraBold.otf}{color=#60301c}{size=80}GAME SUMMARY{/size}":
        xalign 0.5
        yalign 0.2

    vbox:
        spacing 30
        xalign 0.5
        

        if current_chapter == 1:
            yalign 0.6
            for i in range(0, 3):
                if i < len(player_answers):
                    hbox:
                        spacing 20
                        xalign 0.5
                        add number_images[i + 1]
                        text "[player_answers[i]]" color "#60301c" xmaximum 1100

        elif current_chapter == 2:
            yalign 0.6
            for i in range(3, 6):
                if i < len(player_answers):
                    hbox:
                        spacing 20
                        xalign 0.5
                        add number_images[i - 2] 
                        text "[player_answers[i]]" color "#60301c" xmaximum 1300

        elif current_chapter == 3:
            yalign 0.6
            for i in range(6, 11):
                if i < len(player_answers):
                    hbox:
                        spacing 20
                        xalign 0.5
                        yalign 0.9
                        add number_images[i - 5] zoom 0.6
                        text "[player_answers[i]]" color "#60301c" size 28 xmaximum 1350


    # Footer buttons
    hbox:
        xalign 0.5
        yalign 1.0
        yoffset -40
        spacing 100
        imagebutton:
            idle "btn_main_menu_idle"
            hover "btn_main_menu_hover"
            action MainMenu()
        imagebutton:
            idle "btn_restart_idle"
            hover "btn_restart_hover"
            action Jump("start")
        imagebutton:
            idle "btn_continue_idle"
            hover "btn_continue_hover"
            action If(current_chapter < 3, SetVariable("current_chapter", current_chapter + 1), Return())


label game_summary:
    scene background_chapter_three
    $ current_chapter = 1
    call screen game_summary_components
    return

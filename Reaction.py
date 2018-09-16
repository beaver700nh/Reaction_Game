from tkinter import *
from time import sleep
from threading import Lock

global running
global mutex

running = True
mutex = Lock()

class Game:
    '''Class to run most of the system functions'''
    
    def __init__(object):
        def kill():
            global running
            running = False
            object.tk.after_cancel(object.timer)
            object.tk.destroy()
        
        object.tk = Tk()
        object.tk.title('Reaction Game')
        object.tk.resizable(0, 0)
        object.tk.wm_attributes('-topmost', 1)

        object.tk.protocol('WM_DELETE_WINDOW', kill)

        object.canvas = Canvas(object.tk, width=250, height=250, bd=0, highlightthickness=0)
        object.canvas.pack()
        object.redraw()

        object.sprites = []
        object.playing = True
        object.current = 0
        object.to_change = 1

    def redraw(object):
        '''Redraws the screen so that things aren't hidden'''
        
        global running
        if running == True:
            object.tk.update()
        if running == True:
            object.tk.update_idletasks()

    def add_sprite(object, sprite):
        '''Adds the sprite "sprite" to the list of sprites to animate'''
        
        object.sprites.append(sprite)

    def set_color(object):
        object.sprites[object.current].set_color()

    def mainloop(object):
        '''Runs the main loop that animates the sprites
in the list of sprites that were added by
"add_sprite"'''
        
        def blink_sprite():  
            # for sprite in object.sprites:
            global mutex
            if mutex.acquire(blocking=False):
                try:
                    if object.playing:
                        object.sprites[object.current].blink()
                        
                        object.current += object.to_change
                        if object.current == 4 and \
                           object.to_change == 1:
                            object.to_change = -1

                        elif object.current == 0 and \
                             object.to_change == -1:
                            object.to_change = 1

                finally:
                    mutex.release()

            object.timer = object.tk.after(100, blink_sprite)

        object.timer = object.tk.after(100, blink_sprite)
            
        object.tk.mainloop()
        # global running
        # while running == True:
        #     for sprite in object.sprites:
        #         global mutex
        #         mutex.acquire()
        #         try:
        #             if object.playing:
        #                 sprite.blink()

        #         finally:
        #             mutex.release()
        
class Light:
    '''Class for the lights on the screen'''
    
    def __init__(object, color, coords, game):
        object.position = coords.split('@')
        object.canvas = game.canvas
        object.game = game
        object.color = color
        object.id = object.canvas.create_oval(0, 0, 15, 15, fill='#bcbcbc')
        object.canvas.move(object.id, int(object.position[0]), int(object.position[1]))

        object.game.redraw()

    def set_color(object):
        object.canvas.itemconfig(object.id, fill=object.color)
        object.game.redraw()

    def blink(object):
        '''Turns the light on and off; "blinking"'''
        
        global running
        if running == True:
            object.canvas.itemconfig(object.id, fill=object.color)
            object.game.redraw()
            
        if running == True:
            sleep(0.1)
            
        if running == True:
            object.canvas.itemconfig(object.id, fill='#bcbcbc')
            object.game.redraw()

class ControlButtons:
    '''Class to show the buttons controlling the lights'''
    
    def __init__(object, color, text_color, text, coords, command, game):
        object.game = game
        object.position = coords.split('@')

        object.button = Button(object.game.tk, text=text, bg=color, fg=text_color, command=command)
        object.button.place(x=int(object.position[0]), y=int(object.position[1]))
        object.game.redraw()

g = Game()

left         = Light('#ff0000', '60@120', g)
left_center  = Light('#ffee00', '90@120', g)
center       = Light('#00bb00', '120@120', g)
right_center = Light('#ffee00', '150@120', g)
right        = Light('#ff0000', '180@120', g)

def stop_lights():
    '''Stops the light from running back and forth'''
    
    g.playing = False
    g.set_color()

def start_lights():
    '''Starts the light running back and forth that was stopped by 
the function stop_lights()'''
    
    g.playing = True
            
stop = ControlButtons('#ff0000', '#0000ff', 'Stop', '90@170', stop_lights, g)
start = ControlButtons('#00ff00', '#ffffff', 'Start', '130@170', start_lights, g)

g.add_sprite(left)
g.add_sprite(left_center)
g.add_sprite(center)
g.add_sprite(right_center)
g.add_sprite(right)

g.mainloop()

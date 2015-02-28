from Tkinter import *


class Sprite(object):
    def __init__(self, root, **kwargs):
	self.position_left = 0
	self.position_top = 0
        self._root_app = root
	self._set_up(**kwargs)
        self._loopframes(0)
    
    def _set_up(self, **kwargs):
	self._spritesheet = PhotoImage(file=kwargs.get('sheet', 'spritesheet.gif'))
	self.set_frames(**kwargs)
	self.load_frames(kwargs.get('start_frames', 'idle'))
	self._canvas = Canvas(self._root_app, width=kwargs.get('width', 200), height=kwargs.get('height', 200))
	self._canvas.pack()
	self.set_controls()
    
    def set_frames(self, **kwargs):
	self.last_frame = None
	self.position_left = kwargs.get('left', self.position_left)
	self.position_top = kwargs.get('top', self.position_top)
	frame_settings = kwargs.get('frames', {'idle': [(32, 48), (0,0)]})

	for name, settings in frame_settings.iteritems():
	    frame_width = settings[0][0]
	    frame_height = settings[0][1]
	    frame_left = settings[0][2] + self.position_left if len(settings[0])>2 else self.position_left
	    frame_top = settings[0][3] + self.position_top if len(settings[0])>3 else self.position_top
	    frame_cooridinates = settings[1:] # list of frame cooridinates
	
	    frames = [] # list of frame images

	    for frame in frame_cooridinates:
	     	i = frame[0]
	    	j = frame[1]
	    	x = frame[2] if len(frame)>2 else 0
	    	y = frame[3] if len(frame)>3 else 0

	   	frames.append( self.create_frame(frame_width*i, frame_height*j, frame_width*(i+1), frame_height*(j+1), frame_left+x, frame_top+y) )

	    self.save_frames(name, frames, settings)

    def create_frame(self, l, t, r, b, left=None, top=None):
	left = self.position_left if left is None else (left if left>=0 else 0)
	top = self.position_top if top is None else (top if top>=0 else 0)
        dst = PhotoImage()
        dst.tk.call(dst, 'copy', self._spritesheet, '-from', l, t, r, b, '-to', left, top)
	return dst

    def get_frames(self, name):
	settings = self.frame_store.get(name, {'settings': []})['settings']
	return {name: settings}
 
    def has_name(self, name):
	return self.frame_store.get(name) is not None

    def save_frames(self, name, frames, settings):
	self.frame_store = self.frame_store if hasattr(self, 'frame_store') else {}
	self.frame_store[name] = {'frames': frames,'settings': settings}

    def load_frames(self, name):
	self.name = name
	self.frames = self.frame_store.get(name, {'frames':[]})['frames']

    def set_controls(self):
	self._root_app.bind("<Key>", self.key_mapper)
    
    def key_mapper(self, event):
	print('KEYPRESS')
	if event.keycode == 113:
	    self.move(left=25, name='left')
	elif event.keycode == 114:
	    self.move(right=25, name='right')
	elif event.keycode == 111:
	    self.move(up=25, name='up')
	elif event.keycode == 116:
	    self.move(down=25, name='down')
	elif event.keycode == 65:
	    self.move(name='jump')
	else:
	    self.move(name='idle')
	    print("Keycode " + str(event.keycode) + " is not registered")

    def move(self, **kwargs):
	self._canvas.delete(self.last_frame)
	position = [self.position_left, self.position_top]

	for direction, offset in kwargs.iteritems():
	    if direction == 'left':
		position[0] = self.position_left-offset if self.position_left>=offset else self.position_left
	    elif direction == 'up':
		position[1] = self.position_top-offset if self.position_top>=offset else self.position_top
   	    elif direction == 'right':
		position[0] = self.position_left+offset
	    elif direction == 'down':
		position[1] = self.position_top+offset
	
	self.set_frames(left=position[0], top=position[1], frames=self.get_frames(kwargs.get('name', self.name)))
	self.load_frames(kwargs.get('name', self.name))
		

    def _loopframes(self, frame):
	frame = len(self.frames)-1 if frame>len(self.frames)-1 else frame
        self._canvas.delete(self.last_frame)
        self.last_frame = self._canvas.create_image(16, 24, image=self.frames[frame])
        self._root_app.after(75, self._loopframes, (frame+1) % len(self.frames))

app = Tk()
sprite = Sprite(app,
    frames={
	'idle':[(32, 48), (0,0)],
	'left':[(32, 48), (0,1), (1,1), (2,1), (3,1)],
	'up':[(32, 48), (0,3), (1,3), (2,3), (3,3)],
	'right':[(32, 48), (0,2), (1,2), (2,2), (3,2)],
	'down':[(32, 48), (0,0), (1,0), (2,0), (3,0)],
	'jump':[(32, 48), (0,0,0,-2), (0,0,0,-5), (0,0,0,-8), (0,0,0,-15)]
    }
)
app.mainloop()
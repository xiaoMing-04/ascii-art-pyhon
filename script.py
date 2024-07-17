import pygame as pg
import cv2
import time
from ffpyplayer.player import MediaPlayer

class Artconvert:
    def __init__(self, path='my_video.mp4', font_size=12) -> None:
        pg.init()
        
        self.path = path
        
        self.cap = cv2.VideoCapture(path)
        self.player = MediaPlayer(path)
        self.WIDTH = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)) // 2
        self.HEIGHT = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) // 2
        self.RES = (self.WIDTH, self.HEIGHT)
        self.CHAR_STEP = int(font_size * 0.5)
        
        self.image = self.get_image()
        self.surface = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        
        self.font = pg.font.SysFont('Courier', font_size, bold=True)
        self.ASCII_CHARS = "  .:-=+*#%@"
        self.RENDERED_ASCII_CHARS = [self.font.render(char, False, 'white') for char in self.ASCII_CHARS]
        self.ASCII_COEFF = 255 // (len(self.ASCII_CHARS) - 1)
        
        self.rec_fps = 25
        self.record = False
        # self.recorder = cv2.VideoWriter('my_video.mp4', cv2.VideoWriter_fourcc(*'mp4v'), self.rec_fps, self.RES)
    def get_frame(self):
        frame = pg.surfarray.array3d(self.surface)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame
    
    def record_frame(self):
        if self.record:
            frame = self.get_frame()
            self.recorder.write(frame)
            cv2.imshow('video', frame)
            if cv2.waitKey(1) & 0XFF == 27:
                self.record = False
    
    def draw_converted_image(self):
        self.image = self.get_image()
        
        char_indices = self.image // self.ASCII_COEFF
        
        for x in range(0, self.HEIGHT, self.CHAR_STEP):
            for y in range(0, self.WIDTH, self.CHAR_STEP):
                
                char_index = char_indices[x, y]
        
                self.surface.blit(self.RENDERED_ASCII_CHARS[char_index], (y, x))
    
    def get_image(self):
        ret, self.cv2_image = self.cap.read()
        audio_frame, val = self.player.get_frame()
        if not ret or val == 'eof':
            exit()
        self.cv2_image = cv2.resize(self.cv2_image, (self.WIDTH, self.HEIGHT), interpolation=cv2.INTER_AREA)
        image = cv2.cvtColor(self.cv2_image, cv2.COLOR_BGR2GRAY)
        return image
    
    def draw_cv2_image(self):
        new_image = cv2.resize(self.cv2_image, (int(self.WIDTH/1.5), int(self.HEIGHT/1.5)))
        cv2.imshow('video', new_image)
    
    def draw(self):
        self.surface.fill('black')
        self.draw_converted_image()
        self.draw_cv2_image()
    
    def save_image(self):
        pygame_image = pg.surfarray.array3d(self.surface)
        cv2.imwrite('new_img.png', pygame_image)
    
    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    exit()
                elif event.type == pg.KEYDOWN:
                    if event.key == pg.K_s:
                        self.save_image()   
                    elif event.key == pg.KEY_r:
                        self.record = not self.record
                    self.record_frame()    
            self.draw()
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick()
            time.sleep(18/1000)
                
if __name__ == '__main__':
    app = Artconvert()
    app.run()

# Naoto Isayama
# Pong is a program that bounces a ball and keeps track of a players score, and allows for user controls of the paddles

import pygame

def main():
   
   # initialization
   pygame.init()
   
   # create display and caption
   pygame.display.set_mode((500, 400))
   pygame.display.set_caption('Pong version 3')  
   
   # create the display surface
   w_surface = pygame.display.get_surface() 
   
   # create a game object and call play
   game = Game(w_surface)
   game.play() 

   # quit
   pygame.quit() 


# User-defined classes

class Game:
   # An object in this class represents a complete game.

   def __init__(self, surface):

      # surface attributes
      self.surface = surface
      self.surface_origin = [0, 0]
      self.surface_width = 500
      self.surface_height = 400
      
      # color attribues
      self.bg_color = pygame.Color('black')
      self.paddle_color = pygame.Color('white')
      self.font_color = pygame.Color('white')
      
      # Paddle attributes
      self.left_paddle_up = False
      self.left_paddle_down = False
      self.paddle_velocity = 7
      
      # game specific objects
      self.Ball = Ball('white', 5, [250, 200], [-6, 4], self.surface)
      self.paddle_left = pygame.Rect(25, 150, 10, 100)
      self.paddle_right = pygame.Rect(465, 150, 10, 100)
      self.score_left = 0
      self.score_right = 0
      self.max_score = 15
      
      # ball attributes
      self.center = Ball.get_center(self.Ball)
      self.velocity_ball = Ball.get_velocity(self.Ball)
      self.radius = Ball.get_radius(self.Ball)

      # font attributes
      self.font_score = pygame.font.SysFont('', 60)
      self.font_text = pygame.font.SysFont('', 25)
      self.font_start = pygame.font.SysFont('', 45)
      self.font_color = pygame.Color('white')
      
      # other attributes
      self.FPS = 60
      self.game_Clock = pygame.time.Clock()
      self.close_clicked = True
      self.is_starting = True
      self.continue_game = True
      
   def play(self):

      # startup loop
      while self.is_starting:
         # Startup text
         self.draw_start_text()
         events = pygame.event.get()
         for event in events:
            if event.type == pygame.KEYDOWN:
               if event.key == pygame.K_SPACE:
                  self.close_clicked = False
                  self.is_starting = False
            if event.type == pygame.QUIT:
               pygame.quit()
               
      # game loop
      while not self.close_clicked:  # until player clicks close box
         # play frame
         self.handle_events()
         self.draw()             
         if self.continue_game:
            self.update()
            self.decide_continue()
         self.game_Clock.tick(self.FPS) # run at most with FPS Frames Per Second 

   def draw_start_text(self):
      # draw the text upon start up

      self.surface.fill(self.bg_color)

      # Startup text
      start_text = self.font_start
      start_text_surface = start_text.render('Press SPACEBAR to begin', False, self.font_color)
      size = start_text.size('Press SPACEBAR to begin')
      self.surface.blit(start_text_surface,(((self.surface_width - size[0])//2),((self.surface_height//2) - size[1])))

      pygame.display.update()


   def handle_events(self):
      # Handle each user event by changing the game state appropriately.
      # - self is the Game whose events will be handled
      events = pygame.event.get()
      for event in events:
         if event.type == pygame.QUIT:
            self.close_clicked = True
            
         # If any of the movement keys are pressed down, the corresponding attribute is set to True
         if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
               self.left_paddle_down = True
            if event.key == pygame.K_q:
               self.left_paddle_up = True
         
         # If any of the movement keys are released, the corresponding attribute is set to False
         if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
               self.left_paddle_down = False
            if event.key == pygame.K_q:
               self.left_paddle_up = False
           
            

   def draw(self):
      # Draw all game objects.
      # - self is the Game to draw     
      self.surface.fill(self.bg_color) # clear the display surface first

      # Render the instructions to the screen
      intro_text = self.font_text
      intro_text_surface_1 = intro_text.render('Use Q and A to move the left paddle', False, self.font_color)
      intro_text_surface_2 = intro_text.render('Use P and L to move the right paddle', False, self.font_color)
      self.surface.blit(intro_text_surface_1,(((self.surface_width - intro_text.size('Use Q and A to move the left paddle')[0])//2),0))
      self.surface.blit(intro_text_surface_2,(((self.surface_width - intro_text.size('Use P and L to move the right paddle')[0])//2), 25))
      
      # draw the ball, paddles, and the scores
      self.Ball.draw()
      pygame.draw.rect(self.surface, self.paddle_color, self.paddle_left)
      pygame.draw.rect(self.surface, self.paddle_color, self.paddle_right)
      self.scorekeeping()
      
      pygame.display.update() # make the updated surface appear on the display
      
   def update(self):
      # Update the game objects for the next frame.
      # - self is the Game to update
      
      self.Ball.move()
      self.Ball.bounce()

      computer_prediction = self.center.copy()
      
      # Paddle bounce mechanics
      if self.paddle_right.collidepoint(self.center[0], self.center[1] ) and self.velocity_ball[0] > 0:
         self.velocity_ball[0] = -self.velocity_ball[0]
      if self.paddle_left.collidepoint(self.center[0] - self.radius, self.center[1]) and self.velocity_ball[0] < 0:
         self.velocity_ball[0] = -self.velocity_ball[0]
         
      # Scorekeeping
      if self.radius > self.center[0]:  # Left bounce
         self.score_right += 1
      if (self.radius + self.center[0]) > self.surface_width:  # Right Bounce
         self.score_left += 1
      
      # paddle movement mechanics
      
        # left paddle
      if self.paddle_left.bottom < self.surface_height:
         if self.left_paddle_down == True:
            self.paddle_left.top += self.paddle_velocity
      if self.paddle_left.top > self.surface_origin[0]:
         if self.left_paddle_up == True:
            self.paddle_left.top -= self.paddle_velocity
      if self.left_paddle_up == False and self.left_paddle_down == False:
         pass         


      if self.velocity_ball[0] > 0:
         
         while computer_prediction[0] < self.surface_width:
            computer_prediction[0] += self.Ball.velocity[0]
            computer_prediction[1] += self.Ball.velocity[1]

         if computer_prediction[1] < self.paddle_right.center[1] and self.paddle_right.top > self.surface_origin[0]:
            self.paddle_right.top -= self.paddle_velocity
         
         elif computer_prediction[1] > self.paddle_right.center[1] and self.paddle_right.bottom < self.surface_height:
            self.paddle_right.top += self.paddle_velocity
         
         print(computer_prediction)


         
   def scorekeeping(self):
      
      #initialize font
      font = self.font_score
      
      #render fonts
      score_display_right = font.render(str(self.score_right),True,self.font_color,self.bg_color)
      score_display_left = font.render(str(self.score_left),True,self.font_color,self.bg_color)
      
      #set locations for each score
      location_right = ((self.surface.get_width() - score_display_right.get_width()), 0)
      location_left = (0,0)
      
      #apply to surface of the game
      self.surface.blit(score_display_right,location_right)
      self.surface.blit(score_display_left,location_left)

   def decide_continue(self):
      # Check and remember if the game should continue
      # - self is the Game to check
      
      if self.score_right == self.max_score:
         self.continue_game = False
      
      if self.score_left == self.max_score:
         self.continue_game = False


class Ball:
   # An object in this class represents a ball that moves and bounces
   
   def __init__(self, dot_color, dot_radius, dot_center, dot_velocity, surface):
      # Initialize a Dot.
      # - self is the Dot to initialize
      # - color is the pygame.Color of the dot
      # - center is a list containing the x and y int
      #   coords of the center of the dot
      # - radius is the int pixel radius of the dot
      # - velocity is a list containing the x and y components
      # - surface is the window's pygame.Surface object

      self.color = pygame.Color(dot_color)
      self.radius = dot_radius
      self.center = dot_center
      self.velocity = dot_velocity
      self.surface = surface
      
   def move(self):
      # Change the location of the Dot by adding the corresponding 
      # speed values to the x and y coordinate of its center
      # - self is the Dot
      
      for i in range(0,2):
         self.center[i] = (self.center[i] + self.velocity[i])
         
   def bounce(self):
      if self.radius > self.center[0]:  # Left bounce
         self.velocity[0] = -self.velocity[0]
      elif (self.radius + self.center[0]) > 500:  # Right bounce
         self.velocity[0] = -self.velocity[0]
      elif self.center[1] < self.radius:  # Top bounce
         self.velocity[1] = -self.velocity[1]
      elif (self.center[1] + self.radius) > 400:  # Bottom bounce
         self.velocity[1] = -self.velocity[1]
   
   def draw(self):
      # Draw the dot on the surface
      # - self is the Dot
      
      pygame.draw.circle(self.surface, self.color, self.center, self.radius)

   # methods that return various attributes of the Ball class (used in Game class)
   
   def get_center(self):
      return self.center
   
   def get_radius(self):
      return self.radius
   
   def get_velocity(self):
      return self.velocity

main()
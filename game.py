import pygame
from models import Spaceship, Asteroid
from utilis import load_sprite, get_random_position, print_text


class SpaceRocks:
    MIN_ASTEROID_DISTANCE = 250

    def __init__(self):
        self._init_pygame()

        # creates a display surface. Images in Pygame are represented by surfaces.
        # Here are a few things to know about them:
        #    x Surfaces can be drawn on one another, allowing you to create complex
        #      scenes from simple pictures.
        #
        #    x There’s one special surface in each Pygame project. That surface represents
        #      the screen and is the one that will eventually be displayed to players.
        #      All other surfaces have to be drawn on this one at some point.
        #      Otherwise, they won’t be shown.
        #
        #    x To create the display surface, your program uses pygame.display.set_mode().
        #      The only argument you pass to this method is the size of the screen,
        #      represented by a tuple of two values: width and height.
        #      In this case, Pygame will create a screen with a width of 800 pixels
        #      and a height of 600 pixels.
        self.screen = pygame.display.set_mode((800, 600))
        self.background = load_sprite("space", False)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 64)
        self.message = ""

        self.asteroids = []
        self.bullets = []
        self.spaceship = Spaceship((400, 300), self.bullets.append)

        for _ in range (6):
            while True:
                position = get_random_position(self.screen)
                if (
                    position.distance_to(self.spaceship.position)
                    > self.MIN_ASTEROID_DISTANCE
                ):
                    break
            self.asteroids.append(Asteroid(position, self.asteroids.append))
        # self.asteroid = GameObject(
        #     (400, 300), load_sprite("asteroid"), (1, 0)
        # )

    def main_loop(self):
        while True:
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):

        # This single line of code is responsible for setting up
        # the amazing features of Pygame.
        # Every time you work with Pygame, you should call pygame.init()
        # at the beginning of your program to make sure
        # that the framework will work correctly.
        pygame.init()
        pygame.display.set_caption("Space Rocks")

    def _handle_input(self):

        #  It happens when someone requests the program to end,
        #  either by clicking Close or by pressing Alt+F4
        #  on Windows and Linux or Cmd+W on macOS. Or Esc
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()
            elif (
                self.spaceship
                and event.type == pygame.KEYDOWN
                and event.key == pygame.K_SPACE
            ):
                self.spaceship.shoot()

        is_key_pressed = pygame.key.get_pressed()

        if self.spaceship:
            if is_key_pressed[pygame.K_RIGHT]:
                self.spaceship.rotate(clockwise=True)
            elif is_key_pressed[pygame.K_LEFT]:
                self.spaceship.rotate(clockwise=False)
            if is_key_pressed[pygame.K_UP]:
                self.spaceship.accelerate()
            elif is_key_pressed[pygame.K_DOWN]:
                self.spaceship.slow_down()

    def _get_game_objects(self):
        game_objects = [*self.asteroids, *self.bullets]

        if self.spaceship:
            game_objects.append(self.spaceship)

        return game_objects

    def _process_game_logic(self):
        for game_object in self._get_game_objects():
            game_object.move(self.screen)

        if self.spaceship:
            for asteroid in self.asteroids:
                if asteroid.collides_with(self.spaceship):
                    self.spaceship = None
                    self.message = "You lost"
                    break

        for bullet in self.bullets[:]:
            for asteroid in self.asteroids[:]:
                if asteroid.collides_with(bullet):
                    self.asteroids.remove(asteroid)
                    self.bullets.remove(bullet)
                    asteroid.split()
                    break

        for bullet in self.bullets[:]:
            if not self.screen.get_rect().collidepoint(bullet.position):
                self.bullets.remove(bullet)

        if not self.asteroids and self.spaceship:
            self.message = "You won"

    def _draw(self):

        # fills the screen with a color using screen.fill(). The method takes a tuple with three values,
        # representing three base colors: red, green, and blue. Each color value ranges between 0 and 255,
        # representing its intensity. In this example, a tuple of (0, 0, 255) means
        # that the color will consist only of blue, with no traces of red or green.
        # self.screen.fill((0, 0, 255))

        # To display one surface on another in Pygame, you need to call blit()
        # on the surface you want to draw on. This method takes two arguments:
        #   x  The surface that you want to draw
        #   x   The point where you want to draw it
        self.screen.blit(self.background, (0,0))
        for game_object in self._get_game_objects():
            game_object.draw(self.screen)
        # self.asteroid.draw(self.screen)
        # updates the content of the screen using pygame.display.flip(). Because your game will
        # eventually display moving objects, you’ll call this method every frame to update
        # the display. Because of this, you need to fill your screen with color every frame,
        # as the method will clear the contents generated during the previous frame.
        if self.message:
            print_text(self.screen, self.message, self.font)
        pygame.display.flip()
        self.clock.tick(60)

"""Implements a simple, extensible game."""
import sys
import traceback

import pygame


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

DEFAULT_WINDOW_SIZE = (700, 500)


class DefaultText(object):
    """Displays some centered demo text."""
    def __init__(self):
        self.font = pygame.font.SysFont("Arial", 36, True, False)
        self.text = "Make a game!"

    def draw(self, surface):
        """Draws the DefaultText in the center of a surface."""

        # Render the text to a surface (i.e. a bitmap).
        rendered_text = self.font.render(self.text, True, BLACK)

        # Center the text on the surface:

        # 1. Calculate the coordinates for the center of the surface.
        surface_center_x = surface.get_width() / 2
        surface_center_y = surface.get_height() / 2

        # 2. Calculate the top-left coordinates for drawing centered
        #    text, based on the center of the surface and the
        #    width/height of the text.
        #
        #    Here's another little trick for centering text: your eye
        #    perceives the center of a surface to be somewhat higher
        #    than the true center of the surface.
        optical_center_fudge = int(surface.get_height() * 0.02)
        centered_text_coords = (
            surface_center_x - (rendered_text.get_width() / 2),
            surface_center_y - (rendered_text.get_height() / 2) - optical_center_fudge
        )

        # 3. Draw the text on the surface using the top-left coords
        #    that we calculated.
        surface.blit(rendered_text, centered_text_coords)


class SimpleGame(object):
    """Implements a base game that just displays text.

    Also intended to be used as a simple framework for other games.

    Attributes:
      window_title (string): The title for the main window.
      dt (integer): The time in milliseconds since the last frame.
        If there was no previous frame, it is None.
      screen (pygame.Surface): The surface for the main window.
        It is created for you.
      fps (integer): The desired frames per second. Default is 30.
    """
    def __init__(self):
        self.window_title = "Card Game"
        self.dt = None
        self.screen = None
        self._default_text = None
        self.fps = 30

    def make_window(self):
        """Creates the main game window.

        Override if you want to customize how the window is created.
        """
        self.screen = pygame.display.set_mode(DEFAULT_WINDOW_SIZE)
        pygame.display.set_caption(self.window_title)

    def ready_to_run(self):
        """Initialization that happens after pygame is initialized.

        This is called before the main loop starts. Because the pygame
        library and the main game window are already initialized, you
        will almost certainly want to override this and put the bulk
        of your game initialization here.
        """
        # This is specific to our default game.
        self._default_text = DefaultText()

    def handle_event(self, event):
        """Handles input events from the mouse, keyboard, joystick, etc.

        Override this if you want your game to respond to input. Note
        that you don't have to respond to the quit message (i.e. the
        close button on the window); that's automatically handled for
        you.

        Arguments:
          event (pygame.EventType): The event to handle. You do not need
            to worry about removing it from the event queue or deleting
            it.
        """
        pass

    def draw(self):
        """Draws your game. Runs once per frame.

        You want to override this; this is where your game's rendering
        should take place.

        This is called after handle_event in the main event loop.
        """
        self.screen.fill(WHITE)
        self._default_text.draw(self.screen)
        pygame.display.flip()

    def main_loop(self):
        """Executes the game's main loop.

        You probably won't need to override this, unless you need to
        restructure the game loop altogether.
        """
        clock = pygame.time.Clock()
        done = False
        while not done:
            # This delays the program as necessary so we run at a smooth 60fps (if possible),
            # and returns the time elapsed in milliseconds since the last frame.
            self.dt = clock.tick(self.fps)

            # Process all pending events.
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                else:
                    self.handle_event(event)

            # Go draw something!
            self.draw()

    def run(self):
        """Runs the game.

        This won't return until the game is finished.
        """
        pygame.init()
        self.make_window()
        self.ready_to_run()
        self.main_loop()
        pygame.quit()


def main(game_maker):
    """This is the main entry point to the game.

    This function creates a game object and then runs it. It will exit
    the program instead of returning.

    This function is designed to work on any game that derives from
    SimpleGame.

    Arguments: game_maker (function): A callable object which, when
      called with no arguments, returns an object representing the
      game with a run method(). (Hint: it can be a class that derives
      from SimpleGame, since calling the class as a function creates
      objects.)
    """
    try:
        game = game_maker()
        game.run()
    except:
        traceback.print_exc()
        sys.exit(1)
    sys.exit(0)


# When you execute this module from the command line, e.g. by running
# `python simple_game.py`, this sets up and runs the demo game
# implemented above.
if __name__ == '__main__':
    main(SimpleGame)

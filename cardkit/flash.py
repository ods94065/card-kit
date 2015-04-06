import pygame


BLACK = (0,0,0)
TRANSPARENT = (0, 0, 0, 0)


class FlashMessage(object):
    """A text message that displays and then fades after a certain duration.

    Attributes:
      message (string): The text message to be displayed
      duration (integer): The duration in milliseconds before the
        message starts to fade.
      fade_duration (integer): The time it takes for the message to
        fade in milliseconds. By default, it is 2 seconds long.
      color (tuple): An RGBA tuple representing the initial color of
        the text.
      font (pygame.Font or None): The font to use for the message. If
        None, a default font will be used.
    """
    def __init__(self, message, duration, fade_duration=2000, color=BLACK, font=None):
        self.color = color

        # Pygame's fonts can't render newlines; we have to actually
        # handle the line breaks ourselves.  So, let's turn this into
        # a list of text lines we want to display.
        self.messages = message.split('\n')
        self.rendered_messages = None # The images of the rendered lines
        self.duration = duration
        self.fade_duration = fade_duration
        self.should_show = False # Are we showing this message now?
        self.show_start_time = None # The game time since we started showing
        self.show_fade_time = None # The game time we should start to fade
        self.show_end_time = None # The game time we should stop showing
        if font is None:
            self.font = pygame.font.SysFont("Arial", 20, False, False)
        else:
            self.font = font

    def show(self):
        """Mark the flash message to be displayed in the next frame."""
        # For now, just mark that we want to show the text. Don't
        # start the stopwatch yet, just in case we haven't started the
        # main loop yet and won't for a while.
        self.should_show = True

        # At this point, it should be safe to pre-calculate these images.
        self.rendered_messages = [self.font.render(message, True, self.color) for message in self.messages]

    def _draw_message(self, message, surface, location, fade_amount):
        """Draws one line of text at a location on the surface."""
        if fade_amount == 0:
            # No fade required; we can save some work!
            surface.blit(message, location)
        else:
            # Here we show a technique for doing basic math on pixel
            # values without having to write a relatively expensive
            # Python loop.
            #
            # Start with an RGBA value which will be subtracted from
            # each pixel in the fading message (red from red, blue
            # from blue, and so forth).
            #
            # Note that the alpha channel (the fourth channel)
            # controls transparency: 0 is totally transparent, 255 is
            # totally opaque.
            #
            # Therefore, subtracting 255 alpha (we will automatically
            # clip at 0) will turn any pixel transparent, and
            # subtracting 0 won't affect transparency at all.
            fade_rgba = (0, 0, 0, int(fade_amount * 255))

            # Create a surface that has this special RGBA value on
            # every pixel. We'll call it an overlay since we will
            # draw it on top of the text.
            fade_overlay = pygame.Surface(message.get_size(), pygame.SRCALPHA)
            fade_overlay.fill(fade_rgba)

            # This is the image that will be drawn to the surface.
            fading_message = pygame.Surface(message.get_size(), pygame.SRCALPHA)

            # Now, we draw the fading text in three layers:
            # 1. Start with a transparent background.
            fading_message.fill(TRANSPARENT)

            # 2. Draw the (possibly antialiased) text.
            fading_message.blit(message, (0, 0))

            # 3. Draw the fade overlay on top, but in a special
            # drawing mode that subtracts the overlay's values
            # (including its alpha values!) from the pixels
            # underneath.
            fading_message.blit(
                fade_overlay, (0, 0),
                special_flags=pygame.BLEND_RGBA_SUB)

            # Finally, draw the faded text.
            surface.blit(fading_message, location)

    def _draw_messages(self, surface, location, fade_amount=0):
        """Draws the entire flash message at a location on the surface.

        Arguments:
          surface (pygame.Surface): See draw().
          location (tuple): See draw().
          fade_amount (float): A number between 0 and 1 representing
            how much to fade the line of text. 0 shows the text at
            full strength; 1 makes the text completely invisible.
        """
        for message in self.rendered_messages:
            self._draw_message(message, surface, location, fade_amount)
            location = (location[0], location[1] + self.font.get_linesize())

    def draw(self, surface, location):
        """Draws the flash message at a location on the surface.

        Arguments:
          surface (pygame.Surface): The surface to draw on.
          location (tuple): An (x, y) coordinate pair in surface
            coordinates representing where the top left of the message
            should go.
        """
        if not self.should_show:
            return

        now = pygame.time.get_ticks()
        if not self.show_start_time:
            # We start keeping track of time on the first frame that
            # we start showing the text.
            self.show_start_time = now
            self.show_fade_time = self.show_start_time + self.duration
            self.show_end_time = self.show_fade_time + self.fade_duration

        if now < self.show_fade_time:
            self._draw_messages(surface, location)
        elif now < self.show_end_time:
            # Fade amount should be a ratio of how much we want to
            # fade.  0 should be no fading; 1.0 should be totally
            # faded away.  We will gradually and linearly ramp up
            # from 0 to 1 over the fade duration.
            fade_amount = float(now - self.show_fade_time) / (self.show_end_time - self.show_fade_time)
            self._draw_messages(surface, location, fade_amount)
        else:
            self.should_show = False
            self.show_start_time = None
            self.show_fade_time = None
            self.show_end_time = None

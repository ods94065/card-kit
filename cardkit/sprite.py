import pygame


class Sprite(object):
    """A portion of a Surface that can be drawn independently from the
    rest of the Surface.

    For performance reasons, small images (bitmaps) are often bundled
    together into a single image file and loaded to a single
    Surface. The Sprite represents a region in that Surface that gets
    drawn to the screen repeatedly. These sprites can be icons, character
    renderings, textures, objects in the game... pretty much anything
    you want!

    Currently, only rectangular regions are represented; it's assumed that
    anything in that rectangular region that you _don't_ want to draw is
    set to be transparent.

    The coordinate systems related to Sprites can get a little
    complicated. To wit, you have:

    1. The coordinate system of the spritesheet, where (0, 0) is the
       top-left corner of the spritesheet.
    2. The coordinate system of the sprite's bounding rect (its region
       of the spritesheet), where (0, 0) is the top-left corner of the
       sprite's bounding rect.
    3. The coordinate system of the sprite itself, where (0, 0) is
       defined as some point relative to the sprite's bounding box
       coordinate system (we call that the "origin" of the
       sprite). Frequently, this is just left as the top-left corner
       of the sprite's bounding box (thus making coordinate systems
       (2) and (3) identical), but you can also use this origin to
       align multiple sprites around a common anchor point that is
       independent of the bounds of the sprite: for example, the
       center point of an animated character with a shifting bounding
       rect.

    When we draw a sprite, we specify the location we want the sprite
    to be drawn at; the origin specifies the pixel of the sprite
    (again, relative to the top-left corner of the sprite) that will
    be drawn at that location. If the origin is in the center of the
    sprite's bounding rect, the sprite will be drawn centered around
    the location; if the origin's at the top left of the bounding
    rect, the sprite will be drawn down and left from the location.

    Attributes:
      source (pygame.Surface): The image (aka spritesheet) the sprite
        comes from.
      size (tuple): A (w, h) pair that represents the width and height
        of the sprite.
      source_rect (pygame.Rect): The actual region of the source that
        the sprite represents.
      origin (tuple): An (x, y) coordinate pair that represents where
        the "anchor" of the Sprite is. It is a point somewhere within
        the bounds of size_rect (i.e. relative to the top-left of the
        sprite).
    """
    def __init__(self, source, source_position, size, origin=(0, 0)):
        """Creates a sprite.

        Arguments:
          source (pygame.Surface): The image (aka stylesheet) that the
            sprite comes from.
          source_position (tuple): An (x, y) coordinate pair that
            represents where the top-left corner of the sprite is on
            the stylesheet.
          size (tuple): An (w, h) pair that represents the width and
            height of the sprite in pixels.
          origin (tuple): An (x, y) coordinate pair, relative to the
            top-left corner of the sprite, that represents the drawing
            origin of the sprite. Defaults to (0, 0) (the top-left
            corner of the sprite).
        """
        if source is None:
            raise ValueError('A source Surface must be provided.')
        self.source = source
        self.size = size
        self.source_rect = pygame.Rect(
            source_position[0],
            source_position[1],
            size[0],
            size[1])
        self.origin = origin

    def draw(self, surface, location):
        """Draws the sprite on the given surface at the given location.

        Note that the sprite's origin point is what will get drawn at
        the location.
        """
        # We want the sprite's origin to be drawn at the given
        # location.  However, the blit's destination needs to be where
        # the top-left corner of the sprite should go. So, we must
        # subtract the origin from the location to get the location
        # that we should blit to.
        blit_location = (
            location[0] - self.origin[0],
            location[1] - self.origin[1])
        surface.blit(self.source, blit_location, self.source_rect)

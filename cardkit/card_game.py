"""A very simple demo card game.

All this game does is allow the player to draw cards from a deck and add them to a discard pile.
Pressing 'n', or clicking on the discard pile after the deck is exhausted, starts a new game.
"""
import pygame

from cardkit import card
from cardkit import card_constants as ck
from cardkit import card_sprite
from cardkit import deck
from cardkit import flash
from cardkit import simple_game


BACKGROUND_COLOR = (200, 230, 200)
LEFT_BUTTON = 1


class CardGame(simple_game.SimpleGame):
    def ready_to_run(self):
        """Initialization done after pygame initializes.

        This happens before the run looop starts.
        """
        card_sprite.load_spritesheet()

        self.deck = deck.Deck()
        self.deck.shuffle()
        self.deck_location = (150, 150)

        self.discard_pile = deck.Deck(initial_cards=[])
        self.discard_pile_location = (300, 150)

        self.flash = flash.FlashMessage(message="Draw some cards!\nPress 'n' to reset.", duration=3000, fade_duration=2000)
        self.flash.show()
        self.flash_location = (100, 50)

        deck_rect = self.deck.drawing_rect()
        self.deck_bounding_rect = deck_rect.move(self.deck_location)
        self.discard_pile_bounding_rect = deck_rect.move(self.discard_pile_location)

    def draw_and_discard(self):
        """Draws a card from the deck and places it on the discard pile."""
        c = self.deck.deal(face=ck.FACE_UP)
        self.discard_pile.add(c)

    def reset(self):
        """Restarts the game."""
        self.deck.reset()
        self.discard_pile.reset()
        self.deck.shuffle()

    def handle_event(self, event):
        """Handles input events from the mouse, keyboard, joystick, etc."""
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_n:
                # We pressed 'n'. Note that the key value that we're
                # checking here is not the value of a character, but a
                # lower-level representation of the actual key on the
                # keyboard. This allows us to handle things like the
                # arrow keys and Escape, which may not have character
                # equivalents.
                self.reset()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == LEFT_BUTTON:
            click_pos = event.pos
            if self.deck_bounding_rect.collidepoint(click_pos):
                # We clicked on the deck!
                if not self.deck.is_empty():
                    self.draw_and_discard()

            if self.discard_pile_bounding_rect.collidepoint(click_pos):
                # We clicked on the discard pile. Let's have this only
                # take effect if the deck is exhausted.
                if self.deck.is_empty():
                    self.reset()

    def draw(self):
        """Draws the entire game."""
        self.screen.fill(BACKGROUND_COLOR)
        self.deck.draw(self.screen, self.deck_location)
        self.discard_pile.draw(self.screen, self.discard_pile_location)
        self.flash.draw(self.screen, self.flash_location)
        pygame.display.flip()


if __name__ == '__main__':
    simple_game.main(CardGame)

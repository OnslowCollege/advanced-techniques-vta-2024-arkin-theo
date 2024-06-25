import pygame
import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

class Deck:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "Ace"]

    def __init__(self, nmb_decks):
        self.cards = [Card(suit, rank) for suit in self.suits for rank in self.ranks for _ in range(nmb_decks)]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if len(self.cards) > 0:
            return self.cards.pop()
        else:
            return None

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)

class Button:
    def __init__(self, x, y, width, height, text, color=GRAY, hover_color=WHITE, font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font(None, font_size)
        self.text = text
        self.text_surface = self.font.render(text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, self.hover_color, self.rect)
        else:
            pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(self.text_surface, self.text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def update_text(self, new_text):
        self.text = new_text
        self.text_surface = self.font.render(new_text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

class Main:
    def __init__(self):
        pygame.init()
        self.screenDim = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.screenDim)
        self.background = BLACK
        self.running = False
        self.button = Button(x=SCREEN_WIDTH/2+100, y=620, width=100, height=50, text='Draw Card')
        self.d_shoe = Deck(nmb_decks=1)  # Initialize the Deck
        self.current_card_image = None
        self.card_images = self.load_card_images()
        self.previous_cards_p = []

    def load_card_images(self):
        card_images = {}
        for suit in Deck.suits:
            for rank in Deck.ranks:
                # Update this to the correct path for your images
                # image_path = f"C:/Users/arkin/OneDrive/Documents/Blackjack-pygame/Sprites/{suit}_{rank}.png"
                image_path = f"C:/Users/arkin/OneDrive/Documents/Blackjack-pygame/Sprites/KIN's_Playing_Cards/{suit}_{rank}.png"
                # image_path = f"C:/Users/arkin/OneDrive/Documents/Blackjack-pygame/Sprites/kanban-sprint1.png"
                image = pygame.image.load(image_path).convert_alpha()
                # scaled_image = pygame.transform.scale(image, (20, 100))  # Scale to 20x100 pixels
                card_images[f'{rank}_of_{suit}'] = image
        return card_images

    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if self.button.is_clicked(event):
                self.draw_card()

    def update(self, dt):
        pass

    def draw(self):
        self.button.draw(self.screen)
        c_offset = 0
        for card in self.previous_cards_p:
            if card:
                self.screen.blit(card, (100+c_offset, 250-c_offset))
                c_offset += 10
        
        # if self.current_card_image:
        #     self.screen.blit(self.current_card_image, (200+c_offset, 100+c_offset))  # Position the image above the button
        #     c_offset += 10

    def run(self):
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(40) / 1000.0
            self.screen.fill(self.background)
            self.poll()
            self.update(dt)
            self.draw()
            pygame.display.flip()

    def draw_card(self):
        card_drawn = self.d_shoe.deal()
        if card_drawn:
            card_key = f"{card_drawn.rank}_of_{card_drawn.suit}"
            if card_key in self.card_images:
                self.current_card_image = self.card_images[card_key]
                self.previous_cards_p.append(self.current_card_image)
        else:
            self.button.update_text("No more cards")

if __name__ == '__main__':
    main = Main()
    print("starting...")
    main.run()
    print("shutting down...")

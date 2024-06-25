import pygame
import random

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.owner = ""

class Deck:
    suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
    ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "ACE"]

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

class ScoreText:
    def __init__(self, x, y, width, height, text, font_size=30):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = pygame.font.Font(None, font_size)
        self.text = text
        self.text_surface = self.font.render(text, True, BLACK)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, screen):
        screen.blit(self.text_surface, self.text_rect)

    def update_text(self, new_text):
        self.text = new_text
        self.text_surface = self.font.render(new_text, True, WHITE)
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
        # Player buttons
        self.hit_button = Button(
            x=SCREEN_WIDTH / 2 - 100,
            y=620,
            width=100,
            height=50,
            text="Hit"
        )
        self.stand_button = Button(
            x=SCREEN_WIDTH / 2,
            y=620,
            width=100,
            height=50,
            text="Stand"
        )

        # Score texts
        self.p_score = ScoreText(
            x=SCREEN_WIDTH / 2 - 50,
            y=580,
            width=100,
            height=50,
            text="0"
        )
        self.d_score = ScoreText(
            x=SCREEN_WIDTH / 2 - 50,
            y=150,
            width=100,
            height=50,
            text="0"
        )
        self.p_total = 0
        self.d_total = 0


        self.d_shoe = Deck(nmb_decks=1)  # Initialize the Deck
        self.current_card_image = None
        self.card_images = self.load_card_images()

        image_path = "/workspaces/advanced-techniques-vta-2024-arkin-theo/Sprites/KIN's_Playing_Cards/Back_1.png"
        self.card_back = pygame.image.load(image_path).convert_alpha()
        self.card_back = pygame.transform.scale(self.card_back, (94, 132))

        self.previous_cards_p = []
        self.previous_cards_d = []

        self.draw_history_p = []
        self.draw_history_d = []

        self.d_hidden_card = ""

        self.p_turn = True
        self.hide_card = True


    def load_card_images(self):
        card_images = {}
        for suit in Deck.suits:
            for rank in Deck.ranks:
                root_dir = "/workspaces/advanced-techniques-vta-2024-arkin-theo/Sprites/KIN's_Playing_Cards"

                # Update this to the correct path for your images
                image_path = f"{root_dir}/{suit}_{rank}.png"
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (94, 132))
                card_images[f'{rank}_of_{suit}'] = image

        return card_images

    def poll(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if self.p_total < 21:
                if self.hit_button.is_clicked(event):
                    self.card_drawn("player")
            
                elif self.stand_button.is_clicked(event):
                    self.p_turn = False
                    self.d_score.update_text(f"{self.d_total}")

            else:
                if self.d_total > 21:
                    self.d_score.update_text("BUSTED")
                elif self.d_total == 21:
                    self.d_score.update_text("BLACKJACK")
                else:
                    self.d_score.update_text(f"{self.d_total}")


    def update(self, dt): # idk might get rid of
        pass

    def draw(self):
        if self.p_turn:
            self.hit_button.draw(self.screen)
            self.stand_button.draw(self.screen)

        # Draw all cards
        pc_offset = 0
        dc_offset = 0
        for card in self.previous_cards_p:
            self.screen.blit(
                card, (SCREEN_WIDTH / 2 - 20 + pc_offset, 410)
            )
            pc_offset += 25

        # self.screen.blit(
        #     self.card_back, (SCREEN_WIDTH / 2 - 20 + dc_offset, 210)
        # )
        # dc_offset += 25

        for card in self.previous_cards_d:
            if self.previous_cards_d.index(card) == 0 and self.p_turn:
                self.screen.blit(
                    self.card_back, (SCREEN_WIDTH / 2 - 20 + dc_offset, 210)
                )
                dc_offset += 25

            if self.previous_cards_d.index(card) != 0 and self.p_turn:
                self.screen.blit(
                    card, (SCREEN_WIDTH / 2 - 20 + dc_offset, 210)
                )
                dc_offset += 25

            if not self.p_turn:
                self.screen.blit(
                    card, (SCREEN_WIDTH / 2 - 20 + dc_offset, 210)
                )
                dc_offset += 25



        # Draw the scores
        self.p_score.draw(self.screen)
        self.d_score.draw(self.screen)


    def setup(self):
        self.card_drawn("player")
        self.card_drawn("dealer")
        self.card_drawn("player")
        self.card_drawn("dealer")


    def run(self):
        self.setup()
        self.running = True
        clock = pygame.time.Clock()
        while self.running:
            dt = clock.tick(40) / 1000.0
            self.screen.fill(self.background)
            
            self.poll()
            self.draw()
            self.update(dt)

            if self.p_turn != True:
                while self.d_total < 17:
                    self.card_drawn("dealer")

            pygame.display.flip()



    def card_drawn(self, onwer: str):
        card_drawn = self.d_shoe.deal()
        card_drawn.owner = onwer

        if self.d_hidden_card == "" and card_drawn.owner == "dealer":
            self.d_hidden_card = card_drawn.rank

        if card_drawn:
            # If player
            if card_drawn.owner == "player":
                self.draw_history_p.append(card_drawn)
                if card_drawn.rank in ["J", "Q", "K"]:
                    self.p_total += 10

                elif card_drawn.rank == "ACE":
                    if self.p_total <= 10:
                        self.p_total += 11
                    else:
                        self.p_total += 1

                else:
                    self.p_total += int(card_drawn.rank)

                # Check player bust
                if self.p_total > 21:
                    found = False
                    for c in self.draw_history_p:
                        if c.rank == "ACE":
                            ind = self.draw_history_p.index(c)
                            self.draw_history_p.pop(ind)
                            found = True
                            break
                    if not found:
                        self.p_score.update_text("BUSTED")
                        self.p_turn = False
                        print("BUSTED - p")
                    else:
                        self.p_total -= 10
                        if self.p_total > 21:
                            self.p_score.update_text("BUSTED")
                            self.p_turn = False
                            print("BUSTED - p")
                        else:
                            self.p_score.update_text(f"{self.p_total}")


                elif self.p_total == 21:
                    self.p_score.update_text("BLACKJACK")
                    print("BLACKJACK - p")
                    self.p_turn = False
                else:
                    self.p_score.update_text(f"{self.p_total}")


            # If dealer
            if card_drawn.owner == "dealer":
                self.draw_history_d.append(card_drawn)
                if card_drawn.rank in ["J", "Q", "K"]:
                    self.d_total += 10

                elif card_drawn.rank == "ACE":
                    if self.d_total <= 10:
                        self.d_total += 11
                    else:
                        self.d_total += 1

                else:
                    self.d_total += int(card_drawn.rank)

                # Check dealer bust
                if self.d_total > 21:
                    found = False
                    for c in self.draw_history_d:
                        if c.rank == "ACE":
                            ind = self.draw_history_d.index(c)
                            self.draw_history_d.pop(ind)
                            found = True
                            break

                    if not found:
                        self.d_score.update_text("BUSTED")
                        print("BUSTED - d")
                    else:
                        self.d_total -= 10
                        if self.d_total > 21:
                            self.d_score.update_text("BUSTED")
                            print("BUSTED - d")
                        else:
                            self.d_score.update_text(f"{self.d_total}")


                elif self.d_total == 21:
                    self.d_score.update_text("BLACKJACK")
                    print("BLACKJACK - d")
                else:
                    self.d_score.update_text(f"{self.d_total}")
                
                # Start of game
                if self.p_turn:
                    if self.d_hidden_card in ["J", "Q", "K"]:
                        self.d_score.update_text(f"{self.d_total - 10}")

                    elif self.d_hidden_card == "ACE":
                        self.d_score.update_text(f"{self.d_total - 11}")

                    else:
                        self.d_score.update_text(f"{self.d_total - int(self.d_hidden_card)}")
                

                




            # Save card to a history list
            card_key = f"{card_drawn.rank}_of_{card_drawn.suit}"
            if card_key in self.card_images:
                self.current_card_image = self.card_images[card_key]
                if card_drawn.owner == "player":
                    self.previous_cards_p.append(self.current_card_image)
                elif card_drawn.owner == "dealer":
                    self.previous_cards_d.append(self.current_card_image)
        else:
            self.hit_button.update_text("No more cards") # wont be possible if reshuffle deck

if __name__ == '__main__':
    main = Main()
    print("starting...")
    main.run()
    print("shutting down...")

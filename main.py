import random
import slider
import pygame
import os


class Button:
    def __init__(self, x, y, width, height, text, color=(208, 25, 32), hover_color=(135, 17, 20), font_size=30):
        self.rect = pygame.Rect(x, y, width+20, height)
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.Font('Grand9K.ttf', font_size)
        self.text = text
        self.text_surface = self.font.render(text, True, (255,255,255), (0,0,0))
        self.text_surface.set_colorkey((0,0,0))
        self.text_rect = pygame.Rect(0,0, width, height)
        self.text_rect.center = self.rect.center

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
        self.text_surface = self.font.render(new_text, True, (255,255,255))
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)


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
GRAY = (175, 175, 175)






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
HIDDEN_NMB = 1




class Main:
    def __init__(self):
        self.event = None
        self.restarted = False
        self.bet_button_isdrawn = False


        pygame.init()
        self.screenDim = (SCREEN_WIDTH, SCREEN_HEIGHT)
        self.screen = pygame.display.set_mode(self.screenDim)
        self.background = pygame.transform.scale_by(pygame.image.load('black_jack_table.jpg').convert(),1)
        self.running = False
        self.bank = 10000
        self.minimum_bet = 10
        self.current_bet = 0
        self.bet_subtracted_yet = False
        self.font = pygame.font.Font('Grand9K.ttf', 30)


        self.account_balance = self.font.render(f'${self.bank}', True,
                                                (255, 255, 255), (208, 25, 32))
        self.account_balance_rect = self.account_balance.get_rect()
        self.account_balance_rect.center = (100,40)
        self.bet_slider = slider.slider([640, 540], self.screen, [10, 40], (90, 90, 90), [640, 540],
                                        [400, 20], self.bank, self.minimum_bet, (255, 255, 255))
        self.current_bet_text = self.font.render(f'${round(self.current_bet/10)*10}', True,
                                                            (255, 255, 255), (208, 25, 32))
        self.current_bet_text_rect = self.current_bet_text.get_rect()
        self.current_bet_text_rect.center = (SCREEN_WIDTH/2, SCREEN_HEIGHT/4)
        # Player buttons
        self.restart_button = Button(x=SCREEN_WIDTH / 2 - 230 / 2, y=1.25 * SCREEN_HEIGHT / 3, width=230, height=75, text="Restart", font_size=50)
        self.bet_button = Button(x=SCREEN_WIDTH / 2 - 240 / 2, y=1.25 * SCREEN_HEIGHT / 3, width=240, height=75, text="Place bet", font_size=50)
        self.hit_button = Button(
            x=SCREEN_WIDTH / 2 -100,
            y=620,
            width=50,
            height=50,
            text="Hit"
        )
        self.stand_button = Button(
            x=SCREEN_WIDTH / 2 +25,
            y=620,
            width=100,
            height=50,
            text="Stand"
        )


        # Score texts
        self.p_score = ScoreText(
            x=SCREEN_WIDTH / 2 - 50,
            y=550,
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
        self.event_text = ScoreText(
            x=SCREEN_WIDTH / 2 - 50,
            y=100,
            width=100,
            height=50,
            text="None"
        )


        self.p_total = 0
        self.d_total = 0


        self.d_shoe = Deck(nmb_decks=1)  # Initialize the Deck
        self.current_card_image = None
        self.card_images = self.load_card_images()

        dir_path = os.path.dirname(os.path.realpath(__file__))


        image_path = dir_path + r"\Sprites\KIN's_Playing_Cards\Back_1.png"
        self.card_back = pygame.image.load(image_path).convert_alpha()
        self.card_back = pygame.transform.scale(self.card_back, (94, 132))


        self.previous_cards_p = []
        self.previous_cards_d = []


        self.draw_history_p = []
        self.draw_history_d = []


        self.d_hidden_card = ""
        self.counter = 0


        self.p_turn = True
        self.hide_card = True
        self.bet = False
        self.hand_finsihed = False
        self.started = False


    def load_card_images(self):
        card_images = {}
        for suit in Deck.suits:
            for rank in Deck.ranks:
                
                dir_path = os.path.dirname(os.path.realpath(__file__))
                root_dir = dir_path + r"\Sprites\KIN's_Playing_Cards"


                # Update this to the correct path for your images
                image_path = f"{root_dir}/{suit}_{rank}.png"
                image = pygame.image.load(image_path).convert_alpha()
                image = pygame.transform.scale(image, (94, 132))
                card_images[f'{rank}_of_{suit}'] = image


        return card_images


    def poll(self):
        for event in pygame.event.get():
            if self.bet_button.is_clicked(event) and not self.started and self.bet_button_isdrawn:
                self.bet_button_isdrawn = False
                self.started = True
                # print("self.started = True", self.started)
                self.bet = True



                if self.event != None:
                    self.old_event = self.event
                # events

                # first: standonly
                # must stand

                # second: no_risk
                # bet +100 every time you hit

                # third: 21or0
                # 21 or nothing


                random_id = random.random()
                if 0 <= random_id < 0.34:
                    print("0 - .33")
                    self.event = "standonly"
                elif .34 <= random_id < 0.67:
                    print(".34 - .66")
                    self.event = "no_risk"
                else:
                    print(".67 - 1")
                    self.event = "21or0"
                print(random_id)
                print(self.event)


                if not self.bet_subtracted_yet and self.event != "no_risk":
                        self.bank -= self.current_bet
                        self.bet_subtracted_yet = True

            self.restarted = False

            # print("self.started = ", self.started)
            if self.restart_button.is_clicked(event) and not self.bet_button_isdrawn:
                self.event_text.update_text("Current Event: None")
                self.started = False
                # print("self.started = False", self.started)
                self.restarted = True
                self.d_shoe = Deck(nmb_decks=4)



            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            if self.p_total < 21:
                if self.hit_button.is_clicked(event) and self.event != "standonly" and not self.bet_button_isdrawn:
                    self.card_drawn("player")


                elif self.stand_button.is_clicked(event) and not self.bet_button_isdrawn:
                    self.p_turn = False
                    if self.d_total > 21:
                        self.d_score.update_text("BUSTED")
                    elif self.d_total == 21:
                        self.d_score.update_text("BLACKJACK")
                    else:
                        self.d_score.update_text(f"{self.d_total}")


            else:
                self.p_turn = False
                if self.d_total > 21:
                    self.d_score.update_text("BUSTED")
                elif self.d_total == 21:
                    self.d_score.update_text("BLACKJACK")
                else:
                    self.d_score.update_text(f"{self.d_total}")



            if ((not self.p_turn and self.d_total >= 17) or (self.p_total>21)) and self.restarted:
                self.previous_cards_p.clear()
                self.previous_cards_d.clear()
                if self.p_total < self.d_total <= 21 or self.p_total > 21:
                    print(self.bank)
                    self.bet_slider = slider.slider([640, 540], self.screen, [10, 40], (90, 90, 90), [640, 540],
                                                    [400, 20], self.bank, self.minimum_bet, (255, 255, 255))
                    if self.bank == 0:
                        pygame.quit()


                elif self.p_total == self.d_total:
                    

                    if (self.event == "21or0"):
                        if (self.p_total == 21):
                            self.bank += self.current_bet
                            
                    else:
                        if event != "no_risk":
                            self.bank += self.current_bet


                elif self.p_total == 21:
                    self.bank += 2.5*self.current_bet


                else:
                    if (self.event == "21or0"):
                        if (self.p_total == 21):
                            self.bank += self.current_bet*2
                    else:
                        self.bank += self.current_bet*2
                    
                    print(self.bank)
                    self.bet_slider = slider.slider([640, 540], self.screen, [10, 40], (90, 90, 90), [640, 540],
                                                    [400, 20], self.bank, self.minimum_bet, (255, 255, 255))


                self.event = "None"
                if self.d_total > 0:
                    self.d_total = 0
                if self.p_total>0:
                    self.p_total = 0
                self.p_turn = True
                self.bet_subtracted_yet = False
                self.bet =False
                self.restarted = False
                self.setup()


    def update(self, dt):  # idk might get rid of
        pass


    def draw(self):


        if self.p_turn:
            if self.event != "standonly":
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




        for i, card in enumerate(self.previous_cards_d):
            if i == HIDDEN_NMB and self.p_turn:
                self.screen.blit(
                    self.card_back, (SCREEN_WIDTH / 2 - 20 + dc_offset, 210)
                )
                dc_offset += 25


            if i != HIDDEN_NMB and self.p_turn:
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
        self.previous_cards_p.clear()
        self.previous_cards_d.clear()
        self.draw_history_p.clear()
        self.draw_history_d.clear()
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
            self.screen.blit(self.background, (0,0))
            self.poll()


            self.event_text.update_text(f"Current Event: {self.event if self.event else 'None'}")
            self.event_text.draw(self.screen)

            if self.bet:


                self.draw()
                if not self.p_turn:
                    while self.d_total < 17:
                        self.card_drawn("dealer")
            else:
                self.bet_button.draw(self.screen)
                self.bet_button_isdrawn = True
                self.current_bet = round(self.bet_slider.slider_update(self.screen, (255,255,255))/10)*10
                self.current_bet_text = self.font.render(f'${round(self.current_bet / 10) * 10}', True,
                                                        (255, 255, 255), (208, 25, 32))
                self.screen.blit(self.current_bet_text, self.current_bet_text_rect)
            if self.p_turn is False and self.d_total >= 17:


                self.restart_button.draw(self.screen)
            self.account_balance = self.font.render(f'${self.bank}', True,
                                                    (255, 255, 255), (208, 25, 32))
            self.screen.blit(self.account_balance,self.account_balance_rect)
            self.update(dt)
            pygame.display.flip()


    def check_ace(self, owner):
        if owner == "player":
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
                    print("BUSTED - p", self.p_total)
                else:
                    self.p_total -= 10
                    if self.p_total > 21:
                        self.check_ace("player")
                    else:
                        self.p_score.update_text(f"{self.p_total}")


            elif self.p_total == 21:
                self.p_score.update_text("BLACKJACK")
                print("BLACKJACK - p", self.p_total)
                self.p_turn = False


            else:
                self.p_score.update_text(f"{self.p_total}")


        if owner == "dealer":
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
                    print("BUSTED - d - ", self.d_total)


                else:
                    self.d_total -= 10
                    if self.d_total > 21:
                        self.check_ace("dealer")
                    else:
                        self.d_score.update_text(f"{self.d_total}")


                        if self.p_turn:
                            self.d_score.update_text(f"{self.d_total + 10}")




            elif self.d_total == 21:
                self.d_score.update_text("BLACKJACK")
                print("BLACKJACK - d -", self.d_total)
            else:
                self.d_score.update_text(f"{self.d_total}")


    # Change
    def card_drawn(self, onwer: str):


        card_drawn = self.d_shoe.deal()
        card_drawn.owner = onwer


        if self.d_hidden_card == "" and card_drawn.owner == "dealer":
            self.counter += 1


        if self.counter == HIDDEN_NMB:
            self.d_hidden_card = card_drawn.rank


        if card_drawn:
            # If player
            if card_drawn.owner == "player":
                self.draw_history_p.append(card_drawn)
                if card_drawn.rank in ["J", "Q", "K"]:
                    self.p_total += 10


                elif card_drawn.rank == "ACE":
                    self.p_total += 11
                    self.check_ace("player")




                else:
                    self.p_total += int(card_drawn.rank)


                if self.p_total > 21:
                    self.check_ace("player")


                elif self.p_total == 21:
                    self.p_score.update_text("BLACKJACK")
                    print("BLACKJACK - p", self.p_total)
                    self.p_turn = False


                else:
                    self.p_score.update_text(f"{self.p_total}")


            # If dealer
            if card_drawn.owner == "dealer":
                self.draw_history_d.append(card_drawn)
                if card_drawn.rank in ["J", "Q", "K"]:
                    self.d_total += 10


                elif card_drawn.rank == "ACE":
                    self.d_total += 11
                    self.check_ace("dealer")


                else:
                    self.d_total += int(card_drawn.rank)


                if self.d_total > 21:
                    self.check_ace("dealer")


                elif self.d_total == 21:
                    self.d_score.update_text("BLACKJACK")
                    print("BLACKJACK - d", self.d_total)


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
            self.hit_button.update_text("No more cards")  # wont be possible if reshuffle deck




if __name__ == '__main__':
    main = Main()
    print("starting...")
    main.run()
    print("shutting down...")

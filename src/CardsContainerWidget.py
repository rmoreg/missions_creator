
from PyQt5.QtWidgets import QHBoxLayout, QVBoxLayout, QWidget, QLabel, QFrame

STYLESHEET = {}
STYLESHEET["CustomCardsContainer"]  = """
    QFrame#cardContainer {background-color: white;
    }
"""

class CardsContainerWidget(QWidget):
    def __init__(self, parent=None):
        super(CardsContainerWidget, self).__init__(parent)
        self._n_cards = 0
        self._cards = []
        self.create_base_content()

    def create_base_content(self):
        
        # --- MAIN CONTAINER ---
        self.main_layout = QHBoxLayout()
        self.main_frame = QFrame()
        self.main_frame.setObjectName("cardContainer")
        self.setStyleSheet(STYLESHEET["CustomCardsContainer"])

        self.main_layout.addWidget(self.main_frame)

        self.setLayout(self.main_layout)

        # --- CARDS CONTAINER ---
        self.frame_layout = QHBoxLayout()

        

        
    def insert_card(self, card):
        self._cards.append(card)
        self._n_cards += 1

        self.connect_card_to_signal(card)
        self.update_content()

    def connect_card_to_signal(self, card):
        card.card_selected_signal.connect(self.update_cards_status)

    def update_cards_status(self, card_clicked_title:str):
        for card in self._cards:
            if card.title == card_clicked_title:
                print(f"{card_clicked_title} clicked!!")
                if card.clicked_flag:
                    card.restart_position()
                    card.clicked_flag = False
                else:
                    card.clicked_flag = True

                
            else:
                card.restart_position()
                card.clicked_flag = False

    def update_content(self):
        
        if self._n_cards > 0:
            for i, card in enumerate(self._cards):
                self.frame_layout.addWidget(card)

        self.main_frame.setLayout(self.frame_layout)


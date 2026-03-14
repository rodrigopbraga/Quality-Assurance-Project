import time
from typing import Final
from selenium import webdriver

from pages import Website

URL: Final[str] = "C:/Users/Konma/Documents/Prisoners-Dilemma/Prisoners-Dilemma/main.html"
PROFILES: Final[list[str]] = ['Random', 'TitForTat', 'Cooperate', 'Defect', 'Detective', 'ParForTat']

class TestPrisonerDilemma:
    driver = webdriver.Chrome()
    driver.maximize_window()

    def start_server(self):
        self.driver.get(URL)
        return Website(self.driver)


    #Player selection
    # > 0 for player A
    # > 1 for player B
    # > Profile list:
    #       Random
    #       TitForTat
    #       Cooperate
    #       Defect
    #       Detective
    #       ParForTat


    # Test to set both players
    def test_player_selection(self):
        pdp = self.start_server()
        profilea = "ParForTat"
        profileb = "Defect"
        pdp.set_player(0, profilea)
        pdp.set_player(1, profileb)
        print(profilea, profileb)
        time.sleep(2)
        assert pdp.assert_both_players(profilea, profileb), f"Incorrect player selection!!!"

    # Same test as previous
    def test_player_selection2(self):
        pdp = self.start_server()
        profilea = "Cooperate"
        profileb = "Random"
        pdp.set_player(0, profilea)
        pdp.set_player(1, profileb)
        print(profilea, profileb)
        time.sleep(2)
        assert pdp.assert_both_players(profilea, profileb), f"Incorrect player selection!!!"

    # Tests Round SlideBar Manipulation
    def test_round_bar(self):
        pdp = self.start_server()
        r = 22
        pdp.set_round(r)
        time.sleep(2)
        assert pdp.assert_round_count(r), f"Incorrect number of rounds!!!"

    # Tests Round Direct Value Manipulation
    def test_round_value(self):
        pdp = self.start_server()
        r = 999
        pdp.set_round_value(r)
        time.sleep(2)
        assert pdp.assert_round_count(r), f"Incorrect rounds value!!!"

    # Tests Mistake SlideBar Manipulation
    def test_mistake_bar(self):
        pdp = self.start_server()
        r = 22
        pdp.set_mistake(r)
        time.sleep(2)
        assert pdp.assert_mistake_count(r), f"Incorrect mistake ratio!!!"

    # Tests Mistake Direct Value Manipulation
    def test_mistake_value(self):
        pdp = self.start_server()
        r = 22
        pdp.set_mistake_value(r)
        time.sleep(2)
        assert pdp.assert_mistake_count(r), f"Incorrect mistake value!!!"

    # Tests sets the Round Count SlideBar,
    #       each Player Profile,
    #       the Mistake Ratio SlideBar,
    #       and how many times the game will be played;
    def test_spar_bar(self):
        pdp = self.start_server()
        nrounds = 20
        pdp.set_round(nrounds)
        profilea = "Detective"
        profileb = "ParForTat"
        pdp.set_player(0, profilea)
        pdp.set_player(1, profileb)
        nmistake = 5
        nplays = 10
        pdp.set_mistake(nmistake)
        pdp.start(nplays)
        time.sleep(2)
        assert pdp.assert_spar(nrounds, profilea, profileb, nmistake, nplays), f"Incorrect spar configuration!!!"

    def test_all_against_all(self):
        pdp = self.start_server()
        for a in PROFILES:
            pdp.set_player(0, a)
            for b in PROFILES:
                pdp.set_player(1, b)
                rp = pdp.get_rounds_played() # or reset game
                pdp.start(1)
                assert pdp.assert_all_against_all(a, b, rp), f"No match between {a} vs {b}!!!"


    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
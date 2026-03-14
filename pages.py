from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class Website:
    #Head
    TITLE = (By.ID, 'website-title')
    TOGGLE_BUTTON = (By.ID, 'display-toggle-button')

    #Body
    #   Left Div
    ROUND_COUNTER = (By.ID, 'roundvalue')
    ROUND_SLIDER_BAR = (By.ID, 'roundcounter')
    KNOWPLAYER_SPAN = (By.ID, 'knowplayersbutton')
    CLOSE_KNOWPLAYER_BUTTON = (By.ID, 'close-modal')
    PLAYERA_SELECTOR = (By.ID, 'playerA')
    PLAYERB_SELECTOR = (By.ID, 'playerB')
    WHICH_PLAYER = [PLAYERA_SELECTOR, PLAYERB_SELECTOR] # Players will be referred in a list
    MISTAKE_COUNTER = (By.ID, 'mistakevalue')
    MISTAKE_SLIDER_BAR = (By.ID, 'mistakeratio')

    #   Central Div
    START_BUTTON = (By.ID, 'start-button')
    APLAYS = (By.ID, 'Aplays')
    BPLAYS = (By.ID, 'Bplays')

    #   Right Div
    NAMEA_H3 = (By.ID, 'stats-name-a')
    CPOINTSA_SPAN = (By.ID, 'stat-cpoints-a')
    LPLAYA_SPAN = (By.ID, 'stat-lpLay-a')
    ATPOINTSA_SPAN = (By.ID, 'stat-atpoints-a')
    ATROUNDSA_SPAN = (By.ID, 'stat-atrounds-a')

    NAMEB_H3 = (By.ID, 'stats-name-b')
    CPOINTSB_SPAN = (By.ID, 'stat-cpoints-b')
    LPLAYB_SPAN = (By.ID, 'stat-lplay-b')
    ATPOINTB_SPAN = (By.ID, 'stat-atpoints-b')
    ATROUNDB_SPAN = (By.ID, 'stat-atrounds-b')

    #Bottom
    RESET_GAME_BUTTON = (By.ID, 'reset-button')


    def __init__(self, driver):
        self.driver = driver  # Inicializa o driver


    def assert_player(self, player, profile):
        return Select(self.driver.find_element(*self.WHICH_PLAYER[player])).first_selected_option.get_attribute("value") == profile

    def assert_both_players(self, profilea, profileb):
        return (Select(self.driver.find_element(*self.WHICH_PLAYER[0])).first_selected_option.get_attribute("value") == profilea
                and Select(self.driver.find_element(*self.WHICH_PLAYER[1])).first_selected_option.get_attribute("value") == profileb)

    def assert_round_count(self, n):
        return int(self.driver.find_element(*self.ROUND_COUNTER).text)==n

    def assert_mistake_count(self, n):
        return int(self.driver.find_element(*self.MISTAKE_COUNTER).text)==n

    def assert_spar(self, nrounds, profilea, profileb, nmistake, nplays):
        return (nrounds == int(self.driver.find_element(*self.ROUND_COUNTER).text)
                and profilea == self.driver.find_element(*self.NAMEA_H3).text
                and profileb == self.driver.find_element(*self.NAMEB_H3).text
                and nmistake == int(self.driver.find_element(*self.MISTAKE_COUNTER).text)
                and int(self.driver.find_element(*self.ATROUNDSA_SPAN).text) == nrounds * nplays)

    def assert_all_against_all(self, profilea, profileb, rp):
        return (profilea == self.driver.find_element(*self.NAMEA_H3).text
            and profileb == self.driver.find_element(*self.NAMEB_H3).text
            and int(self.driver.find_element(*self.ATROUNDB_SPAN).text) == rp + 10)

#----------------------------------------------------------------------------------------------------------------------#

    # Get current rounds played count
    def get_rounds_played(self):
        return int(self.driver.find_element(*self.ATROUNDSA_SPAN).text)
    # Set Player
    def set_player(self, player, profile):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.WHICH_PLAYER[player]))
        Select(self.driver.find_element(*self.WHICH_PLAYER[player])).select_by_value(profile)


    # Set Round Bar with Keyboard
    def set_round(self, n):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ROUND_SLIDER_BAR))
        sb = self.driver.find_element(*self.ROUND_SLIDER_BAR)
        if n>=10:
            for _ in range(n-10):
                sb.send_keys(Keys.RIGHT)
        else:
            for _ in range(10-n):
                sb.send_keys(Keys.LEFT)


    # Set Round Count directly (javascript)
    def set_round_value(self, n):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.ROUND_COUNTER))
        self.driver.execute_script("arguments[0].innerText = arguments[1];",
                                   self.driver.find_element(*self.ROUND_COUNTER), str(n))


    # Set Mistake Bar with Keyboard
    def set_mistake(self, n):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.MISTAKE_SLIDER_BAR))
        sb = self.driver.find_element(*self.MISTAKE_SLIDER_BAR)
        for _ in range(n):
            sb.send_keys(Keys.RIGHT)


    # Set Mistake Value
    def set_mistake_value(self, n):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.MISTAKE_COUNTER))
        self.driver.execute_script("arguments[0].innerText = arguments[1];",
                                   self.driver.find_element(*self.MISTAKE_COUNTER), str(n))


    def start(self, n):
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(self.START_BUTTON))
        for _ in range(n):
            self.driver.find_element(*self.START_BUTTON).click()

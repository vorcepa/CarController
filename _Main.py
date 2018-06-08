import pygame as pg
import utils
from BackgroundMap import GameMap
from GenericCar import CarActive, DirectionOfMotion, DirectionReticle
from Controller import Controller
from Sensors import Sensor
from pygooey import textbox, button


class PIDCar():
    def __init__(self, gameWindow):
        self.gameWindow = gameWindow
        pg.display.set_caption("Self-driving car")
        self.clock = pg.time.Clock()
        self.FPS = 60
        self.map = GameMap()
        self.car = CarActive()
        self.cos_theta, self.sin_theta, self.radian = (0, 0, 0)
        self.direction = DirectionOfMotion(self.car.image,
                                           (self.car.rect.centerx,
                                            self.car.rect.centery))
        self.dirReticle = DirectionReticle(self.car.image,
                                           (self.car.rect.centerx,
                                            self.car.rect.centery))

        self.controller = Controller()
        self.controller_coeffs = [self.controller.p_const,
                                  self.controller.i_const,
                                  self.controller.d_const]

        ### UI Elements START
        # Start screen
        self.start_btn = button.Button(rect=(325, 385, 150, 30), command=start_btn_func, **settings_startbtn)
        self.input_updatebtn = button.Button(rect=(475, 175, 285, 30), command=input_updatebtn, **settings_input_updatebtn)
        self.exit_btn = button.Button(rect=(325, 425, 150, 30), command=exit_btn_func, **settings_exitbtn)
        self.p_input = textbox.TextBox(rect=(170, 140, 150, 30), **settings_controller_input_box)
        self.i_input = textbox.TextBox(rect=(170, 180, 150, 30), **settings_controller_input_box)
        self.d_input = textbox.TextBox(rect=(170, 220, 150, 30), **settings_controller_input_box)

        # Game Running
        self.show_sensors_btn = button.Button(rect=(650, 470, 150, 30), command=show_sensors, **settings_show_sensors)
        self.hide_sensors_btn = button.Button(rect=(650, 470, 150, 30), command=hide_sensors, **settings_hide_sensors)
        self.see_sensors_btn = True

        self.update_coeffs_btn = button.Button(rect=(650, 440, 150, 30), command=update_coeffs, **settings_update_coeffs)
        self.confirm_update_btn = button.Button(rect=(650, 440, 150, 30), command=confirm_update, **settings_confirm_update)
        self.p2_input = textbox.TextBox(rect=(648, 300, 150, 30), **settings_controller_input_box)
        self.i2_input = textbox.TextBox(rect=(648, 335, 150, 30), **settings_controller_input_box)
        self.d2_input = textbox.TextBox(rect=(648, 370, 150, 30), **settings_controller_input_box)
        self.cancel_btn = button.Button(rect=(650, 405, 150, 30), command=cancel_update, **settings_cancel_update)
        self.defaults_btn = button.Button(rect=(650, 265, 150, 30), command=defaults, **settings_defaults)
        self.see_coeff_box = False

        self.reset_btn = button.Button(rect=(650, 500, 150, 30), command=reset_func, **settings_reset)
        ### UI Elements END

        self.sensor0 = Sensor(self.gameWindow, False, .1875, 200, 1)   # Starts at top right
        self.sensor1 = Sensor(self.gameWindow, False, 1.75, 180, 1)  # Starts at bottom right

        self.sensorList = [self.sensor0, self.sensor1]
        self.sensorOffsets = [i.rOffset for i in self.sensorList]
        self.sensorTest = [None] * len(self.sensorList)

        self.menu = True
        self.show_error_toggle = False
        self.error_timer = 0
        self.error_msg = ""

        self.testCD = 15
        self.testCDMax = 15

    def quitGame(self):
        pg.quit()
        raise SystemExit(0)

    def gotoMenu(self):
        while self.menu:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quitGame()
                if event.type == pg.KEYUP:
                    if event.key == pg.K_s:
                        return
                    if event.key == pg.K_ESCAPE:
                        self.quitGame()
                    if event.key == pg.K_c:
                        input_updatebtn()

                self.start_btn.get_event(event)
                self.exit_btn.get_event(event)
                self.input_updatebtn.get_event(event)
                self.p_input.get_event(event)
                self.i_input.get_event(event)
                self.d_input.get_event(event)

            self.gameWindow.fill(utils.WHITE)

            """Text to display on screen"""
            title = utils.getFont(size=64, style='bold').render("Self-driving Car", False, utils.BLACK)
            titleRect = title.get_rect()
            titleRect.center = self.gameWindow.get_rect().center
            titleRect.y -= 250

            font = utils.getFont()
            settings_text = utils.getFont(style="bold").render("Controller Settings", False, utils.BLACK)
            settings_text_rect = settings_text.get_rect()
            settings_text_rect.center = self.gameWindow.get_rect().center
            settings_text_rect.y -= 200
            settings_text_rect.x -= 165

            proportional_word = font.render("Proportional", False, utils.BLACK)
            proportional_word_rect = proportional_word.get_rect()
            proportional_word_rect.center = self.gameWindow.get_rect().center
            proportional_word_rect.y -= 145
            proportional_word_rect.x -= 315

            integral_word = font.render("Integral", False, utils.BLACK)
            integral_word_rect = integral_word.get_rect()
            integral_word_rect.center = self.gameWindow.get_rect().center
            integral_word_rect.y -= 105
            integral_word_rect.x -= 315

            derivative_word = font.render("Derivative", False, utils.BLACK)
            derivative_word_rect = derivative_word.get_rect()
            derivative_word_rect.center = self.gameWindow.get_rect().center
            derivative_word_rect.y -= 65
            derivative_word_rect.x -= 315

            font.set_underline(True)
            coefficient_word = font.render("Coefficient", False, utils.BLACK)
            coefficient_word_rect = coefficient_word.get_rect()
            coefficient_word_rect.center = self.gameWindow.get_rect().center
            coefficient_word_rect.y -= 180
            coefficient_word_rect.x -= 315

            current_word = font.render("Current", False, utils.BLACK)
            current_word_rect = current_word.get_rect()
            current_word_rect.center = self.gameWindow.get_rect().center
            current_word_rect.y -= 180
            current_word_rect.x -= 25
            font.set_underline(False)

            p_value = font.render(str(round(self.controller_coeffs[0], 4)), False, utils.BLUE)
            p_value_rect = p_value.get_rect()
            p_value_rect.center = self.gameWindow.get_rect().center
            p_value_rect.y -= 145
            p_value_rect.x -= 25

            i_value = font.render(str(round(self.controller_coeffs[1], 4)), False, utils.BLUE)
            i_value_rect = i_value.get_rect()
            i_value_rect.center = self.gameWindow.get_rect().center
            i_value_rect.y -= 105
            i_value_rect.x -= 25

            d_value = font.render(str(round(self.controller_coeffs[2], 4)), False, utils.BLUE)
            d_value_rect = d_value.get_rect()
            d_value_rect.center = self.gameWindow.get_rect().center
            d_value_rect.y -= 65
            d_value_rect.x -= 25

            error_message = utils.getFont(size=16, style="bold").render(self.error_msg, False, utils.BLACK)
            error_message_rect = error_message.get_rect()
            error_message_rect.center = self.gameWindow.get_rect().center
            error_message_rect.y -= 80
            error_message_rect.x += 215
            """End text displays.  Make sure you blit/draw them all"""

            self.gameWindow.blit(title, titleRect)
            self.gameWindow.blit(settings_text, settings_text_rect)
            self.gameWindow.blit(coefficient_word, coefficient_word_rect)
            self.gameWindow.blit(proportional_word, proportional_word_rect)
            self.gameWindow.blit(integral_word, integral_word_rect)
            self.gameWindow.blit(derivative_word, derivative_word_rect)
            self.gameWindow.blit(current_word, current_word_rect)
            self.gameWindow.blit(p_value, p_value_rect)
            self.gameWindow.blit(i_value, i_value_rect)
            self.gameWindow.blit(d_value, d_value_rect)

            self.error_timer -= 1
            if self.error_timer <= 0:
                self.show_error_toggle = False
            else:
                self.show_error_toggle = True
            if self.show_error_toggle:
                self.gameWindow.blit(error_message, error_message_rect)

            self.start_btn.draw(self.gameWindow)
            self.exit_btn.draw(self.gameWindow)
            self.input_updatebtn.draw(self.gameWindow)
            self.p_input.update()
            self.p_input.draw(self.gameWindow)
            self.i_input.update()
            self.i_input.draw(self.gameWindow)
            self.d_input.update()
            self.d_input.draw(self.gameWindow)

            pg.display.update()
            self.clock.tick(self.FPS)

    def playGame(self):  # maybe rename later?
        self.gotoMenu()

        gameActive = True
        rOffsets = []

        self.exit_btn.rect = pg.Rect(650, 570, 150, 30)

        for i in self.sensorList:
            rOffsets.append(i.rOffset)
        while gameActive:
            sensorRead = []
            colorPos = []

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    gameActive = False
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        self.quitGame()

                self.exit_btn.get_event(event)
                self.reset_btn.get_event(event)
                self.update_coeffs_btn.get_event(event)
                if self.see_sensors_btn:
                    self.show_sensors_btn.get_event(event)
                else:
                    self.hide_sensors_btn.get_event(event)
                if not self.see_coeff_box:
                    self.update_coeffs_btn.get_event(event)
                else:
                    self.confirm_update_btn.get_event(event)
                    self.p2_input.get_event(event)
                    self.i2_input.get_event(event)
                    self.d2_input.get_event(event)
                    self.cancel_btn.get_event(event)
                    self.defaults_btn.get_event(event)

            move = self.car.move(self.radian)

            self.gameWindow.fill(utils.WHITE)
            self.map.resetMap()
            self.car.update(self.map.activeMap)

            """
            bgOffset updates the background *and* also returns a tuple
            of the offset (x,y) coordinates between player location
            on the background and the screen pixel location. This tuple
            is used to draw the direction circle to the correct location.
            """

            bgOffset = self.map.update(self.gameWindow, self.car.rect, move)
            directionLoc = (self.car.rect.centerx + bgOffset[0],
                            self.car.rect.centery + bgOffset[1])
            self.direction.update(self.gameWindow, (directionLoc[0],
                                                    directionLoc[1]))

            retLocX = directionLoc[0] + int(round(125*self.cos_theta, 0))
            retLocY = directionLoc[1] + int(round(125*self.sin_theta, 0))
            self.dirReticle.update(self.gameWindow, (retLocX, retLocY))

            """
            Sensors move, then the sensors are read.
            The information from the read sensors is then
            passed to the PID controller
            """
            for i in self.sensorList:
                sensorRead.append(i.move(directionLoc, self.radian))
                colorPos.append((i.rect.centerx, i.rect.centery))

            errorCorrection = self.controller.PID(sensorRead, rOffsets, self.radian)

            if errorCorrection is not None:
                cos_theta, sin_theta, self.radian = errorCorrection

            error_message = utils.getFont(size=16, style="bold").render(self.error_msg, False, utils.BLACK)
            error_message_rect = error_message.get_rect()

            self.exit_btn.draw(self.gameWindow)
            self.reset_btn.draw(self.gameWindow)
            self.update_coeffs_btn.draw(self.gameWindow)
            if self.see_sensors_btn:
                self.show_sensors_btn.draw(self.gameWindow)
            else:
                self.hide_sensors_btn.draw(self.gameWindow)
            if not self.see_coeff_box:
                self.update_coeffs_btn.draw(self.gameWindow)
            else:
                self.confirm_update_btn.draw(self.gameWindow)
                self.cancel_btn.draw(self.gameWindow)
                self.p2_input.draw(self.gameWindow)
                self.p2_input.update()
                self.i2_input.draw(self.gameWindow)
                self.i2_input.update()
                self.d2_input.draw(self.gameWindow)
                self.d2_input.update()
                self.defaults_btn.draw(self.gameWindow)

                self.error_timer -= 1
                if self.error_timer <= 0:
                    self.show_error_toggle = False
                else:
                    self.show_error_toggle = True
                if self.show_error_toggle:
                    self.gameWindow.blit(error_message, error_message_rect)

            pg.display.update()
            self.clock.tick(self.FPS)

        self.quitGame()


# UI Elements
def start_btn_func():
    game.menu = False


def exit_btn_func():
    game.quitGame()


def input_updatebtn():
    errors = 0
    error_type = ""

    if len(game.p_input.final) is not 0:
        try:
            game.controller.p_const = float(game.p_input.final)
        except ValueError:
            errors += 1
            error_type = "p"

    if len(game.i_input.final) is not 0:
        try:
            game.controller.i_const = float(game.i_input.final)
        except ValueError:
            errors += 1
            error_type = "i"

    if len(game.d_input.final) is not 0:
        try:
            game.controller.d_const = float(game.d_input.final)
        except ValueError:
            errors += 1
            error_type = "d"

    if errors > 0:
        game.show_error_toggle = True
        game.error_timer = game.FPS*5
        if errors == 1:
            if error_type == "p":
                game.error_msg = "Invalid proportional value!"
            elif error_type == "i":
                game.error_msg = "Invalid integral value!"
            elif error_type == "d":
                game.error_msg = "Invalid derivative value!"
        elif errors > 1:
            game.error_msg = "Multiple input value errors!"

    game.controller_coeffs = [game.controller.p_const,
                              game.controller.i_const,
                              game.controller.d_const]


def show_sensors():
    game.sensor0.display = True
    game.sensor1.display = True
    game.see_sensors_btn = False


def hide_sensors():
    game.sensor0.display = False
    game.sensor1.display = False
    game.see_sensors_btn = True


def reset_func():
    game.car.rect.x = 0
    game.car.rect.y = 0
    game.radian, game.cos_theta, game.sin_theta = (0, 0, 0)
    game.map.offsetX = 0
    game.map.offsetY = 0
    game.controller.integral = 0
    game.controller.previous_error = 0
    game.controller.gain = 0
    game.controller.omega = 0
    game.controller.radian = 0


def update_coeffs():
    game.see_coeff_box = True


def confirm_update():
    errors = 0
    error_type = ""

    if len(game.p2_input.final) is not 0:
        try:
            game.controller.p_const = float(game.p2_input.final)
        except ValueError:
            errors += 1
            error_type = "p"

    if len(game.i2_input.final) is not 0:
        try:
            game.controller.i_const = float(game.i2_input.final)
        except ValueError:
            errors += 1
            error_type = "i"

    if len(game.d2_input.final) is not 0:
        try:
            game.controller.d_const = float(game.d2_input.final)
        except ValueError:
            errors += 1
            error_type = "d"

    if errors > 0:
        game.show_error_toggle = True
        game.error_timer = game.FPS*3
        if errors == 1:
            if error_type == "p":
                game.error_msg = "Invalid proportional value!"
            elif error_type == "i":
                game.error_msg = "Invalid integral value!"
            elif error_type == "d":
                game.error_msg = "Invalid derivative value!"
        elif errors > 1:
            game.error_msg = "Multiple input value errors!"

    game.controller_coeffs = [game.controller.p_const,
                              game.controller.i_const,
                              game.controller.d_const]
    if errors == 0:
        game.see_coeff_box = False


def cancel_update():
    game.see_coeff_box = False


def defaults():
    game.controller.p_const = .1
    game.controller.i_const = 1/60
    game.controller.d_const = 1/30
    reset_func()
    game.see_coeff_box = False


settings_startbtn = {"text": "Start! (s)", "font": utils.getFont()}
settings_exitbtn = {"text": "Exit (esc)", "font": utils.getFont()}
settings_input_updatebtn = {"text": "Update coefficients (c)", "font": utils.getFont()}
settings_controller_input_box = {"active": False}
settings_show_sensors = {"text": "Show Sensors", "font": utils.getFont()}
settings_hide_sensors = {"text": "Hide Sensors", "font": utils.getFont()}
settings_reset = {"text": "Reset", "font": utils.getFont()}
settings_update_coeffs = {"text": "Update coefficients", "font": utils.getFont(size=12)}
settings_confirm_update = {"text": "Update!", "font": utils.getFont(size=12)}
settings_cancel_update = {"text": "Cancel", "font": utils.getFont()}
settings_defaults = {"text": "Default Values", "font": utils.getFont(size=12)}

if __name__ == "__main__":
    pg.init()
    gameWindow = pg.display.set_mode((800, 600))
    game = PIDCar(gameWindow)
    game.playGame()

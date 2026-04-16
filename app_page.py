import arcade
import os
import json

cwd = os.path.dirname(os.path.abspath(__file__))


def load(path: str) -> str:
    global cwd
    return os.path.join(cwd, path)


class AppPage(arcade.View):
    def __init__(self, app):
        super().__init__()

        # Function variables
        self.is_dragging = False
        self.SCREEN_W = 1
        self.SCREEN_H = 1

        # "Setup" variables
        self.logo = None
        self.app_list = None

    def on_show_view(self):
        self.setup()

    def setup(self):
        # Set background color
        arcade.set_background_color((255, 253, 232, 1))

        # Hide mouse
        self.window.set_mouse_visible(True)

        # Setup window
        self.window.activate()
        self.window.set_location(self.SCREEN_W // 2 - self.window.width // 2,
                                 self.SCREEN_H * 4 // 10 - self.window.height // 2)

        # Setup logo
        self.logo = arcade.Sprite(load('client_assets/logos/logo.png'))
        self.logo.scale = 0.6
        self.logo.position = self.window.width // 2, self.window.height * 2 // 3 - 20

        self.is_dragging = False

        print(self.window.views)

    def on_draw(self):
        self.window.clear()
        arcade.Text('PHOBOS CLIENT',
                    self.window.width // 2,
                    self.window.height // 3 - 30,
                    arcade.color.BLACK,
                    22,
                    anchor_x='center',
                    bold=True,
                    font_name='CNRGNNormal').draw()

    def on_update(self, delta_time):
        pass

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & arcade.MOUSE_BUTTON_LEFT:
            try:
                # New position
                curr_x, curr_y = self.window.get_location()
                new_x = curr_x + dx
                new_y = curr_y - dy

                # Clamp X
                if new_x < 0:
                    new_x = 0
                elif new_x > self.SCREEN_W - self.window.width:
                    new_x = self.SCREEN_W - self.window.width

                # Clamp Y
                if new_y < 0:
                    new_y = 0
                elif new_y > self.SCREEN_H - self.window.height:
                    new_y = self.SCREEN_H - self.window.height

                self.window.set_location(new_x, new_y)

            except Exception:
                pass

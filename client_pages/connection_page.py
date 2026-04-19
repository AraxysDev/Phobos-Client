import arcade
import os

cwd = os.path.dirname(os.path.abspath(__file__))


def load(path: str) -> str:
    global cwd
    return os.path.join(cwd, path)


# Load fonts
arcade.load_font(load('../client_assets/fonts/CNRGNNormal.otf'))


class connection_error(arcade.View):
    def __init__(self, screen_w, screen_h):
        super().__init__()

        # Function variables
        self.is_dragging = False
        self.SCREEN_W = screen_w
        self.SCREEN_H = screen_h

        # "Setup" variables
        self.logo = None
        self.button_height = None
        self.button_width = None
        self.button_y = None
        self.button_x = None

    def on_show_view(self):
        self.setup()

    def setup(self):
        # Set background color
        arcade.set_background_color((255, 253, 232, 1))

        # Hide mouse
        self.window.set_mouse_visible(True)

        # Setup window
        self.window.activate()
        self.window.set_size(550, 280)
        self.window.set_location(self.window.cache['connection_page_pos'][0], self.window.cache['connection_page_pos'][1])

        # Setup logo
        self.logo = arcade.Sprite(load('../client_assets/logos/logo.png'))
        self.logo.scale = 0.25
        self.logo.position = 40, self.window.height - 40

        self.is_dragging = False

        # Setup button
        self.button_x, self.button_y, self.button_width, self.button_height = self.window.width // 2, self.window.height // 2 - 80, 100, 50

    def on_draw(self):
        self.window.clear()

        # Render logo and information
        arcade.draw_sprite(self.logo)

        arcade.Text('Connection Error',
                    self.window.width // 2,
                    self.window.height // 2 + 60,
                    (30, 30, 30),
                    21,
                    anchor_x='center',
                    bold=True,
                    font_name='CNRGNNormal').draw()

        arcade.Text('Please make sure your device is connected to internet with a stable connection. It may also be our servers are down.',
                    self.window.width // 2,
                    self.window.height // 2 + 30,
                    arcade.color.GRAY,
                    14,
                    anchor_x='center',
                    width=400,
                    multiline=True,
                    font_name='CNRGNNormal').draw()

        # Render button
        arcade.draw_lrbt_rectangle_outline(self.button_x - self.button_width // 2, self.button_x + self.button_width // 2, self.button_y - self.button_height // 2, self.button_y + self.button_height // 2, color=arcade.color.GREEN, border_width=2)
        arcade.Text(
            'Retry',
            self.button_x - 2,
            self.button_y - 9,
            arcade.color.GREEN,
            18,
            anchor_x='center',
            font_name='CNRGNNormal').draw()

    def on_update(self, delta_time):
        self.window.cache['connection_page_pos'] = tuple(self.window.get_location())

    def on_mouse_press(self, x, y, button, modifiers):
        # Check if button is clicked
        if self.button_x - self.button_width // 2 < x < self.button_x + self.button_width // 2 and self.button_y - self.button_height // 2 < y < self.button_y + self.button_height // 2:
            self.window.show_view(self.window.views['initial_load'])

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

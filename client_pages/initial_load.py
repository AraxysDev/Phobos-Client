# Import libraries
import arcade
import os
import json
import threading
import requests

# Import Pages
from client_pages.app_page import AppPage

# Import logs
from client_logs.main_logs import page_opened, log

cwd = os.path.dirname(os.path.abspath(__file__))


def load(path: str) -> str:
    global cwd
    return os.path.join(cwd, path)


def calculate_easing(t):
    return t * t * (3 - 2 * t)


# Load fonts
arcade.load_font(load('../client_assets/fonts/CNRGNNormal.otf'))


class initial_load(arcade.View):
    def __init__(self, screen_w, screen_h):
        super().__init__()

        # Function variables
        self.is_dragging = False
        self.SCREEN_W = screen_w
        self.SCREEN_H = screen_h

        # "Setup" variables
        self.app_names = None
        self.switched = None
        self.downloaded_data_queue = None
        self.progress = None
        self.app_list = None
        self.logo = None
        self.json_fetch_thread = None
        self.network_error = None

    def on_show_view(self):
        page_opened('Initial Load')
        self.setup()

    def setup(self):
        # Set background color
        arcade.set_background_color((255, 253, 232, 1))

        # Hide mouse
        self.window.set_mouse_visible(True)

        # Setup window
        self.window.activate()
        self.window.set_size(550, 280)
        self.window.set_location(self.SCREEN_W // 2 - self.window.width // 2,
                                 self.SCREEN_H * 4 // 10 - self.window.height // 2)

        # Setup logo
        self.logo = arcade.Sprite(load('../client_assets/logos/logo.png'))
        self.logo.scale = 0.6
        self.logo.position = self.window.width // 2, self.window.height * 2 // 3 - 20

        self.is_dragging = False
        self.network_error = False

        # Load app list
        with open(load('../client_apps.json'), 'r') as f:
            self.app_list = json.load(f)

        log(f'Found app list: {self.app_list}')

        self.progress = 0
        self.switched = False
        self.downloaded_data_queue = []
        self.app_names = []

        self.json_fetch_thread = threading.Thread(target=self.fetch_all_json, daemon=True)
        self.json_fetch_thread.start()
        log(f'Started fetch_all_json thread: {self.json_fetch_thread}')

    def fetch_all_json(self):
        for app_url in self.app_list:
            try:
                response = requests.get(app_url)
                response.raise_for_status()
                data = response.json()

                self.downloaded_data_queue.append((app_url, data))
            except Exception as e:
                log(f"Failed fetching {app_url}: {e}", error=True)
                self.network_error = True

    def on_draw(self):
        self.window.clear()

        arcade.draw_sprite(self.logo)

        arcade.Text('PHOBOS CLIENT',
                    self.window.width // 2,
                    self.window.height // 3 - 30,
                    arcade.color.BLACK,
                    22,
                    anchor_x='center',
                    bold=True,
                    font_name='CNRGNNormal').draw()

        arcade.draw_lrbt_rectangle_filled(0, self.window.width, 0, 10, (235, 233, 212))

        arcade.draw_lrbt_rectangle_filled(0, self.window.width * self.progress, 0, 10, arcade.color.WHEAT)

    def on_update(self, delta_time):
        if self.downloaded_data_queue:
            # Create object
            app_url, data = self.downloaded_data_queue.pop(0)
            app_name = data.get('name')
            self.app_names.append(app_name)

            self.window.views[app_name] = AppPage(app_url, data, self.SCREEN_W, self.SCREEN_H)

            # Update progress
            self.progress = (len(self.window.views) - 1) / len(self.app_list)

        if self.progress >= 1 and not self.switched:
            self.switched = True
            log(f'Loading pages complete: {self.window.views}')
            self.window.show_view(self.window.views[self.app_names[0]])

        if self.network_error:
            log(f'Switching to connection error page.')
            self.window.show_view(self.window.views['connection_error'])

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

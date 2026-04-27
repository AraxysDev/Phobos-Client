import arcade
import os

cwd = os.path.dirname(os.path.abspath(__file__))


def load(path: str) -> str:
    global cwd
    return os.path.join(cwd, path)


def calculate_easing(t):
    return t * t * (3 - 2 * t)


def in_region(x, y, l, r, b, t):
    return (l <= x <= r) and (b <= y <= t)


# Load fonts
arcade.load_font(load('../client_assets/fonts/CNRGNNormal.otf'))


class AppPage(arcade.View):
    def __init__(self, app_url, app_data, screen_w, screen_h):
        super().__init__()
        # Constants
        self.WINDOW_WIDTH, self.WINDOW_HEIGHT = 1200, 700
        self.sidebar_animation_duration = 0.5
        self.sidebar_animation_threshold = 20
        self.drag_bar_height = 20
        self.tabs_w = 130
        self.tabs_h = 30
        self.tabs_y = self.WINDOW_HEIGHT - self.drag_bar_height - self.tabs_h // 2 - 10
        self.sidebar_width = 80
        self.tabs_center = self.sidebar_width + (self.WINDOW_WIDTH - self.sidebar_width) // 2
        self.tab = 0
        self.tabs = ['APP', 'Patch Notes']
        self.tab_coords = []

        for idx, tab in enumerate(self.tabs):
            self.tab_coords.append([self.tabs_center - int(len(self.tabs) / 2 * self.tabs_w) + idx * self.tabs_w,
                                    self.tabs_center - int(len(self.tabs) / 2 * self.tabs_w) + (idx + 1) * self.tabs_w,
                                    self.tabs_y - self.tabs_h // 2,
                                    self.tabs_y + self.tabs_h // 2])

        # Function variables
        self.is_dragging = False
        self.SCREEN_W = screen_w
        self.SCREEN_H = screen_h

        # "Setup" variables
        self.logo = None
        self.duration = None
        self.is_hovering_sidebar = None

    def on_show_view(self):
        self.setup()

    def setup(self):
        # Set background color
        arcade.set_background_color((255, 253, 232, 1))

        # Hide mouse
        self.window.set_mouse_visible(True)

        # Setup window
        self.window.activate()
        self.window.set_size(self.WINDOW_WIDTH, self.WINDOW_HEIGHT)
        self.window.set_location(self.SCREEN_W // 2 - self.window.width // 2,
                                 self.SCREEN_H * 4 // 10 - self.window.height // 2)

        # Setup logo
        self.logo = arcade.Sprite(load('../client_assets/logos/logo.png'))
        self.logo.scale = 0.2
        self.logo.position = 40, self.window.height - 60

        # Setup sidebar animation
        self.is_hovering_sidebar = False
        self.duration = 0

        self.is_dragging = False
        self.tab = 0

    def on_draw(self):
        self.window.clear()

        # Draw sidebar
        arcade.draw_lrbt_rectangle_filled(0, self.sidebar_width, 0, self.window.height, arcade.color.WHEAT)
        arcade.draw_sprite(self.logo)

        # Draw tabs
        arcade.draw_lrbt_rectangle_filled(self.tabs_center - int(len(self.tabs) / 2 * self.tabs_w),
                                          self.tabs_center + int(len(self.tabs) / 2 * self.tabs_w),
                                          self.tabs_y - self.tabs_h // 2,
                                          self.tabs_y + self.tabs_h // 2,
                                          (235, 233, 212))

        for idx, tab in enumerate(self.tabs):
            if self.current_tab() == tab:
                arcade.draw_lrbt_rectangle_filled(self.tab_coords[self.tab][0],
                                                  self.tab_coords[self.tab][1],
                                                  self.tab_coords[self.tab][2],
                                                  self.tab_coords[self.tab][3],
                                                  arcade.color.WHEAT)
            arcade.Text(tab,
                        self.tabs_center - int(len(self.tabs) / 2 * self.tabs_w) + int((idx + 0.5) * self.tabs_w),
                        self.tabs_y - 6,
                        arcade.color.BLACK,
                        12,
                        anchor_x='center',
                        bold=(self.current_tab() == tab),
                        font_name='CNRGNNormal').draw()

        # Draw elements within tabs
        if self.current_tab() == self.tabs[0]:
            pass
        elif self.current_tab() == self.tabs[1]:
            pass

    def on_update(self, delta_time):
        # Sidebar animation
        if self.is_hovering_sidebar:
            self.duration = min(self.duration + delta_time, self.sidebar_animation_duration)
        else:
            self.duration = max(0, self.duration - delta_time)

        extend_amount = calculate_easing(
            self.duration / self.sidebar_animation_duration) * self.sidebar_animation_threshold
        self.sidebar_width = 80 + extend_amount

    def on_mouse_press(self, x, y, button, modifiers):
        # Check for tab press
        for idx, tab in enumerate(self.tabs):
            res = in_region(x,
                            y,
                            self.tab_coords[idx][0],
                            self.tab_coords[idx][1],
                            self.tab_coords[idx][2],
                            self.tab_coords[idx][3])
            if res and self.current_tab() != tab:
                self.tab = idx

    def on_mouse_motion(self, x, y, dx, dy):
        # Detect if hovering sidebar
        if x <= 80:
            self.is_hovering_sidebar = True
        else:
            self.is_hovering_sidebar = False

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        if buttons & arcade.MOUSE_BUTTON_LEFT and y > (self.window.height - self.drag_bar_height):
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

    def current_tab(self):
        return self.tabs[self.tab]

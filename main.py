# Import libraries
import arcade

# Import pages
from client_pages.initial_load import initial_load
from client_pages.connection_page import connection_error

if __name__ == '__main__':
    # Setup window
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE = 550, 280, 'Phobos Client'
    SCREEN_W, SCREEN_H = arcade.get_display_size()
    win = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, style='borderless')

    # Load views
    win.views = {'initial_load': initial_load(SCREEN_W, SCREEN_H), 'connection_error': connection_error(SCREEN_W, SCREEN_H)}
    win.cache = {'connection_page_pos': (SCREEN_W // 2 - 550 / 2, SCREEN_H * 4 // 10 - 280 / 2)}

    # Show initial screen
    win.show_view(win.views['initial_load'])

    # Run arcade
    arcade.run()

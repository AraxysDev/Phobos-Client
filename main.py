# Import libraries
import arcade

# Import custom modules
from initial_load import initial_load

if __name__ == '__main__':
    # Setup window
    WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE = 550, 280, 'Phobos Client'
    SCREEN_W, SCREEN_H = arcade.get_display_size()
    win = arcade.Window(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE, style='borderless')

    # Load views
    initial_load_view = initial_load(SCREEN_W, SCREEN_H)

    # Set the initial view to the loading screen
    win.show_view(initial_load_view)
    
    # Run arcade
    arcade.run()
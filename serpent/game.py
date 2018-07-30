from serpent.window_controller import WindowController
from serpent.game_launchers import *
import time

class Game:
    def __init__(self,  **kwargs):
        self.kwargs = kwargs
        self.window_name = kwargs.get("window_name")
        self.is_launched = True
        self.window_controller = WindowController()
        self.game_launcher = ExecutableGameLauncher(**kwargs)



    def launch(self, dry_run=False):
        self.before_launch()

        if not dry_run:
            self.game_launcher.launch(**self.kwargs)

        self.after_launch()

    def before_launch(self):
        pass


    def after_launch(self):
        self.is_launched = True

        time.sleep(3)

        self.window_id = self.window_controller.locate_window(self.window_name)

        self.window_controller.move_window(self.window_id, 0, 0)
        self.window_controller.focus_window(self.window_id)

        self.window_geometry = self.extract_window_geometry()

        print(self.window_geometry)


    def extract_window_geometry(self):
        if self.is_launched:
            return self.window_controller.get_window_geometry(self.window_id)

        return None

    def is_focused(self):
        return self.window_controller.is_window_focused(self.window_id)
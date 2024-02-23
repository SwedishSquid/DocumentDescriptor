from UI.View.view import View
import logging_configuration

if __name__ == "__main__":
    logging_configuration.configure_main_logger()
    view = View()
    view.run()

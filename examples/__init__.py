import os

    
class Color:
    # ANSI color codes
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"
    RESET = "\033[0m"
    NAMES = {
        "black": BLACK,
        "red": RED,
        "green": GREEN,
        "yellow": YELLOW,
        "blue": BLUE,
        "magenta": MAGENTA,
        "cyan": CYAN,
        "white": WHITE,
        "reset": RESET,
    }
    @staticmethod
    def cprint(text, color="reset"):
        """
        Prints colored text to the console.

        Parameters:
            text (str): The text to print.
            color (str): The color to use, specified as a color name or ANSI code.
        """
        if color in Color.NAMES:
            color_code = Color.NAMES[color]
        else:
            color_code = color
        print(f"\033[1m{color_code}{text}{Color.RESET}")    

def example_path(file):
    return os.path.join(os.path.dirname(__file__),"data",file)
def ppause(data,color=Color.RESET,print_newline=True):
    Color.cprint(data,color)    
    input("Press Enter to continue...")
    print("\033[F\033[K", end="")    
    if print_newline:print("\n")
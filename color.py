#-----------------------------------------------------------------------------------------------------------------------
# Color palette
# This class serves only to make coloring text for console output easier
#-----------------------------------------------------------------------------------------------------------------------

RED = '\033[91m'
GREEN = '\033[92m'
YELLOW = '\033[93m'
BLUE = '\033[94m'
MAGENTA = '\033[95m'
CYAN = '\033[96m'
END = '\033[0m'



def red(text):
    return f"{RED}{text}{END}"

def green(text):
    return f"{GREEN}{text}{END}"

def yellow(text):
    return f"{YELLOW}{text}{END}"

def blue(text):
    return f"{BLUE}{text}{END}"

def magenta(text):
    return f"{MAGENTA}{text}{END}"

def cyan(text):
    return f"{CYAN}{text}{END}"
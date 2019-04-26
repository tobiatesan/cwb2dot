debug_mode = False

def debug_out(*string):
    if (debug_mode is True):
        print("DEBUG:", string)
    else:
        pass

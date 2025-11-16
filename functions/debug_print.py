# Helper function to remove amount of if statements in flow
def debug_print(printme: str = "", debug: bool = False):
    if debug == True:
        print(printme, flush=True)
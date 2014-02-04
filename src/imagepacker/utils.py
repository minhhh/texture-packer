import sys, traceback

def isMac():
    return False

def print_last_exception():
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print("*** Exception occured:")
    traceback.print_exception(exc_type, exc_value, exc_traceback,
                              limit=4, file=sys.stdout)

import os
def clean(dir = '.'):
    """
    clean the cache in Mac OS
    """
    
    for item in os.listdir(dir):
        path = os.path.join(dir, item)
        if os.path.isdir(path):
            clean(path)
        else:
            if '.DS_Store' in path:
                os.remove(path)

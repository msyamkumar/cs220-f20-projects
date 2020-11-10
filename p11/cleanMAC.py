import os
def clean():
    """
    clean the cache in Mac OS
    """
    for root, dirs, files in os.walk('.'):
        for item in dirs:
            if (item[0]!='.'):
                try:
                    os.remove(os.path.join(item,'.DS_Store'))
                except:
                    pass
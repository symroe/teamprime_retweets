import time
import os

def mkdir(newdir):
    """works the way a good mkdir should :)
        - already exists, silently complete
        - regular file in the way, raise an exception
        - parent directory(ies) does not exist, make them as well
    """
    if os.path.isdir(newdir):
        pass
    elif os.path.isfile(newdir):
        raise OSError("a file with the same name as the desired " \
                      "dir, '%s', already exists." % newdir)
    else:
        head, tail = os.path.split(newdir)
        if head and not os.path.isdir(head):
            mkdir(head)
        #print "_mkdir %s" % repr(newdir)
        if tail:
            os.mkdir(newdir)

def mkpath(*args):
    args = map(str, args)
    return os.path.join(*args)

def mkdate(tweet):
    return time.strftime('%Y-%m-%d', 
                         time.strptime(tweet.created_at,
                         '%a %b %d %H:%M:%S +0000 %Y'))

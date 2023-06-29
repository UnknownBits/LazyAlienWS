if __name__ == '__main__':
    from lazyalienws.__version__ import __version__
    print(__version__)
    
    from lazyalienws.server import core
    core.start()
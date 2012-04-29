#MAIN FILE
import BlockManager
import EntityManager


def main():
    print "Welcome to planet craft"
    eMan = EntityManager
    bMan = BlockManager
    acore = bMan.Core("rwar")
    aplan = eMan.Planet("test")
    print aplan
    print acore

if __name__ == '__main__':
    main()

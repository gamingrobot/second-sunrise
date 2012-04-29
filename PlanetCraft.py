#MAIN FILE
import BlockManager
import EntityManager


def main():
    print "Welcome to PlanetCraft!"
    em = EntityManager
    bm = BlockManager
    acore = bm.Core(21, 56, 30948)
    aplan = em.Planet("test")
    space1 = bm.Space(3, 5, 2)
    dirt = bm.Dirt(5, 6, 8)
    print aplan
    print acore
    print space1
    print dirt

if __name__ == '__main__':
    main()

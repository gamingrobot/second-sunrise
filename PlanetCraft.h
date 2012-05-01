/*
-----------------------------------------------------------------------------
Filename:    PlanetCraft.h
-----------------------------------------------------------------------------
*/
#ifndef __PlanetCraft_h_
#define __PlanetCraft_h_

#include "BaseApplication.h"

typedef unsigned char block_t;

class PlanetCraft : public BaseApplication
{
public:
    PlanetCraft(void);
    virtual ~PlanetCraft(void);
    
    static const int WORLD_SIZE = 256;   // We'll change these later for various test worlds
    static const int CHUNK_SIZE = 8;
 
    int m_ChunkID;              // Used for uniquely naming our chunks
 
    block_t* m_Blocks;          // Holds the block worlds in a [WORLD_SIZE][WORLD_SIZE][WORLD_SIZE] array
 
    // Read/write access method for our block world (doesn't check input)
    block_t& GetBlock (const int x, const int y, const int z) 
    {
        return m_Blocks[x + y * WORLD_SIZE + z * WORLD_SIZE * WORLD_SIZE];
    }
 
    // Used for filling our block world
    void initWorldBlocksRandom (const int Divisor);
    void initWorldBlocksSphere (void);

    //chunking
    void createChunk (const int StartX, const int StartY, const int StartZ);
    void createWorldChunks (void);

    //texturing
    void createSolidTexture (const TCHAR* pName);
    void createTexture (const TCHAR* pName, const TCHAR* pImageFilename);

protected:
    virtual void createScene(void);
    Ogre::ManualObject* createCubeMesh (Ogre::String name, Ogre::String matName) ;
};

#endif // #ifndef __PlanetCraft_h_

/*
-----------------------------------------------------------------------------
Filename:    PlanetCraft.h
-----------------------------------------------------------------------------
*/
#ifndef __PlanetCraft_h_
#define __PlanetCraft_h_

#include "BaseApplication.h"

class PlanetCraft : public BaseApplication
{
public:
    PlanetCraft(void);
    virtual ~PlanetCraft(void);

protected:
    virtual void createScene(void);
};

#endif // #ifndef __PlanetCraft_h_

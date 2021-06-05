from fastapi import APIRouter, Depends

import core
from .user import users
from .project import projects
from .story import stories
from .push import pushes

v1 = APIRouter(prefix="/v1", dependencies=[Depends(core.get_current_user)])

v1.include_router(users)
v1.include_router(projects)
v1.include_router(stories)
v1.include_router(pushes)

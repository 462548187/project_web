from fastapi import APIRouter, Depends

import core
from .user import user_router
from .project import project_router
from .story import story_router
from .push import push_router

v1 = APIRouter(prefix="/v1", dependencies=[Depends(core.get_current_user)])

v1.include_router(user_router)
v1.include_router(project_router)
v1.include_router(story_router)
v1.include_router(push_router)

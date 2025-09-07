from fastapi import APIRouter
from src.models import Pokemon
from src.database.db import SessionType
from typing import List
from fastapi import HTTPException
from sqlmodel import select
from src.services import pokemon_service
from fastapi import Form

# router = APIRouter(prefix="/pokemon", tags=["pokemon"])


# @router.post("/create")
# def add_pokemon(pokemon_name: str, session: SessionType) -> Pokemon:
#     try:
#         p = Pokemon(name=pokemon_name)
#         return pokemon_service.add_pokemon(p, session)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))


# @router.post("/create_with_image/")
# async def create_pokemon_with_image(
#     session: SessionType,
#     name: str = Form(...),
#     description: str = Form(...),
#     physical_attr: str = Form(...),
#     ptype: str = Form(...),
# ):
#     try:
#         result = await pokemon_service.generate_pokemon_image(
#             name, description, physical_attr, ptype, session
#         )
#         return result
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise HTTPException(detail=str(e), status_code=500)


# @router.post("/store_pokemon_base_data")
# async def store_pokemon_base_data(
#     pokemon_id: int,
#     name: str,
#     description: str,
#     physical_attr: str,
#     ptype: str,
#     session: SessionType,
# ):
#     try:
#         result = await pokemon_service.store_pokemon_base_data(
#             pokemon_id, name, description, physical_attr, ptype, session=session
#         )
#         return result
#     except HTTPException as e:
#         raise e


# @router.get("/store_pokemon_base_data")
# async def get_pokemon_base_data(
#     pokemon_id: int,
#     session: SessionType,
# ):
#     try:
#         result = await pokemon_service.get_pokemon_base_data(
#             pokemon_id, session=session
#         )
#         return result
#     except HTTPException as e:
#         raise e


# @router.post("/add_image_dir/")
# async def add_pokemon_image_dir(pokemon_id: int, image_dir: str, session: SessionType):
#     try:
#         return pokemon_service.add_pokemon_image_directory(
#             pokemon_id, image_dir, session
#         )
#     except Exception as e:
#         raise e


# @router.get("/get_all_pokemon_images/")
# async def get_all_pokemon_images(
#     pokemon_id: int, option: ImageDir, session: SessionType
# ):
#     try:
#         return pokemon_service.get_all_pokemon_images(pokemon_id, option, session)
#     except HTTPException as e:
#         raise e
#     except Exception as e:
#         raise e


# @router.get("/{pokemon_id}")
# def get_pokemon(pokemon_id: int, session: SessionType) -> Pokemon:
#     pokemon = session.get(Pokemon, pokemon_id)
#     if not pokemon:
#         raise HTTPException(detail="Not Found", status_code=404)
#     return pokemon


# @router.post("/{pokemon_id}")
# def delete_pokemon(pokemon_id: int, session: SessionType):
#     try:
#         pokemon = get_pokemon(pokemon_id, session)
#     except HTTPException as e:
#         raise e
#     session.delete(pokemon)
#     session.commit()
#     return {"ok": True}


# @router.post("/")
# def list_pokemon(session: SessionType) -> List[Pokemon]:
#     return list(session.exec(select(Pokemon)).all())

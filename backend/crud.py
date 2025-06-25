from models import cats, missions, targets
from database import database

# --- Cats CRUD ---

async def create_cat(cat):
    query = cats.insert().values(
        name=cat.name,
        years_of_experience=cat.years_of_experience,
        breed=cat.breed,
        salary=cat.salary,
    )
    cat_id = await database.execute(query)
    return {**cat.dict(), "id": cat_id}

async def get_cat(cat_id: int):
    query = cats.select().where(cats.c.id == cat_id)
    return await database.fetch_one(query)

async def list_cats():
    query = cats.select()
    return await database.fetch_all(query)

async def update_cat(cat_id: int, salary: float):
    query = cats.update().where(cats.c.id == cat_id).values(salary=salary)
    await database.execute(query)
    return await get_cat(cat_id)

async def delete_cat(cat_id: int):
    query = cats.delete().where(cats.c.id == cat_id)
    return await database.execute(query)

# --- Missions / Targets CRUD ---

async def create_mission(mission):
    query = missions.insert().values(
        cat_id=mission.cat_id,
        completed=False
    )
    mission_id = await database.execute(query)
    # Inserir targets
    for t in mission.targets:
        query = targets.insert().values(
            mission_id=mission_id,
            name=t.name,
            country=t.country,
            notes=t.notes or "",
            completed=False
        )
        await database.execute(query)
    return await get_mission(mission_id)

async def get_mission(mission_id: int):
    query = missions.select().where(missions.c.id == mission_id)
    mission_record = await database.fetch_one(query)
    if not mission_record:
        return None
    # Buscar targets da missão
    query_targets = targets.select().where(targets.c.mission_id == mission_id)
    targets_records = await database.fetch_all(query_targets)
    return {
        **mission_record,
        "targets": targets_records
    }

async def list_missions():
    query = missions.select()
    mission_records = await database.fetch_all(query)
    result = []
    for m in mission_records:
        t = await database.fetch_all(targets.select().where(targets.c.mission_id == m["id"]))
        result.append({**m, "targets": t})
    return result

async def delete_mission(mission_id: int):
    mission = await get_mission(mission_id)
    if not mission:
        return None
    if mission["cat_id"] is not None:
        raise Exception("Mission assigned to a cat, cannot delete")
    await database.execute(targets.delete().where(targets.c.mission_id == mission_id))
    await database.execute(missions.delete().where(missions.c.id == mission_id))
    return True

async def update_target(mission_id: int, target_id: int, notes=None, completed=None):
    mission = await get_mission(mission_id)
    if not mission:
        return None
    if mission["completed"]:
        raise Exception("Mission is completed, cannot update target notes")
    target_record = await database.fetch_one(targets.select().where(targets.c.id == target_id).where(targets.c.mission_id == mission_id))
    if not target_record:
        return None
    if target_record["completed"]:
        if notes is not None:
            raise Exception("Target is completed, cannot update notes")
    values = {}
    if notes is not None:
        values["notes"] = notes
    if completed is not None:
        values["completed"] = completed
    if values:
        await database.execute(targets.update().where(targets.c.id == target_id).values(**values))
    # Atualizar status da missão se todos os targets estiverem completos
    targets_all = await database.fetch_all(targets.select().where(targets.c.mission_id == mission_id))
    if all(t["completed"] for t in targets_all):
        await database.execute(missions.update().where(missions.c.id == mission_id).values(completed=True))
    return await database.fetch_one(targets.select().where(targets.c.id == target_id))

async def assign_cat_to_mission(mission_id: int, cat_id: int):
    mission = await get_mission(mission_id)
    if not mission:
        return None
    if mission["cat_id"] is not None:
        raise Exception("Mission already assigned")
    # Verificar se cat existe e está disponível (não tem missão atribuída)
    query_cat = cats.select().where(cats.c.id == cat_id)
    cat = await database.fetch_one(query_cat)
    if not cat:
        raise Exception("Cat not found")
    # Verificar se cat está livre (não está atribuído a outra missão)
    query_mission_assigned = missions.select().where(missions.c.cat_id == cat_id)
    assigned = await database.fetch_one(query_mission_assigned)
    if assigned:
        raise Exception("Cat already assigned to a mission")
    # Atribuir cat à missão
    await database.execute(missions.update().where(missions.c.id == mission_id).values(cat_id=cat_id))
    return await get_mission(mission_id)

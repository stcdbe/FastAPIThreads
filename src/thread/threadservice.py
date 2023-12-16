from beanie import PydanticObjectId

from src.database.dbmodels import ThreadDB, UserDB
from src.thread.threadschemas import CommentCreate, CommentGet, ThreadCreate


async def get_thread_db(thread_id: PydanticObjectId) -> ThreadDB | None:
    return await ThreadDB.find_one(ThreadDB.id == thread_id, fetch_links=True)


async def get_some_threads_db(offset: int,
                              limit: int,
                              ordering: str,
                              reverse: bool) -> list[ThreadDB]:
    threads = await ThreadDB.find_all().skip(offset).limit(limit).sort(ordering).to_list()

    if reverse:
        threads = threads[::-1]

    return threads


async def create_thread_db(thread_data: ThreadCreate, creator: UserDB) -> ThreadDB | None:
    new_thread = ThreadDB(creator=creator, **thread_data.model_dump(mode='json'))
    return await ThreadDB.insert_one(new_thread)


async def create_com_db(thread: ThreadDB, com_data: CommentCreate) -> ThreadDB:
    if len(thread.comments) == 99:
        thread.is_active = False

    new_com = CommentGet(**com_data.model_dump(mode='json'))
    thread.comments.append(new_com)
    await thread.replace()
    return thread


async def del_thread_db(thread: ThreadDB) -> None:
    await thread.delete()

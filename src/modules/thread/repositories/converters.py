from typing import Mapping, Any

from src.modules.thread.models.entities import Thread, Comment


def convert_thread_doc_to_entity(data: Mapping[str, Any]) -> Thread:
    return Thread(guid=data['guid'],
                  title=data['title'],
                  text=data['text'],
                  created_at=data['created_at'],
                  is_active=data['is_active'])


def convert_comment_doc_to_entity(data: Mapping[str, Any]) -> Comment:
    return Comment(guid=data['guid'], text=data['text'], created_at=data['created_at'])


def convert_thread_doc_to_entity_with_coms(data: Mapping[str, Any]) -> Thread:
    comments = [convert_comment_doc_to_entity(doc) for doc in data['comments']]
    thread = convert_thread_doc_to_entity(data=data)
    thread.comments = comments
    return thread

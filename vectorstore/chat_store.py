import json
import os
import time
import uuid
from typing import Any, Dict, List, Optional

import chromadb

from config import get_config


# ---------------------- ChromaDB Client Initialization ----------------------

def _get_client() -> chromadb.PersistentClient:
    config = get_config()
    db_path = config.get("VECTOR_DIR", "./chroma_db")
    os.makedirs(db_path, exist_ok=True)
    return chromadb.PersistentClient(path=db_path)


# ---------------------- Collection Management ----------------------

def _get_collection():
    client = _get_client()
    return client.get_or_create_collection(
        name="chat_sessions",
        metadata={"kind": "chat_store"},
    )


# ---------------------- Session Serialization ----------------------

def _serialize_session(messages: List[Dict[str, Any]], extra: Optional[Dict[str, Any]] = None) -> str:
    def _make_serializable(obj):
        """Convert non-serializable objects to serializable ones"""
        if hasattr(obj, 'page_content') and hasattr(obj, 'metadata'):
            return {
                "page_content": obj.page_content,
                "metadata": obj.metadata
            }
        elif isinstance(obj, dict):
            return {k: _make_serializable(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [_make_serializable(item) for item in obj]
        else:
            return obj
    
    payload = {"messages": messages, "extra": extra or {}}
    serializable_payload = _make_serializable(payload)
    return json.dumps(serializable_payload, ensure_ascii=False)


# ---------------------- Session Deserialization ----------------------

def _deserialize_session(doc: str) -> Dict[str, Any]:
    try:
        return json.loads(doc)
    except Exception:
        return {"messages": [], "extra": {}}


# ---------------------- Session Listing ----------------------

def list_sessions() -> List[Dict[str, Any]]:
    col = _get_collection()
    results = col.get(include=["metadatas"], limit=1000)
    sessions: List[Dict[str, Any]] = []
    ids = results.get("ids", []) or []
    metadatas = results.get("metadatas", []) or []
    for sid, meta in zip(ids, metadatas):
        sessions.append(
            {
                "id": sid,
                "title": (meta or {}).get("title", "Untitled"),
                "created_at": (meta or {}).get("created_at", 0),
                "updated_at": (meta or {}).get("updated_at", 0),
            }
        )
    sessions.sort(key=lambda s: (s.get("updated_at", 0), s.get("created_at", 0)), reverse=True)
    return sessions


# ---------------------- Session Retrieval ----------------------

def get_session(session_id: str) -> Optional[Dict[str, Any]]:
    col = _get_collection()
    res = col.get(ids=[session_id], include=["documents", "metadatas"])
    ids = res.get("ids", []) or []
    if not ids:
        return None
    doc = (res.get("documents", [None]) or [None])[0]
    meta = (res.get("metadatas", [None]) or [None])[0] or {}
    data = _deserialize_session(doc or "{}")
    return {"id": session_id, "title": meta.get("title", "Untitled"), "created_at": meta.get("created_at"), "updated_at": meta.get("updated_at"), **data}


# ---------------------- Session Creation ----------------------

def create_session(title: str, user_prompt: str, result: Dict[str, Any]) -> str:
    col = _get_collection()
    session_id = str(uuid.uuid4())
    ts = int(time.time())
    messages = [
        {"role": "user", "content": user_prompt},
        {
            "role": "assistant",
            "content": (result.get("pitch") or ""),
        },
    ]
    doc = _serialize_session(messages, extra={"result": result})
    col.add(
        ids=[session_id],
        documents=[doc],
        metadatas=[{"title": title, "created_at": ts, "updated_at": ts}],
    )
    return session_id


# ---------------------- Session Update ----------------------

def update_session(session_id: str, user_prompt: Optional[str], result: Optional[Dict[str, Any]]):
    existing = get_session(session_id)
    if not existing:
        return
    messages: List[Dict[str, Any]] = existing.get("messages", [])
    if user_prompt is not None:
        messages.append({"role": "user", "content": user_prompt})
    if result is not None:
        messages.append({"role": "assistant", "content": (result.get("pitch") or "")})
    doc = _serialize_session(messages, extra={"result": result or existing.get("extra", {}).get("result", {})})
    ts = int(time.time())
    col = _get_collection()
    col.update(
        ids=[session_id],
        documents=[doc],
        metadatas=[{"title": existing.get("title", "Untitled"), "created_at": existing.get("created_at", ts), "updated_at": ts}],
    )



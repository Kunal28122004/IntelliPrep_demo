"""
Session service to maintain active test sessions.

- For simplicity sessions are kept in-memory as dictionary.
- Each session tracks username, attempted question ids, diagnostic progress.
- This design keeps separation of concerns (DB stores attempts; sessions store ephemeral state).
"""

import time
from typing import Dict, Any, Optional

# Simple in-memory store: session_id -> data
_sessions: Dict[int, Dict[str, Any]] = {}
_next_session_id = 1


class SessionService:
    @staticmethod
    def create_session(username: str) -> int:
        global _next_session_id
        sid = _next_session_id
        _next_session_id += 1
        _sessions[sid] = {
            "username": username,
            "attempted": [],
            "created_at": time.time(),
            "diagnostic_done": False,
        }
        return sid

    @staticmethod
    def get_session(session_id: int) -> Optional[Dict[str, Any]]:
        return _sessions.get(session_id)

    @staticmethod
    def add_attempt_to_session(session_id: int, question_id: int):
        s = _sessions.get(session_id)
        if not s:
            return
        if question_id not in s["attempted"]:
            s["attempted"].append(question_id)

    @staticmethod
    def mark_diagnostic_done(session_id: int):
        s = _sessions.get(session_id)
        if s:
            s["diagnostic_done"] = True

    @staticmethod
    def end_session(session_id: int) -> Dict[str, Any]:
        """
        Returns a small summary and removes session from memory.
        """
        s = _sessions.pop(session_id, None)
        if not s:
            return {}
        return {
            "username": s["username"],
            "attempted_count": len(s["attempted"]),
            "attempted": s["attempted"],
        }
import hashlib
import logging
from typing import Optional, Set
from collections import deque
from fastapi import Request, HTTPException

logger = logging.getLogger(__name__)

class WebhookHandler:
    def __init__(self, token: str, encoding_aes_key: str, app_id: str):
        self.token = token
        self.encoding_aes_key = encoding_aes_key
        self.app_id = app_id
        # AC-8/Memory: Idempotency control using a bounded cache for MsgId
        self._processed_msg_ids: Set[str] = set()
        self._msg_id_queue: deque[str] = deque(maxlen=1000)

    def verify_signature(self, msg_signature: str, timestamp: str, nonce: str, echostr: Optional[str] = None) -> bool:
        """
        Verify the signature from WeCom.
        In mock mode or if token is not set, we can skip this.
        """
        if not self.token:
            return True

        # Sort token, timestamp, nonce, echostr (if present)
        lst = sorted([self.token, timestamp, nonce] + ([echostr] if echostr else []))
        sha1 = hashlib.sha1()
        sha1.update("".join(lst).encode("utf-8"))
        hashcode = sha1.hexdigest()

        return hashcode == msg_signature

    def is_duplicate(self, msg_id: str) -> bool:
        if not msg_id:
            return False
        if msg_id in self._processed_msg_ids:
            return True

        # Add to cache
        if len(self._msg_id_queue) >= self._msg_id_queue.maxlen: # type: ignore
            oldest = self._msg_id_queue.popleft()
            self._processed_msg_ids.remove(oldest)

        self._processed_msg_ids.add(msg_id)
        self._msg_id_queue.append(msg_id)
        return False

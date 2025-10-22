from typing import Optional, Dict, Any
from Resource import Resource


class StagingEnv(Resource):
    def __init__(
        self,
        name: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        super().__init__(name=name, metadata=metadata)

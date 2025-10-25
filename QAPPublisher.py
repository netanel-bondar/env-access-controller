from typing import Optional, Dict, Any
from Resource import Resource


class QAPPublisher(Resource):
    def __init__(
        self,
        publisherId: str,
        name: str,
        metadata: Optional[Dict[str, Any]] = None
    ):
        super().__init__(name=name, metadata=metadata)
        self.id = publisherId

    def get_status(self) -> Dict[str, Any]:
        return super().get_status()

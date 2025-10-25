from typing import Dict, Optional, List
from QAPPublisher import QAPPublisher
from StagingEnv import StagingEnv
from persistence import ResourcePersistence

class ResourceRegistry:

    def __init__(self):
        self.publishers: Dict[str, QAPPublisher] = {}
        self.environments: Dict[str, StagingEnv] = {}
        self.persistence = ResourcePersistence()
        self._initialize_resources()
        self._load_state()

    def _initialize_resources(self):
        self._initialize_qa_publishers()
        self._initialize_staging_environments()

    def _initialize_qa_publishers(self):

        # QA Publisher 1: PaidPubs
        self.publishers["1469036"] = QAPPublisher(
            publisherId="1469036",
            name="PaidPubs",
            metadata={
                "domain": "pushpaidpubs.taboola.qa",
                "product": "web-push-qa",
                "transformer_url": "https://transformer.taboola.com/products?accountId=1469036",
                "type": "paidpubs"
            }
        )

        # QA Publisher 2: Newsroom
        self.publishers["1590830"] = QAPPublisher(
            publisherId="1590830",
            name="Newsroom",
            metadata={
                "domain": "pushnewsroom.taboola.qa",
                "product": "webpushqa-tropit",
                "transformer_url": "https://transformer.taboola.com/products?accountId=1590830",
                "type": "newsroom"
            }
        )

        # QA Publisher 3: SMB
        self.publishers["1689467"] = QAPPublisher(
            publisherId="1689467",
            name="SMB",
            metadata={
                "domain": "pushsmb.taboola.qa",
                "product": "web-push-qa-smb",
                "transformer_url": "https://transformer.taboola.com/products?accountId=1689467",
                "type": "smb"
            }
        )

        # QA Publisher 4: Android
        self.publishers["1704250"] = QAPPublisher(
            publisherId="1704250",
            name="Android",
            metadata={
                "platform": "android",
                "package_name": "com.newsplace.app.qa"
            }
        )

        # QA Publisher 5: iOS
        self.publishers["1791194"] = QAPPublisher(
            publisherId="1791194",
            name="iOS",
            metadata={
                "platform": "ios",
                "bundle_id": "com.taboola.pushAppQA"
            }
        )

    def _initialize_staging_environments(self):
        """Initialize staging environments."""

        # Prime
        self.environments["prime-staging"] = StagingEnv(
            name="Prime",
            metadata={}
        )

        # Epsilon
        self.environments["epsilon-staging"] = StagingEnv(
            name="Epsilon",
            metadata={}
        )

        # Tropit
        self.environments["tropit-staging"] = StagingEnv(
            name="Tropit",
            metadata={}
        )

        # Transformer
        self.environments["transformer-staging"] = StagingEnv(
            name="Transformer",
            metadata={}
        )

        # Jade Pubs 1
        self.environments["jade-pubs-1-staging"] = StagingEnv(
            name="Jade Pubs 1",
            metadata={
                "instance": "1"
            }
        )

        # Jade Pubs 2
        self.environments["jade-pubs-2-staging"] = StagingEnv(
            name="Jade Pubs 2",
            metadata={
                "instance": "2"
            }
        )

    def get_publisher(self, publisher_id: str) -> Optional[QAPPublisher]:
        """Get a publisher by ID."""
        return self.publishers.get(publisher_id)

    def get_all_publishers(self) -> Dict[str, QAPPublisher]:
        """Get all publishers."""
        return self.publishers

    def get_publishers_by_type(self, publisher_type: str) -> List[QAPPublisher]:
        """Get all publishers of a specific type (paidpubs, newsroom, smb, android, ios)."""
        return [
            pub for pub in self.publishers.values()
            if pub.metadata.get("type") == publisher_type or
               pub.metadata.get("platform") == publisher_type
        ]

    def get_qa_publishers(self) -> List[QAPPublisher]:
        """Get all QA publishers."""
        return list(self.publishers.values())

    # Environment access methods
    def get_environment(self, env_id: str) -> Optional[StagingEnv]:
        """Get an environment by ID."""
        return self.environments.get(env_id)

    def get_all_environments(self) -> Dict[str, StagingEnv]:
        """Get all environments."""
        return self.environments

    # Status and info methods
    def get_available_publishers(self) -> List[QAPPublisher]:
        return [pub for pub in self.publishers.values() if pub.taken_by is None]

    def get_available_environments(self) -> List[StagingEnv]:
        return [env for env in self.environments.values() if env.taken_by is None]

    def get_all_status(self) -> dict:
        return {
            "publishers": {
                pub_id: pub.get_status()
                for pub_id, pub in self.publishers.items()
            },
            "environments": {
                env_id: env.get_status()
                for env_id, env in self.environments.items()
            }
        }

    # Persistence methods
    def _load_state(self) -> None:
        """Load the persisted state on startup."""
        if self.persistence.load_state(self):
            print("Successfully loaded resource state from disk")
        else:
            print("No previous state found, starting fresh")

    def save_state(self) -> None:
        """Save the current state to disk."""
        self.persistence.save_state(self)


# Global singleton instance
resources = ResourceRegistry()


# Convenience exports
def get_publisher(publisher_id: str) -> Optional[QAPPublisher]:
    return resources.get_publisher(publisher_id)


def get_environment(env_id: str) -> Optional[StagingEnv]:
    return resources.get_environment(env_id)


def get_all_publishers() -> Dict[str, QAPPublisher]:
    return resources.get_all_publishers()


def get_all_environments() -> Dict[str, StagingEnv]:
    return resources.get_all_environments()

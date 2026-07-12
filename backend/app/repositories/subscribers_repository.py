from app.repositories.base import SupabaseRepository


class SubscribersRepository(SupabaseRepository):
    def __init__(self) -> None:
        super().__init__("subscribers")

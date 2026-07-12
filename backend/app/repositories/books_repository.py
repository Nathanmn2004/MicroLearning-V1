from app.repositories.base import SupabaseRepository


class BooksRepository(SupabaseRepository):
    def __init__(self) -> None:
        super().__init__("books")

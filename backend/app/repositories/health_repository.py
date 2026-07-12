from app.repositories.supabase_client import get_supabase_admin_client


class SupabaseHealthRepository:
    def check_connection(self) -> bool:
        client = get_supabase_admin_client()
        client.table("books").select("id").limit(1).execute()
        return True

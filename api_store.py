from supabase_client import supabase

def save_user_keys(user_id, openai_key, deepseek_key):
    existing = supabase.table("user_api_tokens").select("*").eq("user_id", user_id).execute()
    if not existing.data:
        supabase.table("user_api_tokens").insert({
            "user_id": user_id,
            "openai_api_key": openai_key,
            "deepseek_api_key": deepseek_key
        }).execute()

def get_user_keys(user_id):
    result = supabase.table("user_api_tokens").select("*").eq("user_id", user_id).execute()
    return result.data[0] if result.data else None

def get_free_usage(user_id):
    result = supabase.table("user_usage").select("*").eq("user_id", user_id).execute()
    return result.data[0]["free_uses"] if result.data else 0

def increment_free_usage(user_id):
    usage = supabase.table("user_usage").select("*").eq("user_id", user_id).execute()
    if not usage.data:
        supabase.table("user_usage").insert({"user_id": user_id, "free_uses": 1}).execute()
    else:
        count = usage.data[0]["free_uses"] + 1
        supabase.table("user_usage").update({"free_uses": count}).eq("user_id", user_id).execute()
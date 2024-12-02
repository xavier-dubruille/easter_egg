import os
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from supabase import create_client, Client

_supabase = None


@dataclass
class EggCode:
    code: str = ""
    name: str = ""
    noma: str = ""


class EGG_STATUS(Enum):
    ALREADY_FOUND = "ALREADY_FOUND"
    SUCCESS = "SUCCESS"
    NOT_FOUND = "NOT_FOUND"


def get_supa_client():
    # global _supabase  # todo do not create _supabase each time
    # _supabase = None
    #
    # if _supabase is not None:
    #     return _supabase

    url = os.getenv("API_URL")
    key = os.getenv("API_KEY")

    _supabase: Client = create_client(url, key)
    return _supabase


def get_eggs():
    supabase_client: Client = get_supa_client()

    response = supabase_client.table("eggs").select("*").execute()
    return sorted(response.data, key=lambda x: x['id']) if response else None


def get_num_of_not_yet_discovered_eggs():
    return sum(1 for d in get_eggs() if d.get("decouvert_par") in (None, ""))


def get_code_status(code: str):
    egg = next((d for d in get_eggs() if d.get("code") == code), None)
    if egg is None:
        return EGG_STATUS.NOT_FOUND, ""
    if egg['decouvert_par'] is None or egg['decouvert_par'] == "":
        return EGG_STATUS.SUCCESS, ""
    return EGG_STATUS.ALREADY_FOUND, egg['decouvert_par']


def found_egg(egg: EggCode):
    print(f'found: {egg}')
    supabase_client: Client = get_supa_client()
    try:
        # Date actuelle
        now = datetime.now().isoformat()  # Format ISO 8601 pour PostgreSQL

        response = supabase_client.table("eggs").update({
            "decouvert_par": egg.name,
            "decouvert_le": now,
            "noma": egg.noma,
        }).eq("code", egg.code).execute()

        return response.data[0]

    except Exception as e:
        print(f"Erreur lors de la mise à jour : {e}")

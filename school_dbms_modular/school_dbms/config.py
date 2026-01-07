import os
from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class DBConfig:
    host: str
    user: str
    password: str
    database: str

def _load_dotenv(path: Path) -> None:
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        k, v = k.strip(), v.strip()
        os.environ.setdefault(k, v)

def load_config() -> DBConfig:
    # Load .env from project root if present
    _load_dotenv(Path(__file__).resolve().parent.parent / ".env")
    host = os.getenv("DB_HOST", "localhost")
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASS", "")
    database = os.getenv("DB_NAME", "ishaanray_12a1")
    if password == "":
        print("⚠️  Warning: DB_PASS is empty. Set it in your .env for local MySQL.")
    return DBConfig(host=host, user=user, password=password, database=database)

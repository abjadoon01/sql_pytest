from pathlib import Path

current_file = Path(__file__).resolve()
current_folder = current_file.parent
db_path = current_folder / "data" / "orders" 
db_path.mkdir(parents=True, exist_ok=True)
orders_db = db_path / "order.db"
backup_db = db_path / "backup.db"
orders_db.touch()
backup_db.touch()
data_path = current_folder / "data"

for file in db_path.iterdir():
    print(file)
for file in db_path.glob("*.db"):
    print(file)
for file in data_path.rglob("*.db"):
    print(file)

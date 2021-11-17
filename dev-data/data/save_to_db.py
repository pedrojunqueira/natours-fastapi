from models.tour_model import Tours
from models.database import engine as db
import json

with open("tours-simple.json", "r") as fp:
    trs = json.load(fp)

tours = [{ k:v for k, v in d.items() if k != "id"} for d in trs]
await db.save_all([Tours(**t) for t in tours])
        

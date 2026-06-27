import json
import asyncio
from src.db.session import async_session_factory
from src.db.models import CustomerModel, MaterialModel
from sqlalchemy import select

async def seed_master_data(json_path: str):
    """Seed the database with mock master data."""
    with open(json_path, 'r') as f:
        data = json.load(f)

    async with async_session_factory() as session:
        # Seed Customers
        for c in data.get("customers", []):
            result = await session.execute(select(CustomerModel).where(CustomerModel.id == c["id"]))
            if not result.scalar_one_or_none():
                customer = CustomerModel(
                    id=c["id"],
                    name=c["name"],
                    code=c.get("code"),
                    contact=c.get("contact"),
                    email=c.get("email")
                )
                session.add(customer)

        # Seed Materials
        for m in data.get("materials", []):
            result = await session.execute(select(MaterialModel).where(MaterialModel.id == m["id"]))
            if not result.scalar_one_or_none():
                material = MaterialModel(
                    id=m["id"],
                    name=m["name"],
                    code=m.get("code"),
                    specification=m.get("specification"),
                    unit=m.get("unit"),
                    unit_price=m["unit_price"]
                )
                session.add(material)

        await session.commit()
        print("Master data seeded successfully.")

if __name__ == "__main__":
    import os
    fixture_path = os.path.join(os.path.dirname(__file__), "../../tests/fixtures/mock_master_data.json")
    asyncio.run(seed_master_data(fixture_path))

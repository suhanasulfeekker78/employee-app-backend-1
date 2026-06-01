import pytest
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.pool import StaticPool

from database import Base
from employees import service as employee_service
from auth.utils import hash_password


@pytest.mark.asyncio
async def test_create_employee_persists_the_record():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=True,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    session_factory = async_sessionmaker(bind=engine, class_=AsyncSession)

    async with session_factory() as db:
        hashed_password = hash_password("secret123")
        employee = await employee_service.create(
            db,
            name="Ada",
            email="ada@example.com",
            age=None,
            password_hash=hashed_password,
            address_data=None,
        )
        # employee = await db.run_sync(
        #     lambda sync_session: employee_service.create(sync_session, name="Ada",email="ada@example.com", age=None ,password_hash=hashed_password, address_data=None)
        # )

        assert employee.id is not None
        assert employee.name == "Ada"
        assert employee.email == "ada@example.com"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()

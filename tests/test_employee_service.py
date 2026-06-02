from auth.utils import hash_password

from employees import service as employee_service
from models.employee import Employee


async def test_get_by_id_returns_seeded_employee(db_session):

    # Seed a row directly via the ORM. We construct Employee ourselves
    # (with a real `password_hash`) because service.create currently
    # drops the password field — bypassing it keeps this test focused.
    seeded = Employee(
        name="Ada", email="ada@example.com", password_hash=hash_password("secret123")
    )
    # `add()` is sync — it just stages the row in the session.
    db_session.add(seeded)

    await db_session.commit()

    await db_session.refresh(seeded)

    fetched = await employee_service.employee_by_id(db_session, seeded.id)

    assert fetched.id == seeded.id
    assert fetched.email == "ada@example.com"

"""ORM Entity Mapping"""


from models.employee import Employee
from models.entity import Entity, datetime_to_iso

__all__ = ["Employee", "Entity", "datetime_to_iso"]
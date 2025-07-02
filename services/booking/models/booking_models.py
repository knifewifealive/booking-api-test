from datetime import datetime as dt
from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator, model_validator
from typing import Optional


class BookingSchema(BaseModel):
    firstname: str
    lastname: str
    totalprice: int | float = Field(ge=0)
    depositpaid: bool
    checkin: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$')
    checkout: str = Field(pattern=r'^\d{4}-\d{2}-\d{2}$')
    checkout: str
    additionalneeds: Optional[str] = Field(default=None,max_length=200)

    model_config = ConfigDict(str_max_length=20)

    @classmethod
    @field_validator('checkin', 'checkout')
    def validate_date(cls, value: str) -> str:
        try:
            dt.strptime(value, '%Y-%m-%d')
        except ValidationError as Err:
            raise Err
        return value

    @model_validator(mode='after')
    def validate_checkin_before_checkout(self) -> 'BookingSchema':
        checkin = dt.strptime(self.checkin, '%Y-%m-%d')
        checkout = dt.strptime(self.checkout, '%Y-%m-%d')
        if checkin > checkout:
            raise ValidationError
        return self

    @model_validator(mode='after')
    def validate_checkin(self) -> 'BookingSchema':
        checkin = dt.strptime(self.checkin, '%Y-%m-%d')
        checkout = dt.strptime(self.checkout, '%Y-%m-%d')
        if (checkin < dt.today()) and (checkout < dt.today()):
            raise ValidationError
        return self


booking = BookingSchema(
    firstname='Mark',
    lastname='Bybin',
    totalprice=4,
    depositpaid=True,
    checkin='2025-07-03',
    checkout='2025-07-10',
    additionalneeds='Something cool Something cool Something cool Something cool Something cool'
)

booking1 = BookingSchema(
    firstname='Mark',
    lastname='Bybin',
    totalprice=4,
    depositpaid=True,
    checkin='2024-07-03',
    checkout='2025-07-10'
)

try:
    print(repr(booking))
    print(repr(booking1))
except ValidationError as e:
    print(e)

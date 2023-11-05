import sqlalchemy
from sqlalchemy import and_

from src.db import database
from src.schemas import records_table


async def passport_check(input_series: int, input_number: int):
    series = records_table.c.PASSP_SERIES
    number = records_table.c.PASSP_NUMBER
    query = sqlalchemy.select([records_table]).where(and_(
        input_series == series,
        input_number == number))
    select_res = database.execute(query)
    if select_res.fetchall():
        return True
    else:
        return False

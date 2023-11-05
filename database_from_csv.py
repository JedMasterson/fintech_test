import asyncio
import csv
import sqlalchemy
from pathlib import Path


async def write_record(connection, row):
    series = row[0]
    number = row[1]
    connection.execute(
        sqlalchemy.text("INSERT INTO list_of_expired_passports (PASSP_SERIES, PASSP_NUMBER) VALUES (:ser, :num)"),
        {"ser": series, "num": number})


async def database_from_csv(csvpath: str, dbpath: str):
    Path(dbpath).touch()


    engine = sqlalchemy.create_engine(f"sqlite:///{dbpath}")
    engine.execution_options(isolation_level="AUTOCOMMIT")
    connection = engine.connect()

    if not engine.dialect.has_table(connection, "list_of_expired_passports"):
        connection.execute(sqlalchemy.text("CREATE TABLE list_of_expired_passports (PASSP_SERIES, PASSP_NUMBER)"))
    with open(csvpath, newline='\n') as record:
        reader = csv.reader(record)
        headers = next(reader)
        records = []
        for row in reader:
            records.append(asyncio.create_task(write_record(connection, row)))
        await asyncio.gather(records)
        connection.commit()


if __name__ == "__main__":
    asyncio.run(database_from_csv("/home/jedmasterson/Desktop/list_of_expired_passports.csv",
                                  "/home/jedmasterson/Documents/Projects/fintech_test/database"))

import sqlalchemy

metadata = sqlalchemy.MetaData()

records_table = sqlalchemy.Table(
    'list_of_expired_passports',
    metadata,
    sqlalchemy.Column('PASSP_NUMBER', sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column('PASSP_SERIES', sqlalchemy.Integer),
)

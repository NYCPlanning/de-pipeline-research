import sqlalchemy as db
import os
from datetime import datetime

from operator import itemgetter


class PostgisLoader():
    def __init__(self, src_engine_url, dst_engine_url):
        self.src_engine = db.create_engine(src_engine_url)
        self.dst_engine = db.create_engine(dst_engine_url)

    def get_latest_table(self, schema_name):
        src_connection = self.src_engine.connect()
        query = f'select table_name from information_schema.tables as t where t.table_schema=\'{schema_name}\''
        result = src_connection.execute(query)

        date_times = [(datetime.strptime(date[0], '_%m_%d_%Y'), date[0])
                      for date in result]
        return max(date_times, key=itemgetter(0))[1]

    def dump_to_dst(self, schema_name, date='latest'):
        """Fetches the latest table given a schema_name and dumps it into an [engine] """
        query = 'create schema if not exists {};'.format(schema_name)
        dst_connection = self.dst_engine.connect()
        dst_connection.execute(query)

        if date == 'latest':
            table_name = self.get_latest_table(schema_name)

        query = f'DROP TABLE IF EXISTS {table_name}'
        dst_connection.execute(query)

        os.system(
            'docker exec db pg_dump -t parks_properties._08_07_2019 --no-owner -d $DB_SRC | psql $DB_DEST')

        query = f'DROP TABLE IF EXISTS {schema_name}'
        dst_connection.execute(query)

        query = f'create table {schema_name} as table {schema_name}.{table_name};'
        dst_connection.execute(query)

        query = f'DROP SCHEMA IF EXISTS {schema_name} CASCADE'
        dst_connection.execute(query)

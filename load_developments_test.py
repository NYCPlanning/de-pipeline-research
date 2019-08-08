from archive_dumper import ArchiveDumper
from postgres_loader import PostgresDumper

import os


def main():
    src_engine = os.environ['SRC_DB']
    dst_engine = os.environ['DST_DB']

    loader = PostgresDumper(src_engine, dst_engine)

    schema_name = 'parks_properties'
    loader.dump_to_dst(schema_name)


if __name__ == '__main__':
    main()

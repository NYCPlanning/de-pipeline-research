from postgis_dumper import PostgisDumper
from postgis_loader import PostgisLoader


def main():

    src_engine = 'postgresql://Ben:g650u8hn2d32agd7@edm-data-do-user-1939427-0.db.ondigitalocean.com:25060/recipe'
    dst_engine = 'postgresql://postgres@localhost:5433/postgres'

    loader = PostgisLoader(src_engine, dst_engine)

    schema_name = 'parks_properties'
    loader.dump_to_dst(schema_name)


if __name__ == '__main__':
    main()

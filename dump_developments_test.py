from archive_dumper import ArchiveDumper
import os

def main():

    engine = os.environ['SRC_DB']

    ad = ArchiveDumper(engine=engine)

    datasets = [{'schema_name': 'parks_properties',
                 'path': 'https://data.cityofnewyork.us/api/geospatial/k2ya-ucmv?method=export&format=GeoJSON'}]

    for dataset in datasets:
        print("Loading {} from {}".format(
            dataset['schema_name'], dataset['path']))
        ad.dump_to_archive(dataset['schema_name'], dataset['path'])


if __name__ == '__main__':
    main()

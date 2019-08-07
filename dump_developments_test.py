from postgis_dumper import PostgisDumper


def main():

    engine = 'postgresql://Ben:g650u8hn2d32agd7@edm-data-do-user-1939427-0.db.ondigitalocean.com:25060/recipe'

    pd = PostgisDumper(engine=engine)

    datasets = [{'schema_name': 'parks_properties',
                 'path': 'https://data.cityofnewyork.us/api/geospatial/k2ya-ucmv?method=export&format=GeoJSON'}]

    for dataset in datasets:
        print("Loading {} from {}".format(
            dataset['schema_name'], dataset['path']))
        pd.dump(dataset['schema_name'], dataset['path'])


if __name__ == '__main__':
    main()

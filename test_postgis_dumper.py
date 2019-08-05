from postgis_dumper import PostgisDumper
from datetime import datetime

import pandas as pd

import sqlalchemy as db

import unittest


class TestPostgisDumper(unittest.TestCase):
    def succesful_file_type_test(self, schema_name, url, true_column_names, true_num_entries):
        # TODO: delete table in db, then check if it exists in the table
        try:
            engine = 'postgresql://postgres@localhost:5433/postgres'
            postgis_dumper = PostgisDumper(engine=engine)
            postgis_dumper.dump(db_table_name=schema_name, path=url)
        except:
            self.fail("Failed to load: {}".format(url))

        # Get table_name from engine and check dim on table
        sql_engine = db.create_engine(engine)
        date_name = datetime.now().strftime("_%m_%d_%Y")
        
        # Compare Column names.  GDAL adds ogc_fid and wkb_geometry fields
        column_query = 'SELECT column_name FROM information_schema.columns WHERE table_schema = \'{}\' AND table_name = \'{}\';'.format(
            schema_name, date_name)
            
        true_column_names = list(map(lambda x : x.lower(), true_column_names))
        
        test_column_names = pd.read_sql_query(column_query, sql_engine)[
            'column_name'].values
        
        for col_a, col_b in zip(test_column_names, true_column_names):
            self.assertEqual(col_a, col_b)

        # Compare number of entries
        num_entries_query = 'select count(*) from {}.{}'.format(
            schema_name, date_name)
        test_num_entries = pd.read_sql_query(num_entries_query, sql_engine)[
            'count'].values[0]

        self.assertEqual(test_num_entries, true_num_entries)

    def failed_file_type_test(self, table_name, url):
        engine = 'postgresql://postgres@localhost:5433/postgres'
        postgis_dumper = PostgisDumper(engine=engine)

        with self.assertRaises(Exception):
            postgis_dumper.dump(db_table_name=table_name, path=url)

    def test_succesful_zip_1(self):
        url = 'https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyct2010_19b.zip/nyct2010_19b/nyct2010.shp'
        table_name = 'census_tracts'
        column_names = ['ogc_fid', 'ctlabel', 'borocode', 'boroname', 'ct2010', 'boroct2010', 'cdeligibil', 'ntacode', 'ntaname', 'puma', 'shape_leng', 'shape_area', 'wkb_geometry']
        num_entries = 2166
        self.succesful_file_type_test(table_name, url, column_names, num_entries)

    def test_succesful_zip_2(self):
        url = 'https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nysd_19b.zip/nysd_19b/nysd.shp'
        table_name = 'dcp_school_districts'
        column_names = ['ogc_fid', 'schooldist',
                        'shape_leng', 'shape_area', 'wkb_geometry']
        num_entries = 33
        self.succesful_file_type_test(
            table_name, url, column_names, num_entries)

    def test_failed_zip(self):
        url = 'http://publicfiles.dep.state.fl.us/dear/BWR_GIS/2007NWFLULC/NWFWMD2007LULC.zip'
        table_name = 'dep_state'
        self.failed_file_type_test(table_name, url)
    
    def test_succesful_csv(self):
        url = 'https://raw.githubusercontent.com/NYCPlanning/db-data-recipes/master/recipes/dcp_pops/dcp_pops.csv'
        table_name = 'dcp_pops'
        column_names = ['ogc_fid', 'POPS_Number','Borough_Name','Borough_Code','Community_District','Address_Number','Street_Name','Zip_Code','Building_Address_With_Zip_Code','Tax_Block','Tax_Lot','Building_Name','Building_Location','Year_Completed','Stories','Alternate_Stories','New_Building_Number','Building_Constructed','Primary_Building_Use','Additional_Addresses','Public_Space_Location','Public_Space_Type','Arcade','Covered_Pedestrian_Space','Elevated_Plaza','Open_Air_Concourse','Pedestrian_Circulation_Space','Plaza','Public_Plaza','Residential_Plaza','Sidewalk_Widening','Through_Block_Arcade','Through_Block_Connection','Through_Block_Galleria','Urban_Plaza','Other_Public_Spaces','Other_Public_Spaces_List','Developer','Building_Architect','Principal_Public_Space_Designer','Size_Required','Hour_Of_Access_Required_List','Hour_Of_Access_Required','Open_24_Hours','Restricted_Hours','Closing_for_Events','Amenities_Required_List','Amenities_Required','None','Artwork','Bicycle_Parking','Climate_Control','Drinking_Fountain','Elevator','Escalator','Food_Service','Lighting','Litter_Receptacles','Planting','Plaque_Sign','Programs','Restrooms','Retail_Frontage','Seating','Subway','Tables','Trees_on_Street','Trees_within_Space','Water_Feature','Other_Required','Permitted_Amenities_List','Permitted_Amenities','Open_Air_Cafe','Other_Permitted','Physically_Disabled','Latitude','Longitude','XCoordinate','YCoordinate', 'wkb_geometry']
        num_entries = 355
        
        self.succesful_file_type_test(table_name, url, column_names, num_entries)


if __name__ == '__main__':
    unittest.main()
    # main()

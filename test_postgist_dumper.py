from postgis_dumper import PostgisDumper

import unittest

class TestPostgisDumper(unittest.TestCase):
    def succesful_file_type_test(self, table_name, url):
        # TODO: delete table in db, then check if it exists in the table
        try:
            engine = 'postgresql://postgres@localhost:5433/postgres'
            pd = PostgisDumper(engine=engine)
            pd.dump(db_table_name=table_name, path=url)
        except:
                self.fail("Failed to load: {}".format(url))
    
    def failed_file_type_test(self, table_name, url):
        engine = 'postgresql://postgres@localhost:5433/postgres'
        pd = PostgisDumper(engine=engine)
        
        with self.assertRaises(Exception):
            pd.dump(db_table_name=table_name, path=url)
    
    def test_succesful_zip_1(self):
        url = 'https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nyct2010wi_19b.zip/nyct2010wi_19b/nyct2010wi.shp'
        table_name = 'census_tracts'
        self.succesful_file_type_test(table_name, url)
        
    def test_succesful_zip_2(self):
        url = 'https://www1.nyc.gov/assets/planning/download/zip/data-maps/open-data/nysd_19b.zip/nysd_19b/nysd.shp'
        table_name = 'dcp_school_districts'
        self.succesful_file_type_test(table_name, url)
            
    def test_failed_zip(self):
        url = 'http://publicfiles.dep.state.fl.us/dear/BWR_GIS/2007NWFLULC/NWFWMD2007LULC.zip'
        table_name = 'dep_state'
        self.failed_file_type_test(table_name, url)

    def test_succesful_csv(self):
        url = 'https://raw.githubusercontent.com/NYCPlanning/db-data-recipes/master/recipes/dcp_pops/dcp_pops.csv'
        table_name = 'dcp_pops'
        self.succesful_file_type_test(table_name, url)   
    
        
        
    

if __name__ == '__main__':
    unittest.main()
    # main()
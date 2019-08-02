import os
import logging
from osgeo import ogr
from osgeo import gdal
from pathlib import Path
import tempfile
from urllib.parse import urlparse

from osgeo.gdalconst import GA_ReadOnly

from datetime import datetime

from osgeo import ogr

class PostgisDumper():
    def __init__(self,
                 srcSRS='EPSG:4326', 
                 dstSRS='EPSG:4326',
                 engine='env://DATAFLOWS_DB_ENGINE'):

        if engine.startswith('env://'):
            env_var = engine[6:]
            engine = os.environ.get(env_var)
            if engine is None:
                raise ValueError("Couldn't connect to DB - "
                                 "Please set your '%s' environment variable" % env_var)

        self.engine = self.parse_engine(engine)
        self.srcSRS = srcSRS
        self.dstSRS = dstSRS
    
    def parse_engine(self, engine):
        result = urlparse(engine)
        username = result.username
        password = result.password
        database = result.path[1:]
        hostname = result.hostname
        portnum = result.port
        
        return f'PG:host={hostname} port={portnum} user={username} dbname={database} password={password}'
    
    @staticmethod
    def format_path(path):
        """ Adds vsizip to [path] if [path] is a ShapeFile."""
        filename, extension = os.path.splitext(os.path.basename(path))
        
        if extension == '.shp' or extension == '.zip':
            # TODO: Assuming its a shapefile we want on the inside
            path = "/vsizip/vsicurl/" + path
        return path
        
    def get_allowed_drivers(path):
        """ Returns allowed drivers for OpenEx given the file type of [path]"""
        allowed_drivers = [gdal.GetDriver(i).GetDescription() for i in range(gdal.GetDriverCount())]
        
        filename, extension = os.path.splitext(os.path.basename(path))
        
        # GDAL thinks .csv files should be parsed using the GeoJSONSeq Driver and throws parsing errors when it tries the other JSON Drivers
        if extension == '.csv':
            allowed_drivers = [driver for driver in allowed_drivers if "JSON" not in driver]
        # allowed_drivers.remove('GeoJSONSeq')
        return allowed_drivers
        
    
    @staticmethod
    def load_srcDS(path):
        path = PostgisDumper.format_path(path)
        print(path)
        
        allowed_drivers = PostgisDumper.get_allowed_drivers(path)

        # srcDS = gdal.OpenEx(path, gdal.OF_VECTOR, open_options=['CPL_VSIL_CURL_ALLOWED_EXTENSIONS=.csv','AUTODETECT_TYPE=NO', 'EMPTY_STRING_AS_NULL=YES', 'GEOM_POSSIBLE_NAMES=the_geom'])
        srcDS = gdal.OpenEx(path, gdal.OF_VECTOR, allowed_drivers=allowed_drivers)
        
        # OpenEx returns None if the file can't be opened
        if (srcDS is None):
            raise Exception('Could not open {}'.format(path)) 
        
        return srcDS
        
    
    def dump(self, db_table_name, path):
        
        dstDS = gdal.OpenEx(self.engine, gdal.OF_VECTOR)
        if (dstDS is None):
            raise Exception('Could not connect to postgres db.')
        
        srcDS = PostgisDumper.load_srcDS(path)
            
        print("GDAL used the {} driver.\n".format(srcDS.GetDriver().ShortName))
            
        dstDS.ExecuteSQL('create schema if not exists {};'.format(db_table_name))
        
        layerName = "{}.{}".format(db_table_name, datetime.now().strftime("_%m_%d_%Y"))
        print(layerName)

        gdal.VectorTranslate(
            dstDS,
            srcDS,
            layerCreationOptions = ['precision=NO'],
            format='PostgreSQL',
            dstSRS=self.dstSRS,
            srcSRS=self.srcSRS,
            geometryType='MULTIPOLYGON',
            layerName=layerName,
            accessMode='overwrite')
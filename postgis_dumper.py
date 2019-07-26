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
        filename, extension = os.path.splitext(os.path.basename(path))
        
        if extension == '.shp':
            # TODO: Assuming its a shapefile we want on the inside
            path = "/vsizip/vsicurl/" + path
        return path
        
    
    def dump(self, db_table_name, path):
        path = PostgisDumper.format_path(path)
        print(path)
        
        dstDS = gdal.OpenEx(self.engine, gdal.OF_VECTOR)
        if (dstDS is None):
            raise Exception('Could not connect to postgres db.')
        
        # srcDS = gdal.OpenEx(path, gdal.OF_VECTOR, open_options=['CPL_VSIL_CURL_ALLOWED_EXTENSIONS=.csv','AUTODETECT_TYPE=NO', 'EMPTY_STRING_AS_NULL=YES', 'GEOM_POSSIBLE_NAMES=the_geom'])
        
        allowed_drivers = [gdal.GetDriver(i).GetDescription() for i in range(gdal.GetDriverCount())]
        allowed_drivers.remove('GeoJSONSeq')
            
        srcDS = gdal.OpenEx(path, gdal.OF_VECTOR, allowed_drivers=allowed_drivers)
    
        if (srcDS is None):
            raise Exception('Could not open {}'.format(path)) 
            
        print("GDAL used the {} driver.".format(srcDS.GetDriver().ShortName))
            
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
# de-pipeline-research
Research on how to improve our data loading pipelines using GDAL.
# Installation
Pull the repository. 

`git pull git@github.com:NYCPlanning/de-pipeline-research.git`

Move into the repository's directory. 

`cd de-pipeline-research`

Pull the GDAL docker image.

`docker pull osgeo/gdal:ubuntu-small-latest`

Create the docker container. Remember to set the environment variables!

```docker run -itd --network=host -v `pwd`:/home/de_pipelines/ -w /home/de_pipelines/ -e SRC_DB={archive_connection_string} -e DST_DB={dst_connection_string} --name=de_pipelines osgeo/gdal:ubuntu-small-latest bash```

`docker start de_pipelines`

`docker exec -it de_pipelines bash`

Once the container's bash is running, run `sh docker_init.sh` to install the dependencies.

# Usage
Small test by loading `parks_properties` into the archive with `python3 dump_developments_test.py` and then loading `parks_properties` from archive to the data product postgres with `python3 load_developments_test.py`.



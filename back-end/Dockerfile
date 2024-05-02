FROM continuumio/miniconda3

# FROM continuumio/anaconda-pkg-build:2023.03.28-amd64
 
# RUN conda update conda

RUN apt-get update && apt-get install build-essential -y

RUN conda install python=3.10

# RUN conda install -c conda-forge gdal
 
# RUN conda install -c conda-forge gcc

# RUN conda install -c conda-forge pcraster
 
# RUN conda install future

# RUN conda install netcdf4

# RUN conda install matplotlib
# 
# RUN conda install refet

# RUN conda install requests

# RUN conda install scipy

# RUN conda install requests-html

WORKDIR /app
 
COPY ./requirements.txt .

# RUN pip install -r requirements.txt

# RUN pip install openpyxl

# RUN pip install drigo --no-deps

# RUN conda install gcc_linux-64 gxx_linux-64

# RUN pip install aquacrop && pip install --upgrade numpy && pip install --upgrade numba

# RUN pip install xarray

# COPY ./tools /tools

# WORKDIR /tools/pypro4sail 

# RUN python setup.py install

# WORKDIR /tools/pyTSEB

# RUN python setup.py install

# WORKDIR /tools/pyMETRIC

# RUN python setup.py install

# WORKDIR /app

CMD ["tail", "-f"]

# CMD python manage.py runserver 0.0.0.0:8000
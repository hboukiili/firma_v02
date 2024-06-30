FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN conda install python=3.10

RUN conda install -y -c conda-forge \
    python=3.10 gdal gcc_linux-64 gxx_linux-64 pcraster \
    && conda update --all \
    && conda clean --all --yes

WORKDIR /app
 
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install aquacrop==3.0.7 && pip install --upgrade numpy && pip install --upgrade numba

RUN pip install xarray

COPY ./script.sh /app/

RUN chmod +x /app/script.sh

# ENTRYPOINT [ "/app/script.sh" ]

# CMD python managy.py makemigrations && python manage.py migrate && python manage.py makemigrations models_only && python manage.py migrate models_only && python manage.py runserver 0.0.0.0:8000

# RUN pip install openpyxl

# RUN pip install aquacrop && pip install --upgrade numpy && pip install --upgrade numba

# COPY ./tools /tools

# WORKDIR /tools/pypro4sail 

# RUN python setup.py install

# WORKDIR /tools/pyTSEB

# RUN python setup.py install

# WORKDIR /tools/pyMETRIC

# RUN python setup.py install

# WORKDIR /app

CMD ["tail", "-f"]
FROM continuumio/miniconda3

RUN apt-get update && apt-get install -y \
    build-essential \
    redis-server \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN conda install python=3.10

RUN conda install -y -c conda-forge \
    gdal gcc_linux-64 gxx_linux-64 pcraster \
    && conda update --all \
    && conda clean --all --yes

WORKDIR /app
 
COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

RUN pip install aquacrop==3.0.7

RUN export DJANGO_SETTINGS_MODULE=firma_v02.settings

WORKDIR /app

COPY ./script.sh /app/

RUN chmod +x /app/script.sh

# ENTRYPOINT [ "/app/script.sh" ]


# CMD ["/app/script.sh"]

CMD ["tail", "-f"]
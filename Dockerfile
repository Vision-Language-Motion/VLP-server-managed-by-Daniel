ARG PYTORCH="1.8.1"
ARG CUDA="10.2"
ARG CUDNN="7"
ARG DO_DATABASE_PASSWORD
ARG AUTH_PASSWORD

FROM pytorch/pytorch:${PYTORCH}-cuda${CUDA}-cudnn${CUDNN}-devel
ENV DO_DATABASE_PASSWORD=${DO_DATABASE_PASSWORD}
ENV AUTH_PASSWORD=${AUTH_PASSWORD}

# To fix GPG key error when running apt-get update
RUN rm /etc/apt/sources.list.d/cuda.list \
    && rm /etc/apt/sources.list.d/nvidia-ml.list \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/ubuntu1804/x86_64/3bf863cc.pub \
    && apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1804/x86_64/7fa2af80.pub

# Install system dependencies for opencv-python
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 python-psycopg2 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install mmcv
ARG MMCV=""
RUN if [ "${MMCV}" = "" ]; then pip install -U openmim && mim install 'mmcv>=2.0.0rc1' && mim install mmpose; else pip install -U openmim && mim install mmcv==${MMCV} && mim install mmpose; fi

# Verify the installation
RUN python -c 'import mmcv;print(mmcv.__version__)'

# Add the rest of the code
COPY . /code/

RUN pip install Django djangorestframework python-dotenv gunicorn psycopg2-binary 

# Make port 8000 available to the world outside this container
EXPOSE 8000

WORKDIR /code/vlp



RUN python manage.py collectstatic --noinput



RUN python manage.py test poseestimator

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server.wsgi:application"]

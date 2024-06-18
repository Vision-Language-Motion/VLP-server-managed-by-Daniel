# VLP-server-managed-by-Daniel

VLP server (please do not adjust anything here without letting me (Daniel) know) | I did not restrict the main branch. If we use this repo together e.g. creating an issue for each new function or something like that I will restrict the main branch against accidental pushes. Please remind me, if I forget.

```bash
docker build --build-arg DO_DATABASE_PASSWORD=$(grep DO_DATABASE_PASSWORD .env | cut -d '=' -f2) \
             --build-arg AUTH_PASSWORD=$(grep AUTH_PASSWORD .env | cut -d '=' -f2) \
             -t prodbuild .
```

then
`docker run -p 80:8000 prodbuild`

### How to run tests

```bash
docker build --build-arg DO_DATABASE_PASSWORD=$(grep DO_DATABASE_PASSWORD .env | cut -d '=' -f2)              --build-arg AUTH_PASSWORD=$(grep AUTH_PASSWORD .env | cut -d '=' -f2) --build-arg TEST="true"            -t testbuild .
```

\(For saving the build-log:)

```bash
docker build --build-arg DO_DATABASE_PASSWORD=$(grep DO_DATABASE_PASSWORD .env | cut -d '=' -f2)              --build-arg AUTH_PASSWORD=$(grep AUTH_PASSWORD .env | cut -d '=' -f2) --build-arg TEST="true"            -t testbuild . &> build.log
```

### Git lfs

Install git-lfs (for the pytorch models): (On Ubuntu)

```bash
git lfs install
```

--------

# Documentation

The goal of our VLP-server is to effectively filter a large number of video resources to compose a useful, high-quality dataset of human motion video clips for machine learning. Ideally the dataset will become useful for a multimodal model. As a resource we mainly use YouTube for its relatively lenient legal policy, so a YouTube video is POSTed to the server, downloaded, segmented into scences, processed and deleted. So only the url and the calculated metric of human presence likelihood is saved.

### Server architecture
The server is built with the python Django web-development library, using the Django REST-Framework for queries/POST-/GET-requests and celery for task management. The code is segmented into different folders/apps (i.e. [pose estimator](./vlp/poseestimator) and [api](./vlp/api)) which communicate through [serialization](./vlp/api/serializers.py). 

In the current working version we have a simple REST-Framework for POSTing a video, which then gets processed immediately by the MMPose algorithm and assesses the visibility of humans.

Docker simplifies deployment by encapsulating the entire application, including its dependencies, configurations, and environment settings, into a container. Especially useful for MMPose.

### MMPose Human Pose detection
We are using the MMPose library, which is based on pytorch and 
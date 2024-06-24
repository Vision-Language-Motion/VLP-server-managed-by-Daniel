# VLP-server-managed-by-Daniel

VLP server (please do not adjust anything here without letting me (Daniel) know) | I did not restrict the main branch. If we use this repo together e.g. creating an issue for each new function or something like that I will restrict the main branch against accidental pushes. Please remind me, if I forget

## Keyword Process
We have a Query model of Keywords with a use counter and a last processed timestamp, and every day a scheduled celery worker retrieves the top 100 Keywords (Queries) from our list, that have been used the least, and retrieves 50 YouTube urls per query through the Google API. The urls are saved in the URL list and processed by a separate worker, that downloads each video from the given url, processes it with an algorithm using pyscenedetect and mmpose, and gives the video a metric of number of humans visible and the quality of the visual presence. The videos are deleted from local storage to make space for the next ones.

### (Stand der Dinge.)
  * Können wir Keywords hochladen? ja
    * Können Keywords nicht doppelt hochgeladen werden? nein
  * Können wir mit Keywords suchanfragen stellen? 
    * Werden die URLs nicht doppelt gespeichert?
  * Können wir die Keywords automatisch durchlaufen, alle 24h z.B.
  * Können wir die URLs automatisch verarbeiten?
Später:
  * Können wir schauen wie gut ein Keyword ist, und neue irgendwie ranschaffen? (Semantic Web oder LLM?)


### Git lfs

Install git-lfs (for the pytorch models): (On Ubuntu)

```bash
git lfs install
```

### How to run the server:

> Add Google Developer key to .env and add .env to main directory

```bash
docker build --build-arg DO_DATABASE_PASSWORD=$(grep DO_DATABASE_PASSWORD .env | cut -d '=' -f2) \
             --build-arg AUTH_PASSWORD=$(grep AUTH_PASSWORD .env | cut -d '=' -f2) \
             --build-arg GOOGLE_DEV_API_KEY=$(grep GOOGLE_DEV_API_KEY .env | cut -d '=' -f2) \
             --build-arg DEBUG=$(grep DEBUG .env | cut -d '=' -f2) \
             -t prodbuild .
```

then
`docker run -p 80:8000 prodbuild`

### How to run tests

```bash
docker build --build-arg DO_DATABASE_PASSWORD=$(grep DO_DATABASE_PASSWORD .env | cut -d '=' -f2)              --build-arg AUTH_PASSWORD=$(grep AUTH_PASSWORD .env | cut -d '=' -f2) --build-arg TEST="true"   --build-arg GOOGLE_DEV_API_KEY=$(grep GOOGLE_DEV_API_KEY .env | cut -d '=' -f2)     --build-arg DEBUG=$(grep DEBUG .env | cut -d '=' -f2)    -t testbuild .
```

### Write log to file
```bash
docker build  --progress=plain  --build-arg DO_DATABASE_PASSWORD=$(grep DO_DATABASE_PASSWORD .env | cut -d '=' -f2)              --build-arg AUTH_PASSWORD=$(grep AUTH_PASSWORD .env | cut -d '=' -f2) --build-arg TEST="true"   --build-arg GOOGLE_DEV_API_KEY=$(grep GOOGLE_DEV_API_KEY .env | cut -d '=' -f2)     --build-arg DEBUG=$(grep DEBUG .env | cut -d '=' -f2)    -t    testbuild . >& build.log
```

Testbuild runs all the TestCase Classes in [api/tests.py](./vlp/api/tests.py) and [poseestimator/tests.py](./vlp/poseestimator/tests.py). Note that all tests are run first and then all errors that occured during testing are printed consecutively.

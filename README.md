# VLP-server-managed-by-Daniel

VLP server (please do not adjust anything here without letting me (Daniel) know) | I did not restrict the main branch. If we use this repo together e.g. creating an issue for each new function or something like that I will restrict the main branch against accidental pushes. Please remind me, if I forget

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

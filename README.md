# VLP-server-managed-by-Daniel

VLP server (please do not adjust anything here without letting me (Daniel) know) | I did not restrict the main branch. If we use this repo together (e.g. creating an issue for each new function or something like that I will restrict the main branch against accidental pushes. Please remind me, if I forget.

```bash
docker build --build-arg DO_DATABASE_PASSWORD=$(grep DO_DATABASE_PASSWORD .env | cut -d '=' -f2) \
             --build-arg AUTH_PASSWORD=$(grep AUTH_PASSWORD .env | cut -d '=' -f2) \
             -t prodbuild .
```

then
`docker run -p 80:8000 prodbuild`

### How to run tests

```bash
docker build --build-arg DO_DATABASE_PASSWORD=$(grep DO_DATABASE_PASSWORD .env | cut -d '=' -f2)              --build-arg AUTH_PASSWORD=$(grep AUTH_PASSWORD .env | cut -d '=' -f2) --build-arg TEST="true"            -t prodbuild .
```

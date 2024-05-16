# VLP-server-managed-by-Daniel

VLP server (please do not adjust anything here without letting me (Daniel) know)

Docker command
`docker build -t testbuild .`
`docker run --env-file .env -p 8000:8000 testbuild`

```bash
docker build --build-arg DO_DATABASE_PASSWORD=$(grep DO_DATABASE_PASSWORD .env | cut -d '=' -f2) \
             --build-arg AUTH_PASSWORD=$(grep AUTH_PASSWORD .env | cut -d '=' -f2) \
             -t prodbuild .
```

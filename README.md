# MLM

```shell
docker build -t helloi .
docker run helloi
gcloud app deploy --version dev --quiet
```



gcloud auth login

gcloud config set project xxx

export GOOGLE_CLOUD_PROJECT=xxx

gsutil mb gs://$GOOGLE_CLOUD_PROJECT$-media

gcloud app deploy

gcloud app logs tail -s default


https://baseline-ml.appspot.com/?utm_source=marc_test&utm_medium=referral
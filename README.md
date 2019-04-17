# Baseline ML

``` shell
    docker build -t bml-image .
    docker run bml-image
    gcloud app deploy --version dev --quiet
```

gcloud auth login

gcloud config set project xxx

gsutil mb gs://$GOOGLE_CLOUD_PROJECT$-media

gcloud beta app deploy --quiet --verbosity debug

gcloud app logs tail -s default

https://baseline-ml.appspot.com/?utm_source=marc_test&utm_medium=referral


echo "Creating Service Account"
gcloud iam service-accounts create baseline-ml-account --display-name "Baseline ML Account"
gcloud iam service-accounts keys create baseline-ml-key.json --iam-account=baseline-ml-account@baseline-ml.iam.gserviceaccount.com

export GOOGLE_CLOUD_PROJECT=baseline-ml
export GOOGLE_APPLICATION_CREDENTIALS=baseline-ml-key.json

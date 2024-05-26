
# Buy me a bag- GenAI e-ecommerce agent

Router Agent, E-commerce Assistant


## Demo

![Demo](https://github.com/g-emarco/find-me-a-bag/blob/main/static/demo.gif)

## Architecture 

![Alt Text](https://github.com/g-emarco/find-me-a-bag/blob/main/static/architecture.jpg)

## Contributors

### Frontend
- [**Avi Shitrit**](https://www.linkedin.com/in/avi-shitrit-a2895218/)
### Backend
- [**Eden Marco**](https://www.linkedin.com/in/eden-marco/)
### Dataset preparation, Indexing and Vector Search
- [**Laura Bouaziz**](https://www.linkedin.com/in/laurabouaziz/)

## Tech Stack

**Client:** React

**Server Side:** LangGraph 🦜🕸️, Flask

**Vectorstore:** VertexAI Vector Search

**Database:** Firestore

**LLM:** Gemini 1.5 Flash

**Runtime:** Cloud Run  

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file



`SENDGRID_API_KEY`
`GOOGLE_APPLICATION_CREDENTIALS`
`PROJECT_ID`
`LOCAL`

## Run Locally


Clone the project

```bash
  git clone https://github.com/emarco177/find-me-a-bag.git
```

Go to the project directory

```bash
  cd find-me-a-bag
```

Install dependencies

```bash
  poetry install
```

Start the Flask server

```bash
  flask run app.py --debug
```

NOTE: When running locally make sure `GOOGLE_APPLICATION_CREDENTIALS` is set to a service account with permissions to use VertexAI


## Deployment to cloud run

CI/CD via Cloud build is available in ```cloudbuild.yaml```

Please replace $PROJECT_ID with your actual Google Cloud project ID.

To deploy manually:

1. Make sure you enable GCP APIs:

```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable secretmanager.googleapis.com
gcloud services enable artifactregistry.googleapis.com
gcloud services enable vertexai.googleapis.com

```

2. Create a service account `langgraph-agent-sa` with the following roles:




```bash
gcloud iam service-accounts create vertex-ai-consumer \
    --display-name="LangGraph Agent SA"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:langgraph-agent-sa@P$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/run.invoker"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:langgraph-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/serviceusage.serviceUsageConsumer"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:langgraph-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/ml.admin"

gcloud projects add-iam-policy-binding PROJECT_ID \
    --member="serviceAccount:langgraph-agent-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/vertexai.admin"

```

3. Create the secrets:
`SENDGRID_API_KEY`

and for each secret grant the SA `langgraph-agent-sa@$PROJECT_ID.iam.gserviceaccount.com` Secret Manager Secret Accessor
role to th secrets

4. Build Image
```bash
docker build . -t me-west1-docker.pkg.dev/$PROJECT_ID/app/find-me-a-bag:latest
```

5. Push to Artifact Registry
```bash
docker push me-west1-docker.pkg.dev/$PROJECT_ID/app/find-me-a-bag:latest
```

6. Deploy to cloud run
```gcloud run deploy $PROJECT_ID \
    --image=me-west1-docker.pkg.dev/$PROJECT_ID/app/find-me-a-bag:latest \
    --region=me-west1 \
    --service-account=langgraph-agent-sa@$PROJECT_ID.iam.gserviceaccount.com \
    --allow-unauthenticated \
    --set-secrets="SENDGRID_API_KEY=projects/PROJECT_ID/secrets/SENDGRID_API_KEY/versions/latest"
```



## 🚀 About Me
Eden Marco, Customer Engineer @ Google Cloud, Tel Aviv🇮🇱

[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/eden-marco/) 

[![twitter](https://img.shields.io/badge/twitter-1DA1F2?style=for-the-badge&logo=twitter&logoColor=white)](https://twitter.com/EdenEmarco177)

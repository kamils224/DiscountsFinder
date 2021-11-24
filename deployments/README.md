# Minikube deployment
Create secret for MONGO DB:

`kubectl create secret generic mongo-credentials --from-literal=mongo-uri=<yourMongoURI>`

`kubectl apply -f redis-deployment.yaml`

`kubectl apply -f redis-service.yaml`

`kubectl apply -f config-map.yaml`

`kubectl apply -f celery-deployment.yaml`

`kubectl apply -f backend-deployment.yaml`

`kubectl apply -f backend-service.yaml`
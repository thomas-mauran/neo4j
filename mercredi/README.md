## Install the spark operator using helm

helm repo add spark-operator https://kubeflow.github.io/spark-operator

helm repo update

helm install spark-operator spark-operator/spark-operator \
    --namespace spark-operator --create-namespace --wait


We need to create a service account and a cluster role binding for the spark operator to use.

kubectl create clusterrolebinding spark-role --clusterrole=edit --serviceaccount=default:default --namespace=default


docker build -t custom-spark:latest .

k3d image import custom-spark:latest

kubectl apply -f kube/spark-pi.yaml



## Minio

helm repo add minio-operator https://operator.min.io
helm repo update
helm install \
  --namespace minio-operator \
  --create-namespace \
  operator minio-operator/operator

kubectl apply -f kube/minio.yaml

![alt text](<Capture d’écran, le 2025-03-27 à 10.42.36.png>)

kubectl port-forward -n minio minio-86c6bc7865-g9z4v 9001:9001

![alt text](<Capture d’écran, le 2025-03-27 à 10.43.09.png>)

![alt text](<Capture d’écran, le 2025-03-27 à 10.55.01.png>)

I added the readme file
![alt text](<Capture d’écran, le 2025-03-27 à 10.56.35.png>)

lets build the wordcount image and push it to the registry

docker build --no-cache -t wordcount-minio:latest -f Dockerfile-minio .

k3d image import wordcount-minio:latest

![alt text](<Capture d’écran, le 2025-03-27 à 11.24.46.png>)


and here is the result of the process
![alt text](<Capture d’écran, le 2025-03-27 à 12.12.25.png>)
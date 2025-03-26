## Install the spark operator using helm

helm repo add spark-operator https://kubeflow.github.io/spark-operator

helm repo update

helm install spark-operator spark-operator/spark-operator \
    --namespace spark-operator --create-namespace --wait

docker build -t custom-spark:latest .

k3d image import custom-spark:latest
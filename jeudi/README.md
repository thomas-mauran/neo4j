We are gonna work in the activity folder

docker build -t stream:latest .

k3d image import stream:latest

![alt text](<Capture d’écran, le 2025-03-27 à 15.16.41.png>)

the element runs as seen


![alt text](<Capture d’écran, le 2025-03-27 à 15.23.56.png>)

when I drop a new file in the minio  dont see it getting processed even though the spark job keeps running maybe there is an issue about the spark job itself


### Kafka


helm repo add strimzi https://strimzi.io/charts/
helm upgrade --install my-strimzi-kafka-operator strimzi/strimzi-kafka-operator --version 0.45.0 --set fullReconciliationIntervalMs=3000 --set watchAnyNamespace=true


![alt text](<Capture d’écran, le 2025-03-27 à 16.49.42.png>)


![alt text](<Capture d’écran, le 2025-03-27 à 16.56.27.png>)


kafka doesnt seem to work well

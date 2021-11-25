# Druid + Kafka + Grafana

## Deployment

### Config Env

1. Follow the [official instruction](https://docs.docker.com/get-docker/) to nstall docker & docker-compose. If you are using the *nix system with apt, just type the following commands:

```bash
sudo apt install docker
sudo apt install docker-compose
```



### Build Image

2. Download this repo to your machine.
3. Enter `druid_docker` folder in terminal and run the following commands to build the docker image with the file `docker-compose.yml`:

```bash
sudo docker-compose up -d
```

This may take a while to fetch and build the docker image, you can get yourself a cup of coffee and wait :)



### Create Kafka Topic

4. Check if all the components are running

```bash
sudo docker ps
```

5. Create your Kafka topic, replace the `topic_name` with your unique topic name. You can learm more about Kafka concepts from its [offcial site](https://kafka.apache.org/documentation/#gettingStarted)

```bash
sudo docker exec -it druid-docker_kafka_1 /opt/kafka/bin/kafka-topics.sh --create --topic [topic_name] --partitions 4 --zookeeper zookeeper_kafka:2181 --replication-factor 1
```

Example:

```bash
sudo docker exec -it druid-docker_kafka_1 /opt/kafka/bin/kafka-topics.sh --create --topic test_topic --partitions 4 --zookeeper zookeeper_kafka:2181 --replication-factor 1
```

>You will get a result says: 
>
>Created topic test_topic.

6. `test_producer.py` and `test_consumer.py` provide a simple producer and consumer. Replace the topic name in these two files with the topic you just created and run them to check if your Kafka words.

> The consumer will keep listening the topic, so you need to open another terminal to run the producer. Each time you call the producer, your consumer is expected to receive a message.



### Access Druid Console

7. In `docker-compose.yml` , router of Druid runs in port 9999, so open your browser and type `http://localhost:9999`, you will be able to access the Druid console. The Druid is successfully running on your machine if you can see the console page.



### Access Grafana

8. Open ` http://localhost:3000`, you will see the grafana login page. Your username and password will be `admin` as default.



### Shutdown Cluster

9. You can use the following command to stop all the containers after finish using the druid.

```bash
sudo docker-compose down
```




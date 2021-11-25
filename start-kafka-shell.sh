#!/bin/bash
docker run --network=ruby_net --rm -v /var/run/docker.sock:/var/run/docker.sock -e HOST_IP=$1  -e ZK=$2 -i -t wurstmeister/kafka /bin/bash

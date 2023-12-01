# TDC
Distributed Machine Learning (TDC)

Presentation Link:
https://docs.google.com/presentation/d/1vBBeuVx0xfII3VDPJeyIUC4QW-R763cumkEjGmkaMvU/edit#slide=id.g28ce11a3496_0_636

Installation and Running:

First Install RabbitMQ server and Erlang OTP and Docker

This project is containerized using Docker, making it easy to build and run regardless of your development environment.

To install and run the Prover and Verifier:

Clone this repository:
git clone https://github.com/varshith09red/TDC

Setup Configuration:
Before running the application, you need to set up configuration files for both the Prover and the Verifier. Create .env files for both the Prover and the Verifier in their directories.

Adjust the values in the .env files as per your needs. Ensure that the configuration matches between the Prover and Verifier so they can interact correctly.

Build and run
From the root directory of the project, build and run the Docker images using docker-compose:

docker-compose up -d

The Prover and Verifier services will start interacting once RabbitMQ is up and running.

To review the results, you can check the logs of both the Prover and Verifier containers. This can be done with Docker's log command:

docker logs <container_id>

Where <container_id> is the ID of the container for which you want to view the logs.

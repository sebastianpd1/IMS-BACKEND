FROM gitpod/workspace-mysql:branch-mysql
USER root
RUN apt-get update && apt-get install -y pkg-config python3-dev

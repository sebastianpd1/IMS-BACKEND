FROM gitpod/workspace-mysql:branch-mysql

RUN apt-get update && apt-get install -y pkg-config python3-dev
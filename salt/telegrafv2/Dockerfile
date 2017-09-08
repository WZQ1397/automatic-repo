FROM ubuntu:16.04
MAINTAINER Justin Downing <justin@downing.us>

RUN apt-get -qq update && apt-get install -y curl vim
RUN curl -s -o- https://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest/SALTSTACK-GPG-KEY.pub | apt-key add -
RUN echo "deb http://repo.saltstack.com/apt/ubuntu/16.04/amd64/latest xenial main" | tee /etc/apt/sources.list.d/saltstack.list
RUN apt-get -qq update && apt-get install -y salt-minion

RUN mkdir -p /srv/salt/base/states && mkdir -p /srv/salt/base/pillars
RUN echo "file_roots:\n  base:\n    - /srv/salt/base/states\npillar_roots:\n  base:\n    - /srv/salt/base/pillars" | tee /etc/salt/minion.d/roots.conf
RUN echo "base:\n  '*':\n    - telegraf" | tee /srv/salt/base/states/top.sls
RUN echo "base:\n  '*':\n    - telegraf" | tee /srv/salt/base/pillars/top.sls

COPY telegraf /srv/salt/base/states/telegraf
COPY pillar.example /srv/salt/base/pillars/telegraf/init.sls
RUN salt-call --local state.apply

FROM kcollins/ignition:8.0.16
USER root

RUN apt-get update && apt-get install -y git

# Clone version control tools project
RUN mkdir /var/lib/ignition/data/projects && cd /var/lib/ignition/data/projects && \
    git clone https://github.com/jlbcontrols/ignition-vcs-tools.git

# Create folder for the development project
RUN mkdir /var/lib/ignition/data/projects/pidbot-manager

# Modules
RUN mkdir /modules && cd /modules && \
    curl -L -s "https://github.com/jlbreleases/pb-rel/releases/download/v1.10.2/pidbot-1.10.2-20200922.modl" -O && \
    curl -L -s "https://github.com/jlbcontrols/vision-client-opc-browser/releases/download/v1.10.0-beta/vcob-1.10.0-beta-20201003.modl" -O

#USER ${IGNITION_UID}

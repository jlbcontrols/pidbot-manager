FROM kcollins/ignition:8.0.16
USER root

# Build Arguments for UID/GID
ARG IGNITION_UID=1000
ENV IGNITION_UID=1000
ARG IGNITION_GID=1000
ENV IGNITION_GID=1000


RUN apt-get update && apt-get install -y git

# Clone version control tools project
RUN mkdir /var/lib/ignition/data/projects && cd /var/lib/ignition/data/projects && \
    git clone https://github.com/jlbcontrols/ignition-vcs-tools.git

# Create folder for the development project
RUN mkdir /var/lib/ignition/data/projects/pidbot-manager && \
    chown -R ${IGNITION_UID}:${IGNITION_GID} /var/lib/ignition/data/projects

# Modules
RUN mkdir /modules && cd /modules && \
    curl -L -s "https://github.com/jlbreleases/pb-rel/releases/download/v1.10.2/pidbot-1.10.2-20200922.modl" -O && \
    curl -L -s "https://github.com/jlbcontrols/vision-client-opc-browser/releases/download/v1.10.0-beta/vcob-1.10.0-beta-20201003.modl" -O





# Setup dedicated user, map file permissions, and set execution flags
RUN usermod -u 1000 ignition && groupmod -g 1000 ignition


# Copy Ignition Installation from Build Image
RUN chown -R ${IGNITION_UID}:${IGNITION_GID} ${IGNITION_INSTALL_USERHOME} ${IGNITION_INSTALL_LOCATION} /var/lib/ignition /var/log/ignition


USER ${IGNITION_UID}

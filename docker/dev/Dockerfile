FROM kcollins/ignition:8.0.16
USER root

# Match typical linux user/group (TODO: Make this a build arg instead)
ENV IGNITION_UID=1000
ENV IGNITION_GID=1000

# Install Git
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

# Modify user/group from base image, and update file ownership.
RUN usermod -u IGNITION_UID ignition && groupmod -g ENV IGNITION_GID ignition
RUN chown -R ${IGNITION_UID}:${IGNITION_GID} ${IGNITION_INSTALL_USERHOME} ${IGNITION_INSTALL_LOCATION} /var/lib/ignition /var/log/ignition

USER ${IGNITION_UID}

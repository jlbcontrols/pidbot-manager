FROM kcollins/ignition:8.0.16
USER root

# Gateway Backup
RUN curl -L -s "https://github.com/jlbcontrols/pidbot-manager/releases/latest/download/backup.gwbk" -o /restore.gwbk

# Modules
RUN mkdir /modules && cd /modules && \
    curl -L -s "https://github.com/jlbcontrols/vision-client-opc-browser/releases/download/v1.10.0-beta/vcob-1.10.0-beta-20201003.modl" -O && \
    curl -L -s "https://github.com/jlbreleases/pb-rel/releases/download/v1.10.2/pidbot-1.10.2-20200922.modl" -O

USER ${IGNITION_UID}

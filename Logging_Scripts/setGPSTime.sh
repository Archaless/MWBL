ZDA=$(gpspipe -r -n 10 | grep 'GNZDA' | head -n1)
IFS=',' read -r _ hhmmss dd mm yyyy _ <<< "$ZDA"
HH=${hhmmss:0:2}
MM=${hhmmss:2:2}
SS=${hhmmss:4:2}
sudo date -u -s "${yyyy}-${mm}-${dd} ${HH}:${MM}:${SS}"

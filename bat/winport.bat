@echo off
echo {
echo         "data":[
for /F "tokens=2 delims= " %%i IN ('netstat -anp tcp^|find /i "LISTENING"') DO echo                 {"{#TCP_PORT}":"%%i"},
for /F "tokens=2 delims= " %%i IN ('netstat -anp tcp^|find /i "ESTABLISHED"') DO echo                 {"{#TCP_PORT}":"%%i"},
for /F "tokens=2 delims= " %%i IN ('netstat -anp udp^|find /i "LISTENING"') DO echo                 {"{#UDP_PORT}":"%%i"},
for /F "tokens=2 delims= " %%i IN ('netstat -anp udp^|find /i "ESTABLISHED"') DO echo                 {"{#UDP_PORT}":"%%i"},
echo                 {"{#TCP_PORT}":"10050"}
echo         ]
echo }
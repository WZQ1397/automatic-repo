@echo off
title --IP�Զ����� -- 
MODE con: COLS=80 lines=30
color 0a

:main
cls

echo  ����ʾ����
echo.
echo �밴 1: ����IP��ַ1: 10.86.164.254
echo �밴 2: ����IP��ַ2: 192.168.1.2
echo �밴 3: �Զ���ȡIP
echo �밴 4: �˳�����IP
echo.
echo  ע�⣺�粻����ȷ����IP������Local Area Connection�����Ƿ���ű��е����Ʊ���һ�¡�
echo.
@rem ��һ���ǿ�һ��

set /p choice=      ����ѡ��

echo.

if "%choice%"=="1" goto ip1
if "%choice%"=="2" goto ip2
if "%choice%"=="3" goto ip3
if "%choice%"=="4" goto end

goto main

:ip1
echo IP:10.86.164.254 �Զ����ÿ�ʼ....
echo.
echo ��������IP����������
cmd /c netsh interface ip set address name="Local Area Connection" source=static addr=10.86.164.254 mask=255.255.255.0 gateway=10.86.164.1 gwmetric=1
echo ��������DNS������
cmd /c netsh interface ip set dns name="Local Area Connection" source=static addr=10.86.130.25 register=PRIMARY
@rem �������Ϊ����DNSΪ10.86.130.25
echo ��������DNS������
cmd /c netsh interface ip add dns name="Local Area Connection" addr=202.96.209.5 index=2
@rem �������Ϊ����DNSΪ202.96.209.5
@cmd /c route add 139.0.0.0 mask 255.0.0.0 139.66.92.1 -p
@cmd /c route add 172.0.0.0 mask 255.0.0.0 139.66.92.1 -p
@cmd /c route add 65.0.0.0 mask 255.0.0.0 139.66.92.1 -p
echo �������

pause
exit 

if errorlevel 2 goto main
if errorlevel 1 goto end 



:ip2
echo IP: 192.168.1.2 �Զ����ÿ�ʼ....
echo.
echo ��������IP����������
cmd /c netsh interface ip set address name="Local Area Connection" source=static addr=192.168.1.2 mask=255.255.255.0 gateway=192.168.1.1 gwmetric=1
echo �Զ���ȡDNS������....
netsh interface ip set dns name = "Local Area Connection" source = dhcp
echo �������

pause
exit 

if errorlevel 2 goto main
if errorlevel 1 goto end 


:ip3
echo IP�Զ����ÿ�ʼ....
echo.
echo �Զ���ȡIP��ַ....
netsh interface ip set address name = "Local Area Connection" source = dhcp
echo �Զ���ȡDNS������....
netsh interface ip set dns name = "Local Area Connection" source = dhcp 
@rem �����Զ���ȡIP
cmd /c route delete 139.0.0.0 mask 255.0.0.0 139.66.92.1 -p
cmd /c route delete 172.0.0.0 mask 255.0.0.0 139.66.92.1 -p
cmd /c route delete 65.0.0.0 mask 255.0.0.0 139.66.92.1 -p
echo �������


pause
exit 

if errorlevel 2 goto main
if errorlevel 1 goto end 


:end  


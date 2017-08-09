@echo off
title --IP自动设置 -- 
MODE con: COLS=80 lines=30
color 0a

:main
cls

echo  按提示操作
echo.
echo 请按 1: 设置IP地址1: 10.86.164.254
echo 请按 2: 设置IP地址2: 192.168.1.2
echo 请按 3: 自动获取IP
echo 请按 4: 退出设置IP
echo.
echo  注意：如不能正确设置IP，请检查Local Area Connection名称是否与脚本中的名称保持一致。
echo.
@rem 上一句是空一行

set /p choice=      您的选择：

echo.

if "%choice%"=="1" goto ip1
if "%choice%"=="2" goto ip2
if "%choice%"=="3" goto ip3
if "%choice%"=="4" goto end

goto main

:ip1
echo IP:10.86.164.254 自动设置开始....
echo.
echo 正在设置IP及子网掩码
cmd /c netsh interface ip set address name="Local Area Connection" source=static addr=10.86.164.254 mask=255.255.255.0 gateway=10.86.164.1 gwmetric=1
echo 正在设置DNS服务器
cmd /c netsh interface ip set dns name="Local Area Connection" source=static addr=10.86.130.25 register=PRIMARY
@rem 以上这句为设置DNS为10.86.130.25
echo 正在设置DNS服务器
cmd /c netsh interface ip add dns name="Local Area Connection" addr=202.96.209.5 index=2
@rem 以上这句为设置DNS为202.96.209.5
@cmd /c route add 139.0.0.0 mask 255.0.0.0 139.66.92.1 -p
@cmd /c route add 172.0.0.0 mask 255.0.0.0 139.66.92.1 -p
@cmd /c route add 65.0.0.0 mask 255.0.0.0 139.66.92.1 -p
echo 设置完成

pause
exit 

if errorlevel 2 goto main
if errorlevel 1 goto end 



:ip2
echo IP: 192.168.1.2 自动设置开始....
echo.
echo 正在设置IP及子网掩码
cmd /c netsh interface ip set address name="Local Area Connection" source=static addr=192.168.1.2 mask=255.255.255.0 gateway=192.168.1.1 gwmetric=1
echo 自动获取DNS服务器....
netsh interface ip set dns name = "Local Area Connection" source = dhcp
echo 设置完成

pause
exit 

if errorlevel 2 goto main
if errorlevel 1 goto end 


:ip3
echo IP自动设置开始....
echo.
echo 自动获取IP地址....
netsh interface ip set address name = "Local Area Connection" source = dhcp
echo 自动获取DNS服务器....
netsh interface ip set dns name = "Local Area Connection" source = dhcp 
@rem 设置自动获取IP
cmd /c route delete 139.0.0.0 mask 255.0.0.0 139.66.92.1 -p
cmd /c route delete 172.0.0.0 mask 255.0.0.0 139.66.92.1 -p
cmd /c route delete 65.0.0.0 mask 255.0.0.0 139.66.92.1 -p
echo 设置完成


pause
exit 

if errorlevel 2 goto main
if errorlevel 1 goto end 


:end  


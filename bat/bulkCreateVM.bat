CD "C:\Program Files (x86)\VMware\VMware Workstation\"
 
REM 为指定的虚拟机，创建快照名称为VM11
vmrun -T ws snapshot "F:\VMS-2016\Windows 7\Windows 7.vmx" VM11
PAUSE 创建快照完成，按任意键继续
 
REM 创建克隆链接的虚拟机，克隆10个
for /l%%a in (1001,1,1010) do  (
vmrun.exe -T ws clone "F:\VMS-2016\Windows 7\Windows 7.vmx"  F:\VMS-2017\%%a\%%a.vmx  linked -snapshot=VM11  -cloneName=%%a
)
PAUSE 克隆虚拟机完成，按任意键继续
 
REM 启用VNC，端口%%b，密码为空
@echo on
for  /l  %%bin (1001,1,1010) do (
echo answer.msg.uuid.altered = "I Copied It" >>F:\VMS-2017\%%b\%%b.vmx
echo RemoteDisplay.vnc.enabled = "TRUE" >>F:\VMS-2017\%%b\%%b.vmx
echo RemoteDisplay.vnc.port = "%%b" >>F:\VMS-2017\%%b\%%b.vmx
rem echo RemoteDisplay.vnc.key = "" >>F:\VMS-2017\%%b\%%b.vmx
)
pause 配置端口完成，按任意键继续
REM 克隆完成，间隔30秒启动虚拟机

for /l%%c in (1001,1,1010) do  (
vmrun.exe -T ws start F:\VMS-2017\%%c\%%c.vmx
choice /t 30 /d y /n >nul
)
pause 启动虚拟机完成，按任意键继续
 
REM 下课，间隔30秒停止虚拟机
for /l%%d in (1001,1,1010) do  (
vmrun.exe -T ws stop F:\VMS-2017\%%d\%%d.vmx
ping -n 30 127.0.0.1 >nul
)
PAUSE 关闭所有正在运行的虚拟机完成，按任意键退出

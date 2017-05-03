#$language = "VBScript"
#$interface = "1.0"

crt.Screen.Synchronous = True

' This automatically generated script may need to be
' edited in order to work correctly.

Sub Main
	crt.Screen.Send "df -Tha" & chr(13)
	crt.Screen.WaitForString "[root@localhost " & chr(126) & "]# "
	crt.Screen.Send "cat /proc/meminfo" & chr(13)
	crt.Screen.WaitForString "[root@localhost " & chr(126) & "]# "
	crt.Screen.Send "cat /proc/cpuinfo " & chr(124) & " grep name " & chr(124) & " cut -f2 -d: " & chr(124) & " uniq -c" & chr(13)
	crt.Screen.WaitForString "[root@localhost " & chr(126) & "]# "
	crt.Screen.Send "cat /proc/cpuinfo " & chr(124) & " grep physical " & chr(124) & " uniq -c" & chr(13)
End Sub

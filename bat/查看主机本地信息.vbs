#$language = "VBScript"
#$interface = "1.0"

crt.Screen.Synchronous = True

' This automatically generated script may need to be
' edited in order to work correctly.

Sub Main
	crt.Screen.Send "more /etc/redhat-release " & chr(13)
	crt.Screen.WaitForString "[root@localhost " & chr(126) & "]# "
	crt.Screen.Send "uname -a" & chr(13)
	crt.Screen.WaitForString "[root@localhost " & chr(126) & "]# "
	crt.Screen.Send "sestatus" & chr(13)
	crt.Screen.WaitForString "[root@localhost " & chr(126) & "]# "
	crt.Screen.Send "hostname " & chr(13)
	crt.Screen.WaitForString "[root@localhost " & chr(126) & "]# "
	crt.Screen.Send "uptime" & chr(13)
End Sub

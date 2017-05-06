#$language = "VBScript"
#$interface = "1.0"

crt.Screen.Synchronous = True

' This automatically generated script may need to be
' edited in order to work correctly.

Sub Main
	crt.Screen.Send "vmstat" & chr(13)
	crt.Screen.WaitForString "[root@localhost " & chr(126) & "]# "
	crt.Screen.Send "free " & chr(65293) & "b " & chr(65293) & "s5" & chr(13)
End Sub

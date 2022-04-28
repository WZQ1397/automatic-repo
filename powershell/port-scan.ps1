$ip = Read-Host "Enter Host"
$port = Read-Host "Enter Port"
Test-NetConnection -Port $port -InformationLevel "Detailed" $ip
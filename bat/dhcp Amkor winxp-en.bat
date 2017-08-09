netsh interface ip set address name="Local Area Connection" source=dhcp 
netsh interface ip set dns name="Local Area Connection" source=dhcp register=PRIMARY
netsh interface ip set wins name="Local Area Connection" source=dhcp

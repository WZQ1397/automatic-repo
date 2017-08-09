netsh interface ip set address name="Local Area Connection" source = static addr = 10.86.164.254 mask=255.255.255.0 
netsh interface ip set address name="Local Area Connection" gateway = 10.86.164.1 gwmetric =0
netsh interface ip set dns name="Local Area Connection" source = static addr = 10.86.130.25 register=PRIMARY
netsh interface ip add dns name="Local Area Connection" addr = 10.86.130.26 index=2
netsh interface teredo set state disabled
netsh interface ipv6 add v6v4tunnel interface=IP6Tunnel 122.144.169.198 216.218.221.6
netsh interface ipv6 add address IP6Tunnel 2001:470:18:3f2::2
netsh interface ipv6 add route ::/0 IP6Tunnel 2001:470:18:3f2::1

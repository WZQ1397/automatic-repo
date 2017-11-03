# frp

## What is frp?

frp is a fast reverse proxy to help you expose a local server behind a NAT or firewall to the internet. Now, it supports tcp, udp, http and https protocol when requests can be forwarded by domains to backward web services.

## Table of Contents

* [What can I do with frp?](#what-can-i-do-with-frp)
* [Status](#status)
* [Architecture](#architecture)
* [Example Usage](#example-usage)
    * [Access your computer in LAN by SSH](#access-your-computer-in-lan-by-ssh)
    * [Visit your web service in LAN by custom domains](#visit-your-web-service-in-lan-by-custom-domains)
    * [Forward DNS query request](#forward-dns-query-request)
    * [Forward unix domain socket](#forward-unix-domain-socket)
    * [Expose your service in security](#expose-your-service-in-security)
    * [Connect website through frpc's network](#connect-website-through-frpcs-network)
* [Features](#features)
    * [Configuration File](#configuration-file)
    * [Dashboard](#dashboard)
    * [Authentication](#authentication)
    * [Encryption and Compression](#encryption-and-compression)
    * [Hot-Reload frpc configuration](#hot-reload-frpc-configuration)
    * [Privilege Mode](#privilege-mode)
        * [Port White List](#port-white-list)
    * [TCP Stream Multiplexing](#tcp-stream-multiplexing)
    * [Support KCP Protocol](#support-kcp-protocol)
    * [Connection Pool](#connection-pool)
    * [Rewriting the Host Header](#rewriting-the-host-header)
    * [Get Real IP](#get-real-ip)
    * [Password protecting your web service](#password-protecting-your-web-service)
    * [Custom subdomain names](#custom-subdomain-names)
    * [URL routing](#url-routing)
    * [Connect frps by HTTP PROXY](#connect-frps-by-http-proxy)
    * [Plugin](#plugin)
* [Development Plan](#development-plan)
* [Contributing](#contributing)
* [Donation](#donation)
    * [AliPay](#alipay)
    * [Wechat Pay](#wechat-pay)
    * [Paypal](#paypal)

<!-- vim-markdown-toc -->

## What can I do with frp?

* Expose any http and https service behind a NAT or firewall to the internet by a server with public IP address(Name-based Virtual Host Support).
* Expose any tcp or udp service behind a NAT or firewall to the internet by a server with public IP address.

## Status

frp is under development and you can try it with latest release version. Master branch for releasing stable version when dev branch for developing.

**We may change any protocol and can't promise backward compatible. Please check the release log when upgrading.**

## Example Usage

Firstly, download the latest programs from [Release](https://github.com/fatedier/frp/releases) page according to your os and arch.

Put **frps** and **frps.ini** to your server with public IP.

Put **frpc** and **frpc.ini** to your server in LAN.

### Access your computer in LAN by SSH

1. Modify frps.ini:

  ```ini
  # frps.ini
  [common]
  bind_port = 7000
  ```

2. Start frps:

  `./frps -c ./frps.ini`

3. Modify frpc.ini, `server_addr` is your frps's server IP:

  ```ini
  # frpc.ini
  [common]
  server_addr = x.x.x.x
  server_port = 7000

  [ssh]
  type = tcp
  local_ip = 127.0.0.1
  local_port = 22
  remote_port = 6000
  ```

4. Start frpc:

  `./frpc -c ./frpc.ini`

5. Connect to server in LAN by ssh assuming that username is test:

  `ssh -oPort=6000 test@x.x.x.x`

### Visit your web service in LAN by custom domains

Sometimes we want to expose a local web service behind a NAT network to others for testing with your own domain name and unfortunately we can't resolve a domain name to a local ip.

However, we can expose a http or https service using frp.

1. Modify frps.ini, configure http port 8080:

  ```ini
  # frps.ini
  [common]
  bind_port = 7000
  vhost_http_port = 8080
  ```

2. Start frps:

  `./frps -c ./frps.ini`

3. Modify frpc.ini and set remote frps server's IP as x.x.x.x. The `local_port` is the port of your web service:

  ```ini
  # frpc.ini
  [common]
  server_addr = x.x.x.x
  server_port = 7000

  [web]
  type = http
  local_port = 80
  custom_domains = www.yourdomain.com
  ```

4. Start frpc:

  `./frpc -c ./frpc.ini`

5. Resolve A record of `www.yourdomain.com` to IP `x.x.x.x` or CNAME record to your origin domain.

6. Now visit your local web service using url `http://www.yourdomain.com:8080`.

### Forward DNS query request

1. Modify frps.ini:

  ```ini
  # frps.ini
  [common]
  bind_port = 7000
  ```

2. Start frps:

  `./frps -c ./frps.ini`

3. Modify frpc.ini, set remote frps's server IP as x.x.x.x, forward dns query request to google dns server `8.8.8.8:53`:

  ```ini
  # frpc.ini
  [common]
  server_addr = x.x.x.x
  server_port = 7000

  [dns]
  type = udp
  local_ip = 8.8.8.8
  local_port = 53
  remote_port = 6000
  ```

4. Start frpc:

  `./frpc -c ./frpc.ini`

5. Send dns query request by dig:

  `dig @x.x.x.x -p 6000 www.goolge.com`

### Forward unix domain socket

Using tcp port to connect unix domain socket like docker daemon.

Configure frps same as above.

1. Start frpc with configurations:

  ```ini
  # frpc.ini
  [common]
  server_addr = x.x.x.x
  server_port = 7000

  [unix_domain_socket]
  type = tcp
  remote_port = 6000
  plugin = unix_domain_socket
  plugin_unix_path = /var/run/docker.sock
  ```

2. Get docker version by curl command:

  `curl http://x.x.x.x:6000/version`

### Expose your service in security

For some services, if expose them to the public network directly will be a security risk.

**stcp(secret tcp)** help you create a proxy avoiding any one can access it.

Configure frps same as above.

1. Start frpc, forward ssh port and `remote_port` is useless:

  ```ini
  # frpc.ini
  [common]
  server_addr = x.x.x.x
  server_port = 7000

  [secret_ssh]
  type = stcp
  sk = abcdefg
  local_ip = 127.0.0.1
  local_port = 22
  ```

2. Start another frpc in which you want to connect this ssh server:

  ```ini
  # frpc.ini
  [common]
  server_addr = x.x.x.x
  server_port = 7000

  [secret_ssh_vistor]
  type = stcp
  role = vistor
  server_name = secret_ssh
  sk = abcdefg
  bind_addr = 127.0.0.1
  bind_port = 6000
  ```

3. Connect to server in LAN by ssh assuming that username is test:

  `ssh -oPort=6000 test@127.0.0.1`

### Connect website through frpc's network

Configure frps same as above.

1. Start frpc with configurations:

  ```ini
  # frpc.ini
  [common]
  server_addr = x.x.x.x
  server_port = 7000

  [http_proxy]
  type = tcp
  remote_port = 6000
  plugin = http_proxy # or socks5
  ```

2. Set http proxy or socks5 proxy `x.x.x.x:6000` in your browser and visit website through frpc's network.

## Features

### Dashboard

Check frp's status and proxies's statistics information by Dashboard.

Configure a port for dashboard to enable this feature:

```ini
[common]
dashboard_port = 7500
# dashboard's username and password are both optional，if not set, default is admin.
dashboard_user = admin
dashboard_pwd = admin
```

Then visit `http://[server_addr]:7500` to see dashboard, default username and password are both `admin`.

### Authentication

Since v0.10.0, you only need to set `privilege_token` in frps.ini and frpc.ini.

Note that time duration between server of frpc and frps mustn't exceed 15 minutes because timestamp is used for authentication.

Howerver, this timeout duration can be modified by setting `authentication_timeout` in frps's configure file. It's defalut value is 900, means 15 minutes. If it is equals 0, then frps will not check authentication timeout.

### Encryption and Compression

Defalut value is false, you could decide if the proxy will use encryption or compression:

```ini
# frpc.ini
[ssh]
type = tcp
local_port = 22
remote_port = 6000
use_encryption = true
use_compression = true
```

### Hot-Reload frpc configuration

First you need to set admin port in frpc's configure file to let it provide HTTP API for more features.

```ini
# frpc.ini
[common]
admin_addr = 127.0.0.1
admin_port = 7400
```

Then run command `frpc -c ./frpc.ini --reload` and wait for about 10 seconds to let frpc create or update or delete proxies.

**Note that parameters in [common] section won't be modified except 'start' now.**

### Privilege Mode

Privilege mode is the default and only mode support in frp since v0.10.0. All proxy configurations are set in client.

#### Port White List

`privilege_allow_ports` in frps.ini is used for preventing abuse of ports:

```ini
# frps.ini
[common]
privilege_allow_ports = 2000-3000,3001,3003,4000-50000
```

`privilege_allow_ports` consists of a specific port or a range of ports divided by `,`.

### TCP Stream Multiplexing

frp support tcp stream multiplexing since v0.10.0 like HTTP2 Multiplexing. All user requests to same frpc can use only one tcp connection.

You can disable this feature by modify frps.ini and frpc.ini:

```ini
# frps.ini and frpc.ini, must be same
[common]
tcp_mux = false
```

### Support KCP Protocol

frp support kcp protocol since v0.12.0.

KCP is a fast and reliable protocol that can achieve the transmission effect of a reduction of the average latency by 30% to 40% and reduction of the maximum delay by a factor of three, at the cost of 10% to 20% more bandwidth wasted than TCP.

Using kcp in frp:

1. Enable kcp protocol in frps:

  ```ini
  # frps.ini
  [common]
  bind_port = 7000
  # kcp needs to bind a udp port, it can be same with 'bind_port'
  kcp_bind_port = 7000
  ```

2. Configure the protocol used in frpc to connect frps:

  ```ini
  # frpc.ini
  [common]
  server_addr = x.x.x.x
  # specify the 'kcp_bind_port' in frps
  server_port = 7000
  protocol = kcp
  ```

### Connection Pool

By default, frps send message to frpc for create a new connection to backward service when getting an user request.If a proxy's connection pool is enabled, there will be a specified number of connections pre-established.

This feature is fit for a large number of short connections.

1. Configure the limit of pool count each proxy can use in frps.ini:

  ```ini
  # frps.ini
  [common]
  max_pool_count = 5
  ```

2. Enable and specify the number of connection pool:

  ```ini
  # frpc.ini
  [common]
  pool_count = 1
  ```

### Rewriting the Host Header

When forwarding to a local port, frp does not modify the tunneled HTTP requests at all, they are copied to your server byte-for-byte as they are received. Some application servers use the Host header for determining which development site to display. For this reason, frp can rewrite your requests with a modified Host header. Use the `host_header_rewrite` switch to rewrite incoming HTTP requests.

```ini
# frpc.ini
[web]
type = http
local_port = 80
custom_domains = test.yourdomain.com
host_header_rewrite = dev.yourdomain.com
```

If `host_header_rewrite` is specified, the Host header will be rewritten to match the hostname portion of the forwarding address.

### Get Real IP

Features for http proxy only.

You can get user's real IP from http request header `X-Forwarded-For` and `X-Real-IP`.

**Note that now you can only get these two headers in first request of each user connection.**

### Password protecting your web service

Anyone who can guess your tunnel URL can access your local web server unless you protect it with a password.

This enforces HTTP Basic Auth on all requests with the username and password you specify in frpc's configure file.

It can only be enabled when proxy type is http.

```ini
# frpc.ini
[web]
type = http
local_port = 80
custom_domains = test.yourdomain.com
http_user = abc
http_pwd = abc
```

Visit `http://test.yourdomain.com` and now you need to input username and password.

### Custom subdomain names

It is convenient to use `subdomain` configure for http、https type when many people use one frps server together.

```ini
# frps.ini
subdomain_host = frps.com
```

Resolve `*.frps.com` to the frps server's IP.

```ini
# frpc.ini
[web]
type = http
local_port = 80
subdomain = test
```

Now you can visit your web service by host `test.frps.com`.

Note that if `subdomain_host` is not empty, `custom_domains` should not be the subdomain of `subdomain_host`.

### URL routing

frp support forward http requests to different backward web services by url routing.

`locations` specify the prefix of URL used for routing. frps first searches for the most specific prefix location given by literal strings regardless of the listed order.

```ini
# frpc.ini
[web01]
type = http
local_port = 80
custom_domains = web.yourdomain.com
locations = /

[web02]
type = http
local_port = 81
custom_domains = web.yourdomain.com
locations = /news,/about
```
Http requests with url prefix `/news` and `/about` will be forwarded to **web02** and others to **web01**.

### Connect frps by HTTP PROXY

frpc can connect frps using HTTP PROXY if you set os environment `HTTP_PROXY` or configure `http_proxy` param in frpc.ini file.

It only works when protocol is tcp.

```ini
# frpc.ini
[common]
server_addr = x.x.x.x
server_port = 7000
http_proxy = http://user:pwd@192.168.1.128:8080
```

### Plugin

frpc only forward request to local tcp or udp port by default.

Plugin is used for providing rich features. There are built-in plugins such as **unix_domain_socket**, **http_proxy**, **socks5** and you can see [example usage](#example-usage).

Specify which plugin to use by `plugin` parameter. Configuration parameters of plugin should be started with `plugin_`. `local_ip` and `local_port` is useless for plugin.

Using plugin **http_proxy**:

```ini
# frpc.ini
[http_proxy]
type = tcp
remote_port = 6000
plugin = http_proxy
plugin_http_user = abc
plugin_http_passwd = abc
```

`plugin_http_user` and `plugin_http_passwd` are configuration parameters used in `http_proxy` plugin.

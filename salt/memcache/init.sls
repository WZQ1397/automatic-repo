# Memcache states and configuration
memcache:
  pkg.installed:
    - name: memcached
  service.running:
    - name: memcached
    - require:
      - pkg: memcached
      - file: /etc/memcached.conf
    - watch:
      - file: /etc/memcached.conf

# Configuration file for memcached
/etc/memcached.conf:
  file.managed:
    - source: salt://memcache/memcached.conf
    - user: root
    - group: root
    - mode: 644

/etc/security/limits.conf:
  file.append:
    - text:
      - memcache	soft	nofile		10000
      - memcache	hard	nofile		10240

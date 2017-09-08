telegraf-service:
  service.running:
    - name: telegraf
    - enable: True
    - watch:
      - sls: telegraf.install
      - sls: telegraf.config
    - require:
      - sls: telegraf.install
      - sls: telegraf.config

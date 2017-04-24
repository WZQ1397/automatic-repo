logstash-download:
  archive.extracted:
    - name: /elk/
    - source: https://artifacts.elastic.co/downloads/logstash/logstash-5.3.1.zip
    - source_hash: 1bb280732c4fe94d0fab43be6de8e8c20dc17ed4
    - archive_format: zip
    - if_missing: /elk/logstash-5.3.1/
    - user: root
    - group: root
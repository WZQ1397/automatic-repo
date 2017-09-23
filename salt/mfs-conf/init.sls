{% set mfsconf = mfs-conf %}

/usr/local/mfs/etc/:
  file.recurse:
    - source: salt://{{ mfsconf }}/
    - include_empty: True
    - user: root
    - dir_mode: 775
    - file_mode: '0644'
    - exclude_pat: *.example
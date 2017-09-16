include:
    - .download_directory

D:\software\win_client.zip:
    file.managed:
        - source: salt://win/repo/win_client.zip

rsync_client:
    cmd.run:
        - name: >
            "C:\program files\7-zip\7z.exe" 
            x D:\software\win_client.zip
            -o"C:\program files" -y
        - unless: dir "C:\program files\win_client" >nul
        - requires:
            - file: D:\software\win_client.zip
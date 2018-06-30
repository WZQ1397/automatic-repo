configuration=
{
    daemon=true,
    pathSeparator="/",

    logAppenders=
    {
        {
            name="console appender",
            type="coloredConsole",
            level=2
        },
        {
            name="file appender",
            type="file",
            level=2,
            fileName="/usr/local/eyou/mail/log/crtmpserver/crtmpserver.log",
            fileHistorySize=10,
            fileLength=1024*1024*1024*2,
            singleLine=true
        },
    },

    applications=
    {
        rootDirectory="/usr/local/eyou/mail/opt/lib/crtmpserver/applications",
        {
            description="eYou gearman auth",
            name="demogm",
            protocol="dynamiclinklibrary",
            gearmanNodes= {
               s1="127.0.0.1:4730",
            },
            validateHandshake=true,
            renameBadFiles=false,
            acceptors =
            {
                {
                    ip="0.0.0.0",
                    port=1935,
                    protocol="inboundRtmp",
                },
            },
        },
        {
            description="eYou FLV Recorder",
            name="flvplayback",
            protocol="dynamiclinklibrary",
            default=true,
            aliases=
            {
                "emmedia"
            },
            validateHandshake=true,
            keyframeSeek=true,
            seekGranularity=600, -- 单位秒, 必须在 0.1 - 600 之间
            clientSideBuffer=5, -- 单位秒, 必须在 5 - 30 之间
            generateMetaFiles=false, -- 是否在启动的时候生成 seek/meta 文件
            renameBadFiles=true,
            mediaFolder="/usr/local/eyou/mail/tmp/rtmp/",
        },
    },
}

from fabric.api import env, run, path, settings, shell_env, prefix, task

env.hosts = ['172.16.6.202','172.16.6.203']
env.user='root'
env.password='edong'

@task(alias='env',default=True)
def env_set():
    with path('/opt/'):
        run('echo $PATH')
    run('echo $PATH')
    #fixme ALL para you can use http://docs.fabfile.org/en/1.13/usage/env.html
    with settings(warn_only=True):
        run('echo $USER')
    with prefix('free'):
        with shell_env(JAVA_HOME='/opt/java'):
            run('echo $JAVA_HOME')

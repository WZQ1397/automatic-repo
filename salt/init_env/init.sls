# Mainly user related tools and other handy stuff
include:
  - system.limits
  - system.ntp
  
bash_completion:
  pkg.installed:
    - name: bash-completion

htop:
  pkg.installed[]

wget:
  pkg.installed[]
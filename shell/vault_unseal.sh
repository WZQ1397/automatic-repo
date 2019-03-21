shopt -s expand_aliases
export VAULT_ADDR=http://127.0.0.1:8200
alias vault='docker exec -it vault-dev vault "$@"'
vault init -address=${VAULT_ADDR} > keys.txt
vault unseal -address=${VAULT_ADDR} $(grep "Key 1:" keys.txt | awk '{print $NF}')
vault unseal -address=${VAULT_ADDR} $(grep "Key 2:" keys.txt | awk '{print $NF}')
vault unseal -address=${VAULT_ADDR} $(grep "Key 3:" keys.txt | awk '{print $NF}')
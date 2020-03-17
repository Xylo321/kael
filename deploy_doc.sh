cd ./doc
make clean
sphinx-apidoc -o ./ ../reborn/
make html
cd ..
ssh wobuhuizaibeishang@serv_pro "rm -rf ~/static_server/reborn"
scp -r ./doc/_build/html wobuhuizaibeishang@serv_pro:~/static_server/reborn
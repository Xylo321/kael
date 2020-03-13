cd ./doc
make clean
sphinx-apidoc -o ./ ../reborn/
make html
cd ..
scp -r ./doc/_build/html wobuhuizaibeishang@serv_pro:~/static_server/reborn
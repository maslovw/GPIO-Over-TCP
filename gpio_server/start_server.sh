echo "start gpio controle 5001"
socat tcp-l:5001,reuseaddr,fork,crlf system:"gpio_server/socat_gpio_cmd.sh",fdin=3,fdout=4 &

#!/bin/bash

echo "hi" >&4 # send to tcp client 'hi'
while read -u 3 BUFFER # recieve from tcp client
do 
	scommand="gpio $BUFFER"
	echo "$scommand" >&4 # send command string back to client
	gpio $BUFFER >&4 2>&1 # execute gpio command
done

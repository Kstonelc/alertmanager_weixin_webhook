#!/bin/sh
if [ "x" == "x$chatKey" ]; then
    echo "FAIL: chatKey is not set"
    exit 1
else
    echo "chatKey is $chatKey"
fi

if [ "x" == "x$env" ]; then
    echo "FAIL: env is not set"
    exit 1
else
    echo "env is $env"
fi

sed -i s/xchatKeyx/"$chatKey"/ app.py
sed -i s/xenvx/"$env"/ app.py
gunicorn -w 4 -b 0.0.0.0:5000 app:app

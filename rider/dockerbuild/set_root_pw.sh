#!/bin/bash

if [ -f /.root_pw_set ]; then
        echo "Root password already set!"
        exit 0
fi

#PASS=${ROOT_PASS:-$(pwgen -s 12 1)}
PASS=notchangeme
_word=$( [ ${ROOT_PASS} ] && echo "preset" || echo "random" )
echo "=> Setting a ${_word} password to the root user"
echo "root:$PASS" | chpasswd

echo "=> Done!"
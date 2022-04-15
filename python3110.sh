#!/bin/bash

echo ${1}
echo ${2}
ssh root@${1} "service ${2} status|egrep 'Active'|awk '{ print \$2 }'|head -n 1"

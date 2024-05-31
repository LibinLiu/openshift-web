#!/bin/sh
if [ X"$#" != X"1"  ]; then
    echo "please spcify your conf file"
    exit 1
fi

conf_file=$1
test_script="config.py"
#uuid=$(uuidgen)
#tmp_test_script="${test_script}.${uuid}.tmp"
#cp -f $test_script $tmp_test_script

while read -r line; do
   line_start=$(echo "$line" |cut -d= -f1 )
   sed -i "/^${line_start}=/c${line}" $test_script
done<"$conf_file"
ret=$?
rm -rf $1
exit $ret



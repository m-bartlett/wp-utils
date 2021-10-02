#!/usr/bin/env bash
mkdir -p ./1080/
for f in *; do 
	res=$(exiv2 $f 2>/dev/null | grep Image\ size | sed 's/^.*: //g') 
	[[ $res == "1920 x 1080" ]] && mv $f 1080/
done

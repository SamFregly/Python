sed -i '/^\s*$/d' parsertest.json
sed -i 's/\\u....//g' parsertest.json
sed -i 's/\\\///g' parsertest.json
#sed -i 's/\s*[^}]$/""\}/g' parsertest.json
#sed -i 's/\}""\}/\}/g' parsertest.json

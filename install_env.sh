#!/bin/bash
BASE=$(pwd)
echo "📁 当前目录: $BASE"

apt-get install -y default-jdk

mkdir -p $BASE/joern
wget -q https://github.com/joernio/joern/releases/download/v1.1.1/joern-cli.zip
unzip -q joern-cli.zip -d $BASE/joern
chmod +x $BASE/joern/joern-cli/joern-parse
chmod +x $BASE/joern/joern-cli/joern

echo "✅ Joern安装完成: $BASE/joern/joern-cli/"

#!/bin/bash
BASE=$(pwd)
echo "📁 当前目录: $BASE"
apt-get install -y default-jdk
mkdir -p $BASE/joern_new
wget -q https://github.com/joernio/joern/releases/download/v1.0.105/joern-cli.zip
unzip -q joern-cli.zip -d $BASE/joern_new
chmod +x $BASE/joern_new/joern-cli/joern-parse
chmod +x $BASE/joern_new/joern-cli/joern
# 复制 graph-for-funcs.sc 到正确位置
cp $BASE/joern/graph-for-funcs.sc $BASE/joern_new/graph-for-funcs.sc
echo "✅ Joern安装完成: $BASE/joern_new/joern-cli/"
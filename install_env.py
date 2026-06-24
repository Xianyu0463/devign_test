import os
import subprocess

# 自动定位devign_test目录
BASE = os.getcwd()
for candidate in ['/content/devign_test/devign_test', '/content/devign_test']:
    if os.path.exists(candidate):
        BASE = candidate
        break

os.chdir(BASE)
print(f"📁 当前目录: {BASE}")

# 安装Python依赖
os.system("pip install pandas scikit-learn gensim==4.3.3 cpgclientlib")
os.system("pip install torch torch-geometric")

# 安装Joern
subprocess.run(["bash", os.path.join(BASE, "install_env.sh")], check=True)

print("✅ 环境配置完成！")

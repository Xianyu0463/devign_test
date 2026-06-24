import os
import subprocess

# 自动cd到devign_test目录
BASE = os.getcwd()
DEVIGN = os.path.join(BASE, "devign_test")

if os.path.exists(DEVIGN):
    os.chdir(DEVIGN)
    BASE = DEVIGN
elif os.path.basename(BASE) == "devign_test":
    pass  # 已经在devign_test目录里
else:
    print(f"⚠️ 找不到devign_test目录，使用当前目录: {BASE}")

print(f"📁 当前目录: {os.getcwd()}")

# 安装Python依赖
os.system("pip install pandas scikit-learn gensim==4.3.3 cpgclientlib")
os.system("pip install torch torch-geometric")

# 安装Joern
subprocess.run(["bash", os.path.join(BASE, "install_env.sh")], check=True)

print("✅ 环境配置完成！")

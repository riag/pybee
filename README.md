# pybee

   pybee 提供一些辅助函数，方便使用 Python 来写系统维护/部署脚本, 使用 Bash 写维护/部署脚本实在不爽；例如提供 sed、awk 工具对应的功能函数，但 pybee 目标不是编写一个 python 版的 sed/awk 工具



## 编译

### 安装依赖工具

* python 3.4+
* pipenv

执行下面命令安装依赖包

```
pipenv install --dev
```



### 编译

```
python3 setup.py build
```

打包 wheel 格式

```
python3 setup.py bdist_wheel
```

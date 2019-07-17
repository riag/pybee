# pybee

   pybee 提供一些辅助函数，方便使用 Python 来写系统维护/部署脚本, 使用 Bash 写维护/部署脚本实在不爽；例如提供 sed、awk 工具对应的功能函数，但 pybee 目标不是编写一个 python 版的 sed/awk 工具



## 编译

### 安装依赖工具

* python 3.4+
* poetry

执行下面命令安装依赖包

```
poetry install
```

### 编译

```
poetry build
```

### pybee 模块
  pybee 模块封装了或者增加常见系统维护需要的函数

* pybee.path 增强 os.path 模块的一些函数
* pybee.compress 封装 zip/tar.gz 压缩函数
* pybee.sed 提供 sed 工具类似功能的函数 
* pybee.ask 封装在 termia 常见交互操作的函数
* pybee.importutil 提供把一个 py 文件当作模块 import 的函数

还有其他模块，这里就不一一列出

### pybee.action 模块
  在 pybee 模块的基础上把常见的操作封装成 action，下面就是一个列子

  ```
import pybee

ac = pybee.action.ActionContext([
    ('SCRIPT_DIR', pybee.path.get_script_path(__file__)),
    ('DIST_DIR', '$CURRENT_DIR/dist'),
    ('OUT_PUT_DIR', '$DIST_DIR/test-demo-portable'),
])

ac.prepare_dir(
    [
        '$DIST_DIR', '$OUT_PUT_DIR',
        '$OUT_PUT_DIR/portable',
    ]
)

ac.check_bin([
    ('gradle','please install gradle', 'GRADLE_BIN'),
])

ac.exec_cmd(
    [
        '$GRADLE_BIN', 'packDist', '-x', 'test'
    ]
)

ac.unzip(
    '$DIST_DIR/test-demo/test-demo.jar',
    '$OUT_PUT_DIR'
)


def ignore_config_files(src, names):
    return ['project.groovy', ]

ac.copy(
    [
        ('$CURRENT_DIR/config', '$OUT_PUT_DIR', {
            'ignore': ignore_config_files
        }),
        ('$CURRENT_DIR/public', '$OUT_PUT_DIR'),
    ]
)

ac.copy(
    [
        ('run.ps1', '$OUT_PUT_DIR'),
        ('run.sh', '$OUT_PUT_DIR'),
        ('portable.groovy', '$OUT_PUT_DIR/config'),
    ],
    work_dir='$SCRIPT_DIR/portable'
)

ac.zip(
    '$OUT_PUT_DIR',
    '$DIST_DIR/test-demo-portable-{datetime}.zip',
    env_name='DIST_FILE'
)


def print_success(context):
    print('')
    zip_file = context.get_env('DIST_FILE')
    print('pack successfully, dist file is %s' % zip_file)


ac.execute(succ_func=print_success)
  ```
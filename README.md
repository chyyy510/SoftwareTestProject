# SoftwareTestProject

## 注意事项

- 使用`python -m venv .venv`创建名为`.venv`的虚拟环境，或者可将`.venv`替换为你想要的名字，并在`.gitignore`文件中加入`xxx/`，`xxx`为你的虚拟环境的名字
- 后续的开发都在该虚拟环境中进行
- 使用`pip install -r requirements.txt`安装所有依赖，当开发过程中引入新的依赖时，在提交更改之前，使用`pip freeze > requirements.txt`更新依赖，并一起提交
- 在本项目根目录新建.env文件，在其中设置必要的环境变量，如`QIANFAN_AK`和`QIANFAN_SK`，格式如下：
    ```
    QIANFAN_AK=Wf9IufaWDkGnSiQgeFaEC5Wa
    QIANFAN_SK=W0RsfiiulYBDO86fNVpq6wJg8B6EjwVq
    ```

## 文件夹
- `samples/`为待测试的代码文件
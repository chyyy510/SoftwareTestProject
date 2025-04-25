# SoftwareTestProject

## 注意事项

- 使用`python -m venv .venv`创建名为`.venv`的虚拟环境，或者可将`.venv`替换为你想要的名字，并在`.gitignore`文件中加入`xxx/`，`xxx`为你的虚拟环境的名字
- 后续的开发都在该虚拟环境中进行
- 使用`pip install -r requirements.txt`安装所有依赖，当开发过程中引入新的依赖时，在提交更改之前，使用`pip freeze > requirements.txt`更新依赖，并一起提交
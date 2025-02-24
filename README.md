<p align="center">
    <picture>
        <img width="205" alt="XH Agent Logo" src="./doc/logo.png">
    </picture>
</p>
<h3 align="center">
    广州新华学院实验报告编写工具  省时、智能、规范!
</h3>
<p align="center">
  <a href="http://www.zivye.asia/"><strong>网站</strong></a> •
  <a href="https://github.com/Yezery/XH_Agent"><strong>项目仓库</strong></a>
</p>
<div align="center"><a href="https://github.com/Yezery/XH_Agent/releases/latest"><img width="220" alt="Download button" src="./doc/download.png"></a> </div>

[![PyPI - Version](https://img.shields.io/pypi/v/kiln-ai.svg?logo=pypi&label=PyPI&logoColor=gold)![PyPI - Python Version](https://img.shields.io/pypi/pyversions/kiln-ai.svg?logo=python&label=Python&logoColor=gold)](https://pypi.org/project/kiln-ai/)[![MacOS](https://img.shields.io/badge/MacOS-black?logo=apple)![Windows](https://img.shields.io/badge/Windows-0067b8.svg?logo=data:image/svg%2bxml;base64,PD94bWwgdmVyc2lvbj0iMS4wIiBlbmNvZGluZz0idXRmLTgiPz4KPHN2ZyBmaWxsPSIjZmZmIiB2aWV3Qm94PSIwIDAgMzIgMzIiIHZlcnNpb249IjEuMSIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4KPHBhdGggZD0iTTE2Ljc0MiAxNi43NDJ2MTQuMjUzaDE0LjI1M3YtMTQuMjUzek0xLjAwNCAxNi43NDJ2MTQuMjUzaDE0LjI1NnYtMTQuMjUzek0xNi43NDIgMS4wMDR2MTQuMjU2aDE0LjI1M3YtMTQuMjU2ek0xLjAwNCAxLjAwNHYxNC4yNTZoMTQuMjU2di0xNC4yNTZ6Ij48L3BhdGg+Cjwvc3ZnPg==)](https://github.com/Kiln-AI/Kiln/releases/latest) <img alt="vue3" src="https://img.shields.io/badge/-Vue3-6DB33F?style=flat-square&logo=vuedotjs&logoColor=white" /><img alt="tailwind" src="https://img.shields.io/badge/-Tailwindcss-00BFFF?style=flat-square&logo=Tailwindcss&logoColor=white" /><img alt="fastapi" src="https://img.shields.io/badge/-FastAPI-6DB33F?style=flat-square&logo=fastapi&logoColor=white" />![Github Downsloads](https://img.shields.io/github/downloads/Yezery/XH_Agent/total)

## 特点

- 🚀 **直观的桌面应用程序**: 适用于 Windows、MacOS 的应用程序.
- 🧠 **智能 Ai 心得**: 导入实验报告模版，自动生成心得.
- 🖊️ **文案智能重写**: 输入的描述文本进行智能重写润色.
- 📂 **图片自动排版**：批量拖拽图片自动排版.
- 🤝 **更新支持**: 软件一键安装更新迭代.
- 🔒 **隐私**: 本地化隐私数据.不会上传云端如您的 API Key也可使用 Ollama 在本地运行.
- 🤖 **对接多款 Ai 模型**: 对接本地 Ollama、Deepseek、Hunyuan、硅基流动 Ai 平台 等多个国内 AI 大模型.
- 💰 **开源免费**: 软件免费下载，源码公开.

## Demo

在这个例子里我们使用本地 Ollama Ai 快速进行了一个Ai心得的生成和实验报告的编写工作，包括页眉的修改、文件的重命名、文档内容的规范化排版.

<img alt="demo1" src="./doc/demo.gif">

## TODO

- [ ] 实验报告逆向工程
- [ ] 对接多模态模型实现图片转文字

## 项目构建 & 开发者

新开发者必须同意开发者许可协议.

我们使用 [uv](https://github.com/astral-sh/uv) 工具去管理 Python 环境与依赖 ，并且使用 [pnpm](https://www.pnpm.cn/) 去管理 web UI.

Windows： [nvm](https://github.com/coreybutler/nvm-windows/releases)  管理工具 

MacOS：n 管理工具：**npm i -g n**

```bash
# 安装 uv: https://github.com/astral-sh/uv
uv sync
cd app/web_ui
# 设置 npm 国内源 
npm config set registry https://registry.npmmirror.com/
# 安装 pnpm
npm i -g pnpm
# 安装项目依赖
pnpm i
```

### 运行开发服务器

分别运行 web-UI 和 Python 服务器有助于开发，因为两者都可以热重载.

运行具有自动重新加载功能的 API 服务器、 Web UI 进行开发，请执行以下操作：

1、在您的项目终端输入

```bash
uv run python -m app.desktop.dev_server
```

2、打开另一个终端，cd 到 Web UI 目录并启动 dev 开发模式

```bash
cd app/web_ui
pnpm run dev
```

3. 打开网页: http://localhost:5173

### 运行和构建桌面应用程序

#### ⚠️ MacOS 环境前置条件

> [!WARNING]
>
> UV python 目前不包括 TK/TCL包. 但是，我们安装了包含 TK/TCL 包在内的系统 python，需要告诉 UV venv 使用系统的 python.

```bash
# 用 homebrew 安装 python 3.12 和 python-tk 3.12
brew install python-tk@3.12
brew install python@3.12

# 检查 uv 查看 hoembrew 版本
uv python list --python-preference only-system

# 设置 python 3.12 UV 管理项目 .VENV
uv venv --python 3.12 --python-preference only-system

# 检查 python 版本
uv run python --version

# 运行开发状态下的桌面程序
uv run python -m app.desktop.desktop
```

#### 构建桌面应用程序

如果您需要在本地构建桌面应用程序，可以使用：

```ini
cd app/desktop
uv run ./build_desktop_app.sh --build-bootloader
```

#### 构建安装包（可选）

##### MacOS

```bash
# npm install -g create-dmg
cd app/desktop
create-dmg --volname "XH Agent setup" --background "./bg.svg" --window-pos 400 200 --window-size 660 400 --icon-size 100 --icon "XH Agent.app" 160 185 --hide-extension "XH Agent.app" --app-drop-link 500 185 --volicon "./installer.icns" build/dist/'XH Agent-darwin.dmg' build/dist/'XH Agent.app'
```

##### Windwos

1、安装：[Inno Setup](https://jrsoftware.org/isdl.php)

2、点击 **WinInnoSetup.iss**（app/desktop/WinInnoSetup.iss）

3、开始构建

## 关于

### 优化改进与市场调研

这个实验报告工具很初级，我很希望您能够在官网提供更多的实验报告编写需求，便于我们不断改进项目.

### 我很希望和对代码与计算机技术的你一起开发维护一些有意思的软件项目

您可以点击查看我的Github主页，了解更多我开发的有趣的软件项目与工具，很高兴您可以加入我！

WeChat：Y__OOO_O

Email：1172029997@qq.com

### 软件开发不易！很希望这个软件帮助到您！也希望您可以请我喝一杯 ☕️ ！

<img width="220" alt="reward" src="./doc/reward.jpg">

开发许可证

 [MIT License](./LICENSE.txt)


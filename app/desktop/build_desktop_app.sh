#!/usr/bin/env bash

set -e

# 移动到项目的/app目录
cd "$(dirname "$0")"
cd ..
APP_DIR=$PWD

if [[ $* != *--skip-web* ]]; then
  # 构建 web 界面
  echo "Building web UI"
  cd web_ui
  pnpm install
  pnpm run build
  cd $APP_DIR
fi

# 构建引导加载程序有助于避免被 windows 上的防病毒软件错误地检测为恶意软件。
# 安装 pyinstaller，构建引导加载程序，并将其安装到pyproject桌面pyproject中。
if [[ $* == *--build-bootloader* ]]; then
  echo "Building pyinstaller inlucding bootloader"
  mkdir -p desktop/build/bootloader
  cd desktop/build/bootloader
  curl -L https://github.com/pyinstaller/pyinstaller/archive/refs/tags/v6.11.1.tar.gz -o pyinstaller.tar.gz
  tar -xzf pyinstaller.tar.gz
  mv pyinstaller-6.11.1 pyinstaller
  cd pyinstaller/bootloader
  python ./waf all

  #将刚刚构建的pyinstaller安装到 desktop 项目中
  cd $APP_DIR/desktop
  uv add build/bootloader/pyinstaller

  # 返回到项目的 /app 目录
  cd $APP_DIR
fi

mkdir -p desktop/build

echo "Building for $(uname)"
if [ "$(uname)" == "Darwin" ]; then
  echo "Building MacOS app"
  cp desktop/mac_taskbar.png desktop/build/taskbar.png
  # onedir启动速度更快，在MacOS.app捆绑包中看起来仍然像1个文件
  PLATFORM_OPTS="--onedir --windowed --icon=../mac_icon.png"

  PY_PLAT=$(python -c 'import platform; print(platform.machine())')
  echo "Building MacOS app for single platform ($PY_PLAT)"
elif [[ "$(uname)" =~ ^MINGW64_NT-10.0 ]] || [[ "$(uname)" =~ ^MSYS_NT-10.0 ]]; then
  echo "Building Windows App"
  cp desktop/win_taskbar.png desktop/build/taskbar.png
  PLATFORM_OPTS="--windowed --splash=../win_splash.png --icon=../win_icon.ico"
elif [ "$(uname)" == "Linux" ]; then
  echo "Building Linux App"
  cp desktop/mac_taskbar.png desktop/build/taskbar.png
  PLATFORM_OPTS="--windowed --onefile --splash=../win_splash.png --icon=../mac_icon.png"
else
  echo "Unsupported operating system: $(uname)"
  exit 1
fi

# Builds the desktop app
# TODO: use a spec instead of long winded command line
pyinstaller $(printf %s "$PLATFORM_OPTS")  \
  --add-data "./taskbar.png:." --add-data "../../web_ui/dist:./web_ui/build" \
  --noconfirm --distpath=./desktop/build/dist --workpath=./desktop/build/work \
  -n "XH Agent" --specpath=./desktop/build \
  --paths=. \
  ./desktop/desktop.py


# MacOS apps have symlinks, and GitHub artifact upload zip will break them. Tar instead.
if [[ $* == *--compress-mac-app* && "$(uname)" == "Darwin" ]]; then
  echo "Compressing MacOS app"
  cd ./desktop/build/dist
  tar czpvf XH Agent.app.tgz XH Agent.app
  rm -r XH Agent.app
  cd ../../..
fi
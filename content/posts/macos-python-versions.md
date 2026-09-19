---
title: "MacOS下使用python的多版本方案"
date: 2018-01-01
categories: ["机器学习相关"]
tags: ["Mac", "Python"]
description: "解决Python 2.x与Python 3.x版本共存的方案"
url: "/MacOS下使用python的多版本方案.html"
---

## 背景

MacOS系统本身自带python，但是版本仍然停留在python2.7。私以为python2与python3语言差别比较大，python3额外一些新特性如**“通配符**，字典可排序，统一的Unicode编码”**等，都值得去尝试。为此，保证电脑上两个版本都能共存是很必要的。

## 方案一：使用pyenv兼容多版本

pyenv 是轻量的Python版本管理器，帮助你在电脑上建立多个版本的python环境，并提供方便的切换方法。pyenv-virtualenv 是 pyenv的扩展工具（类Unix系统上），可以搭建虚拟且独立的python环境，可以使每个项目环境与其他项目独立开来，保持环境的干净，解决包冲突问题。

### 1. 使用Mac OSX的 Homebrew 安装

Homebrew作为OS X上强大的包管理器，为系统软件提供了非常方便的安装方式，独特式的解决了包的依赖问题，并不再需要烦人的sudo，一键式编译，无参数困扰，安装Homebrew：

```plain
~$ curl -L https://raw.githubusercontent.com/yyuu/pyenv-installer/master/bin/pyenv-installer | bash
```

安装完成后，根据提示将如下语句加入到 `～/.bash_profile` 或`~/.bashrc` 中:

```plain
port PYENV_ROOT="$HOME/.pyenv"
export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
eval "$(pyenv virtualenv-init -)" # 这句可以不加
```

### 2. pyenv 常用命令

使用 `pyenv commands` 显示所有可用命令

#### python 安装与卸载

```plain
~$ pyenv install 2.7.3   # 安装python
~$ pyenv uninstall 2.7.3 # 卸载python
```

#### python切换

```plain
~$ pyenv global 2.7.3  # 设置全局的 Python 版本，通过将版本号写入 ~/.pyenv/version 文件的方式。
~$ pyenv local 2.7.3 # 设置 Python 本地版本，通过将版本号写入当前目录下的 .python-version 文件的方式。通过这种方式设置的 Python 版本优先级较 global 高。
```

#### python优先级

**shell > local > global**

pyenv 会从当前目录开始向上逐级查找 .python-version 文件，直到根目录为止。若找不到，就用 global 版本。

```python
~$ pyenv shell 2.7.3 # 设置面向 shell 的 Python 版本，通过设置当前 shell 的 PYENV_VERSION 环境变量的方式。
# 这个版本的优先级比 local 和 global 都要高。–unset 参数可以用于取消当前 shell 设定的版本。
~$ pyenv shell --unset
~$ pyenv rehash  # 创建垫片路径（为所有已安装的可执行文件创建 shims，如：~/.pyenv/versions/*/bin/*，因此，每当你增删了 Python 版本或带有可执行文件的包（如 pip）以后，都应该执行一次本命令）
```

## 方案二：使用Anaconda包管理多版本python

Anaconda 是 Python 的一个发行版，如果把 Python 比作 Linux，那么 Anancoda 就是 CentOS 或者 Ubuntu。它解决了Python开发者的两大痛点。

- 提供包管理，功能类似于 pip，Windows 平台安装第三方包经常失败的场景得以解决。
- 提供虚拟环境管理，功能类似于 virtualenv，解决了多版本Python并存问题。###1. 下载 Anaconda直接在官网下载最新版本的 <https://www.continuum.io/downloads> 安装包， 选择对应Python版本的安装包，下载完成后直接安装，安装过程选择默认配置即可，大约需要1.8G的磁盘空间。

conda 是 Anaconda 下用于包管理和环境管理的命令行工具，是 pip 和 vitualenv 的组合。安装成功后 conda 会默认加入到环境变量中，因此可直接在命令行窗口运行 `conda` 命令，命令帮助可通过`conda -h`查看。如果你熟悉 virtualenv，那么上手 conda 非常容易，不熟悉 virtulenv 的也没关系，它提供的命令就几个，非常简单。我们可以利用 conda 的虚拟环境管理功能在 Python2 和 Python3 之间自由切换。

### 2. 多版本切换

```plain
# 基于 python2.7 创建一个名为py2_env 的环境
conda create --name py2_env python=2.7

# 基于 python3.6 创建一个名为py3_env 的环境
conda create --name py3_env python=3.6 

# 激活python环境
activate py3_env  # windows
source activate py3_env # linux/mac

# 切换到python3
activate py3_env
```

### 3. 包管理

conda 的包管理功能是对 pip 的一种补充，如果当前已经激活了某个Python环境，那么就可以在当前环境开始安装第三方包。

```plain
# 安装 numpy 
conda install numpy
# 查看已安装的包
conda list 
# 包更新
conda update numpy
# 删除包
conda remove numpy
```

<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-prevent-withdrawal
_✨ 防撤回插件 ✨_

<a href="https://11.onebot.dev">
    <img alt="Static Badge" src="https://img.shields.io/badge/OneBot-V11-%23EEE685?style=flat-square&logo=data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAEAAAABABAMAAABYR2ztAAAAIVBMVEUAAAAAAAADAwMHBwceHh4UFBQNDQ0ZGRkoKCgvLy8iIiLWSdWYAAAAAXRSTlMAQObYZgAAAQVJREFUSMftlM0RgjAQhV+0ATYK6i1Xb+iMd0qgBEqgBEuwBOxU2QDKsjvojQPvkJ/ZL5sXkgWrFirK4MibYUdE3OR2nEpuKz1/q8CdNxNQgthZCXYVLjyoDQftaKuniHHWRnPh2GCUetR2/9HsMAXyUT4/3UHwtQT2AggSCGKeSAsFnxBIOuAggdh3AKTL7pDuCyABcMb0aQP7aM4AnAbc/wHwA5D2wDHTTe56gIIOUA/4YYV2e1sg713PXdZJAuncdZMAGkAukU9OAn40O849+0ornPwT93rphWF0mgAbauUrEOthlX8Zu7P5A6kZyKCJy75hhw1Mgr9RAUvX7A3csGqZegEdniCx30c3agAAAABJRU5ErkJggg==">
</a>
<a target="_blank" href="https://qm.qq.com/cgi-bin/qm/qr?k=Uw7I6zuHfpRfXlwddRqDbyE10MZnB4iB&jump_from=webapi&authKey=tp4LiunKcl44e+1gKEag50kyemidx/xV5a9aqdXkn9t9C9bvj18bdd2EBciZmVBt">
    <img alt="Static Badge" src="https://img.shields.io/badge/QQ%E7%BE%A4-814190174-%23EEE685?style=flat-square&logo=tencentqq">
</a>

![Static Badge](https://img.shields.io/badge/Python-3.10%2B-%23E5C62A?style=flat-square&logo=python)
![GitHub repo size](https://img.shields.io/github/repo-size/zhongwen-4/nonebot-prevent-withdrawal?logo=github&label=%E5%82%A8%E5%AD%98%E5%BA%93%E5%A4%A7%E5%B0%8F)
![GitHub Tag](https://img.shields.io/github/v/tag/zhongwen-4/nonebot-prevent-withdrawal?logo=github)
![PyPI - License](https://img.shields.io/pypi/l/nonebot-prevent-withdrawal?label=%E5%BC%80%E6%BA%90%E5%8D%8F%E8%AE%AE)
![PyPI - Version](https://img.shields.io/pypi/v/nonebot-prevent-withdrawal?logo=python&label=PyPi)
![GitHub commit activity](https://img.shields.io/github/commit-activity/t/zhongwen-4/nonebot-prevent-withdrawal?logo=github)


</div>

## 📖 介绍

- 本插件支持多个消息段撤回监听，但是仅支持群聊，目前只支持**Lagrange.OneBot**，因为根据群友的消息~~llonebot和NapCat似乎视频消息不返回网络URL~~，此项目有些奇怪的BUG，例如~~黄豆表情无法显示~~（Lagrange已修复）、超级表情会显示表情和文字等

- 装了此插件后debug级别的日志下会疯狂输出`Running PreProcessors...`，这个作者也没办法，是NoneBot的预处理钩子干的，修不了，~~其实只要开INFO级别的日志就行了，而一般用户默认是INFO级别的日志~~

使用方法请参考[这里](#-使用)

> [!WARNING]
> 私聊模式**不支持**发送撤回的视频消息，因为Lagrange.OneBot的私聊消息有BUG

> [!WARNING]
> 本插件不支持监听撤回的文件，而且由于某些BUG似乎无法发送提示文本

## 💿 安装

<details open>
<summary>使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

    nb plugin install nonebot-prevent-withdrawal

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

    pip install nonebot-prevent-withdrawal
</details>
<details>
<summary>pdm</summary>

    pdm add nonebot-prevent-withdrawal
</details>
<details>
<summary>poetry</summary>

    poetry add nonebot-prevent-withdrawal
</details>
<details>
<summary>conda</summary>

    conda install nonebot-prevent-withdrawal
</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分追加写入

    plugins = ["nonebot-prevent-withdrawal"]

</details>

## 🎉 使用
### 指令表
| 指令 | 权限 | 需要@ | 范围 | 说明 |
|:-----:|:----:|:----:|:----:|:----:|
| 开启/关闭防撤回 | 主人 | 否 | 群聊 | 必须先开启才能用 |
| 切换私聊/群聊 | 主人 | 否 | 通用 | 发送到哪里 |
| 添加群/删除群 | 主人 | 否 | 群聊 | 指定发送的群聊 |
| 加白/删白 [@/输入QQ号] | 主人 | 否 | 通用 | 排除某人的撤回消息 |
| 排除管理 | 主人 | 否 | 通用 | 排除管理和群主的消息 |
| 取消排除 | 主人 | 否 | 通用 | 取消排除管理和群主的消息 |

### 效果图
<details>
<summary>点击展开</summary>

![图片1](./img/1.png)
![图片2](./img/2.jpg)
![图片3](./img/3.png)
![图片4](./img/4.png)

</details>

## ❤️感谢以下项目提供支持
[NoneBot](https://github.com/nonebot/nonebot2)

[Lagrange](https://github.com/LagrangeDev/Lagrange.Core)

[~~疑似小南梁的群友~~](https://ys.mihoyo.com/?utm_source=backup53&from_channel=backup53&msclkid=0c6ba0c279c51d4b80b6c7d51cd912bd#/)

[GITHUB](https://github.com)
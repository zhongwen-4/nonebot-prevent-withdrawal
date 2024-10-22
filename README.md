<div align="center">
  <a href="https://v2.nonebot.dev/store"><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo"></a>
  <br>
  <p><img src="https://github.com/A-kirami/nonebot-plugin-template/blob/resources/NoneBotPlugin.svg" width="240" alt="NoneBotPluginText"></p>
</div>

<div align="center">

# nonebot-prevent-withdrawal
_✨ 防撤回插件 ✨_

</div>

## 📖 介绍

本插件支持多个消息段撤回监听，但是仅支持群聊，目前只支持**Lagrange.OneBot**，因为根据群友的消息~~llonebot和NapCat似乎视频消息不返回网络URL~~，此项目有些奇怪的BUG，例如黄豆表情无法显示、发送火车等表情会显示表情和文字等

> [!IMPORTANT]
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

### 效果图
![图片1](./img/1.png)
![图片2](./img/2.jpg)
![图片3](./img/3.png)
![图片4](./img/4.png)
from nonebot import(
    on_command,
    on_notice,
    require,
    get_driver,
    logger,
    on_message
)


from nonebot.adapters.onebot.v11 import(
    GroupMessageEvent,
    GroupRecallNoticeEvent,
    Bot,
    MessageSegment,
    Message
)


import json, pathlib, httpx, random
require("nonebot_plugin_localstore")
require("nonebot_plugin_alconna")
from nonebot_plugin_localstore import get_plugin_data_dir, get_plugin_cache_dir
from nonebot_plugin_alconna import Alconna, on_alconna, Args, At, Match
from nonebot.permission import SUPERUSER
from nonebot.plugin import PluginMetadata


path = get_plugin_data_dir()
path = f"{path}/data.json"
unseal = on_command("开启防撤回", aliases= {"防撤回开启", "kqfch"}, permission= SUPERUSER)
shut = on_command("关闭防撤回", aliases= {"防撤回关闭", "gbfch"}, permission= SUPERUSER)
send_private = on_command("切换私聊", aliases= {"切换模式私聊", "切换私聊模式","qhsl"}, permission= SUPERUSER)
sed_group = on_command("切换群聊", aliases= {"切换模式群聊", "切换群聊模式", "qhql"}, permission= SUPERUSER)
add_group = on_command("添加群", aliases= {"添加群聊", "addql"}, permission= SUPERUSER)
del_group = on_command("删除群", aliases= {"删除群聊", "delql"}, permission= SUPERUSER)
add_users = on_alconna(Alconna("加白", Args["user", At | int]), permission= SUPERUSER)
del_users = on_alconna(Alconna("删白", Args["user", At | int]), permission= SUPERUSER)
add_admin = on_command("排除管理", permission= SUPERUSER)
del_admin = on_command("取消排除", permission= SUPERUSER)

group_recall= on_notice()
driver = get_driver()
forward = on_message()


__plugin_meta__ = PluginMetadata(
    name="防撤回",
    description="基于NoneBot的群聊防撤回插件",
    usage="查看github获取使用方法~",
    type="application",
    homepage="https://github.com/zhongwen-4/nonebot-prevent-withdrawal",
    supported_adapters={"~onebot.v11"},
)


def xjson(data: dict, path):
    with open(path, "w") as f:
        json.dump(data, f, indent= 4)


def djson(path):
    with open(path, "r") as f:
        return json.load(f)
    

@driver.on_startup
async def startup():
    try:
        data = djson(path)
    except FileNotFoundError:
        data = {}
        xjson(data, path)

    if "model" not in data:
        data["model"] = 0
        xjson(data, path)
        logger.info("未找到模式设置，已默认为私聊")


@unseal.handle()
async def unseal_handle(
    event: GroupMessageEvent
):

    data = djson(path)
    
    if "unseal" not in data:
        data["unseal"] = []
        data["unseal"].append(event.group_id)
        xjson(data, path)
        await unseal.finish("开启成功")
    
    if event.group_id in data["unseal"]:
        await unseal.finish("本群已开启防撤回功能, 无需再次开启")

    else:
        data["unseal"].append(event.group_id)
        xjson(data, path)
        await unseal.finish("开启成功")


@shut.handle()
async def shut_handle(
    event: GroupMessageEvent
):

    data= djson(path)

    if "unseal" not in data:
        await shut.finish("本群并未开启防撤回功能，无需再次关闭")
    
    if event.group_id not in data["unseal"]:
        await shut.finish("本群并未开启防撤回功能，无需再次关闭")

    else:
        data["unseal"].remove(event.group_id)
        xjson(data, path)
        await shut.finish("关闭成功")


@send_private.handle()
async def send_private_handle():
    
    data = djson(path)
    if "private" not in data:
        data["model"] = 0
        xjson(data, path)
        await send_private.finish("切换成功")
    
    if data["model"] == 0:
        await send_private.finish("切换失败，已经是私聊模式了")
    
    if data["model"] == 1:
        data["model"] = 0
        xjson(data, path)
        await send_private.finish("切换成功")

@sed_group.handle()
async def sed_group_handle():

    data = djson(path)
    if "model" not in data:
        data["model"] = 1
        xjson(data, path)
        await sed_group.finish("切换成功")
    
    if data["model"] == 1:
        await sed_group.finish("切换失败，已经是群聊模式了")

    if data["model"] == 0:
        data["model"] = 1
        xjson(data, path)
        await sed_group.finish("切换成功")


@add_group.handle()
async def add_group_handle(
    event: GroupMessageEvent
):
    
    data = djson(path)
    if "group" not in data:
        data["group"] = []
        data["group"].append(event.group_id)
        xjson(data, path)
        await add_group.finish("添加成功")
    
    if event.group_id in data["group"]:
        await add_group.finish("本群已添加，无需再次添加")

    if event.group_id not in data["group"]:
        data["group"].append(event.group_id)
        xjson(data, path)
        await add_group.finish("添加成功")


@del_group.handle()
async def del_group_handle(
    event: GroupMessageEvent
):

    data = djson(path)
    if "group" not in data:
        await del_group.finish("本群并未添加，无需再次删除")

    if event.group_id not in data["group"]:
        await del_group.finish("本群并未添加，无需再次删除")
    
    if event.group_id in data["group"]:
        data["group"].remove(event.group_id)
        xjson(data, path)
        await del_group.finish("删除成功")


@add_users.handle()
async def add_users_handle(user: Match[At | int]):
    data = djson(path)

    if user.available:
        if isinstance(user.result, At):
            user_id = user.result.target
        else:
            user_id = str(user.result)

    if "users" not in data:
        data["users"] = []
        data["users"].append(user_id)
        xjson(data, path)
        await add_users.finish("已排除此人的撤回消息")
    
    if user_id in data["users"]:
        await add_users.finish("此人已排除撤回消息，无需再次排除")
    
    data["users"].append(user_id)
    xjson(data, path)
    await add_users.finish("已排除此人的撤回消息")


@del_users.handle()
async def del_users_handle(user: Match[At | int]):
    data = djson(path)

    if user.available:
        if isinstance(user.result, At):
            user_id = user.result.target
        else:
            user_id = str(user.result)

    if "users" not in data:
        await del_users.finish("此人并未排除撤回消息，无需再次排除")
    
    if user_id not in data["users"]:
        await del_users.finish("此人并未排除撤回消息，无需再次排除")
    
    data["users"].remove(user_id)
    xjson(data, path)
    await del_users.finish("已取消排除此人的撤回消息")


@add_admin.handle()
async def add_admin_handle():
    data = djson(path)

    if "admin" not in data:
        data["admin"] = True
        xjson(data, path)
        await add_admin.finish("排除成功")

    if data["admin"] == True:
        await add_admin.finish("已经是排除状态了")


@del_admin.handle()
async def del_admin_handle():
    data = djson(path)

    if "admin" not in data:
        await del_admin.finish("已经是未排除状态了")
    
    del data["admin"]
    xjson(data, path)
    await del_admin.finish("取消排除成功")

@group_recall.handle()
async def group_recall_handle(
    bot: Bot,
    event: GroupRecallNoticeEvent
):
    
    data = djson(path)
    operator_id = event.operator_id
    user_id = event.user_id
    message_id = event.message_id
    config = get_driver().config.superusers
    group_id = event.group_id

    group_name = await bot.get_group_info(group_id= event.group_id)
    uaer_name = await bot.get_group_member_info(group_id= event.group_id, user_id= user_id)
    operator = await bot.get_group_member_info(group_id= event.group_id, user_id= operator_id)
    msg = await bot.get_msg(message_id= message_id)
    friend_list = await bot.get_friend_list()
    friend_list = [i["user_id"] for i in friend_list]

    group_name = group_name["group_name"]
    uaer_name = uaer_name["nickname"]
    operator_name = operator["nickname"]
    permission = operator["role"]
    message = Message()
    x = []
    
    if config == set():
        logger.error("未配置超级用户，无法发送撤回消息")
        await group_recall.finish()

    if "unseal" not in data :
        logger.error("未开启防撤回功能，无法发送撤回消息")
        await group_recall.finish()
    
    if event.group_id not in data["unseal"]:
        logger.error("未开启防撤回功能，无法发送撤回消息")
        await group_recall.finish()

    if "admin" in data:
        if permission == "admin" or permission == "owner":
            logger.info("此次为管理员操作，已跳过")
            await group_recall.finish()

    if data["model"] == 0:
        for i in config:
            if int(i) not in friend_list:
                x.append(i)
                logger.error(f"这个人没加好友列表，无法发送撤回消息；{i}")
        
        if x != []:
            await group_recall.finish()

    if "users" in data:
        if str(event.user_id) in data["users"]:
            logger.info(f"用户{event.user_id}的撤回消息被管理员排除，此次跳过")
            await group_recall.finish()

    
    if operator_id == event.self_id:
        logger.info("撤回消息为bot，此次跳过")
        await group_recall.finish()


    if "group" in data:
        if data["group"] == []:
            data["model"] = 0
            xjson(data, path)
            logger.info("未找到群聊设置，已设置为私聊")
    
    
    if data["model"] == 0:
        for i in config:
            await bot.send_private_msg(
                user_id= int(i),
                message= f"消息撤回提醒\n操作群：{group_name} - {group_id}\n操作人：{operator_name} - {operator_id}\n撤回人：{uaer_name} - {user_id}\n以下是撤回消息"
            )

    if data["model"] == 1:
        for i in data["group"]:
            await bot.send_group_msg(
                group_id= i,
                message= f"消息撤回提醒\n操作群：{group_name} - {group_id}\n操作人：{operator_name} - {operator_id}\n撤回人：{uaer_name} - {user_id}\n以下是撤回消息"
            )
    
    if len(msg["message"]) == 0:
        if data["model"] == 0:
            for i in config:
                await bot.send_private_msg(
                    user_id= int(i),
                    message= "出错啦！这条消息可能是文件消息，协议端暂时获取不到！"
                )
            
        if data["model"] == 1:
            for i in data["group"]:
                await bot.send_group_msg(
                    group_id= i,
                    message= "出错啦！这条消息可能是文件消息，协议端暂时获取不到！"
                )
            
        await group_recall.finish()

    for msgsegment in msg["message"]:
        if msgsegment["type"] == "video":    # 判断消息类型为视频
            random_name = random.randint(1, 100000)

            if data["model"] == 0:    # 判断私聊模式
                for i in config:
                    await bot.send_private_msg(
                        user_id= int(i),
                        message= f"出错啦！私聊不能发送视频，已自动忽略"
                    )
                await group_recall.finish()

            if data["model"] == 1:    # 判断群聊模式
                async with httpx.AsyncClient() as client:
                    response = await client.get(msgsegment["data"]["url"])
                    response.raise_for_status()
                    _path = get_plugin_cache_dir()
                    with open(f"{_path}/{random_name}.mp4", "wb") as f:
                        f.write(response.content)

                _path = get_plugin_cache_dir()
                for a in data["group"]:
                    await bot.call_api(
                        "upload_group_file",
                        group_id= a,
                        file= f"{_path}/{random_name}.mp4",
                    )
                    
                pathlib.Path(f"{_path}/{random_name}.mp4").unlink()
                await group_recall.finish()

        message += MessageSegment(
            type= msgsegment["type"],
            data= msgsegment["data"]
        )
    
    if data["model"] == 0:
        for i in config:
            await bot.send_private_msg(
                user_id= int(i),
                message= message
            )
    
    if data["model"] == 1:
        for i in data["group"]:
            await bot.send_group_msg(
                group_id= i,
                message= message
            )
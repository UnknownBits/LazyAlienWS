# LazyAlienWS

LazyALienWS，一个基于websocket的LAS多端互通基础python库

**使用说明：**

将lazyalienws作为python库安装，或直接将lazyalienws文件夹拖到python环境目录下

新建一个文件夹作为ws服务端运行目录，打开命令窗口输入python -m lazyalienws，将会自动创建目录。其中/plugins即为插件目录。

修改conf.json后再次使用python -m lazyalienws启动即可

将mcdreforged下的文件拖到mcdr的plugins目录下，并修改配置文件。其中_vc版本为velocity端mcdr插件

---

## 实现功能：

### 更好的Chatbridge（聊天互通）

**效果：**
<img src="https://docimg7.docs.qq.com/image/AgAABa2v9CWS_8vLpMJJWa541-P-dZVM.webp?w=1256&h=687">

*chatbridge在Minecraft中*

<img src="https://docimg7.docs.qq.com/image/AgAABa2v9CX6cNvgM15DMZsdmyO0GAIV.webp?w=658&h=470">

*chatbridge在qq中，图为从mc回复qq消息的效果*

**相比于fallen的传统chatbridge，优点在于？**

- 更好的显示样式，传统chatbridge互通消息全部为灰色，新chatbridge修改了颜色，更加清晰；在游戏内显示QQ消息时，QQ用户昵称将使用灰色以区分开qq互通和群组互通。

- 支持了对CQ码的处理，在QQ中的图片/表情/回复消息/at/合并转发能够在局内正常显示，其中图片/表情可以在局内以网页形式打开查看。

- 在velocity群组上套了一层mcdr，当玩家在子服中切换的时候qq不会提示进入/退出游戏，局内使用velocity chat提示切换；只有当玩家进入/退出群组时，qq才会提示。
---
### 更好的bot前缀与“#在线玩家”功能

效果：

<img src="https://docimg7.docs.qq.com/image/AgAABa2v9CX4xBewM61Gwo0AymTm6TIJ.webp?w=562&h=540">

*局内在线玩家*

<img src="https://docimg7.docs.qq.com/image/AgAABa2v9CX8ShRdM1JBYIYxCTMw4W5f.webp?w=684&h=705">

*qq在线玩家*

<img src="https://docimg7.docs.qq.com/image/AgAABa2v9CXecLRbZ7BLjqFgZH2F3BGt.webp?w=549&h=50">

*bot*

**更好的bot前缀：** 当假人进入游戏时，识别ip为[local]，则为假人加上[BOT]前缀。*（注：此功能可能会导致vris bot无法使用，需要搭配修改后的vris以支持[BOT]前缀）*

**#在线玩家：** 在获取在线玩家时，同时获取team bot内的假人列表，区分开玩家和假人

---

### #mspt #tps 查询

效果：

<img src="https://docimg7.docs.qq.com/image/AgAABa2v9CWDgmsFr5RN3YuG-Le5l7u8.webp?w=690&h=618">

*#mspt查询服务端tps和mspt，#tps同理*

---

### #签到

效果：

<img src="https://docimg7.docs.qq.com/image/AgAABa2v9CWEEOXHPtZPsJrDz4mANIes.webp?w=710&h=401">


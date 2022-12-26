# Bilibili关注列表

对我的关注列表进行分析。此仓库用来爬取数据。

## 使用说明

1. 下载整个代码仓库
```bash
git clone https://github.com/yyngfive/bilibili-following.git
```
或者直接下载压缩包解压

2. 在`bilibili-following`目录下依次执行
```bash
pip install -r requirements.txt
python main.py
```

3. 登录后等待完成，得到`following-ups.csv`和`following-ups.xlsx`，可以使用explore.r进行分析(需要R环境，是个半成品)，或者自行分析。

## 结果说明

### 基本数据：
- **uid**：UP主唯一编号
- **name**：UP主昵称
- **time**：关注时间
- **special**：是否为特别关注
- **face**：头像链接
- **fans**：粉丝数
- **total**：视频总数
- **view**：总播放量
- **likes**：总点赞数
- **fields**：发布的视频占比最多的分区（如果有占比第二的分区发布视频数超过三分之一，也会计入）
- **first**：目前最早发布的视频
- **newest**：目前最新的视频
### 拓展数据：
- **update**：更新现状，目前只是简单的考虑最新视频发布时间距离现在有多远。依据最新视频和距离现在的时间，分为：
  - 仍在更新：小于一个月
  - 更新缓慢：一个月以上未更新
  - 暂时停更：三个月以上未更新
  - 停更风险：半年以上未更新
  - 停更：一年以上未更新
- **single_field**：**fields**中发布视频数占比最高的分区
- **big_field**：依据**single_field**进一步划分：
  - 泛影视：电影、纪录片、影视、动画、国创
  - 泛娱乐：音乐、舞蹈、游戏、鬼畜、娱乐
  - 泛知识：科技、知识、资讯
  - 泛生活：美食、动物圈、汽车、生活、时尚、运动
  - 无：一些没有发布过视频的UP主、注销账号的UP主、以直播为主的UP主、封号的UP主等
- **fans_level**：依据粉丝数进一步划分为：
  - 0-100
  - 100-1000
  - 1000-1万
  - 1万-10万
  - 10万-50万
  - 50万-100万
  - 100万-300万
  - \>300万
- **view_average**：平均播放量
- **likes_average**：平均点赞数

## 问题反馈

[Github Issues](https://github.com/yyngfive/bilibili-following/issues)

## 代码说明

`login.py`：用来执行登录操作，B站限制只能查看用户5页（最多250个）关注，登录后可以查看自己的全部关注。

`follow-list.ipynb`：用来爬取自己的关注列表，保存原始数据到`json`文件

`following-results.ipynb`：用来从原始数据中提取需要的部分，保存到表格

`video-info.ipynb`：用来补充UP主的视频分区和播放量等信息

`update.ipynb`：用来以后增加新关注的UP主以及更新原有UP的信息

`main.py`：一次性完成以上步骤

## 分析步骤

1. 使用此仓库代码爬取数据
2. 按照自己定义的标签为UP主打标签以及其他注释（与B站官方类似，但对于知识区和科技区的定义有区别，增加了更加细节的标签）
3. 结果统计分析

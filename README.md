# sam_buy
山姆买菜

version:1.5

owner :@guyongzx

## V1.5 版本介绍

#### 1.5 版本优化了下单效率,并且支持自定义商品列表
#### 支持根据多个配送时间同时下单,几率更高
#### 下单参数文本化,修改更方便更灵活

## V1.5 操作步骤
#### 抓包获取token和其他用户信息这里不再描述,参考v1和v2版本
#### 这里只说1.5版本操作方法

1: getData.py 类里填写deviceid和authtoken

2: 选择相应地址和仓库

3: 在弹出"在file/goodlist.txt编辑商品后回车,如不编辑直接回车"这里可以修改goodlist.txt内的json文本,决定具体想要下单的商品,如果全部都要直接回车

4: 等待程序结束后,执行order.py即可开始下单

5: order.py内包含了一些线程控制和自定义内容,有python基础的人可以自行修改,但是不要过分

ps:如果1.0是手动挡,2.0是自动挡,那1.5就是半自动(手动狗头)


### 如果本工程对你有所帮助,记得点个star鼓励一下作者QAQ :)

platform: ios15;

app version: v5.0.45.1;

python version: 3.8.6;

## 更新须知
##引入requests 组件
执行
```bash

pip install --index-url https://pypi.douban.com/simple/ configparser
pip install --index-url https://pypi.douban.com/simple/ requests

```

## 有代码基础的使用 v1 or v1.5 分支,无基础使用v2
##代码中有注释，遵循注释进行修改 运行即可

# 关于配置

deviceid,authtoken个字段为购物车的HTTP头部的字段信息

依旧没有bark支持，需要的请自行添加

# 疫情当下上海买菜太难了


## 倡导大家只够买必需品！不要浪费运力


# 仅供学习交流，不可用于非法牟利。

# 版权说明

本项目为 GPL3.0 协议，请所有进行二次开发的开发者遵守 GPL3.0协议，并且不得将代码用于商用。

本项目仅供学习交流，严禁用作商业行为，特别禁止黄牛加价代抢等！

因违法违规等不当使用导致的后果与本人无关，如有任何问题可联系本人删除！

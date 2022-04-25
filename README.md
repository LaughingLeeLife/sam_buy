# sam_buy
山姆买菜

version:1.5

owner :@guyongzx

## V1.5 版本介绍

###

#### 4.25 更新

执行 sam_buy_bao_gong.py

持续扫描是否有货,有货就加购物车并下单

如果持续上3个套餐,会都下单,最后取消你不需要的

加入barkid参数,如果要bark通知在一开始填入barkid

#### 4.24 更新
sam_buy_bao_gong.py 保供功能,加入购物车后动结算

#### 4.22 更新

加入保供套餐搜寻,并且自动加入购物车功能 findBaoGong.py 

直接运行即可

#### 4.19 更新 

加入动态加载order的request body参数,修改data.txt文件可以不用重启直接反应到order请求中,用于临时修改商品列表或者其他参数

如果想完全盲猜不调用getCapacityData接口,可以将guess置为True

修复极速达时间段太多导致线程过多的问题,现在默认只取最后2个


#
#### 1.5 版本优化了下单效率,并且支持自定义商品列表
#### 支持根据多个配送时间同时下单,几率更高
#### 下单参数文本化,修改更方便更灵活

## V1.5 操作步骤
#### 抓包获取token和其他用户信息这里不再描述,参考v1和v2版本
这里只说1.5版本操作方法

1: getData.py 类里填写deviceid和authtoken

2: 选择相应地址和仓库

3: 在弹出"在file/goodlist.txt编辑商品后回车,如不编辑直接回车"这里可以修改goodlist.txt内的json文本,决定具体想要下单的商品,如果全部都要直接回车

4: 等待程序结束后,执行order.py即可开始下单

5: order.py内包含了一些线程控制和自定义内容,有python基础的人可以自行修改,但是不要过分


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

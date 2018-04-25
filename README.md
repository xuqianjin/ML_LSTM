### 基于LSTM的文本预测

## 环境依赖
> * windows
> * keras
> * numpy
> * requests
> * BeautifulSoup
## 数据爬取
数据来源是[金庸网](http://www.jinyongwang.com)鹿鼎记,用requests抓取小说目录并分别抓取每一张,并存在data/lu.txt里面
详细代码见[GetLu.py](https://github.com/xuqianjin/ML_LSTM/blob/master/GetLu.py)

## 训练全流程
> * 获取lu.txt数据
> * 全集共100个字符,硬件有限,只取前5万个字符
> * 排序去重
> * 生成词典<-->整数映射表
> * 定义每个句子长度(本文取40个字符为一句话)
> * 按照映射表生成输入数据,并保持数据的时间顺序
> * 转换数字向量为zero向量 (49960, 40, 1)=>(49960, 40, 2398)
> * 将输出向量one-hot表示
> * 构建lstm网络,optimizer='adam', loss='categorical_crossentropy'
> * 训练并通过回调保存每一次的训练参数
> * 生成随机预测种子,生成预测文本

代码参考[Word_LSTM.py](https://github.com/xuqianjin/ML_LSTM/blob/master/Word_LSTM.py)

## 结论
训练时间大概每epoch 15分钟,总共50个epoch,最优loss=2.1862,[weights-improvement-50-2.1862](https://github.com/xuqianjin/ML_LSTM/blob/master/weights-improvement-50-2.1862.hdf5)文件是训练好的一个模型,可以直接用 keras.models.load_model加载并预测文本,附上我这边预测的文本:
```
此。”茅十八道：“是！”吴之荣见到船头，见到店中，一时兴论，又想：“是你们三人，有一个小市镇上。”那人哈哈大笑，说道：“我说什么？”韦小宝道：“你们这个小朋友，我们就算你是什么大叫？”韦小宝道：“你奶奶的，我们就是我不起来。”茅十八道：“你们这个小孩子不可。”韦小宝道：“你奶奶的，我们就是我的，我们这个小孩子的好汉奸，我们这个小朋友，我们不知道啦！”那妓女大汉奸一个小孩，也不过“啊哟，这一个小子不
```

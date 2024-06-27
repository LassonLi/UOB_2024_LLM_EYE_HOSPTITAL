aws是一个Amazon提供的云服务解决方案，我们主要使用他的计算资源进行模型训练

绝大多数服务需要**收费**且按时间或资源计费，请**使用完后随手关闭或清空**，避免额外账单

注册账号并登录  [here](aws.amazon.com)

# 控制台

登录后控制台如图所示，红圈部位为搜索功能，直接使用搜索搜索想要的服务即可
可以在设置中进行账单限额设置
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/fcd869f3-c407-4759-a30f-db632d1da239)

# EC2
EC2 服务是AWS提供的命令行形式云服务器服务，需要图形界面请启动带 MATE的实例（但是图形界面很占带宽，容易造成不必要的消费）

在控制台搜索EC2并进入

点击实例并点击右上角启动新实例来创建EC2服务
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/7c39ba38-adc5-4ad5-bae1-891549085629)

名称随意设置

蓝笔勾出的分别为选择系统类型和系统预装服务，这里因为是演示选择免费类型，有deeplearning类型但是要收费

红笔勾出的为具体服务器配置，有许多不同种配置，具体参考[这里](https://aws.amazon.com/cn/ec2/instance-types/)

模型训练请参考具体需求，我们这里选择免费实例类型

![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/11aea423-aa98-4f7a-b8e8-dde0c4b37346)

接着点击创建新密钥对，保存好你的私钥

![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/0e4eabc6-dd98-4ca0-acd7-96b5232445e1)

点击网络设置上的编辑，新加入一条安全组规则

将端口8080-8089开放，不然只能通过ssh链接服务器，不能通过网页访问
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/c741f188-3dda-4580-a892-3d89383cb027)

然后设置储存大小，然后点击启动实例即可。

## 连接到EC2
回到实例界面，应该会看到你刚刚新建的实例，点击连接即可进入服务器，记得设置用户名，默认也行
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/cf91210a-053d-490c-9c23-e7c04c39f065)

接下来就是熟悉的linux界面啦

Amazon linux的包管理器和部分命令有些许不同，但是推荐用它

这个东西叫yum，具体自己搜教程

因为是可以内网下载包，比较省流量
但是我们主要并不使用ec2，因为他开机就要钱，太贵了
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/00ebfd6d-e0f9-4abf-9a2c-740ca1260ca7)

# sagemaker
sagemaker 是Amazon开放的一款专门用于机器学习的解决方案，完整到从数据标注到数据分析都有

但是太贵了，我们只用模型训练的部分，其余部分有兴趣可以自己学习

回到控制台，搜索sagemaker， 进入notebook
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/3fae4e67-4c08-4870-a7c2-d6bf03a8397a)
点击创建笔记本实例

这里的笔记本实例类型并非我们模型运行时使用的服务器配置

而是运行jupyter时的服务器，因此选个尽量低配和能运行数据加载预处理的就行

下方的配置git，看情况配置
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/01cb9e64-6f75-4091-8c29-2cc6d03ad662)

然后回到主界面点击对应的笔记本 启动jupyter，我们就来到了熟悉的jupyter

点击新建命令行，由于这是aws的jupyter，命令不会在电脑的terminal里面输出，因此会在这个新建的terminal里面输出

最右侧有sagemaker的机器学习example，建议至少看一个

![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/2994ead8-9f0e-44a7-9824-465a45e03393)

这里涉及到一个将数据从s3储存桶中加载的过程，我们也可以使用s3储存筒，来避免反复上传数据造成的带宽浪费（主要是费钱）
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/519c1e0b-0876-4ad5-851e-36511fe19760)

##训练模型
具体来说，sagemaker有一个sagemaker包来训练模型和调用aws服务器资源

这里是使用sagemaker包定义服务器类型，这才是真正训练模型的服务器，同时，一旦摁下程序运行按钮，这个服务器就会**开始计费**

后续有如何用sagemaker包来创建训练任务的代码，请自行阅读任意example
![image](https://github.com/LassonLi/UOB_2024_LLM_EYE_HOSPTITAL/assets/63943203/f44c64b8-f933-4876-bfcf-e9703b4431db)

# S3
S3储存筒，就是一个云储存系统，控制台搜S3

直接新建一个上传数据就行，注意别重复上传，他是随用随付钱的，反正要钱，如有需要，用它












  

# ShuangChuang
基于多源多维感知的高速公路两客一危车辆轨迹追踪与事故预警部分


二、项目实施情况
项目背景：

两客一危，是指从事旅游的包车、三类以上班线客车和运输危险化学品、烟花爆竹、民用爆炸物品的道路专用车辆。
近年来，随着高速公路快速发展，车流量增长迅速，危化品导致的交通事故不断增多，给社会带来了极大的负面影响，严重威胁到了人们的人身安全。2014年，全国共发生交通事故3906164起，造成65225人死亡，254075人受伤，直接财产损失9.3亿元，其中，两客一危车辆道路交通事故死亡人数占总数的40.2%。由于两客一危车辆具有易燃、易爆等性质，因此其事故造成的人员和财产损失更为巨大，急需监管关键技术。
目前国内的高速公路管理部门无法得知车辆在高速公路上的具体行驶轨迹，不能对可能发生的事故进行有效的预防，也很难在事故发生时立刻发现并发出警告。
我们希望对图像，声音，道路路况、气候情况等信息进行收集和分析，对行驶在高速公路上的两客一危车辆进行轨迹追踪，结合更多信息进行事故的预防，并在意外不幸发生时及时报警。这将会增加高速公路管理部门对两客一危车辆的监控能力，降低事故发生频率，提高高速公路交通安全。


主要进展情况：


1.	整体系统：

我们现在已经完成了整体系统的构建。这个系统包括边缘端和和服务器端。

边缘端为树莓派,它目前的工作是获取数据、处理数据和将处理结果上传到服务器。获取数据方面主要是通过树莓派摄像头拍摄视频,麦克风录取音频。处理数据则是运行我们写好的函数，目标识别函数从视频中获取两客一危车辆图片，颜色识别函数和车型分类函数获取车辆的颜色和车型。

服务器端可以接受树莓派发送来的特征并生成轨迹。
车辆上道时在数据库中创建一条新数据存有这辆车的颜色车型等特征以及唯一标识车牌号。假设高速公路每隔2公里设置一个树莓派，这些树莓派将相继拍摄到上道的这辆两客一危车辆，从而向服务器发送“树莓派n号发现一辆某色某种车”的信息。而服务器则找出数据库中最有可能是这辆车的数据，将树莓派n号的位置添加进此车的轨迹数据。
一辆车在某点被拍到后，它下次有可能被拍到的位置是固定的，因此对一辆车身份的识别是相对准确的。如果相同颜色同类车辆同时行驶并离的很近，它们的身份将暂时难以区分，但在它们缴费下道时我们仍能获取它们的车牌号，从而将轨迹纠正。
服务器前端可将道路上的所有两客一危车辆的轨迹显示在页面上。


2.目标识别：

我们已经完成对小汽车车辆的检测和汽车图片提取。我们完成了如下工作：

	提取图片中的HOG特征
首先我们搜集到了8712张汽车的图片，和8910张非汽车的图片。非汽车类中的图片中有路边房子，道路，和指示牌的图片。将其处理成 64x64x3的RGB图片。然后提取出了每个图片的HOG（方向梯度直方图）特征。

	训练分类器
使用SVM分类器。最终训练的分类器在测试数据集得到98.0%准确率。

	应用滑动窗口实现车辆检测
先直接提取整张图片的HOG特征，然后获取每个窗口所属的那部分HOG特征，利用已经训练好的模型判断窗口中是否有车辆，
我们使用了2类不同大小的滑动窗口对图片中的车辆进行搜索分别是64*64，重叠率为0.75。第二类大小为96x96，重叠率为0.75，用于检测远处的车辆。第三类大小为128x128,重叠率为0.75:第四类大小为224x224,重叠率为0.75，用于检测近处的车辆。
	应用热图过滤了错误检测
由于使用了多个大小不同的窗口去检测车辆，所以可能会出现重叠的现象，即单个车辆图像会被多个窗口捕捉检测。运用热图，记录下一张图片所有可能出现车辆的地方，然后对热图进行阈值过滤。
最后对过滤后的热力图可获取整合的检测窗口。


3.车型分类：

  在车型分类中，我们将两客一危车辆从外形分为三类：货车，客车，危险品车辆（油罐车）。两客一危车辆的定义是“从事旅游的包车、三类以上班线客车和运输危险化学品、烟花爆竹、民用爆炸物品的道路专用车辆”，我们的分类包含了两客一危车辆的同时具备一定区分度，为根据特征查找数据提供了有效的支持。
  我们使用Inception-v3模型进行迁移学习以获取准确度较高的车型分类器。Inception-v3模型可以直接用来进行图像分类，它是谷歌在大型图像数据库ImageNet上训练好的模型。而我们的工作是重新训练模型的最后一层并保留其他部分不变来实现我们需要的车型分类器。重新训练最后一层就能够识别新分类的原因是，之前的训练已经使识别网络的低层级能够识别不同的对象，用于分辨 1000 种分类的信息对于识别新分类通常也十分有用。


4.颜色识别：

颜色识别主要经历两个阶段，当前正处于第二阶段的开发中。
第一阶段主要使用构造颜色表法，对图像进行二值化处理，形态学腐蚀、膨胀去除毛刺、噪点，然后提取边缘，计算不同色域下白色区域的面积，遍历颜色表，找到最大面积对应的颜色。该方法在添加预处理（如去雾、增强等）操作后，对雾天、阴天等条件下的颜色识别具有一定鲁棒性，但是由于部分颜色色域狭窄，且算法本身存在缺陷，导致该算法具有不可弥补的局限性，因此也有了第二阶段的改进和优化。
第二阶段主要利用机器学习的手段，构建多层神经网络，以解决车辆颜色识别这一多类分类问题，该思想由计算机识别手写数字受到启发，在阅读《自然场景下车辆颜色识别研究》和《基于卷积神经网络的对象颜色识别》后得到思路，目前正处于学习和开发同步进行的阶段。


5.音频分析：

	对收集到的声音进行预处理，首先进行端点，由于大型车和小型车行驶时声音能量、短时过零率和频率的不同，可以将一段音频中的噪音以及静音段去除，留下每辆车可以用于识别的部分，进行分帧，切成小段。
	提取每一帧声音特征MFCC参数，并注意应使得输入特征一样大小，获得特征的多维向量。
	建立目前应用广泛的声音识别模型，HMM模型。用大型车和小型车的声音文件对模型进行训练。并用相同数据对其进行检测，识别效果可以达到百分之90%以上。
	由于高速车辆是连续行驶，所以需进行连续声音的端点检测，并对其进行识别，可以判断当前车辆为大型车还是小型车。
三、	项目研究情况
1.	目标识别：

由于本项目是将设备放置在高速旁路道路两旁，所以最主要的是搜集车辆侧面的图片，然而现如今网络中的数据集大多是高速公路高空摄像头，车载摄像头拍摄的，多数是车辆背面，车辆正面，而侧面汽车的数据较少。所以我们可以在以后采集车辆侧面的数据，最主要的是收集两客一危车辆的侧前方，侧后方，和正侧面的图片数据。然后利用SVM+HOG进行训练模型，这种模型训练的好处是训练速度快，识别率较高，缺点是所用到的数据量较大，识别情况比较单一。然后利用滑动窗口实现车辆的检测，最后利用热图进行错误过滤，用阈值筛选出车辆照片。

收集汽车的图片，将其处理成64*64像素，如图所示

图1:将车辆图片和非车辆处理成为64*64像素的局部图




利用SVM向量机进行训练的结果，以及预测结果输出：
  
图2：模型训练完成的截图以及10组图片的输出结果


提取出图像热图

 
图3：经过处理的热图

在车辆识别这一方面，做了特别多的实验，尝试了许多的方法，一直想找到一个既可以快速识别的出车辆，并且准确率很高的方法。比如利用opencv自带的train cascade去训练模型，识别率不高，利用神经网络训练模型，训练的速度较慢，识别速度较慢，对硬件环境要求较高。最后确定使用SVM+HOG作为车辆识别检测的训练方法，该方法即使在大量数据集的情况下也可以做到快速的训练，和快速的识别，并且识别的准确率较高。现在利用该训练模型实现了对小汽车的识别和图片的提取。虽然这种车辆识别技术已经很成熟，但是仍有许多可以改进的地方，下一步可以训练出来可以实现多物体，多种车辆识别的模型，这也是最为理想的情况。


2.	车型分类：

训练车型分类器时，我们的数据来自爬虫爬取的网络图片。搜索关键字为“大货车”、“大客车”、“油罐车”的百度图片，有效图片1000张左右。图片质量参差不齐，我们对此数据集进行了人工的筛选，将其中重复的、水印过大的、角度为正面的图片筛除掉，留下合适的图片。但即使这样，爬虫爬取的网络图片仍然为我们带来过较难解决的bug，让我们花了较长时间解决。
在训练的过程中将图片作为输入计算瓶颈张量时，程序有时不会报错，有时却报错：
“tensorflow.python.framework.errors_impl.InvalidArgumentError: Got 2 frames，but animated gifs can only be decoded by tf.image.decode_gif or tf.image.decode_image”
大意是图片有两帧，但gif不能通过现在的方式解码。这个报错信息并没有直观的告诉我们问题所在，对此信息进行搜索得到的解答也与我们遇到的问题毫不相干。我们多次执行程序来复现这个问题，观察到保存特征向量的文件数目与输入图片的数目并不相符，而且保存特征向量的文件数目在经过一轮训练后常常会增加。我们猜测是因为数据集中存在非标准格式的图片造成的，于是写了将无特征向量文件对应图片删除的程序，最终解决了这个问题。
   
图4：训练时输入的图片和输出的特征向量文件

另一个曾经困扰我们较长时间的问题是，在边缘端树莓派运行分类器时提示内存不足，无法运行程序。如果不能解决这个问题，使用迁移学习训练出来的模型只能作废。我们尝试给树莓派安装更轻量级和性能更高的系统，以及换更大容量的SD卡，最终以64位系统debian9和32g SD卡解决了这个问题。
 
图5：树莓派成功运行分类器并给出分类结果



3.	音频处理：

声音识别主要是为了识别车辆的碰撞以及刹车的声音，从而判断车辆是否要发生事故，但由于我们首先需要判断是否为大型车，并且碰撞声音特征明显较好识别，且数据收集困难，所以我们进行了大型车和小型车的识别用以测试模型。对于收集到的声音数据，里面不仅有车辆行驶的声音，还存在噪音段、静音段，要跟声音的基本特征，例如能量，将这些没有意义的语音数据去除，留下有用的部分。对于声音的识别，需要找到可以描述其特征的表示，常见的就是MFCC倒谱系数。建立声学模型，并用数据对模型进行训练，计算样本的识别概率，对其进行改进，使其识别概率提高，最后应能识别连续行驶的车辆，得出判断结果。

我们搜集了高速路路边大型车、小型车行驶过去的声音片段，并进行截取，将其切分成10个大型车和10个小型车的音频文件，用这些文件对模型进行训练。搜集到一段高速路上连续的车辆驶过的声音，且在声音中不存在声音重叠情况，这也是模型欠缺的地方，以后将考虑两辆车驶过声音有重叠的情况。

首先我们需要对声音进行端点检测，截取需要识别的声音部分，如图所示，还需要能表示声音特征的参数，例如MFCC倒谱系数，建立合适的机器学习模型，对模型进行训练。

现在在声音识别领域中表示声音特征的参数多为MFCC倒谱系数，MFCC特征提取包含两个步骤，转化到梅尔频率，然后进行倒谱分析，梅尔刻度与人的听觉是相符的，所以这个参数有很强的物理意义。

比较常见的声音模型就是HMM模型，HMM模型是经过很多验证的统计学模型，已经广泛应用到声音识别领域，是一个稳定的机器学习模型。最终经过训练的模型能够对所给的连续声音数据得出正确的判断。
 
图6：端点检测
 
图7：HMM原理图


4.	颜色识别：
 
图8：颜色识别流程图

目前主要完成了特征提取中的颜色识别。颜色识别的算法过程相对简单，并且已经成功实现，能够识别出很丰富的颜色。并且在气象状况良好、光照良好的条件下，识别准确率十分可观。通过神经网络训练颜色分类器，在拥有良好数据集的前提下，该方法有效地提高了颜色识别的准确率，并且由于数据集庞大的原因，这种训练可是弱化光线和天气对识别结果的影响程度。之后将会着手于更多方面的特征识别，精细算法，使识别结果更加准确。


 
图9：颜色识别数据

起初使用隔离训练的方法，以取得最好的识别效果，但是效果不好。给程序大量的白色汽车的图片训练后，输出层是一个颜色的向量，如有[红色，绿色，蓝色，白色，黑色，……]，白色汽车训练的理想结果是[0,0,0,1,0,……]，但是训练完白色后再拿其他颜色比如黑色训练分类器，参数又会发生变化，当识别黑色达到理想效果时，识别白色可能又出现了偏差。在这种极端情况下，可能会让白色的分类器给出黑色的是白色的这错误结论。
后来了解到，最好让训练数据充分混开，即使分类数目提升造成分类质量下降是不可避免的。使用GAN对训练集进行扩充，并考虑到鲁棒性问题，可以对数据进行各种变换，比如裁剪，旋转，滤镜，扭曲，这些都能造就数据集。


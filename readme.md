美团电影爬虫/美团电影价格图片混淆破解
===================


----------


项目难点：
-----


----------


让我们先来随便打开一个美团电影的页面

![此处输入图片的描述][1]

真是美滋滋啊，这个价格就写在上面！爬下来不就得了。

定睛一看代码，我了个擦，这是个什么东西。

![此处输入图片的描述][2]

打开图片URL，才明白过来，原来是一张大图一堆数字，用CSS定位的具体数字，美团你为了反爬真是煞费苦心啊……

![此处输入图片的描述][3]


----------

Cracked
=======


----------

requirement:
------------

bs4
requests
Pillow/PIL

需要独立安装tesseract-ocr

使用方法：
-----

 1. 安装tesseract-ocr
 2. 将num.traineddata复制粘贴到tesseract的tessdata目录中
 3. 修改meituan_price_img.py中的TESSERACT_PATH变量定位到tesseract.exe (绝对路径)
 4. 打开meituan.py，Enjoy it！

Example:
--------

    print get_city_url('上海') #获取城市的地址
    print get_all_cinema('sh.meituan.com') #获取城市所有电影院信息
    print get_cinema_movie('http://sh.meituan.com/shop/58174') #获取指定电影院所有电影场次信息

原理：
---

你都看到tesseract-ocr了原理还用我废话嘛？机器学习了所有数字的样本（精准到1px），然后自动识别并输出咯。
PS：如果价格有手机专享价，会自动输出手机专享价！

  [1]: http://storage1.imgchr.com/Evmtg.png
  [2]: http://storage1.imgchr.com/EvnhQ.png
  [3]: http://storage1.imgchr.com/EvKpj.png

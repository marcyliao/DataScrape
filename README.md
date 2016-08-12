# 结构化互联网的非结构化数据，构建网页解析社区

### 数据定义：
* 输入：Start URLs
* 模型：
 * 数据项：Data Items
 * 元数据：Xpaths
* 输出： File Format， Location （缺省为本地Json，可以配置为S3、DB等）


### 目录结构
* 类别， 如餐馆
  * Spider源文件 （可以不公开，留联系方式，或以云服务方式提供）
  * xpath配置文件 （公开，可修改，如需增删需联系定制）
  * 输出配置 （可定制）


### 使用说明
* 下载所需的Spider代码和Xpath配置
* 运行代码获取数据
* 更新Xpath配置
* 新增Spider代码和Xpath配置
* 输出结果可以放在Data Market

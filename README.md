# backtesting

28 March, 2017

进度：
1、完成了数据插入，共101.904GB，最后有报错：
pymongo.errors.OperationFailure: exception: Can't take a write lock while out of disk space
2、为了检查错误原因安装了mongodb的可视化工具Robomongo，还未发现是否有错。

计划：
1、完成UI程序（回测）在Ubuntu及现有数据结构下的调整及运行；
2、找出报错原因，如需要，对插入程序进行修改。

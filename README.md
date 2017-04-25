# backtesting

25 April 2017

进度：
1、将2016年4月各个合约的数据插入数据库
2、经过修改调试基于vnpy的回测已经可以使用strategyGirdTrading 进行，具体流程如下：
(1) cd ~/Downloads/raptor-dev/ctaAlgo
(2) 相关回测参数可在当前文件夹下的parameter_testS.json中修改（如buyPrice等）
(3) 在终端输入python进入python环境
(4) 依次输入如下语句
from ctaBacktesting import *
from strategyGirdTrading import *
engine = BacktestingEngine()
engine.setBacktestingMode(engine.TICK_MODE)
engine.setStartDate('20160401')
engine.loadHistoryData('backtesting', 'AMI')    #在此处修改合约名
engine.initStrategy(strategyGirdTrading, {"className": "theGirdTrading", "name": "testS", "vtSymbol": "rb1710"})
engine.runBacktesting()
engine.showBacktestingResult()

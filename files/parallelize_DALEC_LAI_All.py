#! python
#-*- coding: utf-8 -*-
# 标准化输出。
from __future__ import print_function
# 各种包。
import os, sys, time
import math
# PYMC
import pymc as pm
from pymc import Uniform, Normal, MCMC, AdaptiveMetropolis
# NUMPY
import numpy as np
# SPARK
from pyspark.sql import SparkSession
# 外部依赖项
from model_DALEC_LAI_All import init_Model, NEE_eval, tau_eval, save_Traces
print ('model loaded')
# 数据处理函数。
def run(data):
  #  Mappartions
  # 1. 数据映射。
  # 站点标记
  out_flag = 'NEE_' + str(int(data[0])) 
  sys.stdout.write('>> 站点标记：%s' %(out_flag))
  # 驱动数据。1980-2018,39years 468
  Tave = np.array(data[1:468+1])              # Tave 1
  Nt = len(Tave)                              # Nt 2
  Tmax = np.array(data[468+1:468*2+1])       # Tmax 3
  RH = np.array(data[468*2+1:468*3+1])      # RH 4
  VPD = np.array(data[468*3+1:468*4+1])     # VPD 5 
  Rg = np.array(data[468*4+1:468*5+1])     # Rg 6
  Lat = np.array(data[468*5+1:468*6+1])     # Lat 7         # Lat 1
  LAI = np.array(data[468*6+1:468*7+1])     # LAI 8  obs->driver. #/////////////////////////////
  # 观测数据。1980-2018,39years 468
  soc = np.array(data[468*7+1:468*8+1])     # soc 9
  agbc = np.array(data[468*8+1:468*9+1])    # agbc 10
  bgbc = np.array(data[468*9+1:468*10+1])    # bgbc 11
  o_List = [soc, agbc, bgbc, LAI] #LAI,obs
  print ('数据映射成功')
  # 2、筛选观测数据。
  i_data, o_data = init_Model(o_List)
  # 3、参数映射。
  # 3.1、待优化参数。[690, 730, 10700, 406, 7600]
  # [LMA, Cf_0, Cr_0, Cw_0, Clit_0, Csom_0] -> [Cf_0, Cr_0, Cw_0] #/////////////////////////////
  # 111111111111111111111111111111111111111111111111111111111111111
  #R'''
  #           p1Ra*1e5 p2CLab*1e5 p3NPP2Cf*1e5 p4Clab2Cf*1e5 p5Cf2Cn*1e6 p6Cf2Clit*1e6 p7Cr2Clit*1e6    p8Cn2Clit*1e6    p9Clit2Rhl*1e6 p10Clit2Csom*1e6 p11Csom2Rs*1e6     p12Ft*1e4  p13Fw*1e6  p14NUE*1e6 p15Cn_0*1e7 p16Clit_0*1e7 p17Cr_0*1e8  p18Clab_0*1e7 p19LMA*1e3
  p_lowers = [0.35, 0.15, 0.40, 0.50,    0.70,  0.015,     0.015,   0.015,   0.00015,   0.003,      0.00003,   0.060, 0.70, 0.300, 0.000,    0.001,    0.020,   0.010,  0.011]
  p_uppers = [0.45, 0.40, 0.80, 1.00,    1.00,  0.240,     0.240,   1.000,   1.00000,   0.150,      0.0030,    0.100, 1.20, 0.850, 0.500,    0.200,    1.000,   0.500,  0.030]
  p_values = [0.40, 0.19, 0.57, 0.95,    0.90,  0.150,     0.120,   0.600,   0.45000,   0.080,      0.00090,   0.093, 0.97, 0.400, 0.100,    0.050,    0.100,   0.250,  0.023]
  #'''
  R'''
  #          p1Ra*1e5 p2CLab*1e4 p3NPP2Cf*1e4 p4Clab2Cf*1e4 p5Cf2Cn*1e4 p6Cf2Clit*1e2 p7Cr2Clit p8Cn2Clit p9Clit2Rhl p10Clit2Csom p11Csom2Rs p12Ft   p13Fw   p14NUE  p15Cn_0  p16Clit_0 p17Cr_0 p18Clab_0 p19LMA
  p_lowers = [0.35000, 0.15000, 0.4000, 0.0000,   0.01000, 0.000500, 0.000500, 0.000500, 0.000050, 0.0001000,  0.000001000, 0.03000, 0.10000, 4.0000, 0.0000,  1.000,   1.00,   1.00,  0.011000]
  p_uppers = [0.45000, 0.40000, 0.6500, 0.5000,   0.10000, 0.008000, 0.008000, 0.080000, 0.100000, 0.0050000,  0.000100000, 0.10000, 1.50000, 8.5000, 50.0000, 200.000, 2000.00,100.00,0.025000]
  p_values = [0.40000, 0.19000, 0.5700, 0.4500,   0.05000, 0.001350, 0.004000, 0.040000, 0.014400, 0.0022400,  0.000052500, 0.05760, 1.00000, 8.0000, 10.0000, 100.000, 1000.00,50.00, 0.023000]
  #'''
  R'''
  #           p1*1.e-1		p2*5.e-7	p3*1e-5		p4*1e-5		p5*1.e-3	p6*1.e-1	p7*1.e-3	p8*1.e-2	p9*1.e-1	p10*2.e-6	p11*1e-7	p12*1e-7	p13*1e-7
  p_lowers = [0.0000001,	0.0000001,	0.0000001,	0.0000001,	0.0000001,	0.0000001,	0.0000001,	0.0000001,	0.000001,	0.0000001,	0.0000001,	0.0000001,	0.0000001]	#1,	1,	1]
  p_uppers = [0.001,		0.00000035,	0.000005,	0.000005,	0.0001,		0.001,		0.00001,	0.001,		0.001,		0.0000004,	0.0002000,	0.0002000,	0.0100000]	#2000,	2000,	100000]
  p_values = [0.00001,		0.00000025,	0.000001,	0.000001,	0.000001,	0.00001,	0.000001,	0.00001,	0.00001,	0.0000002,	0.0001000,	0.0001000,	0.0005000]	#1000,	1000,	5000]
  #'''
  p = Uniform(name='p', lower=p_lowers, upper=p_uppers, value=p_values) # p1-p13
  # Clit_0, Csom_0 #/////////////////////////////
  Csom_0 = soc[0]
  # 3.2、辅助参数。
  f = Uniform(name='f', lower=0, upper=100, value=50) # f
  # 3.3、常量。
  
  # ACM
  a2 = 0.0156
  a3 = 4.22
  a4 = 208.9
  a5 = 0.0453
  a6 = 0.378
  a7 = 7
  a8 = 0.011
  a9 = 2.1
  a10 = 0.79
  w = 2  #Max soil-leaf water potential difference (MPa)
  Rtot = 1  #Total plant-soil hydraulic resistance (MPa m2s mmol-1)
  N = 2.7  #叶氮含量
  ##################################################################################
  # 
  print ('相关参数： ')
  print ('p: ', p, 'Csom_0: ', Csom_0,
         'a2:', a2, 'a3:', a3, 'a4:', a4, 'a5:', a5, 'a6:', a6, 'a7:', a7, 'a8:', a8, 'a9:', a9, 'a10:', a10, 'w:', w, 'Rtot:', Rtot, 'N:',N)
  print ('Tave: ', len(Tave), '，  Tmax: ', len(Tmax),  '，  Rg: ', len(Rg), '，  RH: ', len(RH), '，  VPD: ', len(VPD), '，  Lat: ', len(Lat), '， Nt: ', Nt) # LAI obs
  print ('观测数据：', len(o_data), o_data)
  print ('观测索引：', len(i_data))
  # 4、模型。
  NEE_Model =  pm.Deterministic(eval = NEE_eval,
                         name = 'NEE_Model',
                         parents = {'p': p, 'Csom_0': Csom_0, #/////////////////////////////
                                    'Tave': Tave, 'Tmax': Tmax, 'Rg': Rg, 'RH': RH, 'VPD': VPD,'Lat': Lat, # LAI,obs
                                    'a2': a2, 'a3': a3, 'a4': a4, 'a5': a5, 'a6': a6, 'a7': a7, 'a8': a8, 'a9': a9, 'a10': a10, 'w': w, 'Rtot': Rtot, 'N': N,
                                    'Nt': Nt, 'idx': i_data
                                   },
                         doc = '模型构建过程。',
                         trace = True,
                         verbose = 0,
                         dtype = float,
                         plot = False,
                         cache_depth = 2)
  # 5、辅助参数。
  tau = pm.Deterministic(eval = tau_eval,
                         name = 'tau',
                         parents = {'f': f},
                         doc = '辅助参数。',
                         trace = True,
                         verbose = 0,
                         dtype = float,
                         plot = False,
                         cache_depth = 2)
  # 6、模拟数据。
  s_data = NEE_Model
  tau = tau
  # 7、似然。
  obs_size = len(o_data)
  print ('数据尺寸：', obs_size)
  y_s = []
  y = 0
  for i in range(obs_size):
    # added by whp 2017/9/24 12:46
    y_s.append(Normal(name='y{}'.format(i+1), mu=s_data[i], tau=tau, value=o_data[i], observed=True))
    #y_s.append(Normal(name='y1', mu=s_data[i], tau=tau, value=o_data[i], observed=True))
    y += y_s[i].logp
  # 8、取样器。
  # added by whp 2017/9/24 12:46
  sampler = MCMC([p, f, y_s])
  #sampler = MCMC([p, f, y])
  # AM
  sampler.use_step_method(AdaptiveMetropolis, 
                          [p, f],
                          scales = { p:[0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01],  #LAI,obs #19 #/////////////////////////////
                                    f:0.5
                                   }
                         )
  # 9、取样。
  #sampler.sample(2.0e3, 1.0e3)  # 测试
  sampler.sample(3.0e4, 2.0e4)  # 实际
  # 10、评测。
  p.summary(roundto=10)
  f.summary(roundto=10)
  # 11、轨迹数据存储 &1:1 线图。
  p_List = sampler.trace('p')[:]
  parameters = [[a2,a3,a4,a5,a6,a7,a8,a9,a10,w,Rtot,N], Tave, Tmax, Rg, RH, VPD, Lat, Csom_0] #LAI,obs
  save_Traces(p_List, out_flag, parameters, o_List)
  # 测试。
  #p = [0.005163117, 0.311702482, 0.229077374, 0.293167611, 0.068121507, 0.000720798, 0.005462561, 
  #  0.048223621, 0.000126116, 0.087061221, 32.86193663, 93.36776305, 9779.085891]
  #p = np.average(p_List, axis=0)
  #print (p)
  #results = NEE_eval(p, Clit_0, Csom_0, Ta, PAR, RH, VPD, k, aifa, Pmax, tmin, tmax, topt, beta, Nt, i_data) #LAI,obs
  #print (results)
  # ==========================================================================================

# Main: 程序开始执行的地方.
if __name__ == "__main__":
  # 0、spark对话内容。
  spark = SparkSession.builder.appName('parallize_DALEC_LAI_All').getOrCreate()
  sc = spark.sparkContext
  #sc.addPyFile('/root/xuq/20200614/model_DALEC_LAI_All.py')
  #sc.addPyFile('/root/xuq/20200614/simulation_DALEC_LAI_All.py')
  # ======================================================================================
  # 数据标记。
  strFlag = '_20200702'
  #strFlag = '_part_area' # '_all_nation'
  print (time.asctime())
  start_time = time.time()
  # ======================================================================================
  # 1、数据容器：驱动数据 &观测数据。
  # all
  path_all = 'hdfs:///user/root/Data/data_LAI' + strFlag + '.csv'
  all_RDD_data = sc.textFile(path_all).take(2)
  #
  all_List = [map(float, e.split(',')) for e in all_RDD_data]
  all_data = np.array(all_List)
  print (len(all_data))
  
  # ======================================================================================
  print ('数据加载成功 ~')
  # 单个。
  #run(all_data[4561])
  # 并行。
  data = sc.parallelize(all_data)
  data.foreach(run)
  # 结束。
  print ('结束')
  print (time.time() - start_time)
  print (time.asctime())

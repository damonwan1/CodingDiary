#! python
#-*- coding: utf-8 -*-
# 标准化输出。
from __future__ import print_function
# 各种包。
import os, sys, time
import numpy as np
import math
# HDFS
from pywebhdfs.webhdfs import PyWebHdfsClient
# 外部依赖项。
from simulation_DALEC_LAI_All import class_simulation_DALEC_with_LAI

# ==========================================================================================
# 函数。
# ==========================================================================================
# 筛选数据。
def init_Model(observation_data):
  R''' 初始化数据。
  筛选 “观测数据”，
  得到 “有效观测数据”，“有效观测数据索引”
  '''
  temp = np.array(observation_data) # 观测数据文件中所有的观测数据。
  # Without -9999.
  idxList = []
  obsList = []
  #R'''
  # 方法一、numpy 统计
  all_index = np.where(temp!=-9999)
  s1 = 0
  s2 = 0
  for i in range(len(temp)):
    x = np.sum(i==all_index[0])
    s2 += x
    carbon_idx = all_index[1][s1:s2]
    carbon_obs = temp[i][carbon_idx]
    # All of the index, data of observations.
    idxList.append(carbon_idx)
    obsList.append(carbon_obs)
    s1 = s2
  #'''
  R'''
  # 方法二、for 筛选
  # the number of the observations.
  _len = len(temp)
  for j in range(_len):
    # One of the observation. [Cw, Cf, Cr, ...]
    carbon_x = np.array(temp[j])
    # Index, Data of one observation.
    carbon_idx = np.where(carbon_x!=-9999)
    carbon_obs = carbon_x[carbon_idx]
    # All of the index, data of observations.
    idxList.append(carbon_idx)
    obsList.append(carbon_obs)
  #'''
  #
  # The array data.
  i_data = np.array(idxList)
  o_data = np.array(obsList)
  # Returns.
  return i_data, o_data
  # =======================================================================================  

#333333333333333333333333333333333333333333333  #LAI,obs
# The Model.
def NEE_eval(p, Csom_0, Tave, Tmax, Rg, RH, VPD, Lat, a2, a3, a4, a5, a6, a7, a8, a9, a10, w, Rtot, N, Nt, idx):
  # ==========================================hlj
  # p1~p13: 1.e[*]
  #R'''
  p1 = p[0]#*1.e5
  p2 = p[1]#*1.e5
  p3 = p[2]#*1.e5
  p4 = p[3]#*1.e5
  p5 = p[4]#*1.e5
  p6 = p[5]#*1.e6
  p7 = p[6]#*1.e6
  p8 = p[7]#*1.e6
  p9 = p[8]#*1.e6
  p10 = p[9]#*1.e6
  p11 = p[10]#*1.e6
  p12 = p[11]#*1.e4
  p13 = p[12]#*1.e6
  p14 = p[13]*1.e1
  p15 = p[14]*1.e2
  p16 = p[15]*1.e3
  p17 = p[16]*1.e3
  p18 = p[17]*1.e2
  p19 = p[18]#*1.e4
  #'''
  R'''
  p1 = p[0]*1 #1.e1
  p2 = p[1]*1e2 #5.e7
  p3 = p[2]*1e2 #1.e5
  p4 = p[3]*1e2 #1.e5
  p5 = p[4]*1 #1.e3
  p6 = p[5]*1 #1.e1
  p7 = p[6]*1 #1.e3
  p8 = p[7]*1 #1.e2
  p9 = p[8]*1 #1.e1
  p10 = p[9]*1 #2.e6
  p11 = p[10]*1e6 #1.e7
  p12 = p[11]*1e6 #1.e7
  p13 = p[12]*1e7 #1.e7
  #'''
  # ==========================================hlj
  # Carbon p15Cn_0  p16Clit_0 p17Cr_0 p18Clab_0
  Cf_0 = 0 #1,叶片
  Cr_0 = p17 #2,细根
  Cn_0 = p15 #3，木质
  Clit_0 = p16 #4,凋落物  
  Clab_0 = p18 #5,凋落物    
  Csom_0 = Csom_0 #6,土壤有机质
  # driver.
  Tave = Tave
  Tmax = Tmax
  I = Rg
  RH = RH/100
  VPD = VPD
  Lat = Lat
  # LAI,obs
  # =========================================================================
  # LAI: obs.
  LMA = p19
  LAI = np.zeros((1, Nt), dtype='float32')
  # =========================================================================
  # constant.
  #ACM
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
  Ca = [338.751666666667, 340.105000000000, 341.447500000000, 343.054166666667, 344.451818181818, 346.115833333333, 347.420000000000, 349.194166666667, 351.566666666667, 353.120833333333, 354.394166666667, 355.607500000000, 356.445833333333, 357.100000000000, 358.832500000000, 360.820000000000, 362.606666666667, 363.729166666667, 366.700000000000, 368.377500000000, 369.549166666667, 371.143333333333, 373.279166666667, 375.801666666667, 377.522500000000, 379.795833333333, 381.895833333333, 383.791666666667, 385.604166666667, 387.430000000000, 389.899166666667, 391.652500000000, 393.853333333333, 396.520833333333, 398.647500000000, 400.834166666667, 404.239166666667, 406.553333333333, 408.521666666667]
  # 4 observation.
  soc = np.zeros((1, Nt), dtype='float32')
  agbc = np.zeros((1, Nt), dtype='float32')
  bgbc = np.zeros((1, Nt), dtype='float32')
  # =============================================================
  # GPPM.
  gppm = np.array([0.]*Nt, dtype='float32')   # 6, ok
  fw = np.zeros((1, Nt), dtype='float32')    # 4
  gpp = np.zeros((1, Nt), dtype='float32')   # 5
  agc = np.zeros((1, Nt), dtype='float32')   # 22
  bgc = np.zeros((1, Nt), dtype='float32')   # 23
  # DALEC.
  Ra = np.zeros((1, Nt), dtype='float32')   # 7
  Af = np.zeros((1, Nt), dtype='float32')   # 8
  Ar = np.zeros((1, Nt), dtype='float32')   # 9
  Alab = np.zeros((1, Nt), dtype='float32')   # 10
  An = np.zeros((1, Nt), dtype='float32')   # 10
  Afromlab = np.zeros((1, Nt), dtype='float32')   # 10
  Lf = np.zeros((1, Nt), dtype='float32')   # 11
  Ln = np.zeros((1, Nt), dtype='float32')   # 12
  Lr = np.zeros((1, Nt), dtype='float32')   # 13
  Rh1 = np.zeros((1, Nt), dtype='float32')   # 14
  Rh2 = np.zeros((1, Nt), dtype='float32')   # 15
  D = np.zeros((1, Nt), dtype='float32')    # 16
  Cf = np.zeros((1, Nt), dtype='float32')    # 2, 17
  Cn = np.zeros((1, Nt), dtype='float32')    # 18
  Cr = np.zeros((1, Nt), dtype='float32')    # 19
  Clit = np.zeros((1, Nt), dtype='float32')   # 20
  Csom = np.zeros((1, Nt), dtype='float32')   # 21
  Clab = np.zeros((1, Nt), dtype='float32')   # 21
  # =========================================================================
  for i in range(Nt):
    # GPPD->GPPM.
    # =========================================================================
    # LAI: obs.
    # =========================================================================
    # LAI.
    if 0 == i:
      LAI[0][i] = max(0, Cf_0*LMA)
    else:
      LAI[0][i] = max(0, Cf[0][i-1]*LMA)
    # =========================================================================
    #p1Ra  p2gpp2CLab p3NPP2Cf p4Clab2Cf p5Cf2Cn p6Cf2Clit p7Cr2Clit p8Cn2Clit p9Clit2Rhl p10Clit2Csom p11Csom2Rs p12Ft   p13Fw   p14NUE  p15Cn_0  p16Clit_0 p17Cr_0 p18Clab_0 p19LMA

    fw[0][i] = math.pow(RH[i],(VPD[i]/p13))
    if 0 > fw[0][i]:
      fw[0][i] = 0
    if 1 < fw[0][i]:
      fw[0][i] = 1

    DOY = (i+1)%12
    if 0 == DOY:
      DOY = 12
    lat=Lat[0];
    print (lat)
    #ACM
    SD = -0.408*math.cos(2*math.pi*((DOY-1)*30+15+10)/365)#solar decline
    s = 24*math.acos(-math.tan(math.pi*lat/180)*math.tan(SD))/math.pi#daylength
    q = a3-a4
    E = a7*math.pow(LAI[0][i],2)/(math.pow(LAI[0][i],2)+a9)
    g = math.pow(abs(w),a10)/(0.5*(Tmax[i]-Tave[i])+a6*Rtot)
    #a1,氮利用效率
    P = p14*N*LAI[0][i]*math.exp(a8*Tmax[i])/g
    Ci = (Ca[int(i/12)]+q-P+math.pow(math.pow((Ca[int(i/12)]+q-P),2)-4*(Ca[int(i/12)]*q-a3*P),0.5))*0.5
    gpp[0][i] = fw[0][i]*(a2*s+a5)*E*I[i]*g*(Ca[int(i/12)]-Ci)/(E*I[i]+g*(Ca[int(i/12)]-Ci))

    if 0 == LAI[0][i]:
      gpp[0][i]=0

    #gpp[0][i] = gppmax[0][i]*ft*fw[0][i]*12
    gppm[i] = gpp[0][i]*30
    # ==============================================================================
    if 0 == i:
      # same
      Trate = 0.5*np.exp(p12*Tave[i])
      DOY = (i+1)%12
      if 0 == DOY:
        DOY = 12
      Ra[0][i] = p1*gppm[i]
      Af[0][i] = (gppm[i] - Ra[0][i])*p3
      Ar[0][i] = gppm[i] - Ra[0][i] - Af[0][i]
      Alab[0][i] = 0
      An[0][i] = 0
      Afromlab[0][i] = 0
      # 3333333333333333333333333333 #/////////////////////////////
      Lf[0][i] = p6*Cf_0
      Ln[0][i] = p8*Cn_0
      Lr[0][i] = p7*Cr_0
      Rh1[0][i] = p9*Clit_0*Trate*fw[0][i]
      Rh2[0][i] = p11*Csom_0*Trate*fw[0][i]
      D[0][i] = p10*Clit_0*Trate*fw[0][i]
      Cf[0][i] = Cf_0 + Af[0][i] - Lf[0][i]
      Cn[0][i] = Cn_0 + An[0][i] - Ln[0][i]
      Cr[0][i] = Cr_0 + Ar[0][i] - Lr[0][i]
      Clit[0][i] = Clit_0 + Lf[0][i]+ Ln[0][i] + Lr[0][i] -Rh1[0][i] - D[0][i]
      Csom[0][i] = Csom_0 + D[0][i] - Rh2[0][i]
      Clab[0][i] = Clab_0 + Alab[0][i] - Afromlab[0][i]
      # 3333333333333333333
      agc[0][i] = Cf[0][i]
      bgc[0][i] = Cr[0][i]
    else:
      Trate = 0.5*np.exp(p12*Tave[i])
      DOY = (i+1)%12
      if 0 == DOY:
        DOY = 12
      Ra[0][i] = p1*gppm[i]
      #9月开始凋落
      if 8.0 <= DOY:
        Alab[0][i] = p2*(gppm[i] - Ra[0][i])
        An[0][i] = p5*Cf[0][i-1]
      else:
        Alab[0][i] = 0
        An[0][i] = 0

      Af[0][i] = (gppm[i] - Ra[0][i] - Alab[0][i])*p3
      Ar[0][i] = gppm[i] - Ra[0][i] - Af[0][i] - Alab[0][i]
      #4月开始萌发
      #if 1 < p4*30:
      #  p4 = 1/30
      if 3 < DOY < 6:
        Afromlab[0][i] = Clab[0][i-1]*p4
      else:
        Afromlab[0][i] = 0

      # changes
      Lf[0][i] = p6*(Cf[0][i-1] - An[0][i])
      Lr[0][i] = p7*Cr[0][i-1]
      Ln[0][i] = p8*Cn[0][i-1]
      #if Lf[0][i]+An[0][i]>Cf[0][i-1]:
      #  Lf[0][i]=Lf[0][i]/(Lf[0][i]+An[0][i])
      #  An[0][i]=Cf[0][i-1]-Lf[0][i]
      Rh1[0][i] = p9*Clit[0][i-1]*Trate*fw[0][i]
      Rh2[0][i] = p11*Csom[0][i-1]*Trate*fw[0][i]
      D[0][i] = p10*Clit[0][i-1]*Trate*fw[0][i]    #################################
      Cf[0][i] = Cf[0][i-1] + Af[0][i] - Lf[0][i] + Afromlab[0][i] - An[0][i]
      Cn[0][i] = Cn[0][i-1] + An[0][i] - Ln[0][i]
      Cr[0][i] = Cr[0][i-1] + Ar[0][i] - Lr[0][i]
      Clit[0][i] = Clit[0][i-1] + Lf[0][i] + Lr[0][i] + Ln[0][i] -Rh1[0][i] - D[0][i]
      Csom[0][i] = Csom[0][i-1] + D[0][i] - Rh2[0][i]
      Clab[0][i] = Clab[0][i-1] + Alab[0][i] - Afromlab[0][i]
      #if 0 < Cf[0][i]:
      #  Cf[0][i] = 0
      #if 0 < Clab[0][i]:
      #  Clab[0][i] = 0
      # 3333333333333333333 #/////////////////////////////
      agc[0][i] = Cf[0][i]
      bgc[0][i] = Cr[0][i]
    #
  # 
  # 1
  soc[0][0] = np.mean(Csom[0][24:119])#[:96]) # 96 (1:96): 1982-1989年平均值
  soc[0][1] = np.mean(Csom[0][288:371])#[-74:])  #74 (265:348);%2004-2010年平均值 06
  soc[0][2:] = -9999
  # 2
  agbc[0][0] = np.mean(agc[0][24:119])#[:96]) #1982-1989年平均值
  agbc[0][1] = np.mean(agc[0][288:371]) #[-74:]) #2004-2010年平均值
  agbc[0][2:] = -9999
  # 3
  bgbc[0][0] = np.mean(bgc[0][24:119])#[:96]) #1982-1989年平均值
  bgbc[0][1] = np.mean(bgc[0][288:371]) #[-74:]) #2004-2010年平均值
  bgbc[0][2:] = -9999
  # 4
  LAI[0][0:23] = -9999#[:96]) #1980-1981年无LAI数据
  LAI[0][24:455] = LAI[0][24:455] #1982-2017年平均值
  LAI[0][456:467] = -9999 #2018年无LAI数据
  #
  # without -9999
  # LAI: obs
  # =========================================================================
  all_results = [soc, agbc, bgbc, LAI]
  # =========================================================================
  _results = []
  obs_size = len(idx)
  for j in range(obs_size):
    tmp_result = []
    for k in idx[j]:
      tmp_result.append(round(all_results[j][0][k], 8))  # 精度
    _results.append(tmp_result)

  # Return the model result.
  return _results
  # =======================================================================10==========

# 辅助参数。
def tau_eval(f):
  tau = np.power(f, -2)
  return tau

# 取样器数据。
def save_Traces(traces, out_flag, parameters, o_List):
  # =====================================================================================================
  # 存储参数变化轨迹。
  trace_p_all = np.array(traces)
  # 均值, 方差
  avg_p_all = np.average(trace_p_all, axis=0)
  std_p_all = np.std(trace_p_all, axis=0)
  print (avg_p_all)
  print (std_p_all)
  # 输出内容
  traces_out = trace_p_all.tolist()
  traces_out.append(avg_p_all.tolist())
  traces_out.append(std_p_all.tolist())
  # 字符串。
  traces_out = str(traces_out)
  traces_out = traces_out[1:-2].replace(" ", "").replace("[", "").replace("],", "\n").replace(",", "\t").strip()
  #print ('轨迹数据\n', traces_out)
  #R'''
  path_flag = 'out_All_%s.txt' %(out_flag)
  # 定义HDFS数据源，并写入。
  #hdfs = PyWebHdfsClient(host='192.168.1.20', port='50070', user_name='hadoop') # 家里
  
  #hdfs = PyWebHdfsClient(host='192.168.16.217', port='50070', user_name='root') # 所里
  #path_flag = '/user/root/Out20200702/' + path_flag
  
  #path_flag = '/test/out/' + path_flag
  print ('参数轨迹：', path_flag)
  
  #print (traces_out)
  #hdfs.create_file(path_flag, traces_out, overwrite=True)
  with open(path_flag, 'w') as file_object:
    file_object.write(traces_out)
  
  # =====================================================================================================
  # 存储1:1 线图。
  # 对象：[[k, aifa, Pmax, tmin, tmax, topt, beta], Ta, PAR, RH, VPD, Clit_0, Csom_0]。  # LAI: obs
  cSDL = class_simulation_DALEC_with_LAI(parameters)
  # 模拟数据：最优参数。
  sim_results = cSDL.NEE_Model(avg_p_all)
  sim_results = np.squeeze(sim_results) # (n, Nt)
  # 获取输出列表。
  results = str(zip(*sim_results))
  results = results[1:-2].replace(" ", "").replace("(", "").replace("),", "\n").strip()
  #R'''
  path_simulation = 'simulation_%s.csv' %(out_flag)
  # 写入HDFS文件。  
  path_simulation = '/test/out/' + path_simulation                        
  print ('模拟数据：', path_simulation)
  #print (results)
  #with open('./out.csv', 'w') as f:
  #  f.write(results)
  #hdfs.create_file(path_simulation, results, overwrite=True)
  with open(path_simulation, 'w') as file_object:
    file_object.write(results)
  # =====================================================================================================
  print ('存储结束 ')


# main函数。
if __name__ == "__main__":
  # 当前路径。
  curval = os.getcwd()
  print ("当前目录：%r" %(curval))
  # 站点。
  _flag = 'HTFs'
  # 1_0、加载数据。
  # 文件路径。
  driver_path = './HDFS/driver_' + _flag + '.csv'
  observation_path = './HDFS/observation_' + _flag + '.csv'
  # 文件读取 & 转换数据类型。
  driver_org_data = open(driver_path).readlines()
  driver_List = [map(float, e.split(',')) for e in driver_org_data]
  observation_org_data = open(observation_path).readlines()
  observation_List = [map(float, e.split(',')) for e in observation_org_data]
  # 1、数据预处理函数。
  driver_data, index_data, observation_data = init_Model(driver_List, observation_List)
  # ====================================================================================
  # 2_0、参数设置。
  # 参数。
  p = [0.0000040, 0.0000019, 0.0000057, 0.0000045,    0.0000050,  0.0000013,     0.0000040,   0.00000400,   0.000001440,   0.00000224,      0.000000530,   0.0000058, 0.0000010, 0.0000080, 0.0000010,    0.0000100,     0.00001000,  0.0000050,  0.0000023]
  Cf_0 = 0
  Cr_0 = 730
  Cn_0 = 12
  Clab_0 = 20
  Clit_0 = 150
  Csom_0 = 7600

  Tave_0 = 7
  Tave = driver_data[Tave_0-1]
  Tmax_0 = 8
  Tmax = driver_data[Tmax_0-1]
  Rg_0 = 11
  Rg = driver_data[Rg_0-1]
  RH_0 = 9
  RH = driver_data[RH_0-1]
  VPD_0 = 10
  VPD = driver_data[VPD_0-1]
  Lat_0 = 12
  Lat = driver_data[Lat_0-1]
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
  Nt = len(Tave)
  idx = index_data
  sim_List = [0, 0, 1, 1, 1, 1, 1, 1] #[NEE, RE, Cf, Cr, Cw, Clit, Csom, LAI]
  # 2、模型构建。
  simulation_data = NEE_eval(p, Csom_0, Tave, Tmax, Rg, RH, VPD, Lat, a2, a3, a4, a5, a6, a7, a8, a9, a10, w, Rtot, N, Nt, idx, sim_List)
  print ('模拟数据：\n', simulation_data)
  # ======================================================================================
  # 3、辅助参数。
  tau = tau_eval(5.)
  print ('辅助参数：\n', tau)
  # 
  print ('结束~')

#! python
# -*- coding: utf-8 -*-
#
import numpy as np
import csv
import os, sys
import math
#
class class_simulation_DALEC_with_LAI:
  R''' The class.
  '''
  # Initialize the parameters.
  def __init__(self, parameters):
    # [[k, aifa, Pmax, tmin, tmax, topt, beta], Ta, PAR, RH, VPD, Clit_0, Csom_0]
                                                    # Constants.
    self.a2 = parameters[0][0]
    self.a3 = parameters[0][1]
    self.a4 = parameters[0][2]
    self.a5 = parameters[0][3]
    self.a6 = parameters[0][4]
    self.a7 = parameters[0][5]
    self.a8 = parameters[0][6]
    self.a9 = parameters[0][7]
    self.a10 = parameters[0][8]
    self.w = parameters[0][9]  #Max soil-leaf water potential difference (MPa)
    self.Rtot = parameters[0][10]  #Total plant-soil hydraulic resistance (MPa m2s mmol-1)
    self.N = parameters[0][11]  #叶氮含量

    # Ta.Tave, Tmax, Rg, RH, VPD, Lat, Csom_0
    self.Tave = np.array(parameters[1])
    #self.Nt = len(self.Tave)
    # gppd.
    self.Tmax = np.array(parameters[2])
    self.Rg = np.array(parameters[3])
    self.RH = np.array(parameters[4])
    self.VPD = np.array(parameters[5])
    self.Lat = np.array(parameters[6])
    #
    self.Csom_0 = parameters[7] # Csom_0

  #
  # The Model.
  def NEE_Model(self, pList):
    # Params.
    p = np.array(pList, 'float')
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
    p19 = p[18]#*1.e4 #1.e7
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
    R'''
    p1 = p[0]*1.e1
    p2 = p[1]*5.e7
    p3 = p[2]*1.e5
    p4 = p[3]*1.e5
    p5 = p[4]*1.e3
    p6 = p[5]*1.e1
    p7 = p[6]*1.e3
    p8 = p[7]*1.e2
    p9 = p[8]*1.e1
    p10 = p[9]*2.e6
    p11 = p[10]*1.e7
    p12 = p[11]*1.e7
    p13 = p[12]*1.e7
    #'''
    # ==========================================hlj
    # Carbon
    Cf_0 = 0 #1,叶片
    Cr_0 = p17 #2,细根
    Cn_0 = p15 #3，木质
    Clit_0 = p16 #4,凋落物  
    Clab_0 = p18 #5,凋落物    
    Csom_0 = self.Csom_0 #6,土壤有机质
    # driver.
    Tave = self.Tave
    Tmax = self.Tmax
    I = self.Rg
    RH = self.RH/100
    VPD = self.VPD
    Lat = self.Lat
    Nt=len(Tave)
    # =========================================================================
    # LAI: obs.
    LMA = p19
    LAI = np.zeros((1, Nt), dtype='float32')
    # =========================================================================
    # coanstants.
    #ACM
    a2 = self.a2
    a3 = self.a3
    a4 = self.a4
    a5 = self.a5
    a6 = self.a6
    a7 = self.a7
    a8 = self.a8
    a9 = self.a9
    a10 = self.a10
    w = self.w #Max soil-leaf water potential difference (MPa)
    Rtot = self.Rtot #Total plant-soil hydraulic resistance (MPa m2s mmol-1)
    N = self.N
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
        #
      fw[0][i] = math.pow(RH[i],(VPD[i]/p13))

      if 0 > fw[0][i]:
        fw[0][i] = 0
      if 1 < fw[0][i]:
        fw[0][i] = 1

      DOY = (i+1)%12
      if 0 == DOY:
        DOY = 12
      #ACM
      SD = -0.408*math.cos(2*math.pi*((DOY-1)*30+15+10)/365)#solar decline
      s = 24*math.acos(-math.tan(math.pi*Lat[i]/180)*math.tan(SD))/math.pi#daylength
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
        # same
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
          Alab[0][i] = 0

        Af[0][i] = (gppm[i] - Ra[0][i] - Alab[0][i])*p3
        Ar[0][i] = gppm[i] - Ra[0][i] - Af[0][i] - Alab[0][i]
        #4月开始萌发
        #if 1 < p4*30:
        #  p4 = 1/30
        if  3 < DOY<6:
          Afromlab[0][i] = Clab[0][i-1]*p4
        else:
          Afromlab[0][i] = 0

        # changes
        Lf[0][i] = p6*(Cf[0][i-1] - An[0][i])
        Lr[0][i] = p7*Cr[0][i-1]
        Ln[0][i] = p8*Cn[0][i-1]
        Rh1[0][i] = p9*Clit[0][i-1]*Trate*fw[0][i]
        Rh2[0][i] = p11*Csom[0][i-1]*Trate*fw[0][i]
        D[0][i] = p10*Clit[0][i-1]*Trate*fw[0][i]     #################################
        Cf[0][i] = Cf[0][i-1] + Af[0][i] - Lf[0][i] + Afromlab[0][i] - An[0][i]
        Cn[0][i] = Cn[0][i-1] + An[0][i] - Ln[0][i]
        Cr[0][i] = Cr[0][i-1] + Ar[0][i] - Lr[0][i]
        Clit[0][i] = Clit[0][i-1] + Lf[0][i] + Lr[0][i] + Ln[0][i] -Rh1[0][i] - D[0][i]
        Csom[0][i] = Csom[0][i-1] + D[0][i] - Rh2[0][i]
        Clab[0][i] = Clab[0][i-1] + Alab[0][i] - Afromlab[0][i]
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
    LAI[0][456:] = -9999 #2018年无LAI数据
    # =================================================================================
    # 综合。
    # =========================================================================
    # LAI: obs
    # =========================================================================
    all_results = [soc, agbc, bgbc, LAI]
    return all_results

if __name__ == "__main__":
  # 驱动数据路径。
  #driver_path = './HDFS/driver_HTFs.csv'
  # 1.1、驱动数据。
  # tave
  path_Tave = './HDFS/Tave_with_LAI.csv'                          # ta
  Tave_RDD_data = open(path_Tave).readlines()
  Tave_with_LAI = [map(float, e.split(',')) for e in Tave_RDD_data]
  Tave_with_LAI = np.array(Tave_with_LAI)
  # tmax
  path_Tmax = './HDFS/Tmax_with_LAI.csv'                          # ta
  Tmax_RDD_data = open(path_Tmax).readlines()
  Tmax_with_LAI = [map(float, e.split(',')) for e in Tmax_RDD_data]
  Tmax_with_LAI = np.array(Tmax_with_LAI)
  # Rg
  path_Rg = './HDFS/Rg_with_LAI.csv'                            # I
  Rg_RDD_data = open(path_Rg).readlines()
  Rg_with_LAI = [map(float, e.split(',')) for e in Rg_RDD_data]
  Rg_with_LAI = np.array(Rg_with_LAI)
  # RH
  path_RH = './HDFS/RH_with_LAI.csv'                          # RH
  RH_RDD_data = open(path_RH).readlines()
  RH_with_LAI = [map(float, e.split(',')) for e in RH_RDD_data]
  RH_with_LAI = np.array(RH_with_LAI)
  # VPD
  path_VPD = './HDFS/VPD_with_LAI.csv'                        # VP
  VPD_RDD_data = open(path_VPD).readlines()
  VPD_with_LAI = [map(float, e.split(',')) for e in VPD_RDD_data]
  VPD_with_LAI = np.array(VPD_with_LAI)
  # Lat
  path_Lat = './HDFS/Lat_with_LAI.csv'                          # RH
  Lat_RDD_data = open(path_Lat).readlines()
  Lat_with_LAI = [map(float, e.split(',')) for e in Lat_RDD_data]
  Lat_with_LAI = np.array(Lat_with_LAI)
  # 
  #[ta_with_LAI, I_with_LAI, RH_with_LAI, VP_with_LAI]
  # 参数。
  Cf_0 = 0
  Cr_0 = 730
  Cn_0 = 12
  Clab_0 = 20
  Clit_0 = 150
  Csom_0 = 7600
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
  # 模型构造。
  myDALEC = class_simulation_DALEC_with_LAI([[Cf_0, Cr_0, Cn_0, Clab_0, Clit_0, Csom_0, a2, a3, a4, a5, a6, a7, a8, a9, a10, w, Rtot], Tave_with_LAI[0], Tmax_with_LAI[0], Rg_with_LAI[0], RH_with_LAI[0], VPD_with_LAI[0], Lat_with_LAI[0]])
  print ('1、初始化对象成功~')
  print ('2、数据加载成功~')                                               
  # 传递参数，模拟。
  p_List = [0.0000040, 0.0000019, 0.0000057, 0.0000045,    0.0000050,  0.0000013,     0.0000040,   0.00000400,   0.000001440,   0.00000224,      0.000000530,   0.0000058, 0.0000010, 0.0000080, 0.0000010,    0.0000100,     0.00001000,  0.0000050,  0.0000023]
  results = myDALEC.NEE_Model(p_List)
  print (len(results))
  NUM = 4
  print (results[2][0][:NUM], results[3][0][:NUM], results[4][0][:NUM], results[5][0][:NUM], results[6][0][:NUM], results[7][0][:NUM])
  print ('3、结束~')

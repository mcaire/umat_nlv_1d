########################################################################
# SPOSS - Special purpose open source software initiative
# www.inoceano.com/sposs
########################################################################
# Name        : abaqus_umat_nlv_beam.py
# Author      : Marcelo Caire
# Copyright   : <2016>  <INOCEANO>
# Version     : 2.0
# Release Notes: Correction in the strain increment
# Description : This Python subroutine writes an Abaqus UMAT for the 
# unidimensional finite element modeling of nonlinear viscoelastic 
# structures. A brief theoretical description of the constitutive 
# equation employed in the implementation can be found at: 
# http://www.inoceano.com/sposs/umat/
########################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
########################################################################
import os

#=======================================================================
#Define the name of the subroutine
#=======================================================================
filesub = open('umat_subroutine.for','w')

#=======================================================================
#Define the number of terms used in the formulation (qmax and mmax)
#=======================================================================
qmax = 5  # number of terms in the functional series expansion
mmax = 6  # number of prony terms
ddsde = 100000
#=======================================================================
#License terms
filesub.write('C Author       : Marcelo Caire\n')
filesub.write('C Copyright    : <2015>  <INOCEANO>\n')
filesub.write('C Version      : 2.0\n')
filesub.write('C Release notes: Correction made in the strain increment\n')
filesub.write('C This program comes with ABSOLUTELY NO WARRANTY\n')
filesub.write('C This program is free software: you can redistribute it and/or modify\n')
filesub.write('C it under the terms of the GNU General Public License as published by\n')
filesub.write('C the Free Software Foundation version 3 of the License\n')
#UMAT subroutine definitions according to Abaqus manual
filesub.write('\tSUBROUTINE UMAT(STRESS,STATEV,DDSDDE,SSE,SPD,SCD,\n'.expandtabs(7))
filesub.write('\t1 RPL,DDSDDT,DRPLDE,DRPLDT,\n'.expandtabs(5))
filesub.write('\t2 STRAN,DSTRAN,TIME,DTIME,TEMP,DTEMP,PREDEF,DPRED,CMNAME, \n'.expandtabs(5))
filesub.write('\t3 NDI,NSHR,NTENS,NSTATV,PROPS,NPROPS,COORDS,DROT,PNEWDT, \n'.expandtabs(5))
filesub.write('\t4 CELENT,DFGRD0,DFGRD1,NOEL,NPT,LAYER,KSPT,KSTEP,KINC)\n'.expandtabs(5))
filesub.write('C\n')
filesub.write('\tINCLUDE'.expandtabs(7) + " 'ABA_PARAM.INC'" + '\n')
filesub.write('C\n')
filesub.write('\tCHARACTER*80 CMNAME\n'.expandtabs(7))
filesub.write('\tDIMENSION STRESS(NTENS),STATEV(NSTATV),\n'.expandtabs(7))
filesub.write('\t1 DDSDDE(NTENS,NTENS),\n'.expandtabs(5))
filesub.write('\t2 DDSDDT(NTENS),DRPLDE(NTENS),\n'.expandtabs(5))
filesub.write('\t3 STRAN(NTENS),DSTRAN(NTENS),TIME(2),PREDEF(1),DPRED(1),\n'.expandtabs(5))
filesub.write('\t4 PROPS(NPROPS),COORDS(3),DROT(3,3),DFGRD0(3,3),DFGRD1(3,3)\n'.expandtabs(5))
filesub.write('\tDIMENSION DSTRES(6),D(3,3)\n'.expandtabs(7))
#=======================================================================
# Relaxation coefficients - G_qm
filesub.write('C---------------------------------------\n')
for q in range(1,qmax+1):
    filesub.write('\tREAL '.expandtabs(7))
    filesub.write('G' + str(q) + '0' + ',')
    for m in range(1,mmax+1):
        if m < mmax:
            filesub.write('G' + str(q) + str(m) + ',')
        elif m == mmax:
            filesub.write('G' + str(q) + str(m) + '\n')
#=======================================================================
# Relaxation times - TAU_m
filesub.write('C---------------------------------------\n')
filesub.write('\tREAL '.expandtabs(7))
for m in range(1,mmax+1):
    if m < mmax:
        filesub.write('TAU' + str(m) + ',')
    elif m == mmax:
        filesub.write('TAU' + str(m) + '\n')
#=======================================================================
# Q_qm
filesub.write('C---------------------------------------\n')
for q in range(1,qmax+1):
    filesub.write('\tREAL '.expandtabs(7))
    filesub.write('Q' + str(q) + '0' + ',')
    for m in range(1,mmax+1):
        if m < mmax:
            filesub.write('Q' + str(q) + str(m) + ',')
        elif m == mmax:
            filesub.write('Q' + str(q) + str(m) + '\n')
#=======================================================================
# DQ_qm
filesub.write('C---------------------------------------\n')
for q in range(1,qmax+1):
    filesub.write('\tREAL '.expandtabs(7))
    filesub.write('DQ' + str(q) + '0' + ',')
    for m in range(1,mmax+1):
        if m < mmax:
            filesub.write('DQ' + str(q) + str(m) + ',')
        elif m == mmax:
            filesub.write('DQ' + str(q) + str(m) + '\n')
#=======================================================================
# A_m
filesub.write('C---------------------------------------\n')
filesub.write('\tREAL '.expandtabs(7))
for m in range(1,mmax+1):
    if m < mmax:
        filesub.write('A' + str(m) + ',')
    elif m == mmax:
        filesub.write('A' + str(m) + '\n')
#=======================================================================
# B_m
filesub.write('\tREAL '.expandtabs(7))
for m in range(1,mmax+1):
    if m < mmax:
        filesub.write('B' + str(m) + ',')
    elif m == mmax:
        filesub.write('B' + str(m) + '\n')
#=======================================================================
# EV and DEV
filesub.write('\tREAL EV,DEV\n'.expandtabs(7))
#=======================================================================
filesub.write('C---------------------------------------\n')
filesub.write('C Variables to be defined\n')
filesub.write('C---------------------------------------\n')
filesub.write('C DDSDE(NTENS,NTENS) - Jacobian matrix of the constitutive model.\n')
filesub.write('C STRESS(NTENS) - This array is passed in as the stress tensor at the begining of the increment\n')
filesub.write('C                 and must be updated in this routine to be the stress tensor at the end of the increment.\n')
filesub.write('C STATEV(NSTATV)- An array containing the solution-dependent state variables. These are passed in as the values at the\n')
filesub.write('C                 begining of the increment\n')
filesub.write('C---------------------------------------\n')
filesub.write('C Variables passed in for information\n')
filesub.write('C---------------------------------------\n')
filesub.write('C STRAN(NTENS) - An array containing the total strains at the beginning of the increment.\n')
filesub.write('C DSTRAN(NTENS) - Array of strain increments.\n')
filesub.write('C NDI  - Number of direct stress components at this point\n')
filesub.write('C NSHR - Number of engineering shear stress components at this point\n')
filesub.write('C NTENS - Size of the stress or strain component array (NDI + NSHR)\n')
filesub.write('C---------------------------------------\n')
filesub.write('C EVALUATE NEW STRESS TENSOR\n')
filesub.write('C---------------------------------------\n')
#=======================================================================
# Define PROPS (G_qm)
counter = 0 #reset counter
for q in range(1,qmax+1):
    filesub.write('C---------------------------------------\n')
    counter = counter + 1
    filesub.write('\tG'.expandtabs(7) + str(q) + '0' + '=' + 'PROPS(' + str(counter) + ')\n')
    for m in range(1,mmax+1):
        counter = counter + 1
        filesub.write('\tG'.expandtabs(7) + str(q) + str(m) + '=' + 'PROPS(' + str(counter) + ')\n')
#=======================================================================
# Define PROPS (Tau_m)
filesub.write('C---------------------------------------\n')        
for m in range(1,mmax+1):
    counter = counter + 1
    filesub.write('\tTAU'.expandtabs(7) + str(m) + '=' + 'PROPS(' + str(counter) + ')\n')
#=======================================================================
# Define A_m
filesub.write('C---------------------------------------\n')
counter = 0 #reset counter
for m in range(1,mmax+1):
    counter = counter + 1
    filesub.write('\tA'.expandtabs(7)+str(counter) + ' = EXP(-DTIME/TAU' + str(counter) + ')-1\n')
#=======================================================================
# Define B_m
filesub.write('C---------------------------------------\n')
counter = 0 #reset counter
for m in range(1,mmax+1):
    counter = counter + 1
    filesub.write('\tB'.expandtabs(7)+str(counter) + ' = TAU' + str(counter) +'*(1-EXP(-DTIME/TAU' + str(counter) + '))\n')    
#=======================================================================
# Define EV and DEV
filesub.write('C---------------------------------------\n')
filesub.write('\tEV  = STRAN(1) + STRAN(2) + STRAN(3)\n'.expandtabs(7))
filesub.write('\tDEV = DSTRAN(1)+ DSTRAN(2)+ DSTRAN(3)\n'.expandtabs(7))
#=======================================================================
# Define Q_qm
filesub.write('C---------------------------------------\n')
counter = 0 #reset counter
for q in range(1,qmax+1):
    filesub.write('C--------------------\n')
    counter = counter + 1
    filesub.write('\tQ'.expandtabs(7) + str(q) + '0' + '=' + 'STATEV(' + str(counter) + ')\n')
    for m in range(1,mmax+1):
        counter = counter + 1
        filesub.write('\tQ'.expandtabs(7) + str(q) + str(m) + '=' + 'STATEV(' + str(counter) + ')\n')
#=======================================================================
# Auxiliar functions 
def auxdq(q):
	res = '(STRAN(1) + DSTRAN(1))**' + str(q) + ' - STRAN(1)**' + str(q) + '\n'
	return res
#=======================================================================
filesub.write('C---------------------------------------\n')
for q in range(1,qmax+1):
    filesub.write('C---------------------------------------\n')
    filesub.write('\tDQ'.expandtabs(7)+str(q)+'0' + ' = ' + auxdq(q))
    for m in range(1,mmax+1):
        filesub.write('\tDQ'.expandtabs(7)+str(q)+str(m) + ' = Q'+str(q)+str(m)+'*A'+str(m) +
        ' + (DQ' + str(q) + '0/DTIME)*B' + str(m)+ '\n')
#=======================================================================
filesub.write('C---------------------------------------\n')
for q in range(1,qmax+1):
    filesub.write('C---------------------------------------\n')
    filesub.write('\tQ'.expandtabs(7)+str(q)+'0' + ' = Q'+str(q)+'0'+' + DQ'+str(q)+'0'+'\n')
    for m in range(1,mmax+1):
        filesub.write('\tQ'.expandtabs(7)+str(q)+str(m) + ' = Q'+str(q)+str(m)+' + DQ'+str(q)+str(m)+'\n')
#=======================================================================
filesub.write('C---------------------------------------\n')
filesub.write('C For the beam formulation:\n')
filesub.write('C STRESS(1) = S11,  E11\n')
filesub.write('C STRESS(2) = S12,  Y12\n')
filesub.write('C B31 - TIMOSHENKO (*TRANSVERSE SHEAR STIFFNESS must be included)\n')
filesub.write('C B33 - EULER\n')
filesub.write('C---------------------------------------\n')
#=======================================================================
filesub.write('\tSTRESS(1) = STRESS(1) + \n'.expandtabs(7))
for q in range(1,qmax+1):
    filesub.write('\t&'.expandtabs(5)+' G'+str(q)+'0'+'*DQ'+str(q)+'0'+'+\n')
    for m in range(1,mmax+1):
        if q == qmax and m == mmax:
            filesub.write('\t&'.expandtabs(5)+' G'+str(q)+str(m)+'*DQ'+str(q)+str(m)+'\n')
        else:
            filesub.write('\t&'.expandtabs(5)+' G'+str(q)+str(m)+'*DQ'+str(q)+str(m)+'+\n')
#=======================================================================
filesub.write('C---------------------------------------\n')
filesub.write('\tSTRESS(2)'.expandtabs(7)+' = STRESS(2) + '+str(ddsde)+'*DSTRAN(2)\n')
filesub.write('C---------------------------------------\n')
#=======================================================================
counter = 0 #reset counter
for q in range(1,qmax+1):
    counter = counter + 1
    filesub.write('\tSTATEV('.expandtabs(7)+str(counter)+') = Q'+str(q)+'0'+'\n')
    for m in range(1,mmax+1):
        counter = counter + 1
        filesub.write('\tSTATEV('.expandtabs(7)+str(counter)+') = Q'+str(q)+str(m)+'\n')
#=======================================================================
filesub.write('C---------------------------------------\n')
filesub.write('C   CREATE NEW JACOBIAN\n')
filesub.write('C---------------------------------------\n')
#=======================================================================
counter = 0
filesub.write('\tDDSDDE(1,1) = \n'.expandtabs(7))
for q in range(1,qmax+1):
    if q == 1:
        filesub.write('\t&'.expandtabs(5)+' G10 + \n')
    else:
        filesub.write('\t&'.expandtabs(5)+' G'+str(q)+'0*'+str(q)+'*(STRAN(1)+DSTRAN(1))**'+str(q-1) + ' +\n')
    counter = counter + 1        
    for m in range(1,mmax+1):
        #Remove the components STRAIN(1)**0
        if q == 1:
            filesub.write('\t&'.expandtabs(5)+' G'+str(q)+str(m)+'*B'+str(m)+'/DTIME + \n')
        else:
            #Remove '+' from the last component
            if q == qmax and m == mmax: 
                filesub.write('\t&'.expandtabs(5)+' G'+str(q)+str(m)+'*B'+str(m)+'*'+str(q)+'*((STRAN(1)+DSTRAN(1))**'+str(q-1)+')/DTIME \n')
            else:
                filesub.write('\t&'.expandtabs(5)+' G'+str(q)+str(m)+'*B'+str(m)+'*'+str(q)+'*((STRAN(1)+DSTRAN(1))**'+str(q-1)+')/DTIME +\n')
#=======================================================================
filesub.write('C---------------------------------------\n')
filesub.write('\tDDSDDE(2,2)'.expandtabs(7)+' = '+str(ddsde)+'\n')
filesub.write('C---------------------------------------\n')
filesub.write('\tRETURN\n'.expandtabs(7))
filesub.write('\tEND\n'.expandtabs(7))
#=======================================================================
print('UMAT NLV SUBROUTINE CREATED WITH qmax='+str(qmax)+' and mmax='+str(mmax)+' terms')

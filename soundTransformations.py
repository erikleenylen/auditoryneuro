'''
tools for the auditory neuroscientist

erik lee nylen

'''
import numpy as np

def dBtoPa(vectin):
  '''convert vector of decibels values to Pascals'''
  return [np.exp(float(_)/float(20))*2/(10**5) for _ in vectin]	

def PatodB(vectin):	
  '''convert vector (list) of Pascals to decibels'''
  return [20.*np.log(_*(10**5)/2) for _ in vectin]
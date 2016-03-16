'''
tools for the auditory neuroscientist

erik lee nylen

'''
import numpy as np

def dBtoPa(vectin):
  '''convert vector of decibels values to Pascals'''
  return [np.exp(float(_)/float(20))*2/(10**5) for _ in vectin]	

#!/usr/bin/python
from __future__ import division
import sys
import numpy as np
from scipy.fftpack import fft, fftfreq

def pade(signal,max_len=None,w_min=0.0,w_max=0.1,w_step=0.0001):
    """ Routine to take the Fourier transform of a time signal using the method
          of Pade approximants.

        Inputs:
          time:      (list or Numpy NDArray) signal sampling times
          signal:    (list or Numpy NDArray) 

        Optional Inputs:
          sigma:     (float) signal damp factor, yields peaks with 
                       FWHM of 2/sigma 
          max_len:   (int) maximum number of points to use in Fourier transform
          w_min:     (float) lower returned frequency bound
          w_max:     (float) upper returned frequency bound
          w_step:    (float) returned frequency bin width

        Returns:
          fsignal:   (complex NDArray) transformed signal
          frequency: (NDArray) transformed signal frequencies

        From: Bruner, Adam, Daniel LaMaster, and Kenneth Lopata. "Accelerated 
          broadband spectra using transition signal decomposition and Pade 
          approximants." Journal of chemical theory and computation 12.8 
          (2016): 3741-3750. 
    """

    # center signal about zero
    signal = np.asarray(signal) - np.mean(signal)
      
    stepsize = 10.0 

    # Damp the signal with an exponential decay. 
    #damp = np.exp(-(stepsize*np.arange(len(signal)))/float(sigma))
    #signal *= damp

    M = len(signal)
    N = int(np.floor(M / 2))

    # Check signal length, and truncate if too long
    if max_len:
        if M > max_len:
            N = int(np.floor(max_len / 2))

    # G and d are (N-1) x (N-1)
    # d[k] = -signal[N+k] for k in range(1,N)
    d = -signal[N+1:2*N]

    try:
        from scipy.linalg import toeplitz, solve_toeplitz
        # Instead, form G = (c,r) as toeplitz
        #c = signal[N:2*N-1]
        #r = np.hstack((signal[1],signal[N-1:1:-1]))
        b = solve_toeplitz((signal[N:2*N-1],\
            np.hstack((signal[1],signal[N-1:1:-1]))),d,check_finite=False)
    except (ImportError,np.linalg.linalg.LinAlgError) as e:  
        # OLD CODE: sometimes more stable
        # G[k,m] = signal[N - m + k] for m,k in range(1,N)
        G = signal[N + np.arange(1,N)[:,None] - np.arange(1,N)]
        b = np.linalg.solve(G,d)

    # Now make b Nx1 where b0 = 1
    b = np.hstack((1,b))

    # b[m]*signal[k-m] for k in range(0,N), for m in range(k)
    a = np.dot(np.tril(toeplitz(signal[0:N])),b)
    p = np.poly1d(a)
    q = np.poly1d(b)

    # choose frequencies to evaluate over 
    frequency = np.arange(w_min,w_max,w_step)

    W = np.exp(-1j*frequency*stepsize)

    fsignal = p(W)/q(W)
    return frequency*27.211385, abs(fsignal)**2
 
def spec(time,dip):
    '''
        (C) Joshua Goings 2016
        
        CQ_RealTime.py: a post-processing script for computing the absorption spectrum of
         Real Time Time Dependent SCF jobs in Chronus Quantum
        Computes the energy range, w (in eV) and dipole strength function S(w) for
         a given real time TD-SCF run. 
        real_time_file   ... type:string ; the RealTime_Dipole.csv file from a ChronusQ run
        dipole_direction ... type:char   ; which dipole moment contribution is computed (e.g. 'x','y', or 'z')
        kick_strength    ... type:float  ; in a.u., what was the applied field strength (e.g. 0.0001 au)
        damp_const       ... type:float  ; in a.u. of time, gives FWHM of 2/damp_const
    '''
   
    # chronusq file is CSV, also skip the header (first row)

    # subtract the average to prevent zero peak 
    dip = dip - np.mean(dip)

    # do the fourier transform 
    fw = fft(dip)

    # determine frequency range
    n = len(fw)                         # number samples, including padding
    timestep = time[1] - time[0]              # spacing between time samples; assumes constant time step
    w = fftfreq(n,d=timestep)*2.0*np.pi # frequency list
   
    fw_re = np.real(fw)                 # the real FFT frequencies
    fw_im = (np.imag(fw))               # the imaginary FFT frequencies
    fw_abs = abs(fw)**2                    # absolute value of frequencies
    
    w = (w*27.2114)    # give frequencies in eV
    return w,fw_abs 

if __name__ == '__main__':


    Filename   = 'vels.txt'
    rt = np.genfromtxt(Filename)
    x = rt[:,0]
    w, Fx = pade(x) 
    allspec= np.zeros(len(Fx))
    for i in range(0,35):
      x = rt[:,i]
      w, Fx = pade(x) 
      allspec = allspec + Fx
    np.savetxt('spectrum_ev.txt.pade', np.transpose([w,allspec]))  


    

#!/usr/bin/python
from __future__ import division
import sys
import numpy as np
from scipy.fftpack import fft, fftfreq

def pade(time,signal,sigma=5000.0,max_len=None,w_min=0.0,w_max=0.1,w_step=0.001):
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
      
    stepsize = time[1] - time[0]

    # Damp the signal with an exponential decay. 
    damp = np.exp(-(stepsize*np.arange(len(signal)))/float(sigma))
    signal *= damp

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
 

if __name__ == '__main__':

    outfile = sys.argv[1]
    Filename   = 'timedip'
    rt = np.genfromtxt(Filename)
    t      = 10*rt[:,0]
    x      = rt[:,1]
    y      = rt[:,2]
    z      = rt[:,3]
    w, Fx      = pade(t,x) 
    w, Fy      = pade(t,y)
    w, Fz      = pade(t,z)

    np.savetxt(outfile, np.transpose([w,Fx+Fx+Fz]))  
#    np.savetxt('spectrum_ev.txt', np.transpose([w,Fx]))  

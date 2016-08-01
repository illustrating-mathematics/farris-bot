#!/usr/bin/env python3

import argparse

parse = argparse.ArgumentParser()
parse.add_argument('--complex', action='store_true')
parse.add_argument('--symm', type=int, default=5)
parse.add_argument('--steps', type=int, default=10)
parse.add_argument('--fpp', type=int, default=48)
parse.add_argument('--seed', type=int, default=42)
parse.add_argument('--decay', type=float, default=1.1)
parse.add_argument('--dir', default='')
parse.add_argument('--extension', default='png')
opts = parse.parse_args()

from matplotlib import use
use('Agg')

from numpy import array, random, linspace, exp
from matplotlib.pylab import *
import os.path

symm = opts.symm
steps = opts.steps
fpp = opts.fpp
if opts.complex:
    do_complex = 1
else:
    do_complex = 0

seed(opts.seed)

def decay(s):
    return 1/(abs(s*symm+1)+0.5)**opts.decay

coeff0 = {j*symm+1: complex(np.random.normal()*decay(j),
                         do_complex*np.random.normal()*decay(j))
          for j in range(-steps,steps)}
coeff1 = {j*symm+1: complex(np.random.normal()*decay(j),
                         do_complex*np.random.normal()*decay(j))
          for j in range(-steps,steps)}
if do_complex == 1:
    coeff2 = {k: coeff1[k].conjugate() for k in coeff1}
else:
    coeff2 = {j*symm+1: complex(np.random.normal()*decay(j),
                         do_complex*np.random.normal()*decay(j))
          for j in range(-steps,steps)}

theta = linspace(0,2*pi,500)
maxzs = max([sqrt(norm(array([coeff0[j]*exp(complex(0,1)*j*theta) for j in coeff]).sum(axis=0)))
             for coeff in [coeff0, coeff1, coeff2]])
frame = ceil(4*maxzs)/5
axshape = [-frame, frame, -frame, frame]

figure(figsize=(6,6))
for i,t in enumerate(linspace(0,1,fpp)):
    zs = array([((1-t)*coeff0[j]+t*coeff1[j])*exp(complex(0,1)*j*theta) for j in coeff0]).sum(axis=0)
    cla()
    plot(zs.real, zs.imag, 'b', lw=2)
    axis('square')
    axis('off')
    axis(axshape)
    savefig(os.path.join(opts.dir, "frame{:03}.{}".format(i, opts.extension)), bbox_inches='tight')
    
for i,t in enumerate(linspace(0,1,fpp)):
    zs = array([((1-t)*coeff1[j]+t*coeff2[j])*exp(complex(0,1)*j*theta) for j in coeff0]).sum(axis=0)
    cla()
    plot(zs.real, zs.imag, 'b', lw=2)
    axis('square')
    axis('off')
    axis(axshape)
    savefig(os.path.join(opts.dir, "frame{:03}.{}".format(fpp+i, opts.extension)), bbox_inches='tight')

for i,t in enumerate(linspace(0,1,fpp)):
    zs = array([((1-t)*coeff2[j]+t*coeff0[j])*exp(complex(0,1)*j*theta) for j in coeff0]).sum(axis=0)
    cla()
    plot(zs.real, zs.imag, 'b', lw=2)
    axis('square')
    axis('off')
    axis(axshape)
    savefig(os.path.join(opts.dir, "frame{:03}.{}".format(2*fpp+i, opts.extension)), bbox_inches='tight')

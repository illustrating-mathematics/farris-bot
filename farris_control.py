import argparse

parse = argparse.ArgumentParser()
opts = parse.parse_args()

import tweepy
import creds
import os, os.path
import tempfile
import subprocess
import random

auth = tweepy.OAuthHandler(creds.consumerkey, creds.consumersecret)
auth.set_access_token(creds.verifiertoken, creds.verifiersecret)
api = tweepy.API(auth)

seed = random.randint(0,2**20)
use_complex = random.choice([True, False])
symmetry = random.choice([3,3,3,4,5,5,5,5,5,5,5,7,7,9])

# no swastikas
if symmetry == 4:
    use_complex = False

command = "python farris_5fold.py --fpp 48 --seed {seed} --dir output --symm {symm}".format(
    seed=seed, symm=symmetry)
if use_complex:
    command += " --complex"
subprocess.run(command.split())
subprocess.run("convert -delay 4 {path} out.gif".format(
    path=os.path.join('output', "frame*.png")).split())
subprocess.run(("cp out.gif /home/michiexile/webapps/blog_illustrating/symmetric_curves/{symm}-{seed}{cpx}.gif".format(symm=symmetry, seed=seed, cpx={True: '-complex', False: ''}[use_complex])).split())
subprocess.run("python gallery.py".split())
statustext = '{symmetry}-fold symmetry, seed: {seed}'.format(symmetry=symmetry, seed=seed)
if use_complex:
    statustext += ', complex Fourier coefficients'
api.update_with_media('out.gif', status=statustext)

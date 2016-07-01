import argparse

parse = argparse.ArgumentParser()
opts = parse.parse_args()

import tweepy
import creds
import os, os.path
import tempfile
import subprocess

auth = tweepy.tweepy.OAuthHandler(creds.consumerkey, creds.consumersecret)
auth.set_access_token(verifiertoken, verifiersecret)

seed = random.randint(0,2**20)
use_complex = random.choice([True, False])
symmetry = random.choice([3,3,3,4,5,5,5,5,5,5,5,7,7,9])

with tempfile.TemporaryDirectory() as td:
    command = "python3 farris_5fold.py --fpp 48 --seed {seed} --dir {dir} --symm {symm}".format(
        seed=seed, dir=td, symm=symmetry))
    if use_complex:
        command += " --complex"
    subprocess.run(command)
    subprocess.run("convert -delay 4 {path} out.gif".format(path=os.path.join(td, "frame*.png")))
    statustext = '{symmetry}-fold symmetry, seed: {seed}'
    if use_complex:
        statustext += ', complex Fourier coefficients'
    api.update_with_media('out.gif', status=statustext)

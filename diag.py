import os

def env():
    return repr(os.environ.get("CUDA_VISIBLE_DEVICES"))

print("1. CUDA_VISIBLE_DEVICES at start:      ", env())

import torch
print("2. torch version:", torch.__version__, "| built for CUDA:", torch.version.cuda)

import laya
print("3. after importing laya:                ", env())

import decider.infer
print("4. after importing decider:             ", env())

print("5. cuda available:", torch.cuda.is_available(), "| device count:", torch.cuda.device_count())
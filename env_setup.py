"""Import this FIRST in every script, before torch, laya or decider."""
import os

os.environ.pop("CUDA_VISIBLE_DEVICES", None)      # undo the system-wide -1 that hides the GPU
os.environ["USE_TF"] = "0"                        # avoid TensorFlow hang in transformers
os.environ["TORCHDYNAMO_DISABLE"] = "1"           # no torch.compile (fast for short tickets)
os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"

import torch

if not torch.cuda.is_available():
    raise SystemExit("CUDA not available. Run nvidia-smi and check the driver before continuing.")

print(f"[env] GPU: {torch.cuda.get_device_name(0)}")
"""Run scripts/evaluate.py in-process and report wall time and peak GPU memory (G0.3)."""
import json, runpy, sys, time
import torch

t0 = time.time()
sys.argv = ["scripts/evaluate.py"] + sys.argv[1:]
try:
    runpy.run_path("scripts/evaluate.py", run_name="__main__")
except SystemExit:
    pass
dev = torch.cuda.current_device()
print("G0_WRAP " + json.dumps({"wall_s": round(time.time() - t0, 1),
      "peak_alloc_gb": round(torch.cuda.max_memory_allocated(dev) / 2**30, 2),
      "peak_reserved_gb": round(torch.cuda.max_memory_reserved(dev) / 2**30, 2),
      "gpu": torch.cuda.get_device_name(dev)}))

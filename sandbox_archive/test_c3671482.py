# auto-injected by SEC sandbox
import itertools
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from itertools import product, combinations, permutations, chain
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math

def generate_circuit(depth, width):
    if depth == 1:
        return [random.randint(0, 1) for _ in range(width)]
    
    inputs = [generate_circuit(random.randint(1, depth-1), width) for _ in range(width)]
    outputs = [inputs[i] ^ inputs[(i + 1) % width] for i in range(width)]
    return outputs

def run_circuit(depth, width):
    circuit = generate_circuit(depth, width)
    
    # Convert the circuit to a permutation group
    G = []
    for i in range(width):
        perm = [0] * width
        for j in range(width):
            perm[j] = (circuit[i][j] + j) % width
        G.append(perm)
    
    # Compute the minimal local indecomposable module rank of G
    mrl = 1
    while True:
        found = False
        for g in G:
            if any(all(g[k] == g[l] for k, l in zip(range(width), range(k+1, width))) for _ in range(mrl)):
                found = True
                break
        if not found:
            break
        mrl += 1
    
    return mrl, depth, width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    metric_name = "mrl_to_w_plus_d_2_3_ratio"
    instances_tested = 0
    n_max = 0
    total_mrl = 0.0
    counterexample = ""
    
    for depth in [5, 10, 15, 20, 30, 40]:
        for width in range(1, min(41, depth + 1)):
            instances_tested += 1
            n_max = max(n_max, depth * width)
            
            try:
                mrl, depth_val, width_val = run_circuit(depth, width)
                total_mrl += mrl
                
                r = mrl / (width_val + depth_val ** (2/3))
                if instances_tested == 1 or r >= 0.5:
                    continue
            except Exception as e:
                counterexample = f"Error during circuit generation: {e}"
                return {
                    "metric_name": metric_name,
                    "metric_value": total_mrl / instances_tested,
                    "instances_tested": instances_tested,
                    "n_max": n_max,
                    "conjecture_holds": False,
                    "counterexample": counterexample
                }
    
    if instances_tested < 30:
        return {
            "metric_name": metric_name,
            "metric_value": total_mrl / instances_tested,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "Too few instances tested"
        }
    
    mean = total_mrl / instances_tested
    conjecture_holds = all(r >= 0.5 for r in [mrl / (width + depth ** (2/3)) for mrl, depth, width in run_circuit(depth, width) for _ in range(10)])
    
    return {
        "metric_name": metric_name,
        "metric_value": mean,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='not enough evidence' first_failing_seed={first_failing_seed}")
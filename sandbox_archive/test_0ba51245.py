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
    else:
        inputs = [generate_circuit(random.randint(1, depth-1), width) for _ in range(width)]
        outputs = [inputs[i] ^ inputs[(i + 1) % width] for i in range(width)]
        return outputs

def run_circuit(depth, width):
    circuit = generate_circuit(depth, width)
    permutation_group = set()
    for i in range(len(circuit)):
        for j in range(i+1, len(circuit)):
            if circuit[i] == circuit[j]:
                permutation_group.add((i, j))
    mrl = len(permutation_group)
    return mrl, depth, width

def run_trial(seed: int) -> dict:
    random.seed(seed)
    results = []
    n_max = 0
    for _ in range(30):
        depth = random.randint(5, 40)
        width = random.randint(1, min(depth, 20))
        n_max = max(n_max, width + depth)
        mrl, depth_val, width_val = run_circuit(depth, width)
        results.append(mrl / (width_val + depth_val ** (2/3)))
    mean_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 0.5) / len(results)
    conjecture_holds = support_fraction >= 0.8
    counterexample = "" if conjecture_holds else "mapping_undefined"
    return {
        "metric_name": "mrl_ratio",
        "metric_value": mean_value,
        "instances_tested": len(results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = list(map(int, sys.argv[1:])) or [2**i + 3 for i in range(5, 8)]
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    mean_value = sum(results) / len(results)
    support_fraction = sum(1 for r in results if r >= 0.5) / len(results)
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=NA support_fraction={support_fraction}")
    elif any(r < 0.5 for r in results):
        first_failing_seed = seeds[results.index(min(results))]
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
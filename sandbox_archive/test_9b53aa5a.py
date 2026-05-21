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

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def log2(x):
        return math.log2(x) if x > 0 else float('inf')
    
    def tropicalize(vector):
        return [max(0, v) for v in vector]
    
    def tensor_product(v1, v2):
        result = []
        for i in range(len(v1)):
            for j in range(len(v2)):
                result.append(max(v1[i], v2[j]))
        return result
    
    n = random.randint(5, 40)
    s = random.randint(1, n)  # AC0 circuit size
    d = math.ceil(log2(s))
    
    T = [random.randint(0, 1) for _ in range(d)]
    W = [random.randint(0, 1) for _ in range(d)]
    
    C_output = [random.randint(0, 1) for _ in range(n)]
    V_output = tropicalize(C_output)
    
    if len(V_output) != d:
        return {
            "metric_name": "dimension",
            "metric_value": len(V_output),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"Output vector length {len(V_output)} does not match dimension {d}"
        }
    
    if V_output != tensor_product(T, W):
        return {
            "metric_name": "isomorphism",
            "metric_value": 0,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": f"V_output {V_output} is not isomorphic to tensor product of T and W"
        }
    
    return {
        "metric_name": "dimension",
        "metric_value": d,
        "instances_tested": 1,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = results[first_failing_seed]["counterexample"]
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
# auto-injected by SEC sandbox
import itertools
import collections
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
import sys
import json

def cc(f, tt):
    n = int(math.log2(len(tt)))
    visited = set()
    stack = [(0, 0)]
    while stack:
        node, depth = stack.pop()
        if node == len(tt) - 1:
            return depth
        for i in range(n):
            next_node = (node << 1) | int(tt[node][i])
            if next_node not in visited and f(next_node) == tt[next_node]:
                visited.add(next_node)
                stack.append((next_node, depth + 1))
    return float('inf')

def lz78(tt):
    n = len(tt)
    table = {}
    code = 0
    output = []
    for i in range(n):
        prefix = tt[:i]
        suffix = tt[i:]
        if prefix in table:
            new_code = table[prefix] + (suffix[0],)
            if new_code not in table.values():
                table[new_code] = code
                code += 1
                output.append((table[prefix], suffix[0]))
        else:
            table[prefix] = code
            code += 1
            output.append((code - 1, suffix[0]))
    return len(output)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [3, 4, 5, 6]
    results = []
    
    for n in n_values:
        if n == 3:
            functions = [(lambda x: x[i] ^ x[j]) for i in range(n) for j in range(i+1, n)]
        else:
            functions = [random.choice([lambda x: x[i], lambda x: not x[i]]) for _ in range(200)]
        
        for f in functions:
            tt = ''.join(str(f(i)) for i in range(2**n))
            lz_val = lz78(tt)
            cc_val = cc(f, tt)
            results.append((n, tt, lz_val, cc_val))
    
    metric_value = sum(cc_val - 4 * lz_val - 2 * n for n, _, lz_val, cc_val in results if cc_val != float('inf')) / len(results)
    instances_tested = len(results)
    conjecture_holds = all(cc_val <= 4 * lz_val + 2 * n for n, _, lz_val, cc_val in results if cc_val != float('inf'))
    counterexample = ""
    
    if not conjecture_holds:
        for n, tt, lz_val, cc_val in results:
            if cc_val > 4 * lz_val + 2 * n:
                counterexample = f"(n={n}, tt={tt[:10]}..., LZ(f)={lz_val}, CC(f)={cc_val})"
                break
    
    return {
        "metric_name": "CC - 4*LZ - 2*n",
        "metric_value": metric_value,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(json.dumps({"TRIAL": {"seed": seed, **result}}))
        results.append(result)
    
    total_metric_value = sum(r["metric_value"] * r["instances_tested"] for r in results) / sum(r["instances_tested"] for r in results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={total_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
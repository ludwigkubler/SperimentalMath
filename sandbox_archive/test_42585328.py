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
    
    def lz78(s):
        if not s:
            return 1
        codebook = {s[:i]: i for i in range(1, len(s))}
        codebook[s] = len(codebook)
        length = 1
        current = s[0]
        result = []
        while length < len(s):
            next_char = s[length]
            if current + next_char in codebook:
                current += next_char
                length += 1
            else:
                result.append(codebook[current])
                codebook[current + next_char] = len(codebook)
                current = next_char
                length += 1
        result.append(codebook[current])
        return sum(math.ceil(math.log2(x + 1)) for x in result)
    
    def cc(f, s):
        if not f:
            return 0
        n = len(f)
        gates = {'AND', 'OR', 'NOT'}
        queue = [(f, [])]
        visited = set()
        while queue:
            current, path = queue.pop(0)
            if current in visited:
                continue
            visited.add(current)
            if current == s:
                return len(path) + 1
            for g in gates:
                for i in range(len(current)):
                    new_state = current[:i] + g + current[i+1:]
                    queue.append((new_state, path + [g]))
        return float('inf')
    
    def truth_table(n):
        if n == 3:
            return [[0, 0, 0], [0, 0, 1], [0, 1, 0], [0, 1, 1],
                    [1, 0, 0], [1, 0, 1], [1, 1, 0], [1, 1, 1]]
        elif n == 4:
            return [[i >> j & 1 for j in range(n)] for i in range(2**n)]
        else:
            raise ValueError("Unsupported n")
    
    def random_truth_table(n):
        return [[random.choice([0, 1]) for _ in range(2**n)]]
    
    results = []
    for n in [3, 4, 5]:
        tt = truth_table(n) + random_truth_table(n)
        for f in tt:
            lz = lz78(''.join(str(x) for x in f))
            cc_val = cc(f, '0' * (2**n))
            results.append((n, f, lz, cc_val))
    
    violations = [r for r in results if r[3] > 4 * r[2] + 2 * r[0]]
    rho_n = []
    for n in [3, 4, 5]:
        n_results = [r for r in results if r[0] == n]
        lz_vals = [r[2] for r in n_results]
        cc_vals = [r[3] for r in n_results]
        rho_n.append(spearman_rho(lz_vals, cc_vals))
    
    support_fraction = sum(1 for r in results if not any(v > 4 * r[2] + 2 * r[0] for v in violations)) / len(results)
    return {
        "metric_name": "Spearman rho",
        "metric_value": sum(rho_n) / len(rho_n),
        "instances_tested": len(results),
        "conjecture_holds": support_fraction == 1 and all(r >= 0.6 for r in rho_n),
        "counterexample": "" if not violations else f"({violations[0][0]}, {','.join(map(str, violations[0][1]))}, {violations[0][2]}, {violations[0][3]})"
    }

def spearman_rho(x, y):
    n = len(x)
    rank_x = [sorted(x).index(xi) for xi in x]
    rank_y = [sorted(y).index(yi) for yi in y]
    d_squared = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
    return 1 - (6 * d_squared) / (n * (n**2 - 1))

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing = next(i for i, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[first_failing]['counterexample']}\" first_failing_seed={seeds[first_failing]}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
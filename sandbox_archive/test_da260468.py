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
    
    def additive_energy(A):
        n = len(A)
        E = 0
        for a in range(n):
            for b in range(a, n):
                for c in range(b, n):
                    for d in range(c, n):
                        if (A[a] + A[b]) % n == (A[c] + A[d]) % n:
                            E += 1
        return E
    
    def discrepancy(A):
        n = len(A)
        D = float('inf')
        for i in range(n):
            for j in range(i+1, n):
                for k in range(j+1, n):
                    for l in range(k+1, n):
                        count_ones = 0
                        for x in range(n):
                            for y in range(n):
                                if (A[x] + A[y]) % n == (A[i] + A[j]) % n and (x, y) not in [(i, j), (j, i)]:
                                    count_ones += 1
                        D = min(D, abs(count_ones - (n*n - count_ones)))
        return D
    
    n = random.randint(5, 40)
    A = set(random.sample(range(n), random.randint(1, n//2)))
    
    E = additive_energy(A)
    D = discrepancy(A)
    
    if E == 0:
        return {
            "metric_name": "Discrepancy/E",
            "metric_value": float('inf'),
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "Additive energy is zero, discrepancy undefined."
        }
    
    ratio = D / E
    C = ratio * n**2
    
    return {
        "metric_name": "Discrepancy/E",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - C) < 0.2,
        "counterexample": "" if abs(ratio - C) < 0.2 else f"Ratio {ratio} deviates by more than 20% from {C}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, \"metric_name\": \"{result['metric_name']}\", \"metric_value\": {result['metric_value']}, \"instances_tested\": {result['instances_tested']}, \"conjecture_holds\": {result['conjecture_holds']}, \"counterexample\": \"{result['counterexample']}\"}}")
        results.append(result)
    
    mean_ratio = sum(r['metric_value'] for r in results) / len(results)
    std_ratio = math.sqrt(sum((r['metric_value'] - mean_ratio)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r['conjecture_holds']) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any(r['counterexample'] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if r['conjecture_holds'])
        print(f"RESULT: FALSIFIED counterexample=\"{next(r['counterexample'] for r in results if r['counterexample'])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient evidence")
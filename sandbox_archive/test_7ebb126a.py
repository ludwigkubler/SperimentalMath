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
    
    def generate_boolean_algebra(n):
        return {f'x{i}': i for i in range(n)}
    
    def crossed_product(B):
        n = len(B)
        result = {}
        for x in B:
            for y in B:
                result[f'{x}{y}'] = (B[x] + B[y]) % 2
        return result
    
    def minimal_rank_invariant(cp):
        rank = 0
        for key, value in cp.items():
            if value == 1:
                rank += 1
        return rank
    
    def ac0_parity_circuit(n):
        size = 2 ** math.ceil(math.log2(n))
        return size
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        B = generate_boolean_algebra(n)
        cp = crossed_product(B)
        psi_B = minimal_rank_invariant(cp)
        size_C = ac0_parity_circuit(n)
        
        if psi_B < math.log(size_C):
            return {
                "metric_name": "minimal_rank_invariant",
                "metric_value": psi_B,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"psi(B)={psi_B} < log(size(C))={math.log(size_C)}"
            }
    
    return {
        "metric_name": "minimal_rank_invariant",
        "metric_value": sum(results) / len(results),
        "instances_tested": len(n_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 103))  # First 30 primes
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result["metric_value"])
    
    mean = sum(results) / len(results)
    std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
    support_fraction = sum(1 for r in results if r >= mean + 3 * std_dev) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(r < mean + 3 * std_dev for r in results):
        first_failing_seed = seeds[results.index(next(r for r in results if r < mean + 3 * std_dev))]
        print(f"RESULT: FALSIFIED counterexample='psi(B) < log(size(C))' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")
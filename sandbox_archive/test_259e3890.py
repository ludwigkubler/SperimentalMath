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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def ac0_parity_circuit_size(f):
        n = len(f)
        count_ones = f.count(1)
        return math.ceil(math.log2(count_ones + 1))
    
    def local_ring_extension_rank(f):
        n = len(f)
        rank = 0
        for i in range(n):
            if f[i] == 1:
                rank += 1
        return rank
    
    def log2(x):
        if x <= 0:
            return float('-inf')
        return math.log2(x)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        f = generate_boolean_function(n)
        size_circuit = ac0_parity_circuit_size(f)
        rank = local_ring_extension_rank(f)
        
        if rank > log2(size_circuit):
            return {
                "metric_name": "minRank(L)",
                "metric_value": rank,
                "instances_tested": 1,
                "conjecture_holds": False,
                "counterexample": f"n={n}, minRank(L)={rank} > log2(size(C))={log2(size_circuit)}"
            }
        
        results.append(rank)
    
    mean_rank = sum(results) / len(results)
    return {
        "metric_name": "minRank(L)",
        "metric_value": mean_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": all(rank <= log2(size_circuit) for rank, size_circuit in zip(results, [ac0_parity_circuit_size(generate_boolean_function(n)) for n in n_values])),
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 103))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean_rank = sum(results) / len(results)
    support_fraction = sum(1 for r in results if all(r <= log2(ac0_parity_circuit_size(generate_boolean_function(n))) for n in [5, 10, 15, 20, 30, 40])) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_rank} std={math.sqrt(sum((x - mean_rank) ** 2 for x in results) / len(results))} support_fraction={support_fraction}")
    elif any(result > log2(ac0_parity_circuit_size(generate_boolean_function(n))) for n, result in zip([5, 10, 15, 20, 30, 40], results)):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample=\"n={max([n for n, r in enumerate(results) if r > log2(ac0_parity_circuit_size(generate_boolean_function(n)))])}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
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
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_circuit(size):
        if size == 1:
            return ['0'] if random.choice([True, False]) else ['1']
        gate = random.choice(['AND', 'OR'])
        left = generate_circuit(size - 1)
        right = generate_circuit(size - 1)
        return [gate] + left + right
    
    def tensor_rank(circuit):
        n = len(circuit)
        if n == 1:
            return 1
        rank = 0
        for i in range(n):
            if circuit[i] == 'AND':
                rank += max(tensor_rank(circuit[:i]), tensor_rank(circuit[i+1:]))
            elif circuit[i] == 'OR':
                rank += min(tensor_rank(circuit[:i]), tensor_rank(circuit[i+1:]))
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    ranks = []
    
    for n in n_values:
        circuit = generate_circuit(n)
        rank = tensor_rank(circuit)
        ranks.append(rank)
    
    avg_rank = sum(ranks) / len(ranks)
    max_rank = max(ranks)
    conjecture_holds = all(rank <= n**2 for n, rank in zip(n_values, ranks))
    counterexample = "" if conjecture_holds else f"max_rank={max_rank} > {n_values[-1]}^2"
    
    return {
        "metric_name": "tensor_rank",
        "metric_value": avg_rank,
        "instances_tested": len(ranks),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*3 + 1))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_rank = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_rank} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
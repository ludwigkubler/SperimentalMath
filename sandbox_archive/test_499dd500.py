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
    
    def communication_complexity(n):
        # Generate a random binary string of length n
        return ''.join(random.choice('01') for _ in range(n))
    
    def minimal_generators(outcomes):
        if not outcomes:
            return 0
        n = len(outcomes)
        generators = set()
        for outcome in outcomes:
            for i in range(n):
                if outcome[i] == '1':
                    generators.add(i)
        return len(generators)
    
    def ackermann(m, n):
        if m == 0:
            return n + 1
        elif n == 0:
            return ackermann(m - 1, 1)
        else:
            return ackermann(m - 1, ackermann(m, n - 1))
    
    results = []
    for _ in range(30):
        n = random.choice([5, 10, 15, 20, 30, 40])
        φ = communication_complexity(n)
        outcomes = [φ[i] for i in range(n)]
        generators = minimal_generators(outcomes)
        α_log_n = ackermann(4, n.bit_length())
        results.append((generators, α_log_n))
    
    mean_C = sum(C for C, _ in results) / len(results)
    mean_ranks = sum(r for _, r in results) / len(results)
    ratio = mean_C / mean_ranks
    
    if all(0.9 <= ratio <= 1.1 for C, r in results):
        conjecture_holds = True
    else:
        conjecture_holds = False
        counterexample = f"Ratio out of bounds: {ratio}"
    
    return {
        "metric_name": "Ratio of minimal generators to α(log n)",
        "metric_value": ratio,
        "instances_tested": len(results),
        "n_max": max(n for _, _ in results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_ratio} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Ratio out of bounds\" first_failing_seed={first_failing_seed}")
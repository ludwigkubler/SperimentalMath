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
    N = 10 if seed % 2 == 0 else 15 if seed % 3 == 0 else 20
    c = 1 + (seed // 60) % 2
    v = 2 * N
    k = math.ceil(math.log2(v))
    
    rng = random.Random(seed)
    F = set(rng.sample(range(1, v+1), int(N**c)))
    
    G_F = {}
    for T in F:
        for T_prime in F:
            if T != T_prime and len(T & T_prime) > 0:
                G_F.setdefault(T, []).append(T_prime)
                G_F.setdefault(T_prime, []).append(T)
    
    def degree(node):
        return len(G_F.get(node, []))
    
    μ = max(max(0, degree(T) + degree(T_prime) - 4) for T in F for T_prime in G_F[T] if T != T_prime)
    
    sunflowers = {}
    for T in F:
        for T_prime in G_F[T]:
            core = T & T_prime
            if core not in sunflowers:
                sunflowers[core] = []
            sunflowers[core].append((T, T_prime))
    
    κ = max(len([T for T, T_prime in pairs if len(T & T_prime) == len(core)]) for core, pairs in sunflowers.items())
    
    s = 6 * c * math.log2(1 + κ) + 4 - μ
    conjecture_holds = s >= 0
    
    return {
        "metric_name": "slack",
        "metric_value": s,
        "instances_tested": len(F),
        "n_max": N,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"μ={μ}, 6c·log₂(1+κ) + 4 = {6 * c * math.log2(1 + κ) + 4}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(3, 8)]  # Default to first 30 primes
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")
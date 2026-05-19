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
    
    def is_unsat(F):
        # Implement DPLL algorithm here to check unsatisfiability
        pass
    
    def walsh_hadamard_transform(p_F, n):
        p_hat = [0] * (1 << n)
        for x in range(1 << n):
            for C in F:
                polarity = 1 if all(x & (1 << i) == (C[i] + 1) % 2 for i in C) else -1
                p_hat[x] += polarity / math.sqrt(len(F))
        return p_hat
    
    def spectral_entropy(p_hat, n):
        norm_squared = sum(abs(x)**2 for x in p_hat)
        q_F = [x**2 / norm_squared if x != 0 else 0 for x in p_hat]
        H_F = -sum(q * math.log2(q) for q in q_F if q > 0)
        return H_F
    
    def tree_resolution_complexity(F):
        # Implement tree-DPLL algorithm here to compute t*(F)
        pass
    
    n_values = [10, 12, 14, 16, 18, 20]
    results = []
    
    for n in n_values:
        m = int(4.3 * n + random.uniform(-0.5, 0.5))  # Adjusted density
        F = []  # Generate unsat 3-CNF here
        if not is_unsat(F):
            continue
        
        p_F = [sum(1 for C in F if all(x & (1 << i) == (C[i] + 1) % 2 for i in C)) / math.sqrt(len(F)) for x in range(1 << n)]
        p_hat = walsh_hadamard_transform(p_F, n)
        H_F = spectral_entropy(p_hat, n)
        t_star = tree_resolution_complexity(F)
        
        R = math.log2(t_star) * math.log2(1 + n + n**2 + n**3) / (n * H_F)
        results.append(R)
    
    if len(results) < 6:
        return {
            "metric_name": "R",
            "metric_value": None,
            "instances_tested": len(results),
            "conjecture_holds": False,
            "counterexample": "not_enough_data"
        }
    
    mean_R = sum(results) / len(results)
    std_R = math.sqrt(sum((x - mean_R)**2 for x in results) / len(results))
    support_fraction = sum(1 for R in results if R >= 0.05) / len(results)
    
    return {
        "metric_name": "R",
        "metric_value": mean_R,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else str(min(R for R in results if R < 0.01))
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 30))  # Default to first 29 primes
    
    for seed in seeds:
        trial = run_trial(seed)
        print(f"TRIAL: {trial}")
    
    # Compute mean/std of metric_value, fraction of seeds where conjecture_holds
    results = [run_trial(seed) for seed in seeds]
    all_results = [r["metric_value"] for r in results if r["metric_value"] is not None]
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={sum(all_results)/len(all_results):.4f} std={math.sqrt(sum((x - sum(all_results)/len(all_results))**2 for x in all_results) / len(all_results)):.4f} support_fraction={support_fraction:.4f}")
    else:
        first_failing_seed = next(seed for seed, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{r['counterexample']}\" first_failing_seed={first_failing_seed}")
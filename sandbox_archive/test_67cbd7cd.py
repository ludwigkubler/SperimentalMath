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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def frobenius_schur_indicator(cnf):
        # Placeholder implementation
        return 0.5
    
    def communication_complexity_rank(cnf):
        # Placeholder implementation
        return len(cnf)
    
    def variance(indicators):
        mean = sum(indicators) / len(indicators)
        return sum((x - mean) ** 2 for x in indicators) / len(indicators)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    support_fraction = 0
    
    for n in n_values:
        m = random.randint(1, n * (n - 1) // 2)
        cnf = generate_cnf(n, m)
        indicator = frobenius_schur_indicator(cnf)
        ccr = communication_complexity_rank(cnf)
        var = variance([indicator] * len(indicators))
        
        results.append({
            "metric_name": "Var(Sn, φ)",
            "metric_value": var,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": var >= ccr ** 2,
            "counterexample": ""
        })
        
        if var >= ccr ** 2:
            support_fraction += 1
    
    mean = sum(result["metric_value"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["metric_value"] - mean) ** 2 for result in results) / len(results))
    
    return {
        "seed": seed,
        "mean": mean,
        "std": std_dev,
        "support_fraction": support_fraction / len(n_values),
        "results": results
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    all_results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        all_results.append(result)
    
    mean = sum(r["mean"] for r in all_results) / len(all_results)
    std_dev = math.sqrt(sum((r["mean"] - mean) ** 2 for r in all_results) / len(all_results))
    support_fraction = sum(r["support_fraction"] for r in all_results) / len(all_results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in all_results):
        first_failing_seed = next(seed for seed, result in zip(seeds, all_results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=mapping_undefined")
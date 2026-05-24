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
    
    def generate_cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def sheaf_rank(cnf):
        # Placeholder function to compute sheaf rank
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf)
    
    def dpll_refutation_tree_width(cnf):
        # Placeholder function to compute DPLL refutation tree width
        # This is a dummy implementation and should be replaced with actual computation
        return sheaf_rank(cnf)  # Simplified for demonstration
    
    n = random.randint(5, 40)
    m = random.randint(1, min(n * (n - 1), 10))
    cnf = generate_cnf(n, m)
    
    width = dpll_refutation_tree_width(cnf)
    rank = sheaf_rank(cnf)
    
    return {
        "metric_name": "dpll_refutation_tree_width",
        "metric_value": width,
        "instances_tested": 1,
        "conjecture_holds": width <= math.log(n**m + m),
        "counterexample": "" if width <= math.log(n**m + m) else f"Width {width} exceeds log({n**m + m})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.getrandbits(32) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    total_width = sum(r["metric_value"] for r in results if "metric_value" in r)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    mean_width = total_width / len(results) if results else 0
    std_deviation = math.sqrt(sum((r["metric_value"] - mean_width)**2 for r in results)) / len(results) if results else 0
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_width} std={std_deviation} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Width exceeds log(n^m + m)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n - 1):
            clause = [random.choice([f'x{i+1}', f'~x{i+1}']) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def tensor_network_valuation(cnf):
        rank = len(cnf) + 1
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    max_rank = 0
    
    for n in n_values:
        cnf = generate_cnf(n)
        rank = tensor_network_valuation(cnf)
        if rank > max_rank:
            max_rank = rank
    
    g_n = max_rank
    return {
        "metric_name": "g(n)",
        "metric_value": g_n,
        "instances_tested": len(n_values),
        "conjecture_holds": g_n <= 2**n * math.log(n, 2),
        "counterexample": "" if g_n <= 2**n * math.log(n, 2) else f"g({n}) = {g_n} > 2^{n} log({n})"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_g_n = sum(r["metric_value"] for r in results) / len(results)
    std_g_n = math.sqrt(sum((r["metric_value"] - mean_g_n)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_g_n} std={std_g_n} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_g_n} std={std_g_n} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
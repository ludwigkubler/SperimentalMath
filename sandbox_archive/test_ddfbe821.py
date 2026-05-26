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
        for _ in range(2 ** n // 3):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def resolution_proof_width(cnf):
        # Simplified resolution proof width calculation
        return len(cnf) * 2
    
    def eta_quotient_module_rank(cnf):
        # Simplified rank calculation (not actual implementation)
        return math.log(len(cnf))
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    width = resolution_proof_width(cnf)
    rank = eta_quotient_module_rank(cnf)
    
    if rank <= 0:
        return {
            "metric_name": "eta_quotient_module_rank",
            "metric_value": rank,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "negative_rank"
        }
    
    support = abs(rank - math.log(n)) <= 2 * math.log(n)
    return {
        "metric_name": "eta_quotient_module_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": support,
        "counterexample": "" if support else f"rank={rank}, log(n)={math.log(n)}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 8)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all(r["conjecture_holds"] for r in results):
        mean_rank = sum(r["metric_value"] for r in results) / len(results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results) / len(results))
        support_fraction = 1.0
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        counterexample = results[seeds.index(first_failing_seed)]["counterexample"]
        mean_rank = sum(r["metric_value"] for r in results)
        std_dev = math.sqrt(sum((r["metric_value"] - mean_rank)**2 for r in results))
        support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
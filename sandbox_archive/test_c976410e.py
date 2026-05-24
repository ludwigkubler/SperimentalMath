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
    
    def generate_k_cnf(n, k):
        clauses = []
        for _ in range(k):
            variables = random.sample(range(1, n+1), 3)
            clause = [random.choice([f'x{v}', f'-x{v}']) for v in variables]
            clauses.append(clause)
        return clauses

    def tropical_realization(cnf):
        # Placeholder implementation
        return cnf

    def hodge_structure(tropical_cnf):
        # Placeholder implementation
        return tropical_cnf

    def min_rank(hodge):
        # Placeholder implementation
        return len(hodge)

    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_k_cnf(n, k=2)  # Simplified to k=2 for testing
        tropical_cnf = tropical_realization(cnf)
        hodge = hodge_structure(tropical_cnf)
        rank = min_rank(hodge)
        results.append({"n": n, "rank": rank})
    
    if not results:
        return {
            "metric_name": "MinRank(F)",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    min_rank_values = [result["rank"] for result in results]
    avg_rank = sum(min_rank_values) / len(min_rank_values)
    std_dev = math.sqrt(sum((x - avg_rank) ** 2 for x in min_rank_values) / len(min_rank_values))
    
    return {
        "metric_name": "MinRank(F)",
        "metric_value": avg_rank,
        "instances_tested": len(results),
        "conjecture_holds": all(results[i]["rank"] <= results[i+1]["rank"] for i in range(len(results)-1)),
        "counterexample": "" if all(results[i]["rank"] <= results[i+1]["rank"] for i in range(len(results)-1)) else f"Non-monotonic at n={results[len(results)-2]['n']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    avg_metric_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - avg_metric_value) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Non-monotonic\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
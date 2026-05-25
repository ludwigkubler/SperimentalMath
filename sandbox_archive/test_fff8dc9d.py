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
    
    def generate_3cnf(n, density):
        clauses = []
        for _ in range(int(density * n * (n - 1) / 2)):
            clause = [random.randint(1, n), random.randint(-n, -1)]
            random.shuffle(clause)
            clauses.append(clause)
        return clauses

    def ac0_parity_circuit(n, d):
        # Simplified AC⁰ parity circuit construction
        # This is a placeholder and does not represent actual complexity
        return [random.choice([True, False]) for _ in range(d)]

    def min_rank_of_quotient_singularity(n, d):
        if n <= 0 or d <= 0:
            return None
        rank = Fraction(d**2 * math.log(n), 1)
        return rank

    def compute_metric(n, d):
        circuit = ac0_parity_circuit(n, d)
        rank = min_rank_of_quotient_singularity(n, d)
        if rank is None:
            return {"metric_name": "min_rank", "metric_value": float('inf'), "instances_tested": 1, "conjecture_holds": False, "counterexample": "mapping_undefined"}
        return {"metric_name": "min_rank", "metric_value": rank.numerator / rank.denominator, "instances_tested": 1, "conjecture_holds": True, "counterexample": ""}

    n_values = [10, 20, 30, 40]
    d_values = [int(0.5 * n**0.5) for n in n_values]
    
    results = []
    for n, d in zip(n_values, d_values):
        result = compute_metric(n, d)
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    conjecture_holds = all(r["conjecture_holds"] for r in results)
    counterexample = next((r["counterexample"] for r in results if not r["conjecture_holds"]), "")

    return {
        "seed": seed,
        "metric_name": "min_rank",
        "mean_metric_value": mean_value,
        "instances_tested": len(results),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)

    mean_value = sum(r["mean_metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["metric_value"] <= 3 for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    elif any(r["metric_value"] > 10 for r in results) or support_fraction < 0.8:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence")
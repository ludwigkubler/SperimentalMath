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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(2 * n):
            clause = [random.randint(-n, -1), random.randint(1, n)]
            random.shuffle(clause)
            clauses.append(clause)
        return clauses

    def dpll_time_complexity(clauses):
        # Simplified DPLL complexity estimation
        return 2 ** len(clauses)

    def local_system_order(t_star):
        # Simplified order estimation
        return int(math.log2(t_star))

    n = random.choice([12, 14, 16, 18, 20])
    formula = generate_3cnf(n)
    t_star = dpll_time_complexity(formula)
    order = local_system_order(t_star)

    expected_order = math.isclose(order, t_star ** 0.5, rel_tol=0.3) or math.isclose(order, t_star ** 0.5 * 2, rel_tol=0.3)

    return {
        "metric_name": "local_system_order",
        "metric_value": order,
        "instances_tested": 1,
        "conjecture_holds": expected_order,
        "counterexample": f"n={n}, t_star={t_star}, order={order}, expected_order={expected_order}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3

    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['instances_tested']}, t_star={results[0]['t_star']}, order={results[0]['metric_value']}, expected_order={math.isclose(results[0]['metric_value'], results[0]['t_star'] ** 0.5, rel_tol=0.3) or math.isclose(results[0]['metric_value'], results[0]['t_star'] ** 0.5 * 2, rel_tol=0.3)}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
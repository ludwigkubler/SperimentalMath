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
        for _ in range(10 * n):  # Generate 10*n clauses
            clause = [random.choice([1, -1]) * (i + 1) for i in range(n)]
            if random.choice([True, False]):
                clause = [-x for x in clause]
            clauses.append(clause)
        return clauses
    
    def dpll_time(clauses):
        # Simplified DPLL algorithm to estimate proof time
        n = len(clauses[0])
        stack = []
        assignment = [None] * (n + 1)
        def backtrack():
            if not stack:
                return 1
            var, sign = stack.pop()
            for clause in clauses:
                if any(abs(x) == abs(var) and x != sign * var for x in clause):
                    continue
                new_clause = [x for x in clause if abs(x) != abs(var)]
                if not new_clause:
                    return 0
                stack.append((var, -sign))
                backtrack()
            assignment[var] = sign
            return 1
        backtrack()
        return len(stack)
    
    def local_system_order(n):
        # Simplified model to estimate local system order
        return n * math.log2(n)
    
    n_values = [12, 14, 16, 18, 20]
    results = []
    
    for n in n_values:
        clauses = generate_3cnf(n)
        t_star = dpll_time(clauses)
        order = local_system_order(n)
        
        if t_star == 0:
            continue
        
        expected_order = math.sqrt(t_star) * (1 + random.uniform(-0.1, 0.1))
        results.append({
            "n": n,
            "t_star": t_star,
            "order": order,
            "expected_order": expected_order
        })
    
    if not results:
        return {
            "metric_name": "local_system_order",
            "metric_value": None,
            "instances_tested": 0,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    mean_order = sum(result["order"] for result in results) / len(results)
    mean_expected_order = sum(result["expected_order"] for result in results) / len(results)
    std_dev = math.sqrt(sum((result["order"] - mean_order) ** 2 for result in results) / len(results))
    
    support_fraction = sum(1 for result in results if abs(result["order"] - result["expected_order"]) <= 0.3 * result["expected_order"]) / len(results)
    
    return {
        "metric_name": "local_system_order",
        "metric_value": mean_order,
        "instances_tested": len(results),
        "conjecture_holds": support_fraction >= 0.8,
        "counterexample": "" if support_fraction >= 0.8 else f"n={results[0]['n']}, t_star={results[0]['t_star']}, order={results[0]['order']}, expected_order={results[0]['expected_order']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, **result}}")
        results.append(result)
    
    mean_order = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_order) ** 2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_order} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"n={results[0]['n']}, t_star={results[0]['t_star']}, order={results[0]['order']}, expected_order={results[0]['expected_order']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")
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
    
    def generate_k_sat_instance(n, k):
        clauses = []
        for _ in range(k):
            clause = set(random.sample(range(1, n+1), 3))
            clauses.append(clause)
        return clauses
    
    def is_satisfiable(instance):
        # Simplified SAT solver using backtracking
        assignment = [None] * (n + 1)
        
        def backtrack(i):
            if i > n:
                return True
            for val in [True, False]:
                assignment[i] = val
                if all(any(assignment[var] == literal for literal in clause) for clause in instance):
                    if backtrack(i + 1):
                        return True
            assignment[i] = None
            return False
        
        return backtrack(1)
    
    def construct_circuit(instance):
        n = len(instance[0])
        circuit_size = 0
        # Simplified circuit construction (not actual hypergeometric function rank computation)
        for clause in instance:
            circuit_size += len(clause) + 2
        return circuit_size
    
    def hypergeometric_function_rank(circuit_size):
        # Placeholder for actual hypergeometric function rank computation
        return random.uniform(0, circuit_size)
    
    n_values = [5, 10, 15, 20, 30, 40]
    satisfiable_ranks = []
    unsatisfiable_ranks = []
    
    for n in n_values:
        for _ in range(5):  # Ensure at least 30 instances per seed
            instance = generate_k_sat_instance(n, k=2)
            if is_satisfiable(instance):
                circuit_size = construct_circuit(instance)
                rank = hypergeometric_function_rank(circuit_size)
                satisfiable_ranks.append((n, rank))
            else:
                circuit_size = construct_circuit(instance)
                rank = hypergeometric_function_rank(circuit_size)
                unsatisfiable_ranks.append((n, rank))
    
    if not satisfiable_ranks or not unsatisfiable_ranks:
        return {
            "metric_name": "mrf(C)",
            "metric_value": 0,
            "instances_tested": len(satisfiable_ranks) + len(unsatisfiable_ranks),
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    satisfiable_ranks = [rank for _, rank in satisfiable_ranks]
    unsatisfiable_ranks = [rank for _, rank in unsatisfiable_ranks]
    
    mean_satisfiable_rank = sum(satisfiable_ranks) / len(satisfiable_ranks)
    std_satisfiable_rank = math.sqrt(sum((x - mean_satisfiable_rank) ** 2 for x in satisfiable_ranks) / len(satisfiable_ranks))
    correlation_coefficient = (len(satisfiable_ranks) * sum(x * y for x, y in zip(satisfiable_ranks, range(1, len(satisfiable_ranks) + 1))) -
                               len(satisfiable_ranks) * mean_satisfiable_rank * (len(satisfiable_ranks) + 1)) / \
                              math.sqrt((len(satisfiable_ranks) * sum(x ** 2 for x in satisfiable_ranks) - len(satisfiable_ranks) * mean_satisfiable_rank ** 2) *
                                        (len(satisfiable_ranks) * sum((x - (len(satisfiable_ranks) + 1)) ** 2 for x in range(1, len(satisfiable_ranks) + 1)) -
                                         len(satisfiable_ranks) * ((len(satisfiable_ranks) + 1) ** 2)))
    
    all_unsatisfiable = all(rank >= 2 * n for n, rank in unsatisfiable_ranks)
    
    return {
        "metric_name": "mrf(C)",
        "metric_value": mean_satisfiable_rank,
        "instances_tested": len(satisfiable_ranks) + len(unsatisfiable_ranks),
        "n_max": max(n_values),
        "conjecture_holds": correlation_coefficient >= 0.9 and all_unsatisfiable,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...{result}...}}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
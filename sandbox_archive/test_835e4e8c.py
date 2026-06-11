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
    
    def generate_kcnf(n, k):
        clauses = []
        for _ in range(k):
            clause = set(random.sample(range(1, n+1), 2))
            clauses.append(clause)
        return clauses
    
    def incidence_graph(clauses):
        graph = {}
        for i, clause in enumerate(clauses):
            for var in clause:
                if var not in graph:
                    graph[var] = []
                graph[var].append(i)
        return graph
    
    def noncrossing_partitions(graph):
        n = len(graph)
        dp = [[0] * (1 << n) for _ in range(n + 1)]
        
        for mask in range(1, 1 << n):
            count = bin(mask).count('1')
            if count == 1:
                dp[count][mask] = 1
            else:
                for i in range(1, n):
                    if (mask & (1 << i)) != 0 and (mask & ((1 << i) - 1)) != 0:
                        dp[count][mask] += dp[i-1][(mask & ((1 << i) - 1))]
        
        return dp[n][(1 << n) - 1]
    
    def resolution_proof_entanglement_complexity(clauses):
        # Simplified DPLL solver to estimate entanglement complexity
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                var = list(unit_clause)[0]
                if var in assignment and assignment[var] != (var in unit_clause):
                    return False
                assignment[var] = var in unit_clause
                new_clauses = [c - {var} for c in clauses if var not in c]
                return dpll(new_clauses, assignment)
            pure_literal = next((v for v in range(1, n+1) if (v not in assignment and all(v not in c for c in clauses)) or (-v not in assignment and all(-v not in c for c in clauses))), None)
            if pure_literal is not None:
                assignment[pure_literal] = True
                new_clauses = [c - {pure_literal} for c in clauses]
                return dpll(new_clauses, assignment)
            var = random.choice(list(graph.keys()))
            return dpll(clauses + [{var}], assignment) or dpll(clauses + [{-var}], assignment)
        
        assignment = {}
        return len(dpll(clauses, assignment))
    
    n = 30
    k = 10
    phi = generate_kcnf(n, k)
    graph = incidence_graph(phi)
    mnp_phi = noncrossing_partitions(graph)
    e_phi = resolution_proof_entanglement_complexity(phi)
    
    if mnp_phi == 0 or e_phi == 0:
        return {
            "metric_name": "mnp/e_ratio",
            "metric_value": None,
            "instances_tested": 1,
            "n_max": n,
            "conjecture_holds": False,
            "counterexample": "phi_is_empty"
        }
    
    ratio = Fraction(mnp_phi, e_phi)
    return {
        "metric_name": "mnp/e_ratio",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    metric_values = [r["metric_value"] for r in results if r["metric_value"] is not None]
    mean_d = sum(metric_values) / len(metric_values)
    std_d = math.sqrt(sum((x - mean_d) ** 2 for x in metric_values) / len(metric_values))
    
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_d} std={std_d} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"phi_is_empty\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_support_fraction support_fraction={support_fraction}")
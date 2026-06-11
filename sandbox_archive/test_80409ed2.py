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
            clause = set()
            while len(clause) < 2 or len(clause) > n:
                literals = random.sample(range(1, n+1), random.randint(2, n))
                clause = {l if random.choice([True, False]) else -l for l in literals}
            clauses.append(tuple(sorted(clause)))
        return clauses

    def incidence_graph(clauses):
        graph = {}
        for i, clause in enumerate(clauses):
            for literal in clause:
                if literal not in graph:
                    graph[literal] = []
                graph[literal].append(i)
        return graph

    def noncrossing_partitions(graph):
        n = len(graph)
        dp = [[0] * (1 << n) for _ in range(n)]
        for i in range(n):
            dp[i][1 << i] = 1
        for s in range(1, 1 << n):
            for i in range(n):
                if s & (1 << i):
                    dp[i][s] += sum(dp[j][s ^ (1 << i)] for j in range(i) if s & (1 << j))
        return dp[0][(1 << n) - 1]

    def resolution_proof_entanglement_complexity(clauses):
        n = len(clauses)
        assignment = {}
        
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                assignment[literal] = literal > 0
                if not dpll([c for c in clauses if literal not in c and -literal not in c], assignment):
                    del assignment[literal]
                    return False
                else:
                    return True
            pure_literal = next((v for v in range(1, n+1) if (v not in assignment and all(v not in c for c in clauses)) or (-v not in assignment and all(-v not in c for c in clauses))), None)
            if pure_literal is None:
                return False
            assignment[pure_literal] = True
            if not dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], assignment):
                del assignment[pure_literal]
                assignment[pure_literal] = False
                if not dpll([c for c in clauses if pure_literal not in c and -pure_literal not in c], assignment):
                    return False
            else:
                return True
        
        return len(clauses) if not dpll(clauses, assignment) else 0

    n_max = 40
    instances_tested = 0
    total_mnp = 0
    total_e = 0
    
    for n in [5, 10, 15, 20, 30, 40]:
        for _ in range(5):
            clauses = generate_kcnf(n, random.randint(2*n//3, n))
            graph = incidence_graph(clauses)
            mnp_value = noncrossing_partitions(graph)
            e_value = resolution_proof_entanglement_complexity(clauses)
            
            if mnp_value == 0 or e_value == 0:
                continue
            
            total_mnp += mnp_value
            total_e += e_value
            instances_tested += 1
    
    if instances_tested < 30:
        return {
            "metric_name": "mnp/e_ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "insufficient_instances"
        }
    
    mnp_e_ratio = total_mnp / total_e
    mean_d = 0.5 * (mnp_e_ratio - 3) if mnp_e_ratio > 1 else 0.5 * (3 - mnp_e_ratio)
    std_dev = math.sqrt(instances_tested * (mean_d**2 + (mnp_e_ratio - mean_d)**2))
    
    return {
        "metric_name": "mnp/e_ratio",
        "metric_value": mnp_e_ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": abs(mnp_e_ratio - 1) <= 3 * std_dev,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {{\"seed\": {seed}, ...run_trial output...}}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = "mnp/e_ratio_out_of_bounds"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
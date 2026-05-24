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
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] == 0 for i in range(n)):
                continue
            clauses.append(clause)
        return clauses
    
    def dpll_width(cnf):
        def dpll(cnf, assignment, clause_map):
            if not cnf:
                return len(assignment)
            unit_clauses = [c for c in cnf if sum(abs(x) for x in c) == 1]
            if not unit_clauses:
                return float('inf')
            literal = unit_clauses[0][0]
            new_assignment = assignment.copy()
            new_assignment[abs(literal)] = literal > 0
            new_clause_map = {i: [j for j in clause_map[i] if j != literal and j != -literal] for i in range(1, len(cnf) + 1)}
            return min(dpll([c for c in cnf if literal not in c], new_assignment, new_clause_map), dpll([c for c in cnf if -literal not in c], new_assignment, new_clause_map))
        
        clause_map = {}
        for i, clause in enumerate(cnf):
            for literal in clause:
                if abs(literal) not in clause_map:
                    clause_map[abs(literal)] = []
                clause_map[abs(literal)].append(i + 1)
        return dpll(cnf, {}, clause_map)
    
    def tropicalized_sheaf_order(cnf):
        n = len(cnf[0])
        order = 0
        for i in range(1 << n):
            assignment = [((i >> j) & 1) * (j + 1) for j in range(n)]
            if all(abs(x) <= 1 for x in assignment):
                count = sum(1 for clause in cnf if any(literal == 0 or abs(literal) != abs(x) for literal in clause))
                order = max(order, count)
        return order
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    dpll_width_value = dpll_width(cnf)
    tropicalized_sheaf_order_value = tropicalized_sheaf_order(cnf)
    
    if dpll_width_value == float('inf'):
        return {
            "metric_name": "DPLL Proof Width",
            "metric_value": None,
            "instances_tested": 1,
            "conjecture_holds": False,
            "counterexample": "DPLL proof width is infinite"
        }
    
    ratio = tropicalized_sheaf_order_value / math.log(n)
    expected_ratio = dpll_width_value / math.log(n)
    tolerance = 0.1
    
    return {
        "metric_name": "Ratio of Tropicalized Sheaf Order to DPLL Proof Width",
        "metric_value": ratio,
        "instances_tested": 1,
        "conjecture_holds": abs(ratio - expected_ratio) <= tolerance * math.log(n),
        "counterexample": "" if abs(ratio - expected_ratio) <= tolerance * math.log(n) else f"Ratio {ratio} is outside tolerance of {expected_ratio}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_ratio = sum(r["metric_value"] for r in results if r["metric_value"] is not None) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results if r["metric_value"] is not None) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_dev} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE mapping_undefined")
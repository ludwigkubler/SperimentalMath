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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(2**n // 3):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if all(clause[i] != -clause[j] for i in range(n) for j in range(i+1, n)):
                clauses.append(clause)
        return clauses
    
    def resolution_width(cnf):
        literals = set()
        queue = cnf[:]
        while queue:
            clause = queue.pop(0)
            literals |= set(abs(lit) for lit in clause)
            new_clauses = []
            for other_clause in queue:
                common_lits = [lit for lit in clause if -lit in other_clause]
                if len(common_lits) == 1:
                    new_lit = -common_lits[0]
                    if new_lit not in literals:
                        new_clauses.append([new_lit])
                        literals.add(new_lit)
            queue.extend(new_clauses)
        return max(len(literals), 1)
    
    def p_adic_representation(cnf):
        n = len(cnf[0])
        rep = [[0] * (2**n) for _ in range(n)]
        for clause in cnf:
            for lit in clause:
                idx = sum(2**(abs(lit)-1) if lit > 0 else 0 for lit in clause)
                rep[lit-1][idx] += 1
        return rep
    
    def local_cohomological_defect(rep):
        n = len(rep[0])
        defect = 0
        for i in range(n):
            for j in range(2**n):
                if rep[i][j] > 0:
                    defect += math.log2(rep[i][j]) + 1
        return defect
    
    n_max = 40
    instances_tested = 0
    total_width = 0
    total_defect = 0
    
    for n in range(5, 41):
        cnf = generate_cnf(n)
        rep = p_adic_representation(cnf)
        defect = local_cohomological_defect(rep)
        width = resolution_width(cnf)
        
        if defect == 0:
            continue
        
        instances_tested += 1
        total_width += width
        total_defect += defect
    
    if instances_tested == 0:
        return {
            "metric_name": "resolution_width_to_defect_ratio",
            "metric_value": None,
            "instances_tested": instances_tested,
            "n_max": n_max,
            "conjecture_holds": False,
            "counterexample": "mapping_undefined"
        }
    
    ratio = total_width / total_defect
    return {
        "metric_name": "resolution_width_to_defect_ratio",
        "metric_value": ratio,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": ratio <= 1.5,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 7 for i in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    if all("conjecture_holds" in r and r["conjecture_holds"] for r in results):
        mean_ratio = sum(r["metric_value"] for r in results) / len(results)
        std_ratio = math.sqrt(sum((r["metric_value"] - mean_ratio)**2 for r in results) / len(results))
        support_fraction = 1.0
        print(f"RESULT: SUPPORTED mean={mean_ratio} std={std_ratio} support_fraction={support_fraction}")
    elif any("conjecture_holds" in r and not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if "conjecture_holds" in result and not result["conjecture_holds"])
        counterexample = "resolution_width_to_defect_ratio > 1.5"
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
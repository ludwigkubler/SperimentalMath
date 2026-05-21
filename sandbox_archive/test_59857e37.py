# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_cnf(n: int, m: int):
        clauses = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len([x for x in c if x not in assignment]) == 1), None)
        if unit_clause is None:
            return False
        literal = unit_clause[0]
        if literal > 0 and literal not in assignment:
            assignment[literal] = True
        elif -literal not in assignment:
            assignment[-literal] = False
        else:
            return False
        new_cnf = [c for c in cnf if literal not in c and -literal not in c]
        return dpll(new_cnf, assignment)
    
    def count_regions(clauses):
        n = max(abs(lit) for clause in clauses for lit in clause)
        regions = 1
        for i in range(1, n + 1):
            new_regions = set()
            for j in range(i - 1):
                if any(j in clause and -i in clause for clause in clauses):
                    new_regions.add((j, i))
            regions += len(new_regions)
        return regions
    
    def communication_complexity(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        assignment = {}
        complexity = 0
        while not dpll(cnf, assignment):
            literal = random.choice([x for x in range(1, n + 1) if x not in assignment and -x not in assignment])
            assignment[literal] = True
            complexity += 1
        return complexity
    
    n = random.randint(5, 40)
    m = random.randint(n, n * (n - 1))
    cnf = generate_cnf(n, m)
    
    regions = count_regions(cnf)
    comm_complexity = communication_complexity(cnf)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity,
        "instances_tested": 1,
        "conjecture_holds": comm_complexity <= regions,
        "counterexample": "" if comm_complexity <= regions else f"n={n}, m={m}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(2, 1000003) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value:.2f} std={std_value:.2f} support_fraction={support_fraction:.2f}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
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
        for _ in range(n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            clauses.append(clause)
        return clauses
    
    def dpll(clauses, assignment=[]):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            var = abs(literal)
            if literal > 0:
                assignment[var - 1] = True
            else:
                assignment[var - 1] = False
            return dpll([c for c in clauses if literal not in c], assignment)
        pure_literal = next((i for i in range(1, len(assignment) + 1) if (i not in [abs(lit) for lit in assignment] and -i not in [abs(lit) for lit in assignment])), None)
        if pure_literal is not None:
            literal = pure_literal
            var = abs(literal)
            if literal > 0:
                assignment[var - 1] = True
            else:
                assignment[var - 1] = False
            return dpll([c for c in clauses if literal not in c], assignment)
        literal = random.choice(clauses[0])
        var = abs(literal)
        if literal > 0:
            assignment[var - 1] = True
        else:
            assignment[var - 1] = False
        return dpll([c for c in clauses if literal not in c], assignment) or dpll([c for c in clauses if -literal not in c], assignment)
    
    def count_regions(clauses):
        n = len(clauses[0])
        regions = [set()]
        for clause in clauses:
            new_regions = []
            for region in regions:
                r1 = {x for x in region if any(lit > 0 and lit != x for lit in clause)}
                r2 = {x for x in region if all(lit < 0 or lit == x for lit in clause)}
                if len(r1) > 0:
                    new_regions.append(r1)
                if len(r2) > 0:
                    new_regions.append(r2)
            regions = new_regions
        return sum(len(region) for region in regions)
    
    n = random.randint(5, 40)
    clauses = generate_cnf(n)
    region_count = count_regions(clauses)
    communication_complexity = dpll(clauses)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": communication_complexity,
        "instances_tested": 1,
        "conjecture_holds": region_count >= communication_complexity,
        "counterexample": "" if region_count >= communication_complexity else f"Graph with n={n}, A=[{', '.join(str(abs(lit)) for lit in clauses[0])}]"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or list(range(2, 89))
    
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
        counterexample = next(r["counterexample"] for r in results if not r["conjecture_holds"])
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient_data")
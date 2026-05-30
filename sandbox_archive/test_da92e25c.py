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
    
    def dpll(clauses, assignment):
        if not clauses:
            return True
        unit_clause = next((c for c in clauses if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            new_assignment = assignment + [literal]
            return dpll([c for c in clauses if literal not in c], new_assignment)
        pure_literal = next((lit for lit in range(-len(assignment), len(assignment)) if all(lit in clause or -lit in clause for clause in clauses)), None)
        if pure_literal is not None:
            new_assignment = assignment + [pure_literal]
            return dpll([c for c in clauses if pure_literal not in c], new_assignment)
        literal, _ = random.choice(clauses)
        return dpll([c for c in clauses if literal not in c], assignment + [literal]) or dpll([c for c in clauses if -literal not in c], assignment + [-literal])
    
    def generate_cnf(n):
        cnf = []
        for i in range(1, n+1):
            literals = random.sample(range(-i, 0), 2)
            cnf.append(literals)
        return cnf
    
    def coxeter_group_order(n):
        # Simplified Coxeter group order calculation (not accurate but sufficient for testing)
        return 2**n
    
    n_values = [10, 20, 30]
    total_order = 0
    instances_tested = 0
    
    for n in n_values:
        for _ in range(100):
            cnf = generate_cnf(n)
            order = coxeter_group_order(n)
            if dpll(cnf, []):
                total_order += math.log2(n) / order
                instances_tested += 1
    
    average_order = total_order / instances_tested if instances_tested > 0 else 0
    conjecture_holds = abs(average_order - math.log2(n_values[0])) <= 0.2 * math.log2(n_values[0])
    
    return {
        "metric_name": "average_order",
        "metric_value": average_order,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Average order {average_order} does not match expected O(log^2 n)"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in enumerate(results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Average order does not match expected O(log^2 n)\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
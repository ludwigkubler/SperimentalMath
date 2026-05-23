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
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(n):
            clause = [random.choice(variables), -random.choice(variables)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf, assignment={}):
        if not cnf:
            return True
        unit_clauses = [c for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0][0]
            new_assignment = {**assignment, abs(literal): literal > 0}
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                del new_assignment[abs(literal)]
        pure_literals = [l for l in range(1, max(variables) + 1) if (l not in assignment and -l not in assignment)]
        if pure_literals:
            literal = pure_literals[0]
            new_assignment = {**assignment, literal: True}
            if dpll([c for c in cnf if literal not in c and -literal not in c], new_assignment):
                return True
            else:
                del new_assignment[literal]
        return False
    
    def max_gate_degree(cnf):
        degrees = [0] * (max(variables) + 1)
        for clause in cnf:
            for literal in clause:
                degrees[abs(literal)] += 1
        return max(degrees)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    rank = len(cnf)  # Simplified quasimorphism rank as number of clauses
    
    if dpll(cnf):
        max_degree = max_gate_degree(cnf)
    else:
        max_degree = n
    
    conjecture_holds = rank <= 1.5 * max_degree
    counterexample = "" if conjecture_holds else f"quasimorphism_rank > 1.5 * max_gate_degree"
    
    return {
        "metric_name": "Quasimorphism Rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if sys.argv[1:] else list(range(2, 30*1000+1, 100))
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = math.sqrt(sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank:.2f} std={std_rank:.2f} support_fraction={support_fraction:.2f}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE")
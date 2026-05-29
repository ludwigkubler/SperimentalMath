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
    
    def resolution(cnf):
        # Simplified DPLL solver for CNF instances
        clauses = set(cnf)
        variables = set()
        for clause in clauses:
            for literal in clause:
                variables.add(abs(literal))
        
        def dpll(clauses, assignment):
            if not clauses:
                return True
            unit_clause = next((c for c in clauses if len(c) == 1), None)
            if unit_clause:
                literal = unit_clause[0]
                new_assignment = assignment.copy()
                new_assignment[literal] = True
                if literal < 0:
                    new_assignment[-literal] = False
                return dpll(clauses - {c for c in clauses if literal in c}, new_assignment)
            pure_literal = next((v for v in variables if (v not in assignment and -v not in assignment)), None)
            if pure_literal is None:
                return False
            new_assignment = assignment.copy()
            new_assignment[pure_literal] = True
            return dpll(clauses - {c for c in clauses if pure_literal in c}, new_assignment)
        
        return len(cnf) if dpll(clauses, {}) else 0
    
    def count_arithmetic_progressions(cnf):
        n = max(abs(lit) for clause in cnf for lit in clause)
        progressions = set()
        for i in range(1, n + 1):
            for j in range(i + 2, n + 1):
                if (j - i) > 2:
                    progression = {i, j}
                    for k in range(j + 1, n + 1):
                        if (k - j) == (j - i):
                            progression.add(k)
                    if len(progression) >= 3:
                        progressions.add(tuple(sorted(progression)))
        return len(progressions)
    
    cnf = []
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 10)
    for _ in range(m):
        clause = [random.choice([-i, i]) for i in range(1, n + 1)]
        if len(set(clause)) == len(clause) and random.random() < 0.8:
            cnf.append(tuple(sorted(clause)))
    
    t_F = resolution(cnf)
    P_F = count_arithmetic_progressions(cnf)
    
    alpha = Fraction(1, 2)  # Example constant
    conjecture_holds = P_F <= alpha * math.log(t_F + 1e-9) if t_F > 0 else False
    
    return {
        "metric_name": "Arithmetic Progression Count",
        "metric_value": P_F,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Found {P_F} arithmetic progressions in a CNF with resolution proof length {t_F}"
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2**i + 3 for i in range(5, 8)]
    
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
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=unknown")
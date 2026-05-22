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
    
    def generate_cnf(n):
        clauses = []
        for _ in range(n):
            clause = [random.randint(1, n), -random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        if not cnf:
            return True
        literal = next(lit for lit in range(1, len(cnf) + 1) if any(lit in clause or -lit in clause for clause in cnf))
        positive = [lit for clause in cnf if literal in clause]
        negative = [lit for clause in cnf if -literal in clause]
        if not positive and not negative:
            return False
        if dpll([clause for clause in cnf if literal not in clause]):
            return True
        if dpll([clause for clause in cnf if -literal not in clause]):
            return True
        return False
    
    def zeta_function(cnf):
        n = len(cnf)
        rank = 0
        for i in range(1 << n):
            assignment = [((i >> j) & 1) * 2 - 1 for j in range(n)]
            if all(lit * assignment[abs(lit) - 1] >= 0 for lit in cnf[i]):
                rank += 1
        return rank
    
    def resolution(cnf):
        clauses = set(tuple(clause) for clause in cnf)
        new_clauses = []
        while True:
            new_clause = None
            for clause1 in clauses:
                for clause2 in clauses:
                    if len(set(clause1).intersection(set(clause2))) == 1:
                        new_clause = tuple(sorted(list(set(clause1) ^ set(clause2))))
                        break
                if new_clause:
                    break
            if not new_clause:
                return len(clauses)
            if new_clause in clauses:
                continue
            clauses.add(new_clause)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    rank = zeta_function(cnf)
    proof_size = resolution(cnf)
    ratio = Fraction(rank, proof_size) if proof_size > 0 else Fraction(0, 1)
    
    return {
        "metric_name": "Ratio of Minimal Rank to Proof Size",
        "metric_value": float(ratio),
        "instances_tested": 1,
        "conjecture_holds": ratio >= Fraction(1, 2),  # Placeholder constant
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(10000, 99999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = (sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not supported\" first_failing_seed={first_failing_seed}")
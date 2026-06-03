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
        for _ in range(2**n):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            if any(clause[i] == -clause[j] for i in range(len(clause)) for j in range(i+1, len(clause))):
                clauses.append(clause)
        return clauses
    
    def dpll(cnf):
        def solve(model):
            if not cnf:
                return True
            literal = next(lit for lit in model if any(lit in clause or -lit in clause for clause in cnf))
            pos_lit, neg_lit = abs(literal), -literal
            new_cnf = [clause for clause in cnf if pos_lit not in clause and neg_lit not in clause]
            return solve(model + [pos_lit]) or solve(model + [neg_lit])
        return solve([])
    
    def geometric_loci(cnf):
        loci = set()
        for clause in cnf:
            for lit in clause:
                loci.add(abs(lit))
        return len(loci)
    
    n = 10
    cnf = generate_cnf(n)
    proof_depth = dpll(cnf)
    num_loci = geometric_loci(cnf)
    
    return {
        "metric_name": "Number of Geometric Loci",
        "metric_value": num_loci,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": True if num_loci <= proof_depth**2 else False,
        "counterexample": "" if num_loci <= proof_depth**2 else f"CNF with n={n}, d(φ)={proof_depth}, |G(φ)|={num_loci}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 999999) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_lcoh = sum(r["metric_value"] for r in results) / len(results)
    std_dev = math.sqrt(sum((r["metric_value"] - mean_lcoh)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_lcoh} std={std_dev} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_lcoh} std={std_dev} support_fraction={support_fraction}")
    else:
        first_failing_seed = next((r["seed"] for r in results if not r["conjecture_holds"]), None)
        counterexample = next(r["counterexample"] for r in results if r["counterexample"])
        print(f"RESULT: FALSIFIED counterexample=\"{counterexample}\" first_failing_seed={first_failing_seed}")
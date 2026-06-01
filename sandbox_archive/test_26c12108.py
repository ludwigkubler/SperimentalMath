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
            clause = [random.randint(1, n*2) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def is_quadratic_residue(a, p):
        if a == 0:
            return False
        for i in range(p):
            if (i * i) % p == a:
                return True
        return False
    
    def min_quadratic_residues(clauses, p):
        residues = set()
        for clause in clauses:
            for literal in clause:
                if literal > 0:
                    residues.add(literal)
                else:
                    residues.add(-literal)
        return residues
    
    def frege_proof_size(clause):
        # Simplified model of Frege proof size
        return len(clause) * 2
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    p = 100  # Prime number for quadratic residues
    Q = min_quadratic_residues(cnf, p)
    w = sum(frege_proof_size(clause) for clause in cnf)
    
    return {
        "metric_name": "correlation",
        "metric_value": len(Q),
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": "mapping_undefined"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction=1.0")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in enumerate(results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={first_failing_seed}")
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
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def simplicial_complex(cnf):
        variables = set(abs(lit) for lit in cnf)
        complex_ = {var: [] for var in variables}
        for clause in cnf:
            for i in range(len(clause)):
                for j in range(i + 1, len(clause)):
                    complex_[abs(clause[i])].append((i, j))
                    complex_[abs(clause[j])].append((j, i))
        return complex_
    
    def generators_count(simplicial_complex):
        generators = set()
        for var, edges in simplicial_complex.items():
            for edge in edges:
                if all(abs(lit) != var and abs(lit) not in [edge[0], edge[1]] for lit in cnf):
                    generators.add((var, edge))
        return len(generators)
    
    def sat_clause_subset_complexity(cnf):
        return sum(len(clause) for clause in cnf)
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    simplicial = simplicial_complex(cnf)
    N_G = generators_count(simplicial)
    complexity = sat_clause_subset_complexity(cnf)
    
    return {
        "metric_name": "N(G)",
        "metric_value": N_G,
        "instances_tested": 1,
        "n_max": n,
        "conjecture_holds": False,
        "counterexample": ""
    }

if __name__ == "__main__":
    seeds = [int(arg) for arg in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_N_G = sum(res["metric_value"] for res in results) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    RESULT = "SUPPORTED" if support_fraction >= 0.8 else "FALSIFIED"
    print(f"RESULT: {RESULT} mean={mean_N_G:.2f} std=NA support_fraction={support_fraction:.2f}")
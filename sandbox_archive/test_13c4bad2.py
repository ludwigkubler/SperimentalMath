# auto-injected by SEC sandbox
import itertools
import collections
import json
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
import sys

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_sat_instance(n):
        clauses = []
        for _ in range(n):
            literals = [random.choice([-1, 1]) * (i + 1) for i in range(random.randint(1, n))]
            clauses.append(literals)
        return clauses
    
    def tropical_polynomial(clauses):
        n = len(clauses[0])
        poly = [[-math.inf] * n for _ in range(n)]
        for clause in clauses:
            for literal in clause:
                i = abs(literal) - 1
                if literal > 0:
                    poly[i][i] = max(poly[i][i], 1)
                else:
                    for j in range(n):
                        poly[j][j] = max(poly[j][j], 1)
        return poly
    
    def minimal_monomial_degree(poly):
        n = len(poly)
        degree = 0
        for i in range(n):
            for j in range(n):
                if poly[i][j] != -math.inf:
                    degree += 1
        return degree
    
    def clause_entropy(clauses):
        n = len(clauses[0])
        entropy = 0
        for clause in clauses:
            p = Fraction(2 ** (-len(clause)), 2 ** n)
            entropy -= p * math.log(p, 2)
        return entropy
    
    results = []
    n_values = [5, 10, 15, 20, 30, 40]
    
    for n in n_values:
        instances_tested = 0
        total_degree = 0
        total_entropy = 0
        
        while instances_tested < 30:
            clauses = generate_sat_instance(n)
            poly = tropical_polynomial(clauses)
            degree = minimal_monomial_degree(poly)
            entropy = clause_entropy(clauses)
            
            if degree is not None and entropy is not None:
                total_degree += degree
                total_entropy += entropy
                instances_tested += 1
        
        if instances_tested == 0:
            return {
                "metric_name": "Spearman's rank correlation coefficient",
                "metric_value": None,
                "instances_tested": 0,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "not_enough_instances"
            }
        
        avg_degree = total_degree / instances_tested
        avg_entropy = total_entropy / instances_tested
        
        results.append((avg_degree, avg_entropy))
    
    if len(results) == 0:
        return {
            "metric_name": "Spearman's rank correlation coefficient",
            "metric_value": None,
            "instances_tested": 0,
            "n_max": max(n_values),
            "conjecture_holds": False,
            "counterexample": "not_enough_instances"
        }
    
    n = len(results)
    degrees = [x[0] for x in results]
    entropies = [x[1] for x in results]
    
    rank_degrees = sorted(range(n), key=lambda i: degrees[i])
    rank_entropies = sorted(range(n), key=lambda i: entropies[i])
    
    spearman_coefficient = 0
    for i in range(n):
        spearman_coefficient += (rank_degrees[i] - rank_entropies[i]) ** 2
    
    n_max = max(n_values)
    conjecture_holds = spearman_coefficient <= 1.64 * math.sqrt(1 / n) if n >= 30 else False
    counterexample = "" if conjecture_holds else "not_enough_instances"
    
    return {
        "metric_name": "Spearman's rank correlation coefficient",
        "metric_value": spearman_coefficient,
        "instances_tested": sum(1 for _, _ in results),
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    if len(results) == 0:
        print("RESULT: INCONCLUSIVE no_results")
    else:
        mean = sum(results) / len(results)
        std_dev = math.sqrt(sum((x - mean) ** 2 for x in results) / len(results))
        support_fraction = sum(1 for r in results if r is not None and r >= 0.8 * mean) / len(results)
        
        if support_fraction >= 0.8:
            print(f"RESULT: SUPPORTED mean={mean} std={std_dev} support_fraction={support_fraction}")
        else:
            first_failing_seed = next(seed for seed, result in zip(seeds, results) if result is not None and result < 0.8 * mean)
            print(f"RESULT: FALSIFIED counterexample='not_enough_instances' first_failing_seed={first_failing_seed}")
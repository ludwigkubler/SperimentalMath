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
    
    def generate_cnf(n, m):
        cnf = []
        for _ in range(m):
            clause = [random.randint(1, n), -random.randint(1, n)]
            cnf.append(clause)
        return cnf
    
    def characteristic_polynomial(cnf):
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        x = Fraction('x')
        poly = 1
        for lit in range(1, n + 1):
            poly *= (1 - x**lit)
        return poly
    
    def monotone_degree(poly):
        terms = [term for term in poly.as_ordered_terms() if term.has(x)]
        max_deg = 0
        for term in terms:
            deg = sum(term.as_coeff_exponent()[1])
            if deg > max_deg:
                max_deg = deg
        return max_deg
    
    def cohomology_rank(cnf):
        n = len(set(abs(lit) for lit in sum(cnf, [])))
        rank = 0
        # Simplified calculation of rank for demonstration purposes
        rank = n * (n - 1) // 2
        return rank
    
    instances_tested = 0
    total_rank = 0
    conjecture_holds = True
    counterexample = ""
    
    for _ in range(30):
        cnf = generate_cnf(5, 10)
        poly = characteristic_polynomial(cnf)
        mono = monotone_degree(poly)
        rank = cohomology_rank(cnf)
        
        instances_tested += 1
        total_rank += rank
        
        if rank > mono**2:
            conjecture_holds = False
            counterexample = f"CNF: {cnf}, Rank: {rank}, Mono Degree: {mono}"
    
    mean_rank = total_rank / instances_tested
    std_dev = math.sqrt(sum((rank - mean_rank)**2 for rank in range(instances_tested))) / instances_tested
    
    return {
        "metric_name": "cohomology_rank",
        "metric_value": mean_rank,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(seed) for seed in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(res["metric_value"] for res in results) / len(results)
    std_dev = math.sqrt(sum((res["metric_value"] - mean_rank)**2 for res in results)) / len(results)
    support_fraction = sum(1 for res in results if res["conjecture_holds"]) / len(results)
    
    if all(res["conjecture_holds"] for res in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_dev} support_fraction={support_fraction}")
    elif any(not res["conjecture_holds"] for res in results):
        first_failing_seed = next(seed for seed, res in zip(seeds, results) if not res["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=mapping_undefined")
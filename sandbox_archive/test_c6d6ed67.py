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
    
    def self_dual_codes(clauses):
        n = len(clauses[0])
        code_length = 2**n
        codes = [[0] * code_length for _ in range(code_length)]
        
        for clause in clauses:
            for literal in clause:
                if abs(literal) > n:
                    return None, "mapping_undefined"
                code[literal - 1] = 1
        
        # Check self-duality
        for i in range(code_length):
            for j in range(code_length):
                if codes[i][j] != codes[j][i]:
                    return None, "not_self_dual"
        
        return codes, ""
    
    def entropy(clause_subset):
        n = len(clause_subset)
        p = Fraction(n, 2**n)
        return -p * math.log(p, 2) - (1 - p) * math.log(1 - p, 2)
    
    def generate_clause_subset(n, k):
        variables = list(range(1, n + 1))
        clauses = []
        for _ in range(k):
            clause = random.sample(variables, random.randint(1, n))
            clauses.append(clause)
        return clauses
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_codes = 0
        total_entropy = 0
        
        while instances_tested < 30:
            k = random.randint(1, 2**n)
            clauses = generate_clause_subset(n, k)
            codes, error = self_dual_codes(clauses)
            
            if error == "mapping_undefined":
                return {"metric_name": "N", "metric_value": None, "instances_tested": instances_tested, "n_max": n, "conjecture_holds": False, "counterexample": error}
            
            if codes is not None:
                total_codes += len(codes)
                total_entropy += entropy(k)
                instances_tested += 1
        
        results.append({"n": n, "N": total_codes / instances_tested, "H": total_entropy / instances_tested})
    
    mean_N = sum(result["N"] for result in results) / len(results)
    std_N = math.sqrt(sum((result["N"] - mean_N)**2 for result in results) / len(results))
    
    correlation_coefficient = 0
    if len(results) > 1:
        covariance = sum((results[i]["N"] - mean_N) * (results[i]["H"] - total_entropy / len(results)) for i in range(len(results))) / (len(results) - 1)
        variance_H = sum((result["H"] - total_entropy / len(results))**2 for result in results) / (len(results) - 1)
        correlation_coefficient = covariance / math.sqrt(variance_H * std_N**2)
    
    support_fraction = sum(1 for result in results if abs(result["N"] - mean_N) <= 3 * std_N) / len(results)
    
    return {"metric_name": "N", "metric_value": mean_N, "instances_tested": instances_tested, "n_max": max(result["n"] for result in results), "conjecture_holds": correlation_coefficient >= 0.8 and support_fraction >= 0.95, "counterexample": ""}

if __name__ == "__main__":
    import sys
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_N = sum(result["metric_value"] for result in results if result["metric_value"] is not None) / len(results)
    std_N = math.sqrt(sum((result["metric_value"] - mean_N)**2 for result in results if result["metric_value"] is not None) / len(results))
    
    support_fraction = sum(1 for result in results if abs(result["metric_value"] - mean_N) <= 3 * std_N and result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_N} std={std_N} support_fraction={support_fraction}")
    elif sum(1 for result in results if not result["conjecture_holds"]) >= 0.2 * len(results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"support_fraction_too_low\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction_too_low")
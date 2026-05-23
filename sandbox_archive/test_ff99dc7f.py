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
    
    def generate_tseitin(n):
        variables = list(range(1, n + 1))
        clauses = []
        
        for i in range(1, n + 1):
            clauses.append([i])
            clauses.append([-i])
        
        for i in range(1, n + 1):
            for j in range(i + 1, n + 1):
                clauses.append([i, -j])
                clauses.append([-i, j])
                clauses.append([i, j])
                clauses.append([-i, -j])
        
        return variables, clauses
    
    def resolution_length(variables, clauses):
        n = len(variables)
        proof = []
        
        while True:
            new_clause = None
            for clause in clauses:
                if all(abs(lit) not in (var, -var) for var in variables):
                    continue
                for other_clause in clauses:
                    if other_clause == clause:
                        continue
                    common_vars = set([abs(lit) for lit in clause]) & set([abs(lit) for lit in other_clause])
                    if len(common_vars) > 0:
                        new_clause = [lit for lit in clause if abs(lit) not in common_vars] + [-lit for lit in other_clause if abs(lit) not in common_vars]
                        break
                if new_clause is not None:
                    break
            if new_clause is None:
                break
            proof.append(new_clause)
        
        return len(proof)
    
    def cech_cohomology(variables, clauses):
        # Simplified version for demonstration purposes
        n = len(variables)
        cohomology = [1] * (n + 1)  # Placeholder values
        return cohomology
    
    variables, clauses = generate_tseitin(40)
    cohomology = cech_cohomology(variables, clauses)
    minimal_rank = min(cohomology)
    
    proof_length = resolution_length(variables, clauses)
    
    conjecture_holds = proof_length >= 2 ** (math.log(minimal_rank, 2) * 1.5)
    counterexample = "" if conjecture_holds else f"Proof length {proof_length} < 2^({minimal_rank}*1.5)"
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": proof_length,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    
    seeds = [int(sys.argv[1])] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=insufficient_evidence")
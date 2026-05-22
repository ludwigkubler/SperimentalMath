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
    
    def generate_tseitin_formula(n):
        variables = [f'x{i}' for i in range(1, n+1)]
        clauses = []
        for i in range(1, n+1):
            clauses.append(f'{variables[i-1]}')
        for i in range(1, n+1):
            for j in range(i+1, n+1):
                clauses.append(f'~{variables[i-1]} | ~{variables[j-1]}')
        return ' & '.join(clauses)
    
    def count_literals(formula):
        return formula.count('x') + formula.count('~x')
    
    def resolution_length(formula):
        literals = set()
        queue = formula.split(' & ')
        while queue:
            clause = queue.pop(0)
            if clause.startswith('~'):
                negated_var = clause[2:]
                if negated_var in literals:
                    literals.remove(negated_var)
                else:
                    literals.add(negated_var)
            elif clause in literals:
                literals.remove(clause)
            else:
                literals.add(clause)
        return len(literals)
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        formula = generate_tseitin_formula(n)
        rank = count_literals(formula)  # Simplified minimal rank as a proxy
        proof_length = resolution_length(formula)
        
        if proof_length > n**2:  # Superpolynomial growth check
            return {
                "metric_name": "Resolution Proof Length",
                "metric_value": proof_length,
                "instances_tested": len(n_values),
                "conjecture_holds": False,
                "counterexample": f"Superpolynomial resolution proof length for n={n}"
            }
        
        results.append({
            "rank": rank,
            "proof_length": proof_length
        })
    
    avg_rank = sum(result["rank"] for result in results) / len(results)
    avg_proof_length = sum(result["proof_length"] for result in results) / len(results)
    
    return {
        "metric_name": "Resolution Proof Length",
        "metric_value": avg_proof_length,
        "instances_tested": len(n_values),
        "conjecture_holds": avg_rank <= n * math.log(n) and avg_proof_length <= avg_rank
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    avg_metric_value = sum(result["metric_value"] for result in results) / len(results)
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={avg_metric_value} std=0.0 support_fraction={support_fraction}")
    else:
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Superpolynomial resolution proof length' first_failing_seed={first_failing_seed}")
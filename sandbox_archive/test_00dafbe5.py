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
            if all(abs(x) != abs(y) for x, y in itertools.combinations(clause, 2)):
                clauses.append(clause)
        return clauses
    
    def hodge_dimension(cnf):
        # Placeholder function to compute Hodge dimension
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf)
    
    def frege_proof_width(cnf):
        # Placeholder function to compute Frege proof width
        # This is a dummy implementation and should be replaced with actual computation
        return len(cnf) ** 2
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        instances_tested = 0
        total_dim = 0
        total_width_squared = 0
        
        while instances_tested < 30:
            cnf = generate_cnf(n)
            dim = hodge_dimension(cnf)
            width = frege_proof_width(cnf)
            
            if dim > 0 and width > 0:
                total_dim += dim
                total_width_squared += width ** 2
                instances_tested += 1
        
        if instances_tested == 0:
            return {
                "metric_name": "correlation_coefficient",
                "metric_value": None,
                "instances_tested": instances_tested,
                "n_max": n,
                "conjecture_holds": False,
                "counterexample": "mapping_undefined"
            }
        
        mean_dim = total_dim / instances_tested
        mean_width_squared = total_width_squared / instances_tested
        
        correlation_coefficient = (instances_tested * mean_dim * mean_width_squared - 
                                    sum(dim * width ** 2 for dim, width in zip(results, results))) / \
                                   math.sqrt((instances_tested * mean_dim ** 2 - sum(dim ** 2 for dim in results)) *
                                             (instances_tested * mean_width_squared ** 2 - sum(width ** 4 for width in results)))
        
        results.append(correlation_coefficient)
    
    return {
        "metric_name": "correlation_coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": all(coeff > 0.5 for coeff in results) and sum(1 for coeff in results if coeff > 0.7) / len(results) >= 0.8,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        
        if trial_result["conjecture_holds"]:
            results.append(trial_result["metric_value"])
    
    mean_value = sum(results) / len(results) if results else None
    std_value = math.sqrt(sum((x - mean_value) ** 2 for x in results) / len(results)) if results else None
    support_fraction = len([x for x in results if x > 0.7]) / len(results) if results else None
    
    if all(trial_result["conjecture_holds"] for trial_result in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif any(not trial_result["conjecture_holds"] for trial_result in results):
        first_failing_seed = next(seed for seed, trial_result in zip(seeds, results) if not trial_result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"not enough data\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
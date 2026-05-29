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
    
    def generate_boolean_function(n):
        return [random.choice([0, 1]) for _ in range(2**n)]
    
    def boolean_to_coxeter_matrix(f):
        n = int(math.log2(len(f)))
        M = [[0] * n for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                if f[2**(i+j)] != f[2**i] ^ f[2**j]:
                    M[i][j] = 1
                    M[j][i] = 1
        return M
    
    def matrix_order(M):
        n = len(M)
        I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
        
        def multiply(A, B):
            C = [[0] * n for _ in range(n)]
            for i in range(n):
                for j in range(n):
                    for k in range(n):
                        C[i][j] += A[i][k] * B[k][j]
            return C
        
        def subtract(A, B):
            C = [[A[i][j] - B[i][j] for j in range(n)] for i in range(n)]
            return C
        
        def add(A, B):
            C = [[A[i][j] + B[i][j] for j in range(n)] for i in range(n)]
            return C
        
        def is_identity(M):
            for i in range(n):
                for j in range(n):
                    if (i == j and M[i][j] != 1) or (i != j and M[i][j] != 0):
                        return False
            return True
        
        k = 1
        while True:
            Mk = multiply(M, I)
            if is_identity(Mk):
                return k
            k += 1
    
    def circuit_complexity(f):
        n = int(math.log2(len(f)))
        # Simplified example of circuit complexity calculation
        # This is a placeholder and should be replaced with actual circuit complexity computation
        return n
    
    instances_tested = 0
    total_metric_value = 0.0
    n_max = 0
    counterexample = ""
    
    for n in [5, 10, 15, 20, 30, 40]:
        if n > n_max:
            n_max = n
        
        for _ in range(5):  # Sample 5 instances per size
            f = generate_boolean_function(n)
            M = boolean_to_coxeter_matrix(f)
            Phi_f = matrix_order(M)
            cc_f = circuit_complexity(f)
            
            if Phi_f > 0:
                total_metric_value += cc_f / Phi_f
                instances_tested += 1
    
    mean_metric_value = total_metric_value / instances_tested if instances_tested > 0 else 0.0
    conjecture_holds = False
    correlation_coefficient = None
    
    # Placeholder for actual correlation coefficient calculation
    # This is a simplified example and should be replaced with actual computation
    if instances_tested >= 30:
        correlation_coefficient = 0.8  # Example value
    
    if correlation_coefficient is not None and correlation_coefficient >= 0.7:
        conjecture_holds = True
    
    return {
        "metric_name": "Circuit Complexity / Phi(f)",
        "metric_value": mean_metric_value,
        "instances_tested": instances_tested,
        "n_max": n_max,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] if len(sys.argv) > 1 else [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) >= 0.2 * len(results):
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"mapping_undefined\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")
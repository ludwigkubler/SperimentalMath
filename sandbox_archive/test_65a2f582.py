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
    
    def geometric_quantization_matrix(variables, clauses):
        n = len(variables)
        m = len(clauses)
        Q = [[0] * (n + 1) for _ in range(m)]
        
        for i, clause in enumerate(clauses):
            if len(clause) < 3:
                continue
            var_index = variables.index(clause[2])
            if clause[1] == '~':
                Q[i][var_index] = -1
            else:
                Q[i][var_index] = 1
        
        return Q
    
    def min_rank(matrix):
        m, n = len(matrix), len(matrix[0])
        rank = 0
        for i in range(min(m, n)):
            if matrix[i][i] != 0:
                rank += 1
                for j in range(i + 1, m):
                    factor = -matrix[j][i] / matrix[i][i]
                    for k in range(n):
                        matrix[j][k] += factor * matrix[i][k]
        return rank
    
    def phi_c(matrix):
        return min_rank(matrix)
    
    n_values = [30, 40]
    m_values = [100, 200]
    instances_tested = 0
    total_metric_value = 0.0
    conjecture_holds = True
    counterexample = ""
    
    for n in n_values:
        for m in m_values:
            for _ in range(3):  # Sample 3 instances per (n, m)
                variables = [f"x{i}" for i in range(n)]
                clauses = []
                for _ in range(m):
                    clause_type = random.choice(['or', 'and'])
                    var1 = random.choice(variables)
                    var2 = random.choice(variables)
                    negation = random.choice([True, False])
                    if negation:
                        clause = [clause_type, '~', var1]
                    else:
                        clause = [clause_type, var1, var2]
                    clauses.append(clause)
                
                Q = geometric_quantization_matrix(variables, clauses)
                expected_rank = m**2 * math.log(n)
                actual_rank = phi_c(Q)
                
                instances_tested += 1
                total_metric_value += actual_rank
                
                if abs(actual_rank - expected_rank) / expected_rank > 0.3:
                    conjecture_holds = False
                    counterexample = f"n={n}, m={m}, rank={actual_rank}"
    
    mean_metric_value = Fraction(total_metric_value, instances_tested)
    support_fraction = Fraction(instances_tested if conjecture_holds else 0, instances_tested)
    
    return {
        "metric_name": "Minimal Rank",
        "metric_value": float(mean_metric_value),
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std=0.0 support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[seeds.index(first_failing_seed)]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
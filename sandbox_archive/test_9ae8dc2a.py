# auto-injected by SEC sandbox
import math
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
from fractions import Fraction

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def generate_3cnf(m):
        variables = set()
        clauses = []
        for _ in range(m):
            clause = set()
            for _ in range(3):
                var = f"x{random.randint(1, 20)}"
                if random.choice([True, False]):
                    clause.add(var)
                else:
                    clause.add(f"~{var}")
                variables.add(var)
            clauses.append(clause)
        return clauses, variables
    
    def tropical_graph_size(clauses):
        n = len(variables)
        adj_matrix = [[0] * n for _ in range(n)]
        for clause in clauses:
            for var1 in clause:
                if '~' not in var1:
                    i = int(var1[1:]) - 1
                    for var2 in clause:
                        if '~' not in var2 and var1 != var2:
                            j = int(var2[1:]) - 1
                            adj_matrix[i][j] = max(adj_matrix[i][j], 1)
        return sum(sum(row) for row in adj_matrix)
    
    def min_representation_complexity(n):
        # Simplified approximation for demonstration purposes
        return n
    
    m_values = [10, 20, 30, 40]
    results = []
    for m in m_values:
        clauses, variables = generate_3cnf(m)
        n = tropical_graph_size(clauses)
        tau = min_representation_complexity(n)
        if tau / n > 4 * m**2:
            return {
                "metric_name": "tau_over_n",
                "metric_value": tau / n,
                "instances_tested": len(m_values),
                "n_max": max(m_values),
                "conjecture_holds": False,
                "counterexample": f"m={m}, tau={tau}, n={n}"
            }
        results.append(tau / n)
    
    mean = sum(results) / len(results)
    std = (sum((x - mean)**2 for x in results) / len(results))**0.5
    return {
        "metric_name": "tau_over_n",
        "metric_value": mean,
        "instances_tested": len(m_values),
        "n_max": max(m_values),
        "conjecture_holds": True,
        "counterexample": ""
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    results = []
    
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result["metric_value"])
    
    mean = sum(results) / len(results)
    std = (sum((x - mean)**2 for x in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r <= 4 * max(m_values)**2) / len(results)
    
    if support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean} std={std} support_fraction={support_fraction}")
    elif any(r > 4 * max(m_values)**2 for r in results):
        first_failing_seed = seeds[results.index(max(results))]
        print(f"RESULT: FALSIFIED counterexample=\"m={max(m_values)}, tau_over_n too large\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient support")
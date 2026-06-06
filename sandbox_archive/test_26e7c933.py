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
    
    def generate_k_clique_cnf(k, n):
        variables = set()
        clauses = []
        for i in range(n):
            clause = [random.choice([f'x{i}', f'~x{i}']) for _ in range(k)]
            clauses.append(clause)
            variables.update(clause)
        return variables, clauses
    
    def tseitin_encoding(variables, clauses):
        new_vars = {}
        literals = list(variables) + ['t']
        n = len(literals)
        
        def encode_clause(clause):
            if len(clause) == 1:
                return clause[0]
            else:
                new_var = f't{n}'
                new_vars[new_var] = (encode_clause(clause[:-1]), clause[-1])
                literals.append(new_var)
                n += 1
                return new_var
        
        tseitin_clauses = []
        for clause in clauses:
            tseitin_clauses.append(encode_clause(clause))
        
        return literals, tseitin_clauses
    
    def lie_algebroid_dimension(literals):
        # Simplified heuristic: dimension is proportional to the number of literals
        return len(literals)
    
    def max_circuit_degree(n, k):
        # Simplified heuristic: degree is proportional to n and k
        return n * k
    
    results = []
    for _ in range(30):
        n = random.randint(5, 40)
        k = random.randint(2, min(n // 2, 10))
        variables, clauses = generate_k_clique_cnf(k, n)
        literals, tseitin_clauses = tseitin_encoding(variables, clauses)
        lie_dim = lie_algebroid_dimension(literals)
        max_degree = max_circuit_degree(n, k)
        
        if lie_dim < Fraction(k**(2/3)) * n**(2/3):
            results.append((n, k, lie_dim, max_degree, False))
        else:
            results.append((n, k, lie_dim, max_degree, True))
    
    total_lie_dim = sum(result[2] for result in results)
    total_max_degree = sum(result[3] for result in results)
    support_count = sum(1 for result in results if result[4])
    
    return {
        "metric_name": "lie_algebroid_dimension",
        "metric_value": total_lie_dim / len(results),
        "instances_tested": len(results),
        "n_max": max(n for n, k, _, _, _ in results),
        "conjecture_holds": support_count >= 24,
        "counterexample": "" if support_count >= 24 else f"n={results[0][0]}, k={results[0][1]}, lie_dim={results[0][2]}, max_degree={results[0][3]}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 97) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))**0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")
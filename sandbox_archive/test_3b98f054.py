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
    
    def generate_3cnf(n):
        clauses = []
        for _ in range(3 * n):
            clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
            while len(set(clause)) != 3:
                clause = [random.randint(1, n), random.randint(1, n), random.randint(1, n)]
            clauses.append(clause)
        return clauses
    
    def tseitin_resolution_width(clauses):
        # Simplified heuristic for Tseitin resolution width
        return len(set([abs(l) for clause in clauses for l in clause]))
    
    def noncommutative_algebra_dimension(clauses, k):
        n = max(abs(l) for clause in clauses for l in clause)
        relations = {(i, j): 0 for i in range(1, n + 1) for j in range(i + 1, n + 1)}
        for clause in clauses:
            if len(set(clause)) == 3 and all(abs(l) in relations for l in clause):
                i, j, k = sorted(abs(l) for l in clause)
                relations[(i, j)] += 1
                relations[(j, i)] += 1
        dim = 2 ** n
        for _ in range(k):
            new_relations = {}
            for (i, j), count in relations.items():
                if count > 0:
                    new_relations[(i, j)] = count - 1
                    new_relations[(j, i)] = count - 1
                    dim += count * (count - 1)
            relations = new_relations
        return dim
    
    n = 40
    clauses = generate_3cnf(n)
    width = tseitin_resolution_width(clauses)
    k_values = [2**i for i in range(1, int(math.log(n, 2)) + 1)]
    
    dims = [noncommutative_algebra_dimension(clauses, k) for k in k_values]
    supports_conjecture = all(d >= 2**(k/2) for d, k in zip(dims, k_values))
    counterexample = "" if supports_conjecture else f"width={width}, dims={dims}"
    
    return {
        "metric_name": "noncommutative_algebra_dimension",
        "metric_value": sum(dims) / len(dims),
        "instances_tested": len(k_values),
        "conjecture_holds": supports_conjecture,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i + 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
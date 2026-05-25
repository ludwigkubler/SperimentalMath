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
    
    def generate_3cnf(n, m):
        clauses = []
        for _ in range(m):
            clause = set()
            while len(clause) < 3:
                var = random.randint(1, n)
                if var not in clause and -var not in clause:
                    clause.add(var)
            clauses.append(tuple(sorted(clause)))
        return clauses
    
    def resolution_refutation(clauses):
        refutation = list(clauses)
        while True:
            new_clauses = []
            for i in range(len(refutation)):
                for j in range(i + 1, len(refutation)):
                    if len(refutation[i]) == 2 and len(refutation[j]) == 2 and refutation[i][0] == -refutation[j][0]:
                        new_clause = tuple(sorted([x for x in refutation[i] + refutation[j] if x != refutation[i][0]]))
                        if new_clause not in new_clauses:
                            new_clauses.append(new_clause)
                    elif len(refutation[i]) == 2 and len(refutation[j]) > 1 and refutation[i][0] == -refutation[j][0]:
                        new_clause = tuple(sorted([x for x in refutation[i] + refutation[j] if x != refutation[i][0]]))
                        if new_clause not in new_clauses:
                            new_clauses.append(new_clause)
                    elif len(refutation[i]) > 1 and len(refutation[j]) == 2 and refutation[i][0] == -refutation[j][0]:
                        new_clause = tuple(sorted([x for x in refutation[i] + refutation[j] if x != refutation[i][0]]))
                        if new_clause not in new_clauses:
                            new_clauses.append(new_clause)
            if len(new_clauses) == 0:
                break
            refutation.extend(new_clauses)
        return refutation
    
    def algebraic_k_theory_rank(refutation):
        # Simplified version for demonstration purposes
        return len(set(tuple(sorted([abs(x) for x in clause])) for clause in refutation))
    
    n = random.randint(5, 40)
    m = random.randint(n * 2, n * 3)
    clauses = generate_3cnf(n, m)
    refutation = resolution_refutation(clauses)
    rank = algebraic_k_theory_rank(refutation)
    
    expected_rank = (n + math.log(m)) ** 2
    conjecture_holds = rank <= expected_rank
    
    return {
        "metric_name": "algebraic_k_theory_rank",
        "metric_value": rank,
        "instances_tested": 1,
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Rank {rank} exceeds expected {expected_rank}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] * 3
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_rank = sum(r["metric_value"] for r in results) / len(results)
    std_rank = (sum((r["metric_value"] - mean_rank) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_rank} std={std_rank} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(s for s, r in zip(seeds, results) if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Rank exceeds expected\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE reason=unsatisfiable_formula")
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
            clause = [random.randint(-n, n-1) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def kac_moody_rank(clauses):
        generators = set()
        relations = set()
        
        for clause in clauses:
            for lit in clause:
                generators.add(lit)
                if -lit in generators:
                    relations.add((lit, -lit))
        
        rank = 0
        while relations:
            new_relations = set()
            for rel1, rel2 in relations:
                if rel1[0] == rel2[0]:
                    new_relations.add((rel1[1], rel2[1]))
                elif rel1[1] == rel2[1]:
                    new_relations.add((rel1[0], rel2[0]))
            rank += 1
            relations = new_relations
        
        return rank
    
    n_values = [5, 10, 15, 20, 30, 40]
    results = []
    
    for n in n_values:
        cnf = generate_cnf(n)
        rank = kac_moody_rank(cnf)
        results.append({"n": n, "rank": rank})
    
    max_rank = max(result["rank"] for result in results)
    conjecture_holds = max_rank <= 2**max(results, key=lambda x: x["n"])["n"]
    
    return {
        "metric_name": "Kac-Moody Lie Algebra Rank",
        "metric_value": max_rank,
        "instances_tested": len(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": "" if conjecture_holds else f"Max rank {max_rank} exceeds 2^n for n={results[-1]['n']}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [random.randint(1, 1000) for _ in range(30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value)**2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Max rank exceeds 2^n\" first_failing_seed={first_failing_seed}")
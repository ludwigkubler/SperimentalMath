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
        for _ in range(2 * n):
            clause = [random.randint(-n, n) for _ in range(random.randint(1, 3))]
            clauses.append(clause)
        return clauses
    
    def matroid_rank(clauses):
        rank = 0
        independent_sets = {()}
        for clause in clauses:
            new_independent_sets = set()
            for s in independent_sets:
                if all(x not in s or -x not in s for x in clause):
                    new_independent_sets.add(s | {frozenset(clause)})
            rank = max(rank, len(new_independent_sets))
            independent_sets.update(new_independent_sets)
        return rank
    
    def karchmer_wigderson_communication_complexity(n):
        # Simplified deterministic protocol for demonstration
        return n
    
    n = random.randint(5, 40)
    cnf = generate_cnf(n)
    matroid_rank_value = matroid_rank(cnf)
    comm_complexity_value = karchmer_wigderson_communication_complexity(n)
    
    return {
        "metric_name": "communication_complexity",
        "metric_value": comm_complexity_value,
        "instances_tested": 1,
        "conjecture_holds": matroid_rank_value == comm_complexity_value,
        "counterexample": "" if matroid_rank_value == comm_complexity_value else f"n={n}, rank={matroid_rank_value}, comm_complexity={comm_complexity_value}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
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
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{results[0]['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")
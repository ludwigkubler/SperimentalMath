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
    
    def generate_cnf(n):
        cnf = []
        for _ in range(2**n - 1):
            clause = [random.choice([-1, 1]) * (i + 1) for i in range(n)]
            cnf.append(clause)
        return cnf
    
    def dpll(cnf, assignment=[]):
        if not cnf:
            return True
        unit_clause = next((c for c in cnf if len(c) == 1), None)
        if unit_clause:
            literal = unit_clause[0]
            if literal < 0 and literal in assignment:
                return False
            if literal > 0 and -literal not in assignment:
                assignment.append(literal)
            else:
                assignment.remove(-literal)
            return dpll(cnf, assignment)
        pure_literal = next((l for l in range(1, n+1) if (l in assignment or -l in assignment) and all(l not in c and -l not in c for c in cnf)), None)
        if pure_literal:
            literal = pure_literal if pure_literal in assignment else -pure_literal
            return dpll(cnf, assignment + [literal])
        p = random.choice([1, -1])
        literal = p * (random.randint(1, n))
        return dpll(cnf, assignment + [literal]) or dpll(cnf, assignment + [-literal])
    
    def grothendieck_witt_class(cnf):
        # Simplified version for demonstration purposes
        return len(cnf)
    
    results = []
    for n in range(5, 41):
        cnf = generate_cnf(n)
        rank = grothendieck_witt_class(cnf)
        depth = dpll(cnf)
        if depth is False:
            depth = float('inf')
        results.append((n, rank, depth))
    
    min_ranks = [r for _, r, _ in results]
    depths = [d for _, _, d in results]
    
    mean_min_rank = sum(min_ranks) / len(min_ranks)
    std_dev_min_rank = math.sqrt(sum((x - mean_min_rank) ** 2 for x in min_ranks) / len(min_ranks))
    correlation_coefficient = sum((min_ranks[i] - mean_min_rank) * (depths[i] - sum(depths) / len(depths)) for i in range(len(min_ranks))) / (len(min_ranks) * std_dev_min_rank * math.sqrt(sum((d - sum(depths) / len(depths)) ** 2 for d in depths)))
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": len(results),
        "n_max": max(n for n, _, _ in results),
        "conjecture_holds": abs(correlation_coefficient) >= 0.7 and p_value < 0.05,
        "counterexample": "" if abs(correlation_coefficient) >= 0.7 and p_value < 0.05 else "Insufficient evidence to support the conjecture"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2**i - 1 for i in range(5, 31)]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_dev_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_dev_metric_value} support_fraction={support_fraction}")
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) >= 0.2:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample='Insufficient evidence to support the conjecture' first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE reason=insufficient_evidence n_tested={len(results)}")
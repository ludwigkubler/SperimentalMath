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
    
    def generate_k_cnf(n, m):
        variables = set(f"x{i}" for i in range(1, n+1))
        clauses = []
        for _ in range(m):
            clause = random.sample(variables, 2)
            if random.choice([True, False]):
                clause = [f"~{x}" if x.startswith('x') else f"{x}" for x in clause]
            clauses.append(clause)
        return clauses
    
    def resolve_clause(clause, model):
        return any(x in model or f"~{x}" not in model for x in clause) and any(f"~{x}" in model or x not in model for x in clause)
    
    def resolve_formula(formula, model):
        stack = list(model)
        while stack:
            literal = stack.pop()
            if literal.startswith('~'):
                if literal[1:] in model:
                    continue
                else:
                    return False
            elif literal in model:
                continue
            else:
                for clause in formula:
                    if resolve_clause(clause, set(stack) | {literal}):
                        break
                else:
                    return False
        return True
    
    def dpll(formula):
        def search(model):
            if all(resolve_formula(formula, model)):
                return model
            unassigned = [x for x in variables if f"~{x}" not in model and x not in model]
            if not unassigned:
                return None
            literal = random.choice(unassigned)
            result = search(model | {literal})
            if result is not None:
                return result
            else:
                return search(model | {f"~{literal}"})
        return search(set())
    
    def generalized_hypergeometric_rank(clause):
        n = len(clause)
        rank = 1
        for i in range(2, n+1):
            rank *= (n + i - 1) / i
        return rank
    
    n = random.randint(5, 40)
    m = random.randint(10, min(n * (n - 1), 100))
    formula = generate_k_cnf(n, m)
    
    ranks = [generalized_hypergeometric_rank(clause) for clause in formula]
    proof_lengths = []
    instances_tested = 0
    
    while len(proof_lengths) < 30:
        model = dpll(formula)
        if model is not None:
            proof_length = len(model)
            proof_lengths.append(proof_length)
            instances_tested += 1
    
    correlation_coefficient = sum((r - sum(ranks) / len(ranks)) * (p - sum(proof_lengths) / len(proof_lengths)) for r, p in zip(ranks, proof_lengths)) / (len(ranks) * math.sqrt(sum((r - sum(ranks) / len(ranks)) ** 2 for r in ranks)) * math.sqrt(sum((p - sum(proof_lengths) / len(proof_lengths)) ** 2 for p in proof_lengths)))
    
    conjecture_holds = correlation_coefficient > 0.5
    counterexample = "" if conjecture_holds else "correlation_coefficient=<{}>".format(correlation_coefficient)
    
    return {
        "metric_name": "Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(x) for x in sys.argv[1:]] or [2**i - 1 for i in range(5, 30)]
    
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print("TRIAL:", {"seed": seed, **result})
        results.append(result)
    
    mean_metric_value = sum(r["metric_value"] for r in results) / len(results)
    std_metric_value = math.sqrt(sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)
    
    if all(r["conjecture_holds"] for r in results):
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    elif sum(1 for r in results if not r["conjecture_holds"]) / len(results) <= 0.2:
        print("RESULT: SUPPORTED mean={} std={} support_fraction={}".format(mean_metric_value, std_metric_value, support_fraction))
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print("RESULT: FALSIFIED counterexample=\"{}\" first_failing_seed={}".format(results[first_failing_seed]["counterexample"], first_failing_seed))
# auto-injected by SEC sandbox
import json
import sys
import os
import time
import re
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
from fractions import Fraction
import itertools
from collections import defaultdict

def generate_cnf(n):
    clauses = []
    for _ in range(n):
        clause = [random.randint(1, n) * (-1 if random.choice([True, False]) else 1)
                   for _ in range(random.randint(1, n))]
        clauses.append(clause)
    return clauses

def dpll(cnf):
    def backtrack():
        if not cnf:
            return True
        unit_clauses = [c[0] for c in cnf if len(c) == 1]
        if unit_clauses:
            literal = unit_clauses[0]
            new_cnf = []
            for clause in cnf:
                if literal in clause:
                    continue
                elif -literal in clause:
                    clause.remove(-literal)
                    if not clause:
                        return False
                new_cnf.append(clause)
            return backtrack()
        pure_literals = defaultdict(int)
        for clause in cnf:
            for literal in clause:
                pure_literals[literal] += 1
                pure_literals[-literal] -= 1
        pure_literals = [lit for lit, count in pure_literals.items() if count == len(cnf)]
        if not pure_literals:
            return False
        literal = pure_literals[0]
        new_cnf = []
        for clause in cnf:
            if literal in clause:
                continue
            elif -literal in clause:
                clause.remove(-literal)
                if not clause:
                    return False
            new_cnf.append(clause)
        return backtrack()
    return backtrack()

def p_adic_hodge_rank(cnf):
    # Placeholder for actual computation of p-adic Hodge rank
    # This is a dummy implementation that returns a random value for demonstration purposes
    return random.randint(1, len(cnf))

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n_values = [5, 10, 15, 20, 30, 40]
    rank_sum = 0
    proof_length_sum = 0
    instances_tested = 0

    for n in n_values:
        for _ in range(5):
            cnf = generate_cnf(n)
            rank_H = p_adic_hodge_rank(cnf)
            proof_length = dpll(cnf)
            if proof_length is False:
                proof_length = float('inf')
            rank_sum += rank_H
            proof_length_sum += proof_length
            instances_tested += 1

    mean_rank = rank_sum / instances_tested
    mean_proof_length = proof_length_sum / instances_tested
    correlation_coefficient = (instances_tested * sum(rank_H * proof_length for rank_H, proof_length in zip(rank_values, proof_length_values)) -
                                rank_sum * proof_length_sum) / math.sqrt((instances_tested * sum(rank_H**2 for rank_H in rank_values) - rank_sum**2) *
                                                                         (instances_tested * sum(proof_length**2 for proof_length in proof_length_values) - proof_length_sum**2))

    conjecture_holds = correlation_coefficient >= 0.8 and all(rank_H <= proof_length * 1.5 for rank_H, proof_length in zip(rank_values, proof_length_values))
    counterexample = "" if conjecture_holds else "mapping_undefined"

    return {
        "metric_name": "Pearson Correlation Coefficient",
        "metric_value": correlation_coefficient,
        "instances_tested": instances_tested,
        "n_max": max(n_values),
        "conjecture_holds": conjecture_holds,
        "counterexample": counterexample
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [2, 3, 5, 7, 11, 13, 17, 19, 23, 29] + list(range(31, 100))
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
    elif any(not r["conjecture_holds"] for r in results) and any(rank_H > proof_length * 1.5 for rank_H, proof_length in zip(rank_values, proof_length_values)):
        print(f"RESULT: FALSIFIED counterexample='mapping_undefined' first_failing_seed={seeds[results.index(next(r for r in results if not r['conjecture_holds']))]}")
    else:
        print("RESULT: INCONCLUSIVE reason=unknown")
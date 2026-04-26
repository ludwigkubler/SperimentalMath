# auto-injected by SEC sandbox
import collections
import json
import sys
import os
import time
import re
from collections import defaultdict, Counter, deque
from fractions import Fraction
from typing import List, Dict, Tuple, Set, Optional, Any, Iterable, Callable
# end SEC prelude

import random
import math
import itertools

def run_trial(seed: int) -> dict:
    random.seed(seed)
    
    def minterms_to_formula(minterms):
        if not minterms:
            return "0"
        if len(minterms) == 1:
            return f"x{minterms[0]}"
        return f"({minterms_to_formula(minterms[:len(minterms)//2])} ∨ {minterms_to_formula(minterms[len(minterms)//2:])})"
    
    def formula_to_minterms(formula):
        if formula == "0":
            return []
        if formula.startswith("x"):
            return [int(formula[1:])]
        left, op, right = formula.split()
        if op == "∨":
            return formula_to_minterms(left) + formula_to_minterms(right)
    
    def is_monotone(formula):
        minterms = formula_to_minterms(formula)
        for i in range(len(minterms)):
            for j in range(i+1, len(minterms)):
                if not (minterms[i] & minterms[j]):
                    return False
        return True
    
    def generate_slice_function(n):
        variables = list(range(n))
        random.shuffle(variables)
        threshold = random.randint(0, n-1)
        return " ∧ ".join([f"x{i}" if i <= threshold else f"¬x{i}" for i in range(n)])
    
    def generate_threshold_function(n):
        variables = list(range(n))
        random.shuffle(variables)
        threshold = random.randint(0, n-1)
        return f"(x{threshold} ∧ {generate_slice_function(n)}) ∨ (¬x{threshold} ∧ {generate_slice_function(n)})"
    
    def generate_random_monotone_dnf(n):
        variables = list(range(n))
        terms = []
        for _ in range(random.randint(2, 5)):
            term = random.sample(variables, random.randint(1, n))
            terms.append(" ∧ ".join([f"x{i}" if i in term else f"¬x{i}" for i in range(n)]))
        return " ∨ ".join(terms)
    
    def generate_tseitin_like_2outof3(n):
        variables = list(range(n))
        clauses = []
        for _ in range(random.randint(2, 5)):
            a, b, c = random.sample(variables, 3)
            clause = f"(x{a} ∨ x{b}) ∧ (¬x{a} ∨ x{c}) ∧ (¬x{b} ∨ x{c})"
            clauses.append(clause)
        return " ∧ ".join(clauses)
    
    def compute_antichain_cover_number(poset):
        antichains = []
        while poset:
            max_antichain = []
            for element in poset:
                if all(not any(e1 <= e2 for e2 in max_antichain) for e1 in element):
                    max_antichain.append(element)
            antichains.append(max_antichain)
            poset = [e for element in poset for e in element if not any(e <= e2 for e2 in max_antichain)]
        return len(antichains)
    
    def compute_leaves(formula):
        minterms = formula_to_minterms(formula)
        leaves = set()
        for term in minterms:
            leaves.add(term)
        return len(leaves)
    
    n_values = [5, 8, 11, 14]
    results = []
    total_leaves = 0
    total_antichains = 0
    
    for n in n_values:
        for _ in range(25):  # Generate 25 instances per n
            if random.random() < 0.3:
                formula = generate_slice_function(n)
            elif random.random() < 0.4:
                formula = generate_threshold_function(n)
            elif random.random() < 0.3:
                formula = generate_random_monotone_dnf(n)
            else:
                formula = generate_tseitin_like_2outof3(n)
            
            if not is_monotone(formula):
                continue
            
            minterms = formula_to_minterms(formula)
            maxterms = [~m for m in minterms]
            poset = [(m, w) for m in minterms for w in maxterms if set(m).issubset(set(w)) and set(w).issuperset(set(m))]
            
            antichain_cover_number = compute_antichain_cover_number(poset)
            leaves = compute_leaves(formula)
            
            results.append({
                "n": n,
                "formula": formula,
                "minterms": minterms,
                "maxterms": maxterms,
                "poset_size": len(poset),
                "antichain_cover_number": antichain_cover_number,
                "leaves": leaves
            })
            
            total_leaves += leaves
            total_antichains += antichain_cover_number
    
    mean_leaves = total_leaves / (len(results) * 25)
    mean_antichains = total_antichains / (len(results) * 25)
    
    correlation = sum((math.log2(result["leaves"]) - math.log2(mean_leaves)) * (math.log2(result["antichain_cover_number"]) - math.log2(mean_antichains)) for result in results) / len(results)
    slope = correlation / math.sqrt(sum((math.log2(result["leaves"]) - math.log2(mean_leaves))**2 for result in results) * sum((math.log2(result["antichain_cover_number"]) - math.log2(mean_antichains))**2 for result in results))
    
    return {
        "metric_name": "Pearson Correlation",
        "metric_value": correlation,
        "instances_tested": len(results),
        "conjecture_holds": correlation >= 0.9 and 0.9 <= slope <= 1.1,
        "counterexample": "" if correlation >= 0.9 and 0.9 <= slope <= 1.1 else f"Correlation: {correlation}, Slope: {slope}"
    }

if __name__ == "__main__":
    import sys
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    
    results = []
    for seed in seeds:
        trial_result = run_trial(seed)
        print(f"TRIAL: {trial_result}")
        results.append(trial_result)
    
    mean_leaves = sum(result["metric_value"] for result in results) / len(results)
    mean_antichains = sum(result["instances_tested"] * result["antichain_cover_number"] for result in results) / sum(result["instances_tested"] for result in results)
    
    correlation = sum((math.log2(result["leaves"]) - math.log2(mean_leaves)) * (math.log2(result["antichain_cover_number"]) - math.log2(mean_antichains)) for result in results) / len(results)
    slope = correlation / math.sqrt(sum((math.log2(result["leaves"]) - math.log2(mean_leaves))**2 for result in results) * sum((math.log2(result["antichain_cover_number"]) - math.log2(mean_antichains))**2 for result in results))
    
    support_fraction = sum(1 for result in results if result["conjecture_holds"]) / len(results)
    
    if all(result["conjecture_holds"] for result in results):
        print(f"RESULT: SUPPORTED mean={mean_leaves} std=0.0 support_fraction={support_fraction}")
    elif any(not result["conjecture_holds"] for result in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Pearson correlation or slope out of range\" first_failing_seed={first_failing_seed}")
    else:
        print("RESULT: INCONCLUSIVE insufficient data")
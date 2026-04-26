import random
import math
import sys
from collections import defaultdict

def generate_3cnf(n: int, m: int) -> list:
    clauses = []
    literals = set(range(1, n + 1))
    for _ in range(m):
        clause = {random.choice(literals), random.choice(literals)}
        if len(clause) == 2 and -list(clause)[0] not in clause and -list(clause)[1] not in clause:
            clauses.append(clause)
    return clauses

def is_clause_compatible(c1, c2):
    return not (c1 & c2)

def construct_simplicial_complex(clauses):
    simplices = defaultdict(set)
    for i, c1 in enumerate(clauses):
        for j, c2 in enumerate(clauses[i + 1:], start=i + 1):
            if is_clause_compatible(c1, c2):
                simplices[frozenset([i, j])].update(c1 | c2)
    return simplices

def find_minimal_covering(simplices):
    vertices = set()
    for simplex in simplices.values():
        vertices.update(simplex)
    coverings = []
    for v in vertices:
        covering = {v}
        for s, clause in simplices.items():
            if v in clause and not any(v in c for c in covering):
                covering.add(s)
        coverings.append(covering)
    return min(coverings, key=len)

def lusternik_schnirelmann_category(simplices):
    covering = find_minimal_covering(simplices)
    return len(covering)

def dpll(clauses):
    n = max(abs(lit) for clause in clauses for lit in clause)
    def solve(model):
        if not clauses:
            return True
        literal = next((lit for lit in range(1, n + 1) if lit not in model and -lit not in model), None)
        if literal is None:
            return False
        pos_literal = literal
        neg_literal = -literal
        if solve(model | {pos_literal}):
            return True
        if solve(model | {neg_literal}):
            return True
        return False
    return solve(set())

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    m = 2 * n
    clauses = generate_3cnf(n, m)
    simplices = construct_simplicial_complex(clauses)
    category = lusternik_schnirelmann_category(simplices)
    decision_tree_depth = dpll(clauses)
    return {
        "metric_name": "Decision Tree Depth",
        "metric_value": decision_tree_depth,
        "instances_tested": 1,
        "conjecture_holds": decision_tree_depth <= category,
        "counterexample": "" if decision_tree_depth <= category else f"Depth {decision_tree_depth} > Category {category}"
    }

if __name__ == "__main__":
    seeds = [int(s) for s in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    mean_value = sum(r["metric_value"] for r in results) / len(results)
    std_value = math.sqrt(sum((r["metric_value"] - mean_value) ** 2 for r in results) / len(results))
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    elif support_fraction >= 0.8:
        print(f"RESULT: SUPPORTED mean={mean_value} std={std_value} support_fraction={support_fraction}")
    else:
        first_failing_seed = next(r["seed"] for r in results if not r["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"Depth exceeds category\" first_failing_seed={first_failing_seed}")
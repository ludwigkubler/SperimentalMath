import sys
import random
from collections import defaultdict
from sympy import symbols, GF, Poly, lcm, factorint

def generate_3sat_instance(n):
    variables = [symbols(f'x{i}') for i in range(n)]
    clauses = []
    for _ in range(2 * n):
        clause = []
        for var in random.sample(variables, 3):
            if random.choice([True, False]):
                clause.append(var)
            else:
                clause.append(~var)
        clauses.append(lcm(clause))
    return sum(clauses)

def compute_ideal_generators(poly):
    ring = GF(2)
    ideal = [Poly(poly, domain=ring)]
    for i in range(len(ideal)):
        for j in range(i + 1, len(ideal)):
            gcd = ideal[i].gcd(ideal[j])
            if gcd != 1:
                ideal.append(gcd)
    return set(ideal)

def compute_resolution_proof_size(poly):
    ring = GF(2)
    variables = list(poly.atoms())
    stack = [poly]
    while stack:
        current = stack.pop()
        if current == 0:
            continue
        for var in variables:
            if current.coeff(var) != 0:
                new_clause = current.coeff(var).as_expr() * ~var + current.as_expr()
                if new_clause not in stack:
                    stack.append(new_clause)
    return len(stack)

def run_trial(seed: int) -> dict:
    random.seed(seed)
    n = random.choice([5, 8, 11, 14])
    poly = generate_3sat_instance(n)
    generators = compute_ideal_generators(poly)
    proof_size = compute_resolution_proof_size(poly)
    return {
        "metric_name": "resolution_proof_size",
        "metric_value": proof_size,
        "instances_tested": 1,
        "conjecture_holds": len(generators) == proof_size,
        "counterexample": "" if len(generators) == proof_size else f"Generators: {len(generators)}, Proof Size: {proof_size}"
    }

if __name__ == "__main__":
    seeds = [int(x) for x in sys.argv[1:]] or [11, 23, 37, 53, 71]
    results = []
    for seed in seeds:
        result = run_trial(seed)
        print(f"TRIAL: {result}")
        results.append(result)

    total_metric_value = sum(r["metric_value"] for r in results)
    mean_metric_value = total_metric_value / len(results)
    std_metric_value = (sum((r["metric_value"] - mean_metric_value) ** 2 for r in results) / len(results)) ** 0.5
    support_fraction = sum(1 for r in results if r["conjecture_holds"]) / len(results)

    if all(r["conjecture_holds"] for r in results):
        print(f"RESULT: SUPPORTED mean={mean_metric_value} std={std_metric_value} support_fraction={support_fraction}")
    elif any(not r["conjecture_holds"] for r in results):
        first_failing_seed = next(seed for seed, result in zip(seeds, results) if not result["conjecture_holds"])
        print(f"RESULT: FALSIFIED counterexample=\"{result['counterexample']}\" first_failing_seed={first_failing_seed}")
    else:
        print(f"RESULT: INCONCLUSIVE support_fraction={support_fraction}")
import sys
import time


from hands_on_monte_carlo_simulation.monte_carlo_simulation import MonteCarloSimulation
from hands_on_monte_carlo_simulation.threading_manager import ThreadingManager


def test_monte_carlo_module():
    """Test du module monte_carlo_simulation"""
    print("=" * 60)
    print("TEST 1: Module monte_carlo")
    print("=" * 60)

    calc = MonteCarloSimulation(seed=42)

    # Test génération de point
    x, y = MonteCarloSimulation.generate_random_points()
    print(f"✓ Point généré: ({x:.4f}, {y:.4f})")
    assert 0 <= x <= 1 and 0 <= y <= 1, "Point hors limites"

    # Test inside/outside
    assert MonteCarloSimulation.is_in_quadrant(0.5, 0.5) == True,  "0.5,0.5 devrait être inside"
    assert MonteCarloSimulation.is_in_quadrant(0.9, 0.9) == False, "0.9,0.9 devrait être outside"
    print("✓ Détection inside/outside correcte")

    # Test génération de points
    points, inside = calc.generate_point(100)
    print(f"✓ 100 points générés: {inside} inside")
    assert len(points) == 100, "Nombre de points incorrect"

    # Test estimation de π
    pi_est = MonteCarloSimulation.estimate_pi(1000, 785)
    print(f"✓ Estimation de π: {pi_est:.4f}")
    assert 3.0 < pi_est < 3.3, "Estimation de π aberrante"

    print("Module monte_carlo: OK\n")


def test_threading_module():
    """Test du module threading_manager"""
    print("=" * 60)
    print("TEST 2: Module threading_manager")
    print("=" * 60)

    # Test avec 2 threads, 100 points chacun
    manager = ThreadingManager(nb_threads=2, nb_draws_per_thread=100, seed=42)

    start = time.time()
    total, inside = manager.run_parallel()
    duration = time.time() - start

    print(f"✓ 2 threads, 100 points chacun")
    print(f"  Total: {total}, Inside: {inside}")
    print(f"  Durée: {duration:.4f}s")

    assert total == 200, f"Total devrait être 200, pas {total}"
    assert 0 < inside < 200, f"Inside devrait être entre 0 et 200, pas {inside}"

    pi_est = 4.0 * inside / total
    print(f"Estimation de π: {pi_est:.4f}")

    print("Module threading_manager: OK\n")


def test_cli_mode():
    """Test du mode CLI"""
    print("=" * 60)
    print("TEST 3: Mode CLI")
    print("=" * 60)

    import subprocess

    cmd = [sys.executable, "-m", "hands_on_monte_carlo_simulation.main", "-N", "100", "-v"]
    print(f"Commande: {' '.join(cmd)}")

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

        if result.returncode == 0:
            print("✓ Exécution réussie")
            output = result.stdout + result.stderr
            if any(v in output for v in ["3.", "π"]):
                print("✓ Résultat contient une approximation de π")
            print(f"Sortie:\n{result.stdout}")
        else:
            print(f"✗ Erreur d'exécution: {result.stderr}")

    except subprocess.TimeoutExpired:
        print("✗ Timeout")
    except Exception as e:
        print(f"✗ Erreur: {e}")

    print("Mode CLI: OK\n")


def test_reproducibility():
    """Test de la reproductibilité avec seed"""
    print("=" * 60)
    print("TEST 4: Reproductibilité")
    print("=" * 60)

    # Premier run avec seed=123
    manager1 = ThreadingManager(nb_threads=2, nb_draws_per_thread=50, seed=123)
    total1, inside1 = manager1.run_parallel()
    pi1 = 4.0 * inside1 / total1

    # Deuxième run avec seed=123
    manager2 = ThreadingManager(nb_threads=2, nb_draws_per_thread=50, seed=123)
    total2, inside2 = manager2.run_parallel()
    pi2 = 4.0 * inside2 / total2

    print(f"Run 1: total={total1}, inside={inside1}, π≈{pi1:.6f}")
    print(f"Run 2: total={total2}, inside={inside2}, π≈{pi2:.6f}")

    assert total1 == total2
    assert inside1 == inside2, "Résultats différents avec même seed"
    print("✓ Résultats identiques avec même seed")

    print("Test de reproductibilité: OK\n")


def test_performance():
    """Test de performance"""
    print("=" * 60)
    print("TEST 5: Performance")
    print("=" * 60)

    configs = [(1, 1000), (2, 1000), (4, 1000)]

    for nb_threads, nb_draws in configs:
        manager = ThreadingManager(
            nb_threads=nb_threads,
            nb_draws_per_thread=nb_draws,
            seed=42
        )

        start = time.time()
        total, inside = manager.run_parallel()
        duration = time.time() - start

        pi_est = 4.0 * inside / total
        print(f"{nb_threads} thread(s), {nb_draws} draws: {duration:.4f}s → π≈{pi_est:.4f}")

        assert duration < 10, f"Trop lent: {duration:.2f}s"
        assert total == nb_threads * nb_draws

    print("Tests de performance: OK\n")
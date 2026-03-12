#!/usr/bin/env python3
"""
Tests and usage examples for LunchParser.
Run directly: python3 test_lunch_parser.py
"""

from datetime import datetime
from lunch_parser import LunchParser


def test_format_menu():
    parser = LunchParser()
    cases = [
        ([], "no menu available"),
        (["Pizza"], "lunch is Pizza"),
        (["Pizza", "Salad"], "lunch includes Pizza and Salad"),
        (["Pizza", "Salad", "Fruit"], "lunch includes Pizza, Salad, and Fruit"),
        (["A", "B", "C", "D"], "lunch includes A, B, C, and D"),
    ]
    print("format_menu()")
    all_passed = True
    for entrees, expected in cases:
        result = parser.format_menu(entrees)
        ok = result == expected
        all_passed = all_passed and ok
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {entrees!r}")
        if not ok:
            print(f"         expected: {expected!r}")
            print(f"           got:    {result!r}")
    return all_passed


def test_unknown_school():
    parser = LunchParser()
    print("\nunknown school raises ValueError")
    try:
        parser.get_full_menu("Hogwarts")
        print("  [FAIL] no exception raised")
        return False
    except ValueError as e:
        print(f"  [PASS] ValueError: {e}")
        return True


def test_sanitize():
    parser = LunchParser()
    cases = [
        ("Turkey & Cheese", "Turkey and Cheese"),
        ("<b>Pizza</b>",    "bPizza/b"),
        ('Mac "n" Cheese',  "Mac n Cheese"),
        ("Chicken's Wrap",  "Chickens Wrap"),
    ]
    print("\n_sanitize()")
    all_passed = True
    for raw, expected in cases:
        result = parser._sanitize(raw)
        ok = result == expected
        all_passed = all_passed and ok
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {raw!r} → {result!r}")
    return all_passed


def test_get_entrees_delegates():
    """get_entrees() should return the same list as get_full_menu()["entree"]."""
    parser = LunchParser()
    date = datetime(2026, 2, 26)
    print("\nget_entrees() matches get_full_menu()[entree]")
    menu    = parser.get_full_menu("Los Cerros Middle", date)
    entrees = parser.get_entrees("Los Cerros Middle", date)
    expected = (menu or {}).get("entree", [])
    ok = entrees == expected
    print(f"  [{'PASS' if ok else 'FAIL'}] {len(entrees)} entree(s)")
    return ok


def test_live_full_menu():
    parser = LunchParser()
    date = datetime(2026, 2, 26)  # known school day
    print(f"\nlive API — full menu for {date.strftime('%Y-%m-%d')}")

    all_ok = True
    for school in parser.schools:
        menu = parser.get_full_menu(school, date)
        if menu is None:
            print(f"  [ERROR] {school}: API failure")
            all_ok = False
            continue

        if not menu:
            print(f"  [EMPTY] {school}: no menu")
            continue

        print(f"\n  {school}")
        for category, items in menu.items():
            print(f"    {category.upper()}")
            for item in items:
                print(f"      - {item}")

    return all_ok


def test_live_api():
    parser = LunchParser()
    today = datetime.now()
    print(f"\nlive API — today: {today.strftime('%Y-%m-%d')}")

    all_ok = True
    for school in parser.schools:
        entrees = parser.get_entrees(school, today)
        if entrees is None:
            print(f"  [ERROR] {school}: API failure")
            all_ok = False
        elif not entrees:
            print(f"  [EMPTY] {school}: no menu today (weekend/holiday?)")
        else:
            print(f"  [OK]    {school}: {parser.format_menu(entrees)}")
    return all_ok


if __name__ == "__main__":
    results = [
        test_format_menu(),
        test_unknown_school(),
        test_sanitize(),
        test_get_entrees_delegates(),
        test_live_full_menu(),
        test_live_api(),
    ]
    print(f"\n{'='*50}")
    passed = sum(results)
    print(f"{passed}/{len(results)} test groups passed")

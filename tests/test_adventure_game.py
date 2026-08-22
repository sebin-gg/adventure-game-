"""Smoke + regression tests for adventure_game."""

import adventure_game as ag


def test_classes_have_unique_inventories():
    # Regression: STARTING_INVENTORY.copy() used to live in the default arg,
    # so every instance without an explicit inventory shared ONE dict.
    a = ag.Warrior("a")
    b = ag.Warrior("b")
    assert a.inventory is not b.inventory
    a.inventory["Potion"] = 99
    assert b.inventory.get("Potion", 0) != 99


def test_default_inventory_matches_starting():
    w = ag.Warrior("w")
    m = ag.Mage("m")
    r = ag.Rogue("r")
    assert w.inventory == ag.STARTING_INVENTORY
    assert m.inventory == ag.STARTING_INVENTORY
    assert r.inventory == ag.STARTING_INVENTORY


def test_class_names():
    assert ag.Warrior("x").class_name == "Warrior"
    assert ag.Mage("x").class_name == "Mage"
    assert ag.Rogue("x").class_name == "Rogue"

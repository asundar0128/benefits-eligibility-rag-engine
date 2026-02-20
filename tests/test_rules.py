from app.tier_rules import apply_tier_limits

def test_limits_base():
    items = [{"i": i} for i in range(100)]
    assert len(apply_tier_limits("base", items, "benefits")) == 4

def test_limits_gold():
    items = [{"i": i} for i in range(100)]
    assert len(apply_tier_limits("gold", items, "benefits")) == 20

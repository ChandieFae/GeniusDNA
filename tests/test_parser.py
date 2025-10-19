from ai.protocols.longevity_optimizer import generate_protocol_from_dna

def test_generate_protocol():
    test_data = """rs1799853\t10\t96702047\tCC
rs1801133\t1\t11796321\tCT
rs731236\t12\t48230721\tTT
rs4994\t8\t116786572\tAA"""

    result = generate_protocol_from_dna(test_data)

    assert "detox" in result
    assert "methylation" in result
    assert "vitamin_d" in result
    assert "metabolism" in result

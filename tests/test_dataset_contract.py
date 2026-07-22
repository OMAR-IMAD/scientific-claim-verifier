from src.data.audit_dataset import LABEL_MAPPING, REQUIRED_COLUMNS, VALID_LABELS


def test_label_mapping_is_complete() -> None:
    assert set(LABEL_MAPPING) == VALID_LABELS
    assert LABEL_MAPPING[0] == "entailment"
    assert LABEL_MAPPING[1] == "neutral"
    assert LABEL_MAPPING[2] == "contradiction"


def test_required_columns() -> None:
    assert {"premise", "hypothesis", "label"}.issubset(REQUIRED_COLUMNS)

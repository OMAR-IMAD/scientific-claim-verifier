from pathlib import Path

import pandas as pd
import pytest

from src.model import summarize_errors


@pytest.fixture
def sample_dataframe() -> pd.DataFrame:
    """Create sample error data for tests."""

    return pd.DataFrame(
        {
            "premise": [
                "Premise one",
                "Premise two",
                "Premise three",
                "Premise four",
                "Premise five",
                "Premise six",
            ],
            "hypothesis": [
                "Hypothesis one",
                "Hypothesis two",
                "Hypothesis three",
                "Hypothesis four",
                "Hypothesis five",
                "Hypothesis six",
            ],
            "genre": [
                "slate",
                "slate",
                "travel",
                "telephone",
                "government",
                "fiction",
            ],
            "label_name": [
                "NEUTRAL",
                "NEUTRAL",
                "NEUTRAL",
                "CONTRADICTION",
                "ENTAILMENT",
                "NEUTRAL",
            ],
            "prediction_name": [
                "CONTRADICTION",
                "CONTRADICTION",
                "CONTRADICTION",
                "NEUTRAL",
                "NEUTRAL",
                "ENTAILMENT",
            ],
        }
    )


def test_read_error_file_returns_dataframe(
    tmp_path: Path,
    sample_dataframe: pd.DataFrame,
) -> None:
    """Test reading a valid error CSV file."""

    file_path = tmp_path / "errors.csv"

    sample_dataframe.to_csv(
        file_path,
        index=False,
    )

    result = summarize_errors.read_error_file(
        file_path
    )

    assert len(result) == 6
    assert set(
        summarize_errors.REQUIRED_COLUMNS
    ).issubset(result.columns)


def test_read_error_file_rejects_missing_file(
    tmp_path: Path,
) -> None:
    """Test error handling for a missing CSV file."""

    missing_file = tmp_path / "missing.csv"

    with pytest.raises(
        FileNotFoundError,
        match="Error file was not found",
    ):
        summarize_errors.read_error_file(
            missing_file
        )


def test_read_error_file_rejects_missing_columns(
    tmp_path: Path,
    sample_dataframe: pd.DataFrame,
) -> None:
    """Test validation of required CSV columns."""

    invalid_dataframe = sample_dataframe.drop(
        columns=["genre"]
    )

    file_path = tmp_path / "invalid.csv"

    invalid_dataframe.to_csv(
        file_path,
        index=False,
    )

    with pytest.raises(
        ValueError,
        match="genre",
    ):
        summarize_errors.read_error_file(
            file_path
        )


def test_create_transition_table(
    sample_dataframe: pd.DataFrame,
) -> None:
    """Test error transition counting."""

    result = (
        summarize_errors.create_transition_table(
            sample_dataframe
        )
    )

    first_row = result.iloc[0]

    assert first_row["label_name"] == "NEUTRAL"
    assert (
        first_row["prediction_name"]
        == "CONTRADICTION"
    )
    assert int(first_row["count"]) == 3
    assert int(result["count"].sum()) == 6


def test_create_genre_table(
    sample_dataframe: pd.DataFrame,
) -> None:
    """Test genre counting for one transition."""

    result = summarize_errors.create_genre_table(
        sample_dataframe,
        "NEUTRAL",
        "CONTRADICTION",
    )

    assert result.iloc[0]["genre"] == "slate"
    assert int(result.iloc[0]["count"]) == 2

    genre_counts = dict(
        zip(
            result["genre"],
            result["count"],
        )
    )

    assert int(genre_counts["travel"]) == 1


def test_clean_text_removes_extra_whitespace() -> None:
    """Test conversion to one-line clean text."""

    result = summarize_errors.clean_text(
        "  This   is\n a   test.  "
    )

    assert result == "This is a test."


def test_create_dataset_summary(
    sample_dataframe: pd.DataFrame,
) -> None:
    """Test generation of a dataset summary."""

    result = (
        summarize_errors.create_dataset_summary(
            "validation_test",
            sample_dataframe,
        )
    )

    report_text = "\n".join(result)

    assert "## validation_test" in report_text
    assert (
        "Toplam yanlış tahmin sayısı: `6`"
        in report_text
    )
    assert (
        "`NEUTRAL → CONTRADICTION`"
        in report_text
    )
    assert "| slate | 2 |" in report_text
    assert "### Temsilî Yanlış Tahminler" in (
        report_text
    )


def test_main_creates_markdown_report(
    tmp_path: Path,
    sample_dataframe: pd.DataFrame,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Test complete automatic report generation."""

    error_directory = tmp_path / "error_analysis"
    error_directory.mkdir()

    matched_file = (
        error_directory
        / "matched.csv"
    )
    mismatched_file = (
        error_directory
        / "mismatched.csv"
    )
    output_file = (
        error_directory
        / "summary.md"
    )

    sample_dataframe.to_csv(
        matched_file,
        index=False,
    )
    sample_dataframe.to_csv(
        mismatched_file,
        index=False,
    )

    monkeypatch.setattr(
        summarize_errors,
        "ERROR_DIRECTORY",
        error_directory,
    )
    monkeypatch.setattr(
        summarize_errors,
        "ERROR_FILES",
        {
            "validation_matched": matched_file,
            "validation_mismatched": (
                mismatched_file
            ),
        },
    )
    monkeypatch.setattr(
        summarize_errors,
        "OUTPUT_FILE",
        output_file,
    )

    summarize_errors.main()

    assert output_file.exists()

    report_text = output_file.read_text(
        encoding="utf-8"
    )

    assert "## validation_matched" in report_text
    assert (
        "## validation_mismatched"
        in report_text
    )
    assert (
        "toplam yanlış tahmin sayısı: `12`"
        in report_text
    )
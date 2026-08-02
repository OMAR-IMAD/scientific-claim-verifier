from pathlib import Path

import pandas as pd


ERROR_DIRECTORY = Path("reports/error_analysis")

ERROR_FILES = {
    "validation_matched": (
        ERROR_DIRECTORY
        / "validation_matched_misclassified.csv"
    ),
    "validation_mismatched": (
        ERROR_DIRECTORY
        / "validation_mismatched_misclassified.csv"
    ),
}

OUTPUT_FILE = (
    ERROR_DIRECTORY
    / "automatic_error_summary.md"
)

REQUIRED_COLUMNS = {
    "premise",
    "hypothesis",
    "genre",
    "label_name",
    "prediction_name",
}


def read_error_file(file_path: Path) -> pd.DataFrame:
    """Read and validate a misclassified examples file."""

    if not file_path.exists():
        raise FileNotFoundError(
            f"Error file was not found: {file_path}"
        )

    dataframe = pd.read_csv(file_path)

    missing_columns = (
        REQUIRED_COLUMNS
        - set(dataframe.columns)
    )

    if missing_columns:
        missing_text = ", ".join(
            sorted(missing_columns)
        )
        raise ValueError(
            "Missing required columns: "
            f"{missing_text}"
        )

    return dataframe


def create_transition_table(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    """Count actual-to-predicted error transitions."""

    return (
        dataframe.groupby(
            [
                "label_name",
                "prediction_name",
            ]
        )
        .size()
        .reset_index(name="count")
        .sort_values(
            "count",
            ascending=False,
        )
        .reset_index(drop=True)
    )


def create_genre_table(
    dataframe: pd.DataFrame,
    actual_label: str,
    predicted_label: str,
) -> pd.DataFrame:
    """Count genres for a selected error transition."""

    selected_rows = dataframe[
        (
            dataframe["label_name"]
            == actual_label
        )
        & (
            dataframe["prediction_name"]
            == predicted_label
        )
    ]

    return (
        selected_rows.groupby("genre")
        .size()
        .reset_index(name="count")
        .sort_values(
            "count",
            ascending=False,
        )
        .reset_index(drop=True)
    )


def clean_text(value: object) -> str:
    """Prepare text for a one-line Markdown report."""

    return " ".join(
        str(value).split()
    )


def add_transition_section(
    lines: list[str],
    transition_table: pd.DataFrame,
) -> None:
    """Add all error transitions to the report."""

    lines.extend(
        [
            "### Hata Geçişleri",
            "",
            "| Gerçek Sınıf | Tahmin Edilen Sınıf | Sayı |",
            "|---|---|---:|",
        ]
    )

    for row in transition_table.itertuples(
        index=False
    ):
        lines.append(
            f"| {row.label_name} "
            f"| {row.prediction_name} "
            f"| {row.count} |"
        )

    lines.append("")


def add_genre_section(
    lines: list[str],
    genre_table: pd.DataFrame,
) -> None:
    """Add genre counts for the most common error."""

    lines.extend(
        [
            "### En Sık Hatanın Genre Dağılımı",
            "",
            "| Genre | Sayı |",
            "|---|---:|",
        ]
    )

    for row in genre_table.head(5).itertuples(
        index=False
    ):
        lines.append(
            f"| {row.genre} | {row.count} |"
        )

    lines.append("")


def add_example_section(
    lines: list[str],
    dataframe: pd.DataFrame,
    actual_label: str,
    predicted_label: str,
) -> None:
    """Add representative examples for the top error."""

    examples = dataframe[
        (
            dataframe["label_name"]
            == actual_label
        )
        & (
            dataframe["prediction_name"]
            == predicted_label
        )
    ].head(3)

    lines.extend(
        [
            "### Temsilî Yanlış Tahminler",
            "",
        ]
    )

    for number, row in enumerate(
        examples.itertuples(index=False),
        start=1,
    ):
        lines.extend(
            [
                f"#### Örnek {number}",
                "",
                f"- Genre: `{row.genre}`",
                f"- Gerçek sınıf: `{actual_label}`",
                f"- Tahmin: `{predicted_label}`",
                (
                    "- Premise: "
                    f"{clean_text(row.premise)}"
                ),
                (
                    "- Hypothesis: "
                    f"{clean_text(row.hypothesis)}"
                ),
                "",
            ]
        )


def create_dataset_summary(
    dataset_name: str,
    dataframe: pd.DataFrame,
) -> list[str]:
    """Create the summary for one validation dataset."""

    transition_table = create_transition_table(
        dataframe
    )

    top_error = transition_table.iloc[0]

    actual_label = str(
        top_error["label_name"]
    )
    predicted_label = str(
        top_error["prediction_name"]
    )
    top_error_count = int(
        top_error["count"]
    )

    genre_table = create_genre_table(
        dataframe,
        actual_label,
        predicted_label,
    )

    lines = [
        f"## {dataset_name}",
        "",
        (
            "Toplam yanlış tahmin sayısı: "
            f"`{len(dataframe)}`"
        ),
        "",
        (
            "En sık hata: "
            f"`{actual_label} → "
            f"{predicted_label}`"
        ),
        "",
        (
            "Bu hatanın sayısı: "
            f"`{top_error_count}`"
        ),
        "",
    ]

    add_transition_section(
        lines,
        transition_table,
    )
    add_genre_section(
        lines,
        genre_table,
    )
    add_example_section(
        lines,
        dataframe,
        actual_label,
        predicted_label,
    )

    return lines


def main() -> None:
    """Generate the automatic Markdown error summary."""

    ERROR_DIRECTORY.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_lines = [
        "# Otomatik Model Hata Özeti",
        "",
        (
            "Bu rapor, yanlış tahmin CSV "
            "dosyalarından otomatik olarak "
            "oluşturulmuştur."
        ),
        "",
    ]

    total_errors = 0

    for dataset_name, file_path in (
        ERROR_FILES.items()
    ):
        dataframe = read_error_file(
            file_path
        )

        total_errors += len(dataframe)

        report_lines.extend(
            create_dataset_summary(
                dataset_name,
                dataframe,
            )
        )

    report_lines.extend(
        [
            "## Genel Sonuç",
            "",
            (
                "İki validation veri setindeki "
                "toplam yanlış tahmin sayısı: "
                f"`{total_errors}`"
            ),
            "",
            (
                "Hata dağılımları ve temsilî "
                "örnekler otomatik olarak "
                "raporlanmıştır."
            ),
            "",
        ]
    )

    OUTPUT_FILE.write_text(
        "\n".join(report_lines),
        encoding="utf-8",
    )

    print(
        "Automatic error summary created:"
    )
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()
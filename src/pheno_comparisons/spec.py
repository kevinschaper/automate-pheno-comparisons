"""What the release contains: annotation corpora, term roots, and comparisons."""

from __future__ import annotations

from dataclasses import dataclass, field

GENE_TO_PHENOTYPE = "biolink:GeneToPhenotypicFeatureAssociation"
DISEASE_TO_PHENOTYPE = "biolink:DiseaseToPhenotypicFeatureAssociation"


@dataclass(frozen=True)
class Corpus:
    """An annotation corpus: the KG `has_phenotype` edges whose information
    content scores one comparison's shared ancestors."""

    key: str
    ic_table: str
    ic_file: str  # name of the IC file inside the tarball (historical names)
    categories: list[str] = field(default_factory=list)
    subject_prefixes: list[str] = field(default_factory=list)
    object_prefixes: list[str] = field(default_factory=list)
    description: str = ""


@dataclass(frozen=True)
class Comparison:
    """One all-by-all table: subject terms x object terms, scored with `corpus`."""

    key: str
    prefix: str  # tarball / table name prefix
    subject_root: str
    subject_prefix: str
    object_root: str
    object_prefix: str
    corpus: str
    object_ontology: str  # key into the ontology versions recorded in the log


CORPORA: dict[str, Corpus] = {
    c.key: c
    for c in (
        Corpus(
            key="hp", ic_table="information_content_mondo_hp", ic_file="hpa_ic.tsv",
            categories=[DISEASE_TO_PHENOTYPE], subject_prefixes=["MONDO"], object_prefixes=["HP"],
            description="human diseases (MONDO) -> HP, from the KG's HPO annotation edges",
        ),
        Corpus(
            key="mp", ic_table="information_content_mgi_mp", ic_file="mpa_ic.tsv",
            categories=[GENE_TO_PHENOTYPE], subject_prefixes=["MGI"], object_prefixes=["MP"],
            description="mouse genes (MGI) -> MP",
        ),
        Corpus(
            key="zp", ic_table="information_content_zfin_zp", ic_file="zpa_ic.tsv",
            categories=[GENE_TO_PHENOTYPE], subject_prefixes=["ZFIN"], object_prefixes=["ZP"],
            description="zebrafish genes (ZFIN) -> ZP",
        ),
    )
}

COMPARISONS: dict[str, Comparison] = {
    c.key: c
    for c in (
        Comparison("hp-hp", "HP_vs_HP_semsimian_phenio", "HP:0000118", "HP", "HP:0000118", "HP", "hp", "hp"),
        Comparison("hp-mp", "HP_vs_MP_semsimian_phenio", "HP:0000118", "HP", "MP:0000001", "MP", "mp", "mp"),
        Comparison("hp-zp", "HP_vs_ZP_semsimian_phenio", "HP:0000118", "HP", "ZP:0000000", "ZP", "zp", "zp"),
    )
}

# Pairs are kept when the most informative shared ancestor's IC is strictly above this.
MIN_ANCESTOR_INFORMATION_CONTENT = 1.5

# Provenance table written next to the IC tables.
CORPUS_TABLE = "pheno_comparison_corpora"

import sys
from importlib import import_module
from pathlib import Path

try:
    DocumentConverter = import_module("docling.document_converter").DocumentConverter
except ModuleNotFoundError as exc:
    if exc.name == "docling" or (exc.name and exc.name.startswith("docling.")):
        raise ImportError(
            "Docling est introuvable. Installez-le avec : python -m pip install docling"
        ) from exc
    raise


def convertir_dossier(dossier_source: str, dossier_sortie: str):
    source_path = Path(dossier_source)
    output_path = Path(dossier_sortie)

    if not source_path.is_dir():
        raise FileNotFoundError(f"Le dossier source n'existe pas : {source_path}")

    output_path.mkdir(parents=True, exist_ok=True)

    converter = DocumentConverter()

    extensions_valides = {
        ".pdf", ".docx", ".pptx", ".xlsx", ".html", ".htm",
        ".png", ".jpg", ".jpeg", ".webp", ".csv",
    }

    fichiers = sorted(
        (
            path for path in source_path.rglob("*")
            if path.is_file() and path.suffix.lower() in extensions_valides
        ),
        key=lambda path: str(path.relative_to(source_path)).casefold(),
    )
    print(f"Trouvé {len(fichiers)} fichier(s) compatible(s) à traiter.\n")

    erreurs = 0
    for index, file_path in enumerate(fichiers, 1):
        chemin_relatif = file_path.relative_to(source_path)
        output_file = (output_path / chemin_relatif).with_suffix(".md")
        print(f"[{index}/{len(fichiers)}] Conversion de {chemin_relatif}...")
        try:
            result = converter.convert(file_path)
            markdown_content = result.document.export_to_markdown()
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_text(markdown_content, encoding="utf-8")
            print(f"  -> Succès : {output_file}")

        except Exception as e:
            erreurs += 1
            print(f"  -> Échec pour {chemin_relatif} : {e}", file=sys.stderr)

    print(f"\nConversion terminée : {len(fichiers) - erreurs} succès, {erreurs} échec(s).")
    return 1 if erreurs else 0

if __name__ == "__main__":
    sys.exit(convertir_dossier("inputs", "outputs_markdown"))
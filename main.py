import os
import pathlib
from pathlib import Path

from rdflib import ConjunctiveGraph

if __name__ == '__main__':
    for dir in Path("scraperOutput").iterdir():
        idpKG = ConjunctiveGraph()
        if pathlib.Path.is_dir(dir):
            for file in dir.iterdir():
                if file.suffix == ".nq":
                    idpKG.parse(file, format="nquads")
            idpKG.serialize(destination=os.path.join("scraped-ttl", f"{dir.stem}.ttl"), format="turtle",
                            base="https://bioschemas.org/crawl/v1/")

import json
import os
from pathlib import Path
from bs4 import BeautifulSoup


root = Path(os.path.dirname(__file__)).joinpath("sample-test")


def read_text(path, input_format):
    with path.open(encoding="utf-8") as f:
        content = f.read().strip()
        if input_format == "SPL":
            return content
        else:
            soup = BeautifulSoup(content, "html.parser")
            lines = soup.find_all("a", attrs={"id": True})
            content = "\n".join([ln.string.strip() for ln in lines])
            return content


for testf in ["ROUGE-test.xml", "verify-spl.xml", "verify.xml"]:
    file_path = root.joinpath(testf)
    soup = None
    with file_path.open(encoding="utf-8") as f:
        soup = BeautifulSoup(f.read().strip(), "xml")

    evals = soup.find_all("EVAL")
    data = {}
    for e in evals:
        summary_root = e.find_next("PEER-ROOT").string.strip()
        ref_root = e.find_next("MODEL-ROOT").string.strip()
        input_format = e.find_next("INPUT-FORMAT")["TYPE"]
        summaries = []
        references = []
        for kind in ["PEERS", "MODELS"]:
            node = e.find_next(kind)
            node_type = kind[0]
            node_root = summary_root if node_type == "P" else ref_root
            nodes = node.find_all(node_type)
            for n in nodes:
                name = n.string.strip()
                p = root.joinpath(*node_root.split("/"), name)
                content = read_text(p, input_format)
                if node_type == "P":
                    summaries.append(content)
                else:
                    references.append(content)
        data[e["ID"]] = {
            "summaries": summaries,
            "references": references
        }

    serialized = json.dumps(data, indent=4)
    name, ext = os.path.splitext(testf)
    with open(name + ".json", "wb") as f:
        f.write(serialized.encode("utf-8"))

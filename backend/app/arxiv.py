import sys
from typing import NamedTuple

import requests
from lxml import html, etree


def extract_texts_impl(node: etree._Element, tags: set[str], dest: list[tuple[str, str]]) -> None:
    for i in range(len(node)):
        child = node[i]
        if child.tag in tags:
            dest.append((child.tag, child.text_content().strip().replace("  ", " ")))
            continue
        extract_texts_impl(child, tags, dest)


def extract_texts(node: etree._Element, tags: set[str]) -> tuple[list[str], list[str]]:
    tag_and_texts = []
    extract_texts_impl(node, tags, tag_and_texts)

    ext_tags = [t for t, _ in tag_and_texts]
    texts = [text for _, text in tag_and_texts]

    return ext_tags, texts


class Paper(NamedTuple):
    title: str
    tags: list[str]
    texts: list[str]
    math_exprs: list[str]

    def restore_math_expr(self, text: str) -> list[str]:
        while "[a math expression" in text:
            start = text.find("[a math expression")
            end = text.find("]", start)
            idx = int(text[start + 18:end])
            text = text[:start] + f"${self.math_exprs[idx]}$" + text[end + 1:]
        return text

    def to_dict(self) -> dict:
        return {
            "title": self.title,
            "tags": self.tags,
            "texts": self.texts,
            "math_exprs": self.math_exprs,
        }

    def from_dict(data: dict) -> "Paper":
        return Paper(
            title=data["title"],
            tags=data["tags"],
            texts=data["texts"],
            math_exprs=data["math_exprs"],
        )


def parse_html(html: etree._ElementTree) -> Paper:
    title = html.xpath("//title")[0].text
    math_nodes = html.xpath("//math")
    original_math_exprs = []
    for i, node in enumerate(math_nodes):
        original_math_exprs.append(node.attrib["alttext"])
        tail = node.tail or ""
        item = etree.Element("span")
        item.text = f"[a math expression {i}] {tail}"
        node.getparent().replace(node, item)

    abstract_node = html.xpath("//div[@class = 'ltx_abstract']")
    if len(abstract_node) == 1:
        abstract = "\n\n".join(extract_texts(abstract_node[0], {"p"})[1])
    else:
        abstract = ""

    section_nodes = html.xpath("//section")
    tags = ["p"]
    texts = [abstract]
    for node in section_nodes:
        if list(node.classes) != ["ltx_section"]:
            continue

        tg, tt = extract_texts(node, {"p", "h1", "h2", "h3", "h4", "h5", "h6"})

        tags += tg
        texts += tt

    return Paper(
        title=title,
        tags=tags,
        texts=texts,    
        math_exprs=original_math_exprs
    )


def load_from_arxiv(url: str) -> Paper:
    resp = requests.get(url)
    text = resp.text

    root = html.fromstring(text)
    return parse_html(root)

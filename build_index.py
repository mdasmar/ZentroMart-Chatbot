from langchain_chroma import Chroma
from langchain_huggingface.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document
from langchain_text_splitters import MarkdownHeaderTextSplitter
from pathlib import Path

embed_model="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

def split_metadata(text_file):
    parts=text_file.split("---",2)

    metadata=parts[1]
    markdown=parts[2]

    meta={}
    for line in metadata.splitlines():
        if ":" not in line:
            continue
        key,value=line.split(":",1)
        meta[key.strip()]=value.strip()

    return meta,markdown

def knowledge_doc():
    splitter=MarkdownHeaderTextSplitter(
        headers_to_split_on=[("##", "section")],
        strip_headers=False,
    )
    docs=[]
    for file in sorted(Path("kb").glob("*.md")):
        text=file.read_text(encoding="utf-8")
        metadata,markdown=split_metadata(text)
        for sec in splitter.split_text(markdown):
            heading = sec.metadata.get("section")
            if heading is None:
                continue
            sec_id,sec_title=heading[1:].split("]",1)
            sec_title=sec_title.strip()

            docs.append(
                Document(
                    page_content=sec.page_content,
                    metadata={
                        **metadata,
                        "source_file": file.name,
                        "section_id": sec_id,
                        "section_title": sec_title,
                    },
                )
            )

    return docs

def create_embed():
    return HuggingFaceEmbeddings(model_name=embed_model)

def chroma_index():
    embedding=create_embed()
    docs=knowledge_doc()
    vec_store=Chroma(collection_name="zentromart_kb",
                     persist_directory="chroma_db",
                     embedding_function=embedding)
    doc_ids=[]
    for doc in docs:
        doc_id=doc.metadata['doc_id']
        sec_id=doc.metadata['section_id']

        doc_ids.append(f"{doc_id}::{sec_id}")

    vec_store.add_documents(documents=docs,ids=doc_ids)


if __name__=="__main__":
    chroma_index()
    

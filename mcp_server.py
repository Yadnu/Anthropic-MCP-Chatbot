from mcp.server.fastmcp import FastMCP
from pydantic import Field
mcp = FastMCP("DocumentMCP", log_level="ERROR")


docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}

# TODO: Write a tool to read a doc
@mcp.tool(
    name = "read_doc_contents",
    description = "Read the contents of a document and return it as a string.",
)
def read_documents(
        doc_id: str = Field(description="The id of the document to read.")
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found.")
    return docs[doc_id]

# TODO: Write a tool to edit a doc
@mcp.tool(
    name = "edit_doc_contents",
    description = "Edit the contents of a document and return the updated contents as a string.",
)
def edit_document(
    doc_id: str = Field(description="The id of the document to edit."),
    old_contents: str = Field(description="The text to replace. Must match exactly, including whitespace."),
    new_contents: str = Field(description="The text to replace the old text with."),
):
    if doc_id not in docs:
        raise ValueError(f"Doc with id {doc_id} not found.")
    if old_contents not in docs[doc_id]:
        raise ValueError(f"Old contents not found in doc {doc_id}.")
    updated_contents = docs[doc_id].replace(old_contents, new_contents)
    docs[doc_id] = updated_contents
    return updated_contents
# TODO: Write a resource to return all doc id's
@mcp.resource(
    "docs://documents",
    mime_type="application/json"
)
def list_docs():
    return list(docs.keys())
# TODO: Write a resource to return the contents of a particular doc
@mcp.resource(
    "docs://documents/{doc_id}",
    mime_type="text/plain"
)
def get_doc_contents(doc_id: str):
    if(doc_id not in docs):
        raise ValueError(f"Doc with id {doc_id} not found.")
    return docs[doc_id]
# TODO: Write a prompt to rewrite a doc in markdown format
# TODO: Write a prompt to summarize a doc


if __name__ == "__main__":
    mcp.run(transport="stdio")

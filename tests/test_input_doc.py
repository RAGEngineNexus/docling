from io import BytesIO
from pathlib import Path

from docling.backend.pypdfium2_backend import PyPdfiumDocumentBackend
from docling.datamodel.base_models import DocumentStream, InputFormat
from docling.datamodel.document import InputDocument, _DocumentConversionInput


def test_in_doc_from_valid_path():

    test_doc_path = Path("./tests/data/2206.01062.pdf")
    doc = _make_input_doc(test_doc_path)
    assert doc.valid == True


def test_in_doc_from_invalid_path():
    test_doc_path = Path("./tests/does/not/exist.pdf")

    doc = _make_input_doc(test_doc_path)

    assert doc.valid == False


def test_in_doc_from_valid_buf():

    buf = BytesIO(Path("./tests/data/2206.01062.pdf").open("rb").read())
    stream = DocumentStream(name="my_doc.pdf", stream=buf)

    doc = _make_input_doc_from_stream(stream)
    assert doc.valid == True


def test_in_doc_from_invalid_buf():

    buf = BytesIO(b"")
    stream = DocumentStream(name="my_doc.pdf", stream=buf)

    doc = _make_input_doc_from_stream(stream)
    assert doc.valid == False


def test_guess_format():
    """Test docling.datamodel.document._DocumentConversionInput.__guess_format"""
    dci = _DocumentConversionInput(path_or_stream_iterator=[])

    # Valid PDF
    buf = BytesIO(Path("./tests/data/2206.01062.pdf").open("rb").read())
    stream = DocumentStream(name="my_doc.pdf", stream=buf)
    assert dci._guess_format(stream) == InputFormat.PDF
    doc_path = Path("./tests/data/2206.01062.pdf")
    assert dci._guess_format(doc_path) == InputFormat.PDF

    # Valid MS Doc
    buf = BytesIO(Path("./tests/data/docx/lorem_ipsum.docx").open("rb").read())
    stream = DocumentStream(name="lorem_ipsum.docx", stream=buf)
    assert dci._guess_format(stream) == InputFormat.DOCX
    doc_path = Path("./tests/data/docx/lorem_ipsum.docx")
    assert dci._guess_format(doc_path) == InputFormat.DOCX

    # Valid XML USPTO patent
    buf = BytesIO(Path("./tests/data/uspto/ipa20110039701.xml").open("rb").read())
    stream = DocumentStream(name="ipa20110039701.xml", stream=buf)
    assert dci._guess_format(stream) == InputFormat.XML_USPTO
    doc_path = Path("./tests/data/uspto/ipa20110039701.xml")
    assert dci._guess_format(doc_path) == InputFormat.XML_USPTO

    buf = BytesIO(Path("./tests/data/uspto/pftaps057006474.txt").open("rb").read())
    stream = DocumentStream(name="pftaps057006474.txt", stream=buf)
    assert dci._guess_format(stream) == InputFormat.XML_USPTO
    doc_path = Path("./tests/data/uspto/pftaps057006474.txt")
    assert dci._guess_format(doc_path) == InputFormat.XML_USPTO

    # Invalid XML USPTO patent
    stream = DocumentStream(name="pftaps057006474.txt", stream=BytesIO(b"xyz"))
    assert dci._guess_format(stream) == None


def _make_input_doc(path):
    in_doc = InputDocument(
        path_or_stream=path,
        format=InputFormat.PDF,
        backend=PyPdfiumDocumentBackend,
    )
    return in_doc


def _make_input_doc_from_stream(doc_stream):
    in_doc = InputDocument(
        path_or_stream=doc_stream.stream,
        format=InputFormat.PDF,
        filename=doc_stream.name,
        backend=PyPdfiumDocumentBackend,
    )
    return in_doc

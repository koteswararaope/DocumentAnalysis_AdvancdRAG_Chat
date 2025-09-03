from fastapi import FastAPI,UploadFile,File,Form,HTTPException,Request
from fastapi.responses import JSONResponse,HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
from typing import List,Optional,Any,Dict

from src.doc_analyzer.dataanalaysis import DocumentAnalyzer
from src.doccompare.document_compare import DocumentComparatorusingLLM
from src.documentchat.retrieval import ConversationalRAG
from src.documentingestion.dataingestion import FaissManager, Dochandler, DocumentComprator, ChatIngestor

FAISS_BASE = os.getenv("FAISS_BASE", "faiss_index")
UPLOAD_BASE = os.getenv("UPLOAD_BASE", "data")


app = FastAPI(title= "Document Portal API", version= "0.1")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"),name="static")
templates= Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def serve_ui(request:Request):
    return templates.TemplateResponse("index.html",{"request":request})

@app.get("/health")
def health() ->dict[str, str]:
    return{"status":"ok","service":"document-portal"}
class FastAPIFileAdapter:
    """Adapt FastAPI UploadFile -> .name + .getbuffer() API"""
    def __init__(self, uf: UploadFile):
        self._uf = uf
        self.name = uf.filename
    def getbuffer(self) -> bytes:
        self._uf.file.seek(0)
        return self._uf.file.read()

def _read_pdf_via_handler(handler: Dochandler, path: str) -> str:
    if hasattr(handler, "read_pdf"):
        return handler.read_pdf(path)  
    if hasattr(handler, "read_"):
        return handler.read_(path)  
    raise RuntimeError("DocHandler has neither read_pdf nor read_ method.")

@app.post("/analyze")
async def analyze_documents(file:UploadFile=File(...)):
    try:
        dh = Dochandler()
        saved_path = dh.save_pdf(FastAPIFileAdapter(file))
        text = _read_pdf_via_handler(dh, saved_path)
        analyzer=DocumentAnalyzer()
        result = analyzer.analyze_document(text)
        return JSONResponse(content=result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {e}")

@app.post("/compare")
async def compare_documents(reference:UploadFile =File(...), actual:UploadFile=File(...)):
    try:
        dc = DocumentComprator()
        ref_path, act_path = dc.save_uploaded_files(FastAPIFileAdapter(reference), FastAPIFileAdapter(actual))
        _ = ref_path, act_path
        combined_text = dc.combine_documents()
        comp = DocumentComprator()
        df = comp.compare_documents(combined_text)
        return {"rows": df.to_dict(orient="records"), "session_id": dc.session_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Comparison failed: {e}")

@app.post("/chat/index")
async def chat_build_index(
        files: List[UploadFile] = File(...),
        session_id: Optional[str] = Form(None),
        use_session_dirs: bool = Form(True),
        chunk_size: int = Form(1000),
        chunk_overlap: int = Form(200),
        k: int = Form(5),
    ) -> Any:
    try:
        wrapped = [FastAPIFileAdapter(f) for f in files]
        ci = ChatIngestor(
            temp_base=UPLOAD_BASE,
            faiss_base=FAISS_BASE,
            use_session_dirs=use_session_dirs,
            session_id=session_id or None,
        )
        ci.built_retriver(wrapped, chunk_size=chunk_size, chunk_overlap=chunk_overlap, k=k)
        return {"session_id": ci.session_id, "k": k, "use_session_dirs": use_session_dirs}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Indexing failed: {e}")

@app.post("/chat/query")
async def chat(
        question: str = Form(...),
        session_id: Optional[str] = Form(None),
        use_session_dirs: bool = Form(True),
        k: int = Form(5),
    ) -> Any:
    try:
        if use_session_dirs and not session_id:
            raise HTTPException(status_code=400, detail="session_id is required when use_session_dirs=True")

        # Prepare FAISS index path
        index_dir = os.path.join(FAISS_BASE, session_id) if use_session_dirs else FAISS_BASE  # type: ignore
        if not os.path.isdir(index_dir):
            raise HTTPException(status_code=404, detail=f"FAISS index not found at: {index_dir}")

        # Initialize LCEL-style RAG pipeline
        rag = ConversationalRAG(session_id=session_id) #type: ignore
        rag.load_retriever_faiss(index_dir)

        # Optional: For now we pass empty chat history
        response = rag.invoke(question, chat_history=[])

        return {
            "answer": response,
            "session_id": session_id,
            "k": k,
            "engine": "LCEL-RAG"
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Query failed: {e}")
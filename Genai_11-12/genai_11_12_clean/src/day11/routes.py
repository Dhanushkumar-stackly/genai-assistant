import time
from datetime import datetime,timezone
from uuid import uuid4
from fastapi import APIRouter,Depends,HTTPException
from .config import Settings,get_settings
from .database import get_db
from .db_models import RetrievedSourceLog
from .logging_service import log_request
from .metrics import request_metrics
from .models import AskRequest,AskResponse,DocumentResponse,IngestRequest,IngestResponse,Source
from .rag import RAGService,get_rag_service
router=APIRouter()
@router.get('/',response_model=dict[str,str])
def root(settings:Settings=Depends(get_settings)): return {'message':'GenAI RAG API is running','service':settings.app_name,'version':settings.app_version,'environment':settings.environment,'status':'running'}
@router.post('/ingest',response_model=IngestResponse)
async def ingest(request:IngestRequest,rag:RAGService=Depends(get_rag_service),db=Depends(get_db)):
 rid=str(uuid4()); st=datetime.now(timezone.utc); t=time.perf_counter(); result=rag.ingest_document(request.title,request.content); lat=(time.perf_counter()-t)*1000; request_metrics.record_success(lat); await log_request(db,request_id=rid,endpoint='/ingest',start_time=st,total_latency_ms=lat,outcome='success'); return IngestResponse(request_id=rid,**result)
@router.post('/ask',response_model=AskResponse)
async def ask(request:AskRequest,rag:RAGService=Depends(get_rag_service),db=Depends(get_db)):
 rid=str(uuid4()); st=datetime.now(timezone.utc); t=time.perf_counter(); result=rag.ask(request.question,request.filters); lat=(time.perf_counter()-t)*1000; request_metrics.record_success(lat); await log_request(db,request_id=rid,endpoint='/ask',start_time=st,total_latency_ms=lat,outcome='success')
 for source in result['sources']:
  db.add(RetrievedSourceLog(request_id=rid,source_id=source['document_id'],score=1.0,created_at=datetime.now(timezone.utc)))
 await db.commit()
 return AskResponse(request_id=rid,answer=result['answer'],sources=[Source(**s) for s in result['sources']])
@router.get('/documents/{document_id}',response_model=DocumentResponse)
async def get_document(document_id:str,rag:RAGService=Depends(get_rag_service),db=Depends(get_db)):
 rid=str(uuid4()); st=datetime.now(timezone.utc); t=time.perf_counter(); doc=rag.get_document(document_id); lat=(time.perf_counter()-t)*1000
 if doc is None:
  request_metrics.record_failure(lat); await log_request(db,request_id=rid,endpoint='/documents/{document_id}',start_time=st,total_latency_ms=lat,outcome='not_found',error_category='document_not_found'); raise HTTPException(404,'Document not found')
 request_metrics.record_success(lat); await log_request(db,request_id=rid,endpoint='/documents/{document_id}',start_time=st,total_latency_ms=lat,outcome='success'); return DocumentResponse(request_id=rid,document_id=doc['document_id'],title=doc['title'],chunk_count=len(doc['chunks']),status=doc['status'])

from uuid import uuid4
class RAGService:
 def __init__(self): self.documents={}
 def startup(self): return None
 def shutdown(self): return None
 def ingest_document(self,title,content):
  document_id=str(uuid4()); chunks=[c.strip() for c in content.split('\n\n') if c.strip()] or [content.strip()]
  self.documents[document_id]={'document_id':document_id,'title':title,'content':content,'chunks':chunks,'status':'processed'}
  return {'document_id':document_id,'chunk_count':len(chunks),'status':'processed'}
 def get_document(self,document_id): return self.documents.get(document_id)
 def ask(self,question,filters=None):
  if not self.documents:return {'answer':'No documents are available.','sources':[]}
  d=next(iter(self.documents.values())); return {'answer':f"Answer based on document: {d['title']}",'sources':[{'document_id':d['document_id'],'title':d['title']}]}
rag_service=RAGService()
def get_rag_service(): return rag_service

from dataclasses import dataclass
@dataclass
class RequestMetrics:
 total_requests:int=0; successful_requests:int=0; failed_requests:int=0; total_latency_ms:float=0.0
 @property
 def average_latency_ms(self): return 0.0 if self.total_requests==0 else self.total_latency_ms/self.total_requests
 def record_success(self,latency_ms): self.total_requests+=1; self.successful_requests+=1; self.total_latency_ms+=latency_ms
 def record_failure(self,latency_ms): self.total_requests+=1; self.failed_requests+=1; self.total_latency_ms+=latency_ms
 def get_metrics(self): return {'total_requests':self.total_requests,'successful_requests':self.successful_requests,'failed_requests':self.failed_requests,'total_latency_ms':self.total_latency_ms,'average_latency_ms':self.average_latency_ms}
request_metrics=RequestMetrics()

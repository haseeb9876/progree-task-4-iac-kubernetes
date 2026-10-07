"""Apply HTTP load, observe actual HPA expansion and cooldown, then remove load."""
import datetime
import json
import time
from cluster import ROOT, NAMESPACE, k, read
name = 'task4-hpa-load'
record = {'verified_at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'samples':[]}

def sample(phase):
    hpa = read('-n',NAMESPACE,'get','hpa','backend')
    status = hpa.get('status',{})
    result = {'phase':phase,'time_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'current':status.get('currentReplicas',0),'desired':status.get('desiredReplicas',0),'metrics':status.get('currentMetrics',[])}
    record['samples'].append(result)
    print(json.dumps(result),flush=True)
    return result

deadline = time.monotonic() + 420
while True:
    baseline = sample('baseline')
    if baseline['current'] == 2 and baseline['desired'] == 2:
        break
    if time.monotonic() >= deadline:
        raise AssertionError('Idle HPA did not settle to two replicas')
    time.sleep(15)
# HTTP traffic targets the existing real health endpoint; no synthetic CPU route.
js = "const http=require('http');const end=Date.now()+360000;function loop(){if(Date.now()>end)return;http.get('http://backend:5000/health/live',r=>{r.resume();r.on('end',()=>setImmediate(loop));}).on('error',()=>setTimeout(loop,50));}for(let i=0;i<24;i++)loop();"
job = {'apiVersion':'batch/v1','kind':'Job','metadata':{'name':name,'namespace':NAMESPACE},'spec':{'backoffLimit':0,'activeDeadlineSeconds':420,'ttlSecondsAfterFinished':600,'template':{'spec':{'restartPolicy':'Never','automountServiceAccountToken':False,'containers':[{'name':'load','image':'progree-task4-backend:local','imagePullPolicy':'Never','command':['node','-e',js],'resources':{'requests':{'cpu':'50m','memory':'32Mi'},'limits':{'cpu':'300m','memory':'128Mi'}}}]}}}}
k('apply','-f','-',input=json.dumps(job))
try:
    deadline = time.monotonic()+360
    while time.monotonic()<deadline:
        time.sleep(15)
        s=sample('load')
        if s['current']>2 and s['desired']>2:
            deployment=read('-n',NAMESPACE,'get','deployment','backend')
            if deployment.get('status',{}).get('readyReplicas',0) <= 2:
                continue
            record['scale_up']='passed'
            break
    else: raise AssertionError('HPA did not scale above two under load')
finally:
    k('-n',NAMESPACE,'delete','job',name,'--ignore-not-found=true','--wait=true','--timeout=90s')
deadline=time.monotonic()+420
while time.monotonic()<deadline:
    time.sleep(15)
    s=sample('cooldown')
    if s['current']==2 and s['desired']==2:
        record['scale_down']='passed'
        break
else: raise AssertionError('HPA did not return to two after load stopped')
(ROOT/'docs/evidence/hpa.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print('PASS: HPA scaled up under real HTTP traffic and down after load removal',flush=True)

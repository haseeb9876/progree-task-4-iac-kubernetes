"""Verify Mongo PVC persistence and replacement of one backend pod."""
import datetime
import json
import time
import urllib.request
import uuid
from cluster import ROOT, NAMESPACE, k, read
BASE = 'http://127.0.0.1:8084'

def request(path, method='GET', body=None):
    req = urllib.request.Request(BASE + path, data=json.dumps(body).encode() if body is not None else None, method=method, headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=15) as response:
        return json.load(response)

def wait_post(path, title):
    deadline = time.monotonic() + 180
    while time.monotonic() < deadline:
        try:
            if request(path)['title'] == title: return
        except (OSError, KeyError): pass
        time.sleep(3)
    raise AssertionError('Stored post did not return after replacement')

record = {'verified_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
claim = read('-n', NAMESPACE, 'get', 'pvc', 'data-mongodb-0')
assert claim['status']['phase'] == 'Bound'
record['pvc_uid'] = claim['metadata']['uid']
record['volume_name'] = claim['spec']['volumeName']
title = 'Task 4 persistence ' + uuid.uuid4().hex[:10]
post = request('/api/posts', 'POST', {'title':title,'authorName':'Task 4 Verification','imageLink':'https://example.com/demo.jpg','categories':['Travel'],'description':'Temporary persistence verification record','isFeaturedPost':False})
path = '/api/posts/' + post['_id']
try:
    before = read('-n', NAMESPACE, 'get', 'pod', 'mongodb-0')['metadata']['uid']
    k('-n', NAMESPACE, 'delete', 'pod', 'mongodb-0', '--wait=true', '--timeout=90s')
    k('-n', NAMESPACE, 'rollout', 'status', 'statefulset/mongodb', '--timeout=240s')
    after = read('-n', NAMESPACE, 'get', 'pod', 'mongodb-0')['metadata']['uid']
    assert before != after
    assert read('-n', NAMESPACE, 'get', 'pvc', 'data-mongodb-0')['metadata']['uid'] == record['pvc_uid']
    wait_post(path,title)
    record['persistence'] = {'result':'passed','old_pod_uid':before,'new_pod_uid':after,'same_pvc':True}
    pods = read('-n', NAMESPACE, 'get', 'pods', '-l', 'app=backend')['items']
    assert len(pods) >= 2
    old = pods[0]['metadata']
    k('-n', NAMESPACE, 'delete', 'pod', old['name'], '--wait=true', '--timeout=90s')
    k('-n', NAMESPACE, 'rollout', 'status', 'deployment/backend', '--timeout=240s')
    replacement = read('-n', NAMESPACE, 'get', 'pods', '-l', 'app=backend')['items']
    assert old['uid'] not in [p['metadata']['uid'] for p in replacement]
    assert sum(any(c['type']=='Ready' and c['status']=='True' for c in p['status'].get('conditions',[])) for p in replacement) >= 2
    wait_post(path,title)
    record['pod_recovery'] = {'result':'passed','deleted_pod':old['name'],'ready_replicas':len(replacement)}
finally:
    request(path,'DELETE')
record['limitations'] = 'Pod replacement tested, not uninterrupted availability, node loss, database replication, or cloud HA.'
(ROOT/'docs/evidence/resilience.json').write_text(json.dumps(record,indent=2)+'\n',encoding='utf-8')
print(json.dumps(record,indent=2))

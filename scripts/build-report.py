"""Generate Task 4 proof only from verified local execution records."""
import json
from pathlib import Path
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
ROOT=Path(__file__).resolve().parents[1]
E=ROOT/'docs/evidence'
def read(name): return json.loads((E/name).read_text(encoding='utf-8-sig'))
cluster=read('cluster-setup.json'); resilience=read('resilience.json'); hpa=read('hpa.json'); terraform=read('terraform.json'); runtime=read('runtime.json')
assert cluster['metrics_api_available'] and cluster['traefik_ready']
assert resilience['persistence']['result']=='passed' and resilience['pod_recovery']['result']=='passed'
assert hpa['scale_up']=='passed' and hpa['scale_down']=='passed'
assert terraform['mock_tests_failed']==0 and runtime['result']=='passed'
styles=getSampleStyleSheet(); story=[]
def title(t): story.extend([Paragraph(escape(t),styles['Title']),Spacer(1,4*mm)])
def para(t): story.extend([Paragraph(t,styles['BodyText']),Spacer(1,3*mm)])
def table(rows):
    cells=[[Paragraph(escape(str(x)),styles['BodyText']) for x in row] for row in rows]
    t=Table(cells,colWidths=[65*mm,109*mm],repeatRows=1)
    t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e8eef8')),('GRID',(0,0),(-1,-1),0.4,colors.lightgrey),('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),6),('BOTTOMPADDING',(0,0),(-1,-1),6)]))
    story.extend([t,Spacer(1,4*mm)])
title('Progree DevOps Internship - Task 4')
para('<b>Haseeb Ullah</b><br/>Automated Infrastructure as Code and Orchestration Architecture')
para('Selected execution environment: local Minikube on Windows with Docker Desktop. This report separates observed Kubernetes results from an undeployed cloud network design.')
table([['PDF requirement','Implementation and evidence'],['Containerized stack on Kubernetes','Wanderlust frontend/backend, MongoDB and Redis, standalone Task 4 namespace.'],['Persistent volume claims','1 GiB MongoDB PVC; stored record survived database pod replacement.'],['Ingress controller endpoints','Traefik Ingress with actual browser/API traffic through localhost:8084.'],['Horizontal Pod Autoscaler','Backend CPU HPA; actual expansion and cooldown recorded.'],['Declarative isolated cloud networks','Terraform AWS VPC/subnet/route blueprint; validation and mocked tests passed. No cloud apply.'],['Elastic, highly available cluster','Local pod elasticity and recovery tested. Single-node laptop and singleton database are not fully HA.']])
para('<b>Completion boundary:</b> local orchestration demonstrated; live cloud networking and node/control-plane/database high availability remain unverified. This is not a claim that the full cloud/HA objective has been completed.')
para('<link href="https://github.com/haseeb9876/progree-task-4-iac-kubernetes" color="blue">Separate Task 4 GitHub repository</link>')
story.append(PageBreak())
title('Verified cluster and application')
table([['Check','Observed result'],['Cluster',cluster['profile']],['Kubernetes',cluster['nodes'][0]['version']],['Cluster verification time',cluster['verified_at_utc']],['Node Ready',str(cluster['nodes'][0]['ready'])],['Metrics API',str(cluster['metrics_api_available'])],['Ingress controller', 'Traefik Ready'],['Default StorageClass',', '.join(cluster['default_storage_class'])],['Application checks',runtime['result']],['Application check time',runtime['verified_at_utc']]])
for line in (E/'runtime-checks.txt').read_text(encoding='utf-8-sig').splitlines():
    if line.startswith('PASS:'): para(escape(line))
para('Routing: Windows localhost port-forward -&gt; Traefik -&gt; frontend or backend Service -&gt; ready pods. Database and cache use internal ClusterIP services. No cloud load balancer or permanent public endpoint was created.')
story.append(PageBreak())
title('Persistence, recovery and elasticity')
table([['Check','Observed result'],['MongoDB pod replacement',resilience['persistence']['result']],['Same PVC retained',str(resilience['persistence']['same_pvc'])],['Persistent volume',resilience['volume_name']],['Backend replacement',resilience['pod_recovery']['result']],['HPA scale-up',hpa['scale_up']],['HPA maximum observed replicas',max(s['current'] for s in hpa['samples'] if s.get('phase')=='load')],['HPA final replicas',hpa['samples'][-1]['current']],['HPA cooldown',hpa['scale_down']]])
para('The persistence test creates one temporary post, replaces the database pod, verifies the same record using the same PVC, and removes only its test record. The backend test replaces one pod and checks that ready replicas and API access recover.')
para('The load test sends concurrent HTTP requests to the existing backend health endpoint. It observes the HPA rather than manually changing replica counts, removes the load job, and waits for the replica count to settle to two.')
para('These tests do not prove zero downtime or tolerance of laptop, worker-node, control-plane, disk, or database-instance failure. Pod replicas share one node; the database has persistent storage but no replica set.')
story.append(PageBreak())
title('Infrastructure code and presentation')
table([['Terraform check','Result'],['Version',terraform['terraform_version']],['AWS provider',terraform['provider']],['Configuration validation',terraform['validate']],['Mock tests passed',terraform['mock_tests_passed']],['Cloud resources created',str(terraform['cloud_resources_created'])]])
para('The optional AWS module declares an isolated VPC, four subnets across two availability zones, an internet gateway and separate public/private route tables. Private subnets have no internet route or NAT. Mocked plans require no credentials and do not prove that AWS resources exist. This module does not create EKS or connect Minikube to AWS.')
para('<b>Presentation:</b> explain the desired-state manifests; show Ready pods, the running application, the bound PVC, replacement evidence and HPA samples; then explain the Terraform network and its explicit cloud-deployment boundary.')
para('<b>Reproduce:</b> scripts/start-cluster.ps1; py -3 scripts/deploy.py; scripts/serve.ps1; py -3 scripts/verify-stack.py; py -3 scripts/verify-resilience.py; py -3 scripts/verify-hpa.py. Detailed instructions are in the repository README.')
para('<b>Security and attribution:</b> credentials are generated locally and excluded from Git. A namespace is not network isolation; the default kindnet CNI does not enforce NetworkPolicy. Kubernetes Secrets require additional protection for production. Wanderlust is retained under its MIT license. Its inherited post API lacks authorization and login screens are not fully integrated; use this as a local internship demonstration.')
para('<b>Remaining cloud/HA work:</b> authorize a cloud provider/account/region and budget, validate a real plan, deploy the network and a multi-zone cluster, add replicated storage/database and backups, and verify failure tolerance. No cloud resources or internship submission were created by this report.')
def footer(canvas,doc):
    canvas.setFont('Helvetica',8); canvas.drawString(18*mm,10*mm,'Haseeb Ullah | Task 4 | Local evidence and explicit cloud limits'); canvas.drawRightString(A4[0]-18*mm,10*mm,str(doc.page))
output=ROOT/'docs/Task-4-IaC-Kubernetes-Report.pdf'
SimpleDocTemplate(str(output),pagesize=A4,leftMargin=18*mm,rightMargin=18*mm,topMargin=16*mm,bottomMargin=20*mm).build(story,onFirstPage=footer,onLaterPages=footer)
print(output)

## Runtime Job Integration

In essence, this comprises two types of Kubernetes Jobs:
1. **Workflow Submission Job:** This job functions as the "workflow engine" within REANA, responsible for orchestrating all the steps and jobs within a workflow. It serves as the central control point for managing the entire workflow.
2. **Workflow Task Job:** The second Kubernetes Job symbolizes an individual step within the workflow. It represents the execution of a specific task or job as part of the larger workflow orchestrated by the Workflow Submission Job.

To seamlessly integrate our previously designed Kueue Architecture into REANA Runtime Job Submission, two changes using the [[REANA Developer |REANA Debug Cluster]] were done:

1. **reana-workflow-controller:** REANA Component in charge of the Workflow Submission Job.
	The  `_create_job_spec` method is responsible for instantiating a Kubernetes job. It takes several parameters related to the job configuration and constructs a Kubernetes job object accordingly.
	
	To ensure that Kueue is scheduling jobs accordingly, we must add a label to the [job definition](https://github.com/xaviertintin/reana-workflow-controller/blob/master/reana_workflow_controller/workflow_run_manager.py#L499):
	
```python
@JobManager.execution_hook
    def execute(self):
        """Execute a job in Kubernetes."""
        backend_job_id = build_unique_component_name("run-job")
        self.job = {
            "kind": "Job",
            "apiVersion": "batch/v1",
            "metadata": {
                "name": backend_job_id,
                "namespace": REANA_RUNTIME_KUBERNETES_NAMESPACE,
                "labels": {"kueue.x-k8s.io/queue-name": "batch-queue-job"},
            },
            ...
```
	
2. **reana-job-controller:** REANA Component in charge of the Workflow Task Job.
	The `reana_job_controller.kubernetes_job_manager` contains a method `execute()` of which encapsulates the logic for preparing and submitting a Kubernetes job within the REANA environment, ensuring that all necessary configurations are properly set up before job execution.
	
	To ensure that Kueue is scheduling jobs accordingly, we must add a label to the [job definition](https://github.com/xaviertintin/reana-workflow-controller/blob/master/reana_workflow_controller/workflow_run_manager.py#L499C1-L500C1):
	
```python
		...
		workflow_metadata = client.V1ObjectMeta(
            name=name,
            labels={
                "reana_workflow_mode": "batch",
                "reana-run-batch-workflow-uuid": str(self.workflow.id_),
                "kueue.x-k8s.io/queue-name": "local-queue-batch",
            },
            namespace=REANA_RUNTIME_KUBERNETES_NAMESPACE,
        )
        ...
```

## Deploy REANA in Development Mode

```
kubectl config use-context kind-kind
source /opt/homebrew/bin/virtualenvwrapper.sh
mkvirtualenv reana -p python3.8
cd ~/project/reana/src
```

```
kind delete cluster --name kind
cd '/Users/alextintin/project/reana/src/reana'
pip install -e .    
cd ~/project/reana/src
reana-dev cluster-create -m /var/reana:/var/reana --mode=debug
reana-dev cluster-build --parallel 8 --exclude-components r-a-vomsproxy -b DEBUG=1
reana-dev cluster-deploy --admin-email john.doe@example.org --admin-password mysecretpassword --mode=debug
```

```
export REANA_SERVER_URL=https://localhost:30443
export REANA_ACCESS_TOKEN=9snQhLjPtnfuW37I8ynqzg
```

## Install Kueue Manually

```
VERSION=v0.6.1
kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/$VERSION/manifests.yaml
```
## Deploy Kueue Architecture

```
kubectl apply -f resourceFlavor.yaml
kubectl apply -f clusterQueue.yaml
kubectl apply -f localQueue.yaml
```

## Run REANA Workflow Test

```
reana-client create -n newWorkflow                   
export REANA_WORKON=newWorkflow
reana-client upload
reana-client start
```


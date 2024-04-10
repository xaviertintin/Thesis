In essence, this comprises two types of Kubernetes Jobs:
1. **Workflow Submission Job: **This job functions as the "workflow engine" within RE- ANA, responsible for orchestrating all the steps and jobs within a workflow. It serves as the central control point for managing the entire workflow.
2. **Workflow Task Job:** The second Kubernetes Job symbolizes an individual step within the workflow. It represents the execution of a specific task or job as part of the larger workflow orchestrated by the Workflow Submission Job.

To seamlessly integrate our previously designed Kueue Architecture into REANA Runtime Job Submission, two changes using the [[REANA Developer |REANA Debug Cluster]] were done:

1. [[reana-workflow-controller]]: REANA Component in charge of the Workflow Submission Job.
	The  [[_create_job_spec]] method is responsible for instantiating a Kubernetes job. It takes several parameters related to the job configuration and constructs a Kubernetes job object accordingly.
	
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
	
2. [[reana-job-controller]]: REANA Component in charge of the Workflow Task Job.
	The [[reana_job_controller.kubernetes_job_manager]] contains a method `execute()` of which encapsulates the logic for preparing and submitting a Kubernetes job within the REANA environment, ensuring that all necessary configurations are properly set up before job execution.
	
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

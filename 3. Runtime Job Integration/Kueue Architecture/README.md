## Abstraction Design

REANA components execute workflows follow the following sequence:

**Workflow Submission** shows the sequence diagram of the workflow submission stage. The incoming workflows are stored in a queue that is later processed by the scheduler. The first task was to improve the performance of the REANA platform’s server submission end points to allow many concurrent workflow starting requests.

**Workflow Scheduling** shows the next stage how the submitted workflows are being consumed from the incoming queue. The scheduler first checks whether the incoming workflow does not exceed the limits on the total number of workflow the system could handle as well as currently available free memory on the Kubernetes cluster. If the checks succeed, the workflow is accepted for execution. In the opposite case the incoming workflow is being rescheduled and attempted to be accepted for execution several times whilst waiting for the Kubernetes cluster resources to liberate. If the workflow cannot be scheduled for a substantial amount of time, a failure is declared.

**Workflow Execution** shows the stage of the running of the workflow after it has been accepted for execution. Note the interplay of the REANA platform with the underlying Kubernetes cluster: the job is scheduled using the Kubernetes native job scheduler mechanism which include additional scheduling delays that needed to be taken into account for optimization. The progress of the workflow is monitored until the workflow execution terminates. The workflow steps are launched when the worker nodes are free to run the workload. The status of jobs is published in the message queue.

**Workflow Status Update** shows the termination stage of the workflow. When all the steps are finished and the results are produced, the system has to delete the Kubernetes pod and update the status of the workflow in both the message queue and the database.

# Kueue Architecture Design 

Deploy Kueue with the following configuration for LocalQueues, ClusterQueues, and Resource Flavors. Note the separate workflow submission queue and the workflow task queue which were created to divise typical REANA workflow execution scenario.

1. **Workflow Submission Job:** This job functions as the "workflow engine" within REANA, responsible for orchestrating all the steps and jobs within a workflow. It serves as the central control point for managing the entire workflow.
2. **Workflow Task Job:** The second Kubernetes Job symbolizes an individual step within the workflow. It represents the execution of a specific task or job as part of the larger workflow orchestrated by the Workflow Submission Job.

## Administer Cluster Quotas

### 1. Create a ClusterQueue

Create a single ClusterQueue to represent the resource quotas for your entire cluster. 

```yaml
# Run Batch Job
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue-reana-run-batch"
spec:
  namespaceSelector: {} 
  cohort: "reana"
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 2
        borrowingLimit: 0 # blocks this from borrowing resources from another ClusterQueue
      - name: "memory"
        nominalQuota: 4Gi
---
# Run Job
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue-reana-run-job"
spec:
  namespaceSelector: {} 
  cohort: "reana"
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 5
        borrowingLimit: 0 # blocks this from borrowing resources from another ClusterQueue
      - name: "memory"
        nominalQuota: 7Gi
```

To create the [ClusterQueue](https://github.com/xaviertintin/Thesis/blob/main/Test/Runtime%20Job%20Integration/clusterQueue.yaml), run the following command:

```shell
kubectl apply -f clusterQueue.yaml     
```
### 2. Create a ResourceFlavor

A resource flavor has node labels and/or taints to scope which nodes can provide it. To create the [ResourceFlavor](https://github.com/xaviertintin/Thesis/blob/main/Test/resourceFlavor.yaml), run the following command:

```shell
kubectl apply -f resourceFlavor.yaml 
```
### 3. Create LocalQueues

Write the manifest for the LocalQueue. It should look similar to the following:

```yaml
# Run Batch Job
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "batch-queue-batch"
spec:
  clusterQueue: "cluster-queue-reana-run-batch"
---
# Run Job
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "local-queue-job"
spec:
  clusterQueue: "cluster-queue-reana-run-job"
```

To create the [LocalQueue](https://github.com/xaviertintin/Thesis/blob/main/Test/Runtime%20Job%20Integration/localQueue.yaml), run the following command:

```shell
kubectl apply -f localQueue.yaml 
```

### 4. Run a Job

To simulate REANA Runtime Job submission, create a manifest that submits two jobs into the Kubernetes cluster.

```yaml
# Run Batch Job
apiVersion: batch/v1
kind: Job
metadata:
  generateName: batch-
  labels:
    kueue.x-k8s.io/queue-name: batch-queue-batch
spec:
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:latest
        args: ["10s"]
        resources:
          requests:
            cpu: 1
            memory: "200Mi"
      restartPolicy: Never
---
# Run Job
apiVersion: batch/v1
kind: Job
metadata:
  generateName: job-
  labels:
    kueue.x-k8s.io/queue-name: local-queue-job
spec:
  template:
    spec:
      containers:
      - name: dummy-job
        image: gcr.io/k8s-staging-perf-tests/sleep:latest
        args: ["10s"]
        resources:
          requests:
            cpu: 1
            memory: "200Mi"
      restartPolicy: Never
```

Get and submit the job with:

```shell
k create -f sample-job.yaml 
```
### 5. Check Job Status

Monitor in real time the submission of jobs into both Cluster Queues:

```shell
kubectl get clusterqueue cluster-queue-reana-run-batch -o wide -w    
```

```shell
kubectl get clusterqueue cluster-queue-reana-run-job -o wide -w  
```


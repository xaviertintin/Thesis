Get a proof of concept of Kueue, creating a basic Kueue architecture and submitting a job.
## Install Kueue

```
kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.6.2/manifests.yaml
```
## Administer Cluster Quotas

### 1. Create a ClusterQueue

Create a single ClusterQueue to represent the resource quotas for your entire cluster. 

Write the manifest for the LocalQueue. It should look similar to the following:

```yaml
# cluster-queue.yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ClusterQueue
metadata:
  name: "cluster-queue"
spec:
  namespaceSelector: {} # match all.
  resourceGroups:
  - coveredResources: ["cpu", "memory"]
    flavors:
    - name: "default-flavor"
      resources:
      - name: "cpu"
        nominalQuota: 1
      - name: "memory"
        nominalQuota: 2Gi
```

To create the [ClusterQueue](https://raw.githubusercontent.com/xaviertintin/Thesis/main/Test/Proof-Concept/SleepWF-Kueue/clusterQueue.yaml?token=GHSAT0AAAAAACLIWV6AO7NYBNR5R4EKGVZIZOKWJ7A), run the following command:

```shell
kubectl apply -f clusterQueue.yaml     
```

> This ClusterQueue governs the usage of [resource types](https://kubernetes.io/docs/concepts/configuration/manage-resources-containers/#resource-types) `cpu` and `memory`. Each resource type has a single [resource flavor](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue#resourceflavor-object), named `default` with a nominal quota. The empty `namespaceSelector` allows any namespace to use these resources.
### 2. Create a ResourceFlavor

A resource flavor has node labels and/or taints to scope which nodes can provide it. To create the [ResourceFlavor](https://github.com/xaviertintin/Thesis/blob/main/Test/resourceFlavor.yaml), run the following command:

```yaml
# default-flavor.yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: ResourceFlavor
metadata:
  name: "default-flavor"
```

```shell
kubectl apply -f resourceFlavor.yaml 
```
### 3. Create LocalQueues

Users cannot directly send [workloads](https://kueue.sigs.k8s.io/docs/concepts/workload) to ClusterQueues. Instead, users need to send their workloads to a Queue in their namespace. Thus, for the queuing system to be complete, you need to create a Queue in each namespace that needs access to the ClusterQueue.

Write the manifest for the LocalQueue. It should look similar to the following:

```yaml
# localQueue.yaml
apiVersion: kueue.x-k8s.io/v1beta1
kind: LocalQueue
metadata:
  namespace: "default"
  name: "local-queue"
spec:
  clusterQueue: "cluster-queue"
```

To create the [LocalQueue](https://github.com/xaviertintin/Thesis/blob/main/Test/Proof-Concept/SleepWF-Kueue/localQueue.yaml), run the following command:

```shell
kubectl apply -f localQueue.yaml 
```

## Run A Job

### 0. Identify the queues available in your namespace

Run the following command to list the `ClusterQueues` and `LocalQueues` available in your namespace.

```shell
kubectl -n default get clusterqueues
# Or use the 'queues' alias.
kubectl -n default get localqueues
```

The output is similar to the following:

```bash
NAME          CLUSTERQUEUE    PENDING WORKLOADS   ADMITTED WORKLOADS
local-queue   cluster-queue   0                   0
```

> The [ClusterQueue](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue) defines the quotas for the Queue.
### 1. Define the Job 

Running a Job in Kueue is similar to [running a Job in a Kubernetes cluster](https://kubernetes.io/docs/tasks/job/) without Kueue. However, you must consider the following differences:

- You should create the Job in a [suspended state](https://kubernetes.io/docs/concepts/workloads/controllers/job/#suspending-a-job), as Kueue will decide when it’s the best time to start the Job.
- You have to set the Queue you want to submit the Job to. Use the `kueue.x-k8s.io/queue-name`label.
- You should include the resource requests for each Job Pod.

Here is a sample Job with three Pods that just sleep for a few seconds.

```yaml
# sample-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  generateName: sample-job-
  labels:
    kueue.x-k8s.io/queue-name: local-queue
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

### 2. Run the Job

You can run the Job with the following command:

```shell
kubectl create -f sample-job.yaml
```

Internally, Kueue will create a corresponding [Workload](https://kueue.sigs.k8s.io/docs/concepts/workload) for this Job with a matching name.

```shell
kubectl -n default get workloads
```

The output will be similar to the following:

```shell
NAME                         QUEUE         ADMITTED BY     AGE
job-sample-job-mn94g-08ee6   local-queue   cluster-queue   7s
```

### 3. Monitor the status of the workload

You can see the Workload status with the following command:

```shell
kubectl -n default describe workload job-sample-job-mn94g-08ee6
```

When the ClusterQueue has enough quota to run the Workload, it will admit the Workload. The output is similar to the following:

```output
... 
Events:
  Type    Reason         Age   From             Message
  ----    ------         ----  ----             -------
  Normal  QuotaReserved  45s   kueue-admission  Quota reserved in ClusterQueue cluster-queue, wait time since queued was 1s
  Normal  Admitted       45s   kueue-admission  Admitted by ClusterQueue cluster-queue, wait time since reservation was 0s
```

To review more details about the Job status, run the following command:

```shell
kubectl describe job sample-job-mn94g
```

The output is similar to the following:

```output
...

Events:
  Type    Reason            Age                From                        Message
  ----    ------            ----               ----                        -------
  Normal  Suspended         109s               job-controller              Job suspended
  Normal  CreatedWorkload   109s               batch/job-kueue-controller  Created Workload: default/job-sample-job-mn94g-08ee6
  Normal  Started           109s               batch/job-kueue-controller  Admitted by clusterQueue cluster-queue
  Normal  SuccessfulCreate  109s               job-controller              Created pod: sample-job-mn94g-vtv8v
  Normal  Resumed           109s               job-controller              Job resumed
  Normal  Completed         92s                job-controller              Job completed
  Normal  FinishedWorkload  92s (x3 over 92s)  batch/job-kueue-controller  Workload 'default/job-sample-job-mn94g-08ee6' is declared finished
```

Since events have a timestamp with a resolution of seconds, the events might be listed in a slightly different order from which they actually occurred.

## Delete all

```bash
kubectl delete pods --all
kubectl delete workloads --all
kubectl delete jobs --all
```

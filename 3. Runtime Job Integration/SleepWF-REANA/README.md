# Analysis structure

Making a research data analysis reproducible basically means to provide "runnable recipes" addressing (1) where is the input data, (2) what software was used to analysis the data, (3) which computing environments were used to run the software and (4) which computational workflow steps were taken to run the analysis. This will permit to instantiate the analysis on the computational cloud and run the analysis to obtain (5) output results.

## 1. Input data

No input data

## 2. Analysis code

No analysis code

## 3. Compute environment

Since this is merely as a demonstration, this simple example is run with the `riga/py-sci` image.

## 4. Analysis workflow

The analysis workflow is simple and consists of two above-mentioned stages:

	 +---------+
	 |  START  |
	 +---------+
           |  
           V  
	 +-------------+
	 |  (1)create  | -> sleep 40
	 +-------------+
		   |  
		   |  
		   v  
	 +-------------+
	 |  (2)append  | -> sleep 40 + sleep 40
	 +-------------+
		   |  
		   v
	 +----------+
	 |   STOP   |
	 +----------+


## 5. Output results

No output results

# Running the example

In this example we are using a simple Serial workflow engine to represent our sequential computational workflow steps.

## Deploying Locally 

If you are a researcher and would like to try out deploying a small REANA cluster on your laptop, you can proceed as follows:

1. Install `docker`, `kubectl`, `kind`, and `helm` dependencies
   
2. Deploy REANA cluster:
   
```bash
wget https://raw.githubusercontent.com/reanahub/reana/maint-0.9/etc/kind-localhost-30443.yaml 
kind create cluster --config kind-localhost-30443.yaml
wget https://raw.githubusercontent.com/reanahub/reana/maint-0.9/scripts/prefetch-images.sh 
sh prefetch-images.sh 
helm repo add reanahub https://reanahub.github.io/reana
helm repo update 
helm install reana reanahub/reana --namespace reana --create-namespace --wait
```

## Activate REANA client

```shell
source ~/.virtualenvs/reana/bin/activate
```

## Connect to some REANA instance

Navigate to your [profile](https://localhost:30443/profile) and run:

```shell
export export REANA_SERVER_URL=https://localhost:30443
export REANA_ACCESS_TOKEN=XXXXXXX
```

These commands set two environment variables: `REANA_SERVER_URL` and `REANA_ACCESS_TOKEN`.

-   `REANA_SERVER_URL` is being set to the URL of the REANA server
-   `REANA_ACCESS_TOKEN` is being set to a token that provides authorization to access the REANA server. The value `XXXXXXX` is a placeholder and should be replaced with the actual access token.

Setting these environment variables will allow you to use the REANA client to interact with the REANA server, such as submitting and managing workflow jobs.

### Test connection to the REANA cluster
```
reana-client ping
```

# Create new workflow

When running a workflow, you will have to start from here.

### Create new workflow called "HelloWorld"

```shell
reana-client create -n newWorkflow   
```

Expected output:

```python
==> Verifying REANA specification file... /Users/alextintin/Documents/Thesis/Local/Thesis/Proof of Concept/SleepWF-REANA/reana.yaml
  -> SUCCESS: Valid REANA specification file.
==> Verifying REANA specification parameters... 
  -> WARNING: Workflow "inputs" are missing in the REANA specification.
==> Verifying workflow parameters and commands... 
  -> SUCCESS: Workflow parameters and commands appear valid.
==> Verifying dangerous workflow operations... 
  -> SUCCESS: Workflow operations appear valid.
==> Verifying compute backends in REANA specification file...
  -> SUCCESS: Workflow compute backends appear to be valid.
newWorkflow.77
==> SUCCESS: File /reana.yaml was successfully uploaded.
```

### Save workflow name we are currently working on

```shell
export REANA_WORKON=newWorkflow
```

### Upload code and inputs to remote workspace

```shell
reana-client upload
```

No expected output:


### Start the workflow

```shell
reana-client start
```

Expected output:

```python
==> SUCCESS: newWorkflow has been queued
```

### Check its status

```shell
reana-client status
```

Expected outputs:

```python
NAME          RUN_NUMBER   CREATED               STATUS 
newWorkflow   77           2024-05-07T21:57:53   pending
```

... wait a minute or so for workflow to finish



### Check its output logs

```shell
reana-client logs
```

In the expected output you will get:
- Workflow engine logs
- Job logs

### Delete

```shell
reana-client delete -w newWorkflow --include-all-runs
```

```output
==> SUCCESS: All workflows named 'newWorkflow' have been deleted.
```

### More...

If you will to know more commands, you can check out the [reana-client CLI API documentation](https://docs.reana.io/reference/reana-client-cli-api/).


# Fast test

To rapidly test your workflow you can copy and run:

```shell
reana-client create -n newWorkflow                                              
export REANA_WORKON=newWorkflow
reana-client upload
reana-client start
```
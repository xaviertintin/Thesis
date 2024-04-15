# REANA Performance Calculator - Two ClusterQuotas

This Python script helps you calculate the configuration files for two ClusterQueues based on your input resources. You can use it to determine the resource allocation for both workflows and jobs within your cluster. Here's how it works:

## Input Resources

1. **Number of Nodes:** Enter the number of nodes available in your cluster.
2. **CPU per Node:** Specify the number of CPUs you want to allocate for each node (maximum 8).
3. **Memory per Node:** Define the amount of memory you wish to allocate for each node (maximum 14.3 GB).
CPU and Memory Allocation

The script will then guide you through the allocation of CPU and memory resources for both workflows and jobs within your cluster. You can specify the percentage of resources you want to allocate to workflows and the maximum percentage range allowed for workflows. The remaining percentage will be allocated to jobs, with a maximum percentage range for jobs.

## Calculations

The script performs the necessary calculations based on your input and displays the resource requests and borrowing limits for both workflows and jobs. It provides these values in YAML format, making it easy to create configuration files for your ClusterQueues.

## Usage

1. Run the script.
```
python3 calculator.py
```
2. Enter the requested input resources and allocation percentages.
3. Review the calculated resource requests and borrowing limits for both workflows and jobs.
4. Copy the generated YAML configurations to your ClusterQueue configuration files.


By using this calculator, you can efficiently determine the resource allocation for your cluster and create configuration files tailored to your specific requirements.
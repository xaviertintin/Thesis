import yaml
import subprocess

def format_quota_value(value):
    return f"{value}m"

def format_memory_quota_value(value):
    return f"{value}Mi"

def get_number_from_user(prompt):
    while True:
        try:
            num = float(input(prompt))
            return num
        except ValueError:
            print("Invalid input. Please enter a valid number.")

def format_float_value(value):
    if value.is_integer():
        return str(int(value))
    else:
        return str(value)
    
def apply_yaml(filename):
    print("Generated YAML file:")
    with open(filename, 'r') as file:
        print(file.read())
    
    confirm = input("Do you want to apply this YAML file? (yes/no): ").strip().lower()
    if confirm == "yes":
        subprocess.run(["kubectl", "apply", "-f", filename])
    else:
        print("YAML file not applied.")

def generate_yaml(filename, totalCPU_wf, maxCPU_wf, totalMemory_wf, maxMemory_wf, totalCPU_job, maxCPU_job, totalMemory_job, maxMemory_job):
    yaml_data = [
        {
            "apiVersion": "kueue.x-k8s.io/v1beta1",
            "kind": "ClusterQueue",
            "metadata": {
                "name": "cluster-queue-reana-run-batch"
            },
            "spec": {
                "namespaceSelector": {},
                "cohort": "reana",
                "resourceGroups": [
                    {
                        "coveredResources": ["cpu", "memory"],
                        "flavors": [
                            {
                                "name": "default-flavor",
                                "resources": [
                                    {
                                        "name": "cpu",
                                        "nominalQuota": format_quota_value(totalCPU_wf),
                                        "borrowingLimit": format_quota_value(maxCPU_wf)
                                    },
                                    {
                                        "name": "memory",
                                        "nominalQuota": format_memory_quota_value(totalMemory_wf),
                                        "borrowingLimit": format_memory_quota_value(maxMemory_wf)
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        },
        {
            "apiVersion": "kueue.x-k8s.io/v1beta1",
            "kind": "ClusterQueue",
            "metadata": {
                "name": "cluster-queue-reana-run-job"
            },
            "spec": {
                "namespaceSelector": {},
                "cohort": "reana",
                "resourceGroups": [
                    {
                        "coveredResources": ["cpu", "memory"],
                        "flavors": [
                            {
                                "name": "default-flavor",
                                "resources": [
                                    {
                                        "name": "cpu",
                                        "nominalQuota": format_quota_value(totalCPU_job),
                                        "borrowingLimit": format_quota_value(maxCPU_job)
                                    },
                                    {
                                        "name": "memory",
                                        "nominalQuota": format_memory_quota_value(totalMemory_job),
                                        "borrowingLimit": format_memory_quota_value(maxMemory_job)
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        }
    ]

    with open(filename, 'w') as file:
        yaml.dump_all(yaml_data, file, default_flow_style=False)

if __name__ == "__main__":
    print("REANA Performance Calculator - Two ClusterQuotas")

    nodes = get_number_from_user("Enter number of nodes: ")
    cpu = get_number_from_user("How many cpus of each node do you wish to use? (Max 8): ")
    memory = get_number_from_user("How much memory of each node do you wish to use (Max 14.3 GB): ")
    print("\nSpecifications: \nNumber of nodes: \t", nodes, "\nCPU: \t\t\t", cpu, "\nMemory: \t\t", memory)

    # CPU
    print("\nCPU Specifications")
    percentageCPU_wf = get_number_from_user("Percentage of CPUs for workflows [40 -> 40%]: ")
    string = "('Maximum percentage range for workflows (>=" + str(percentageCPU_wf) + "): "
    maxpercentageCPU_wf = get_number_from_user(string)
    percentageCPU_job = 100 - percentageCPU_wf
    print("\nJobs have been assigned %d%% of all resources (CPU)" % percentageCPU_job)
    string = "Maximum CPU percentage for jobs (>=" + str(percentageCPU_job) + "): "
    maxpercentageCPU_job = get_number_from_user(string)

    # Memory
    print("\nMemory Specifications")
    percentageMemory_wf = get_number_from_user("Percentage of memory for workflows [40 -> 40%]: ")
    string = "('Maximum percentage range for workflows (>=" + str(percentageMemory_wf) + "): "
    maxpercentageMemory_wf = get_number_from_user(string)
    percentageMemory_job = 100 - percentageMemory_wf
    print("\nJobs have been assigned %d%% of all resources" % percentageMemory_job)
    string = "Maximum percentage range for jobs (>=" + str(percentageMemory_job) + "): "
    maxpercentageMemory_job = get_number_from_user(string)

    # Calculations

    # Workflows
    print("\nClusterQueue Workflows: ")
    # CPU
    totalCPU = nodes * cpu
    totalCPU_wf = (totalCPU * percentageCPU_wf) / 100
    maxCPU_wf = ((maxpercentageCPU_wf - percentageCPU_wf) * totalCPU ) / 100
    print("CPU Request: \t\t", totalCPU_wf)
    print("Can borrow up to: \t", maxCPU_wf)
    totalCPU_wf *= 1000
    maxCPU_wf *= 1000

    # Memory
    totalMemory = nodes * memory
    totalMemory_wf = (totalMemory * percentageMemory_wf) / 100
    maxMemory_wf = ((maxpercentageMemory_wf - percentageMemory_wf) * totalMemory) / 100
    print("Memory Request: \t", totalMemory_wf)
    print("Can borrow up to: \t", maxMemory_wf, "\n")

    # YAML ClusterQueue Workflows
    print("          resources:")
    print("            - name: \"cpu\"")
    print(f"              nominalQuota: {format_float_value(totalCPU_wf)}m")
    print(f"              borrowingLimit: {format_float_value(maxCPU_wf)}m")
    print("            - name: \"memory\"")
    print(f"              nominalQuota: {format_float_value(totalMemory_wf*1000)}Mi")
    print(f"              borrowingLimit: {format_float_value(maxMemory_wf*1000)}Mi")

    # Jobs
    print("\nClusterQueue Jobs: ")
    # CPU
    totalCPU_job = (totalCPU * percentageCPU_job) / 100
    maxCPU_job = ((maxpercentageCPU_job - percentageCPU_job) * totalCPU) / 100
    print("CPU Request: \t\t", totalCPU_job)
    print("Can borrow up to: \t", maxCPU_job)
    totalCPU_job *= 1000
    maxCPU_job *= 1000

    # Memory
    totalMemory_job = (totalMemory * percentageMemory_job) / 100
    maxMemory_job = ((maxpercentageMemory_job - percentageMemory_job) * totalMemory) / 100
    print("Memory Request: \t", totalMemory_job)
    print("Can borrow up to: \t", maxMemory_job, "\n")

    # YAML ClusterQueue Jobs
    print("          resources:")
    print("            - name: \"cpu\"")
    print(f"              nominalQuota: {format_float_value(totalCPU_job)}m")
    print(f"              borrowingLimit: {format_float_value(maxCPU_job)}m")
    print("            - name: \"memory\"")
    print(f"              nominalQuota: {format_float_value(totalMemory_job*1000)}Mi")
    print(f"              borrowingLimit: {format_float_value(maxMemory_job*1000)}Mi\n")

    # Generate YAML
    generate_yaml("cluster_quotas.yaml", totalCPU_wf, maxCPU_wf, totalMemory_wf, maxMemory_wf, totalCPU_job, maxCPU_job, totalMemory_job, maxMemory_job)

    # Apply YAML
    apply_yaml("cluster_quotas.yaml")
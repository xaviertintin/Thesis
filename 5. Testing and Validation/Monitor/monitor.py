import time
import csv
from kubernetes import client, config

# Load the kubeconfig file
config.load_kube_config()

# Function to get the number of jobs in various states by type
def get_jobs_count_by_phase():
    v1 = client.BatchV1Api()
    ret = v1.list_job_for_all_namespaces(watch=False)
    
    job_statuses = {
        "reana-batch": {"Created": 0, "Pending": 0, "Running": 0, "Finished": 0},
        "reana-job": {"Created": 0, "Pending": 0, "Running": 0, "Finished": 0}
    }

    for job in ret.items:
        job_type = None
        if job.metadata.name.startswith("reana-run-batch-"):
            job_type = "reana-batch"
        elif job.metadata.name.startswith("reana-run-job-"):
            job_type = "reana-job"

        if job_type:
            if job.status.start_time is None:
                job_statuses[job_type]["Created"] += 1
            elif job.status.active:
                job_statuses[job_type]["Running"] += 1
            elif job.status.completion_time:
                job_statuses[job_type]["Finished"] += 1
            else:
                job_statuses[job_type]["Pending"] += 1

    return job_statuses

# Function to get the number of pods in various states by type
def get_pods_count_by_phase():
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)
    
    pod_statuses = {
        "reana-batch": {"Pending": 0, "Running": 0, "Succeeded": 0, "Failed": 0, "Unknown": 0},
        "reana-job": {"Pending": 0, "Running": 0, "Succeeded": 0, "Failed": 0, "Unknown": 0}
    }

    for pod in ret.items:
        pod_type = None
        if pod.metadata.name.startswith("reana-run-batch-"):
            pod_type = "reana-batch"
        elif pod.metadata.name.startswith("reana-run-job-"):
            pod_type = "reana-job"

        if pod_type:
            phase = pod.status.phase
            if phase == "Pending":
                pod_statuses[pod_type]["Pending"] += 1
            elif phase == "Running":
                pod_statuses[pod_type]["Running"] += 1
            elif phase == "Succeeded":
                pod_statuses[pod_type]["Succeeded"] += 1
            elif phase == "Failed":
                pod_statuses[pod_type]["Failed"] += 1
            else:
                pod_statuses[pod_type]["Unknown"] += 1

    return pod_statuses

# Main loop to get job and pod counts and write to respective CSV files every second
def main():
    with open("reana_batch_job_counts.csv", "a", newline='') as file_batch_job, \
         open("reana_job_counts.csv", "a", newline='') as file_job_job, \
         open("reana_batch_pod_counts.csv", "a", newline='') as file_batch_pod, \
         open("reana_job_pod_counts.csv", "a", newline='') as file_job_pod:
        
        writer_batch_job = csv.writer(file_batch_job)
        writer_job_job = csv.writer(file_job_job)
        writer_batch_pod = csv.writer(file_batch_pod)
        writer_job_pod = csv.writer(file_job_pod)

        # Write the header row if the file is empty
        file_batch_job.seek(0, 2)  # Move to the end of the file
        if file_batch_job.tell() == 0:
            writer_batch_job.writerow(["Timestamp", "Created", "Pending", "Running", "Finished"])
        
        file_job_job.seek(0, 2)  # Move to the end of the file
        if file_job_job.tell() == 0:
            writer_job_job.writerow(["Timestamp", "Created", "Pending", "Running", "Finished"])
        
        file_batch_pod.seek(0, 2)  # Move to the end of the file
        if file_batch_pod.tell() == 0:
            writer_batch_pod.writerow(["Timestamp", "Pending", "Running", "Succeeded", "Failed", "Unknown"])
        
        file_job_pod.seek(0, 2)  # Move to the end of the file
        if file_job_pod.tell() == 0:
            writer_job_pod.writerow(["Timestamp", "Pending", "Running", "Succeeded", "Failed", "Unknown"])

        while True:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            job_counts = get_jobs_count_by_phase()
            pod_counts = get_pods_count_by_phase()

            # Write job counts to CSV
            writer_batch_job.writerow([
                timestamp,
                job_counts["reana-batch"]["Created"], job_counts["reana-batch"]["Pending"],
                job_counts["reana-batch"]["Running"], job_counts["reana-batch"]["Finished"]
            ])

            writer_job_job.writerow([
                timestamp,
                job_counts["reana-job"]["Created"], job_counts["reana-job"]["Pending"],
                job_counts["reana-job"]["Running"], job_counts["reana-job"]["Finished"]
            ])

            # Write pod counts to CSV
            writer_batch_pod.writerow([
                timestamp,
                pod_counts["reana-batch"]["Pending"], pod_counts["reana-batch"]["Running"],
                pod_counts["reana-batch"]["Succeeded"], pod_counts["reana-batch"]["Failed"],
                pod_counts["reana-batch"]["Unknown"]
            ])

            writer_job_pod.writerow([
                timestamp,
                pod_counts["reana-job"]["Pending"], pod_counts["reana-job"]["Running"],
                pod_counts["reana-job"]["Succeeded"], pod_counts["reana-job"]["Failed"],
                pod_counts["reana-job"]["Unknown"]
            ])

            # Ensure the data is written to the files immediately
            file_batch_job.flush()
            file_job_job.flush()
            file_batch_pod.flush()
            file_job_pod.flush()

            time.sleep(1)  # Sleep for 1 second before fetching data again

if __name__ == "__main__":
    main()

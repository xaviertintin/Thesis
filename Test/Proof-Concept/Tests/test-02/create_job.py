from kubernetes import client, config
import uuid


class KubernetesJobManager:
    REANA_RUNTIME_KUBERNETES_NAMESPACE = "default"

    def __init__(self, docker_img, cmd, workflow_uuid):
        self.docker_img = docker_img
        self.cmd = cmd
        self.workflow_uuid = workflow_uuid

    def execute(self):
        backend_job_id = f"run-job-{uuid.uuid4().hex[:6]}"
        job_spec = {
            "kind": "Job",
            "apiVersion": "batch/v1",
            "metadata": {
                "name": backend_job_id.lower(),  # Ensure lowercase for name
                "labels": {"kueue.x-k8s.io/queue-name": "mrhackin-queue"},
            },
            "spec": {
                "template": {
                    "metadata": {
                        "labels": {
                            "reana-run-job-workflow-uuid": self.workflow_uuid.lower()
                        }  # Ensure lowercase for label
                    },
                    "spec": {
                        "containers": [
                            {
                                "image": self.docker_img,
                                "command": ["bash", "-c"],
                                "args": [self.cmd],
                                "name": "dummy-job-python",
                            }
                        ],
                        "restartPolicy": "Never",
                    },
                },
            },
        }
        config.load_kube_config()
        batch_v1 = client.BatchV1Api()
        batch_v1.create_namespaced_job(
            namespace=KubernetesJobManager.REANA_RUNTIME_KUBERNETES_NAMESPACE,
            body=job_spec,
        )
        return backend_job_id


# Example usage:
if __name__ == "__main__":
    docker_image = "ubuntu:latest"
    command = "sleep 10"
    workflow_id = str(uuid.uuid4())

    job_manager = KubernetesJobManager(docker_image, command, workflow_id)
    job_id = job_manager.execute()
    print(f"Job submitted with ID: {job_id}")

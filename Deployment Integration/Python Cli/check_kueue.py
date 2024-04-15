# from kubernetes import client, config

# def check_kueue_deployment():
#     """Checks if the Kueue deployment exists in the specified namespace.

#     Returns:
#         True if the deployment exists, False otherwise.
#         Raises an exception on encountering errors.
#     """
#     try:
#         config.load_kube_config()
#         api_instance = client.AppsV1Api()
#         namespace = 'kueue-system'
#         deployment_name = 'kueue-controller-manager'
#         api_instance.read_namespaced_deployment(name=deployment_name, namespace=namespace)
#         return True
#     except client.exceptions.ApiException as e:
#         # Handle API exceptions specifically
#         if e.status == 404:  # Handle not found error (deployment doesn't exist)
#             return False
#         else:
#             raise  # Raise the exception for other errors
#     except Exception as e:
#         raise  # Raise other unexpected exceptions

# if __name__ == "__main__":
#     try:
#         is_deployed = check_kueue_deployment()
#         if is_deployed:
#             print("Kueue deployment exists")
#         else:
#             print("Kueue deployment not found")
#     except Exception as e:
#         print(f"Error checking Kueue deployment: {e}")

import subprocess
import yaml

def get_helm_values(chart_name, namespace):
    # Run helm get values command to retrieve the values of the deployed chart
    helm_command = f'helm get values kueue -n kueue-system'
    helm_values_output = subprocess.run(helm_command, shell=True, capture_output=True, text=True)

    # Parse the output of helm get values as YAML
    helm_values_yaml = yaml.safe_load(helm_values_output.stdout)

    return helm_values_yaml


helm_values = get_helm_values("kueue", "kueue-system")
kueue_enabled = helm_values.get('kueueEnabled', False)

if kueue_enabled:
    print("Kueue is enabled")
else:
    print("Kueue is not enabled")

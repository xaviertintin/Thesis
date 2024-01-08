package main

import (
	"context"
	"flag"
	"fmt"
	"os"
	"path/filepath"

	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/client-go/util/homedir"

	"sigs.k8s.io/kueue/apis/kueue/v1beta1"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
)

func main() {
	var kubeconfig string
	if home := homedir.HomeDir(); home != "" {
		flag.StringVar(&kubeconfig, "kubeconfig", filepath.Join(home, ".kube", "config"), "(optional) absolute path to the kubeconfig file")
	} else {
		flag.StringVar(&kubeconfig, "kubeconfig", "", "absolute path to the kubeconfig file")
	}
	flag.Parse()

	config, err := clientcmd.BuildConfigFromFlags("", kubeconfig)
	if err != nil {
		fmt.Printf("Error building kubeconfig: %v", err)
		os.Exit(1)
	}

	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		fmt.Printf("Error creating clientset: %v", err)
		os.Exit(1)
	}

	kueueClient, err := v1beta1.NewForConfig(config)
	if err != nil {
		fmt.Printf("Error creating Kueue client: %v", err)
		os.Exit(1)
	}

	// Example: List Pods using the clientset
	pods, err := clientset.CoreV1().Pods("").List(context.Background(), metav1.ListOptions{})
	if err != nil {
		fmt.Printf("Error listing Pods: %v", err)
		os.Exit(1)
	}

	fmt.Printf("Found %d Pods:\n", len(pods.Items))
	for _, pod := range pods.Items {
		fmt.Printf("Name: %s, Namespace: %s\n", pod.Name, pod.Namespace)
	}

	listOptions := metav1.ListOptions{}
	clusterQueues, err := kueueClient.ClusterQueues("kueue-system").List(context.Background(), listOptions)
	if err != nil {
		fmt.Printf("Error fetching ClusterQueues: %v", err)
		os.Exit(1)
	}

	fmt.Printf("Found %d ClusterQueues:\n", len(clusterQueues.Items))
	for _, cq := range clusterQueues.Items {
		fmt.Printf("Name: %s, Cohort: %s\n", cq.Name, cq.Spec.Cohort)
	}
}
# Integrating Kubernetes Batch Scheduling Systems for Containerized Declarative Data Analyses

The project aims to evaluate the seamless integration and performance of the Kueue batch scheduling system within the REANA platform, a robust open-source solution designed for reproducible and declarative data analysis in containerized computing clouds. As the REANA platform facilitates streamlined workflows for researchers in the field of High-Energy Physics (HEP), the project focus relies on testing the viability of Kueue within the context of runtime user jobs, laying the groundwork for future developments that may introduce FAIR share capabilities within the REANA ecosystem.

# REANA - Reusable Analyses

[![image](https://github.com/reanahub/reana/workflows/CI/badge.svg)](https://github.com/reanahub/reana/actions)
[![image](https://readthedocs.org/projects/reana/badge/?version=latest)](https://reana.readthedocs.io/en/latest/?badge=latest)
[![image](https://codecov.io/gh/reanahub/reana/branch/master/graph/badge.svg)](https://codecov.io/gh/reanahub/reana)
[![image](https://img.shields.io/badge/discourse-forum-blue.svg)](https://forum.reana.io)
[![image](https://img.shields.io/github/license/reanahub/reana.svg)](https://github.com/reanahub/reana/blob/master/LICENSE)
[![image](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## About

[REANA](http://www.reana.io) is a reusable and reproducible research data analysis
platform. It helps researchers to structure their input data, analysis code,
containerised environments and computational workflows so that the analysis can be
instantiated and run on remote compute clouds.

REANA was born to target the use case of particle physics analyses, but is applicable to
any scientific discipline. The system paves the way towards reusing and reinterpreting
preserved data analyses even several years after the original publication.

## Features Overview

- structure research data analysis in reusable manner
- instantiate computational workflows on remote clouds
- rerun analyses with modified input data, parameters or code
- support for several compute clouds (Kubernetes/OpenStack)
- support for several workflow specifications (CWL, Serial, Yadage, Snakemake)
- support for several shared storage systems (Ceph)
- support for several container technologies (Docker)

## Getting started REANA

You can
[install REANA locally](https://docs.reana.io/administration/deployment/deploying-locally/),
[deploy it at scale on premises](https://docs.reana.io/administration/deployment/deploying-at-scale/)
(in about 10 minutes) or use <https://reana.cern.ch>. Once the system is ready, you can
follow the guide to run
[your first example](https://docs.reana.io/getting-started/first-example/). For more in
depth information visit the [official REANA documentation](https://docs.reana.io/).

### REANA Community, discussion, contribution, and support

- Discuss [on Forum](https://forum.reana.io/)
- Follow us [on Twitter](https://twitter.com/reanahub)
- Collaborate [on GitHub](https://github.com/reanahub)

### Useful links

- [REANA home page](http://www.reana.io/)
- [REANA documentation](http://docs.reana.io/)
- [REANA on DockerHub](https://hub.docker.com/u/reanahub/)



# Kueue

[![GoReport Widget]][GoReport Status]
[![Latest Release](https://img.shields.io/github/v/release/kubernetes-sigs/kueue?include_prereleases)](https://github.com/kubernetes-sigs/kueue/releases/latest)

[GoReport Widget]: https://goreportcard.com/badge/github.com/kubernetes-sigs/kueue
[GoReport Status]: https://goreportcard.com/report/github.com/kubernetes-sigs/kueue

Kueue is a set of APIs and controller for [job](https://kueue.sigs.k8s.io/docs/concepts/workload)
[queueing](https://kueue.sigs.k8s.io/docs/concepts#queueing). It is a job-level manager that decides when
a job should be [admitted](https://kueue.sigs.k8s.io/docs/concepts#admission) to start (as in pods can be
created) and when it should stop (as in active pods should be deleted).

Read the [overview](https://kueue.sigs.k8s.io/docs/overview/) to learn more.

## Features overview

- **Job management:** Support job queueing based on [priorities](https://kueue.sigs.k8s.io/docs/concepts/workload/#priority) with different [strategies](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#queueing-strategy): `StrictFIFO` and `BestEffortFIFO`.
- **Resource management:** Support resource fair sharing and [preemption](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#preemption) with a variety of policies between different tenants.
- **Dynamic resource reclaim:** A mechanism to [release](https://kueue.sigs.k8s.io/docs/concepts/workload/#dynamic-reclaim) quota as the pods of a Job complete.
- **Resource flavor fungibility:** Quota [borrowing or preemption](https://kueue.sigs.k8s.io/docs/concepts/cluster_queue/#flavorfungibility) in ClusterQueue and Cohort.
- **Integrations:** Built-in support for popular jobs, e.g. [BatchJob](https://kueue.sigs.k8s.io/docs/tasks/run/jobs/), [Kubeflow training jobs](https://kueue.sigs.k8s.io/docs/tasks/run/kubeflow/), [RayJob](https://kueue.sigs.k8s.io/docs/tasks/run/rayjobs/), [RayCluster](https://kueue.sigs.k8s.io/docs/tasks/run/rayclusters/), [JobSet](https://kueue.sigs.k8s.io/docs/tasks/run/jobsets/),  [plain Pod](https://kueue.sigs.k8s.io/docs/tasks/run/plain_pods/).
- **System insight:** Build-in [prometheus metrics](https://kueue.sigs.k8s.io/docs/reference/metrics/) to help monitor the state of the system, as well as Conditions.
- **AdmissionChecks:** A mechanism for internal or external components to influence whether a workload can be [admitted](https://kueue.sigs.k8s.io/docs/concepts/admission_check/).
- **Advanced autoscaling support:** Integration with cluster-autoscaler's [provisioningRequest](https://kueue.sigs.k8s.io/docs/admission-check-controllers/provisioning/#job-using-a-provisioningrequest) via admissionChecks.
- **Sequential admission:** A simple implementation of [all-or-nothing scheduling](https://kueue.sigs.k8s.io/docs/tasks/manage/setup_sequential_admission/).
- **Partial admission:** Allows jobs to run with a [smaller parallelism](https://kueue.sigs.k8s.io/docs/tasks/run/jobs/#partial-admission), based on available quota, if the application supports it.



## Getting started Kueue

**Requires Kubernetes 1.22 or newer**.

To install the latest release of Kueue in your cluster, run the following command:

```shell
kubectl apply --server-side -f https://github.com/kubernetes-sigs/kueue/releases/download/v0.6.2/manifests.yaml
```

Learn more about:

- Kueue [concepts](https://kueue.sigs.k8s.io/docs/concepts).
- Common and advanced [tasks](https://kueue.sigs.k8s.io/docs/tasks).

## Kueue Community, discussion, contribution, and support

Learn how to engage with the Kubernetes community on the [community page](http://kubernetes.io/community/)
and the [contributor's guide](CONTRIBUTING.md).

You can reach the maintainers of this project at:

- [Slack](https://kubernetes.slack.com/messages/wg-batch)
- [Mailing List](https://groups.google.com/a/kubernetes.io/g/wg-batch)
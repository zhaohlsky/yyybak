#!/bin/bash
USER=root
CONTROL_PLANE_IPS="master249.k8s  master251.k8s"
for host in ${CONTROL_PLANE_IPS}; do
ssh "${USER}"@$host "mkdir -p /etc/kubernetes/pki/etcd"
scp /etc/kubernetes/pki/ca.* "${USER}"@$host:/etc/kubernetes/pki/
scp /etc/kubernetes/pki/sa.* "${USER}"@$host:/etc/kubernetes/pki/
scp /etc/kubernetes/pki/front-proxy-ca.* "${USER}"@$host:/etc/kubernetes/pki/
scp /etc/kubernetes/pki/etcd/ca.* "${USER}"@$host:/etc/kubernetes/pki/etcd/
scp /etc/kubernetes/admin.conf "${USER}"@$host:/etc/kubernetes/
done

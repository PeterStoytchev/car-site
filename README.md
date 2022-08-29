# car-site

A full-stack web application that Petar Stoychev, Ryan Smith, and Edris Rahimi developed as a Case Study project, during our second semester at Fontys University.

System archetecture:
![overall_diagram](https://user-images.githubusercontent.com/33201521/187232523-01e70afb-fea9-4650-8315-aa7f4dde4798.png)

The system was designed in a way, that it can scale horizontally. The idea is that there is a master MySQL instance, that acts as a sync point, for all pods to use. The connection between a pod and the master MySQL instance, is secured via a VPN.

As systems like this one, are read-heavy, there is a MySQL instance in each pod, that is reponsivle for all read operations. All write/modify operations to the master instance (over the OpenVPN tunnel) and are afterwards propagated back to the individual MySQL instances in each pod, via the standard MySQL sync mechanism.

Users connect directly to a pod. Load-balancing between pods can be handled in whaterver way is conviniet for deployment, but for what we presented at Fontys, we used AWS's Route 53 service, for DNS-based load balancing. 

This is what a pod looks like on the inside:
![Untitled-2](https://user-images.githubusercontent.com/33201521/187236554-6edf1e6e-cbe4-4209-877c-342b22ba0162.png)

An entire pod can be deployed with the help of the setup.sh script.

# Credit
System developed by Petar Stoychev (myserver157@gmail.com), Ryan Smith (rsrnsmith@gmail.com) and Edris Rahimi (edris2002210@gmail.com) as a university project.

MySQL master-slave setup based on repo: https://github.com/vbabak/docker-mysql-master-slave
and article: https://hackernoon.com/mysql-master-slave-replication-using-docker-3pp3u97

# Note
System is not designed to be used or operated by a person or organization outside of the core developer team. There are parts that are hardcoded, as a result, actual deployment may be problematic. It was meant as a case study project, and may not to operate outside of that, without modification.

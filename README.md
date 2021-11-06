# Share-Challange
Python client to list all Bitnami-pods status working under Kubernetes cluster , The main purpose is to launch a microservice url for displaying json format.

# Installation
You can use any playground hosted in KateKoda , CloudGuru for creating and launching a kubernetes cluster , Typically you can install it also on single VM operated by Linux Ubuntu which I have used in this scenerio

# Components
Docker Coumminty Image
kuebctl , kubelet , kubeadmin
nginx pod
flannel
python-client kubernetes lib
vmware
linux ubuntu-latest

# Kubernetes Cluster Architecture
1 Master node with 1 nginx pod

# Detailed Step-By-Step
1. Install VMware with linux image from https://ubuntu.com/download/desktop
2. install curl 
 sudo apt update && sudo apt upgrade
 sudo apt install curl
 
3. Setting up a new cluster is to install a Dockeer container runtime.

 curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
 sudo add-apt-repository \
"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) \
stable"

sudo apt-get update

sudo apt-get install docker-ce docker-ce-cli containerd.io

Stop updating the docker by running : sudo apt-mark hold docker-ce

Check docker version : sudo docker version

4. Now that Docker is installed, we are ready to install the Kubernetes components
Installing Kubeadm, Kubelet, and Kubectl on Master Node with thee following commands :

curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add -
cat << EOF | sudo tee /etc/apt/sources.list.d/kubernetes.list
deb https://apt.kubernetes.io/ kubernetes-xenial main
EOF

sudo apt-get update

sudo apt-get install -y kubelet=1.15.7-00 kubeadm=1.15.7-00 kubectl=1.15.7-00 

(**Note** : I faced an issue when i tried to install version 1.12.2-00 from the Kubernetes ubuntu repositories. You can work around this by using version 1.15.7-00 for kubelet, kubeadm, and kubectl )

Stop updating the Kubernetes components by running : 

sudo apt-mark hold kubelet kubeadm kubectl

Run the following to check your installation : kubeadm version

**NOTE** I faced another issue to disable swap , swap is not required but can be used with another kubernetes processes , Anyhow I didn't require it so you can run the following to fix thee issue : sudo swapoff -a ,Refeerence : https://github.com/kubernetes/kubernetes/blob/master/CHANGELOG/CHANGELOG-1.8.md#before-upgrading

5. Bootstrap the cluster on the Kube master node.
  On the Kube master node, initialize the cluster:(it might take one minute or two minutes based on your internet connection)
    sudo kubeadm init --pod-network-cidr=10.244.0.0/16
    (**Note** The kubeadm init command should output a kubeadm join command containing a token and hash. Copy that command and run it with sudo on both worker                       nodes. It should look something like this:
    
                          sudo kubeadm join $some_ip:6443 --token $some_token --discovery-token-ca-cert-hash $some_hash ) - I was not able to add other worker node                 due to time but you can all above steps same with your worker nodes)
                          
  Set up the local kubeconfig:
  
    mkdir -p $HOME/.kube
    sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
    sudo chown $(id -u):$(id -g) $HOME/.kube/config
 Run the below just to get nodes and it should be "Not Ready" status now.
 
    kubectl get nodes
    
 6. We will configure cluster networking in order to make the cluster fully functional
    we will configure a cluster network using Flannel. You can find more information on Flannel at the official site: https://coreos.com/flannel/docs/latest/.
    On you nodes you will run : 
    
    echo "net.bridge.bridge-nf-call-iptables=1" | sudo tee -a /etc/sysctl.conf
    sudo sysctl -p
    
    Install Flannel in the cluster by running this only on the Master node:
    kubectl apply -f https://raw.githubusercontent.com/coreos/flannel/master/Documentation/kube-flannel.yml
    
    Now we will check nodes if ready or not kubectl get nodes
    
    Since flannel is a system pod kube , we will run the following cmd , as no custom pod has been provisioned yet
    kubectl get pods -n kube-system
    
Now we will run one deployment.yml for creating our ngnix pods

kubectl create -f deployment.yml

You can run the below command to describe the deployment and check if any issue 

(**Note** I faced an issue with pods status as it was showen pending , after drilling down i found out that I need to remove the taint from master node so i followed this work around by running this command : 

kubectl taint nodes  mildevkub020 node-role.kubernetes.io/master-)

Now please run : kubectl get pods --------- it should shows two nginx pods with Running status

    
    
 



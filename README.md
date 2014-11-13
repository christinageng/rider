rider
=====

**Precondition:**

docker installed http://docs.docker.com/installation/ , for Mac OS user , the docker 1.3+ version is required.

If you are on Mac OS X, please install boot2docker as well
docker client configured , for Mac OS user , please set the environment variables which is required by the boot2docker .
docker process initiated


**How to use it step by step**

**Installation**

   1.Start Docker VM and boot2docker up

   2.Install tool suite - pony-rider

		pip install pony-rider
		
 
   3.Check whether it has been installed successfully, type "rider" in the command line. It should return a help guide successfully.
   
**Create your own image with a specific Splunk build (build)**

Create the image

		rider build --splunk-pkg /Users/cgeng/Documents/Build/splunk-6.2.0-237341-Linux-x86_64.tgz --image-name namespace/splunk:clustering
	
Check whether it has been created successfully
	
		docker images
		
You should see images you just create

**Create the Splunk instance with existing image**

**Provision-cluster**

Create cluster with default configuration on the top of existing image. Default configuration is 1 search head, 2 indexer and 1 cluster master. The license binding is not the mandatory.

		rider provision-cluster --license-file /Users/cgeng/Documents/Build/500MB.lic
		
You will get the following message to build a cluster up.


**Create cluster with your configuration on the top of existing image.**
		
		rider provision-cluster --indexer-num 3 --sh-num 2 --image-name cgeng/splunk:clustering
		
You will get the following message to build a cluster up.

**Scale**

When you want to enlarge an existing cluster, take example you have 3 indexers, but I want to extend it as 4 indexers.

		rider scale --indexer-num 4 --image-name cgeng/splunk:clustering
		
You will get the following message to scale the existing cluster topology.

Note: the topology could only be scale out but can not be shrinked.

**Provision-single**

Create single splunk instance with default setting (1 single splunk instance, default image name is 10.66.128.203:49153/coreqa/splunk:latest)

		rider provision-single
		
Create cluster with your configuration on the top of existing image.

		rider provision-single --instance-num 2 --image-name cgeng/splunk:clustering

**Get the Splunk topology information (info)**
		
		rider info
When type "rider info" in the command, it will display all the information about the cluster which is created by rider.

**You can login to your container with ssh**

		root@192.168.59.103 -p 49226
		
**Clean the existing clustering environment (clean)**
		
		rider clean
		
When type "rider clean" in the command, it will remove all the instances (containers) in the cluster which is created by rider.



# Industry 4.0 Use Case for MESON: Optimized Cross-Slice Communication for Edge Computing

One  of  the  prerequisites,  but  open challenges, for Industry 4.0 is the physical interaction between robots that operate on the factory floor and seek to execute a specific task in a coordinated and secure way. Robotic proesses (e.g., localization) rely on various sensors and complex algorithms that require plenty of computing resources. Despite the recent boost in the computing capabilities of robotic systems, local execution still remains a time-consuming process. For this reason, current trends in network service delivery dictate that robotic applications are being developed and treated as VNFs, making their deployment to the cloud feasible. In such a setting, autonomous robotic clusters, deployed by different vendors on the same factory floor, can communicate through their corresponding slices in order to coordinate and perform their tasks (e.g., inventory loading/unloading) more efficiently. 

![Alt text](img/service%20chain.png?raw=true "Figure 1: Industry 4.0 Use Case Architecture")

## Component Architecture

* The Inventory Load Slice is responsible for loading the assets on the shelves.
* The Inventory Unload Slice is responsible for unloading the assets from the shelves.
* For each slice, a mobile robot follows a trajectory and accomplishes a load/unload mission.
* Whenever a mission is completed, the robot notifies its slice and this potentially triggers CSC to inform the other slice about the amounts of the assets in the inventory. The whole operation is dictated by Mission Planner (MP)
* Robotic Services with strict performance constraints are provided as VNFs.
* Path Planning Service is responsible for the trajectory of the robot in the Inventory.
* Localization Service (Loc) computes the accurate position of the robot. 
* Inventory Unload Service (Unload) assigns missions to the robots to take specific assets from the inventory.
* Inventory Load Service (Load) assigns missions to the robots to refill specific assets in the inventory.


## Symmetric CSC Link 

* Inventory Unload VNF can trigger the Inventory Load VNF when Product availability is below threshold. 
* Inventory Load VNF can inform the Inventory Unload VNF for product becoming available. 


## Deployment

![Alt text](img/robotic_uc.png?raw=true "Figure 2: The Network Service of the Robotic Use Case")

The CSC is implemented by port forwarding on a VM dedicated for this as shown in Figure 2.
Run the following commands:

```bash
iptables -t nat -A PREROUTING -s Load_slice_ip -j DNAT --to-destination Unload_slice_ip
iptables -t nat -A PREROUTING -s Unload_slice_ip -j DNAT --to-destination Load_slice_ip
```

The components above are placed in VMs. Run the following commands inside each vm to deploy the slices. 

Install virtualenv and pip:

```bash
sudo apt-get install python3-venv
sudo apt-get -y install python3-pip
```

Clone the existing repo:

```bash
git clone https://github.com/maravger/meson-roboticUC.git
```

Create a virtual environment, source it and install all of the dependencies:

```bash
python3 -m venv environment_directory
source environment_directory/bin/activate
pip install -r meson-roboticUC/requirements.txt
```

Change the ip of the services accordingly, making possible for all the components of the Unload Slice to communicate, while the Load and Unload components communicate with each other via the CSC link. Then run the flask applications.


You're good to go. You can test the deployed CSC link for this deployment!


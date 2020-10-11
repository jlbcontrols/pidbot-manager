<p align="center">
  <img src="./docs/banner-logo.png" alt="Pidbot Manager"/><br/>
  Industrial PID Controller Management - tuning, logging, monitoring and configuration.
</p>  

# Features
* Easy PID import. Browse PLCs for PID tags, and drag them in.
* Compatible with most PLC based PID controllers.
* Simple, **effective** tuning procedure.
* Single interface for all PID types.
* Logs every tuning session.
* Built-in historian.
* PID variable and configuration charts help you troubleshoot and optimize.
* Easy access to PID data via external DB.
* Visualize and organize PIDs with drag and drop ease.
* User management, role based restrictions.
 
# Using Pidbot Manager
Head to the [Pidbot Manager Wiki](../../wiki) for user instructions.

![](./docs/tune-and-log.gif)

# Setup

### Requirements  
* Ignition v8.0.12+
* [Pidbot](https://www.jlbcontrols.com/pidbot) v1.10.2+
* MySQL v8.0.17

### Setup Option 1: Restore a Gateway Backup
* Download the .gwbk file - Navigate to [releases](../../releases), click assets, then click on the .gwbk file.
* Restore the .gwbk following Ignition's [gateway restore instructions](https://docs.inductiveautomation.com/display/DOC80/Gateway+Backup+and+Restore).
* Follow the instructions in the [Database Setup](./README.md#Database-Setup), [Modules Setup](./README.md#Modules-Setup), and [OPC Setup](./README.md#OPC-Setup) sections below to complete the setup.

### Setup Option 2: Add the project to an existing Ignition Gateway.
* Download the project file, UDT definitions, and tag group config files - Navigate to [releases](../../releases), click assets, then click on the PidbotManager.proj file, PidbotTypes.json file, and PidbotTagGroups.json file.
* Using the Ignition Gateway webpage, create a user source called `PidbotUserSource`. Create three roles in the user source: `Administrator`,`Engineer`, and `Tuner`.
* Create a user that has the `Administrator` role so you can login to a Client with full privelages.
* Restore the .proj file following Ignition's [project import instructions](https://docs.inductiveautomation.com/display/DOC80/Project+Export+and+Import).
* Using the Ignition Designer, import the PidbotTypes.json file into the `Data Types` tag folder.
* Using the Ignition Designer, import the PidbotTagGroups.json file into tag groups.
* Follow the instructions in the [Database Setup](./README.md#Database-Setup), [Modules Setup](./README.md#Modules-Setup), and [OPC Setup](./README.md#OPC-Setup) sections below to complete the setup.

### Database Setup
* Create a MySQL database (other databases have not been tested yet). On the Ignition Gateway webpage, under Config >> Databases >> Connections, create (or edit) a database connection called `pidtuningdb`. Change the configuration of this connection as necessary to connect with your database.

### Modules Setup
Two Third-Party modules are used in this project. The Pidbot module is essential, and responsible for PID tuning. The Vision Client OPC Browser module is used to find PID tags in connected PLCs, and create UDT instance tags for them.
* [Download Pidbot](https://www.jlbcontrols.com/pidbot) module v1.10.2 or greater from JLB Controls.
* [Download Vision Client OPC Browser](https://github.com/jlbcontrols/vision-client-opc-browser) module from the releases section of the Github repository.
* Install the .modl files following Ignition's [module installation instructions](https://docs.inductiveautomation.com/display/DOC80/Installing+or+Upgrading+a+Module).

### OPC Setup
* Setup OPC server connections, and PLC connections to access your PID controllers. The easiest way is to use Ignition's built-in OPC-UA Server, and create a device connection using the Ignition Gateway webpage, under OPC UA >> Device Connections.
* If you restored from Gateway Backup (Setup Option 1), there will be a device called `plc1` configured already. You can edit the connectivity settings to connect with your device, or create a new device.

# User Source, Usernames & Passwords 
* If you restored from Gateway Backup (Setup Option 1), you can login to the gateway with username: `admin`, password `password`. There will also be a number of default users configured in `PidbotUserSource`: `defaultAdmin`, `defaultEngr`, `defaultTuner` and `defaultViewer`. The default password for all users is `password`.
* The project's user source is `PidbotUserSource` by default. Note: This means that users must belong to `PidbotUserSource` to log into a client.  

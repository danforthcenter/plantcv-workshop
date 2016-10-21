# Using CyVerse Atmosphere

## Starting a PlantCV virtual machine

1. Log into your CyVerse account at [https://user.cyverse.org/]().
2. Select the Atmosphere service or go to [https://atmo.cyverse.org]().
3. Click on [Images](https://atmo.cyverse.org/application/images) in the top navigation bar.
4. Search for "plantcv" in the search box.
5. Click on the [PlantCV - Ubuntu 14.04.2 XFCE](https://atmo.cyverse.org/application/images/1392) image.
6. Click on the Launch button to start an instance of the PlantCV virtual machine.
7. You will receive an email when the virtual machine is ready.

## Log into the virtual machine

You can access the desktop interface of the virtual machine using a web browser or VNC client. To use a web browser, click on the running instance, then click the Web Desktop button on the lower right, under "Links."

To use [VNC Viewer](https://www.realvnc.com/), enter the IP Address listed next to your running instance into the VNC Viewer login window under VNC Server. After the IP address add ":1" to specify the port. For example: `128.196.64.20:1`. Click continue to accept the security key of the server, then enter your CyVerse username and password to log in.

After login, click the Use default config to dismiss the Panel window.

## Download the workshop materials from GitHub

1. Open a terminal by clicking on the Terminal Emulator icon in the bottom desktop toolbar.
2. Clone the workshop repository using git: `git clone https://github.com/danforthcenter/plantcv-workshop.git`

## Start the Jupyter Notebook service

1. Using the same terminal window, start jupyterhub to initiate the web service. This has to be done as an administrator, so we will use the sudo command to run the command with administrator privileges: `sudo jupyterhub --no-ssl &`
2. Enter your password if prompted.
3. JupyterHub is now running, so minimize the terminal program, then start Google Chrome by double-clicking the desktop icon (click okay to dismiss the dialog box).
4. In the URL bar, enter: `127.0.0.1:8000`
5. In the JuptyerHub login screen, enter your CyVerse username and password.
6. Click on the `plantcv-workshop` folder that was cloned from GitHub.

## Seed phenotyping with PlantCV

In JupyterHub, click on the Jupyter notebook `plantcv-seed-phenotyping.ipynb` to analyze images of seed. Steps 2, 5, 6, 8, and 12 will possibly need to be adjusted for each image analyzed.

## Combine results for each genotype into one file

1. Open a new terminal window.
2. Change directories to the workshop directory: `cd plantcv-workshop`
3. Create a new combined table by initializing it with the header from one of the output files, for example: `head -1 Cs002_plantcv_results.txt > plantcv_seed_phenotypes.table`
4. Append all of your result files (excluding the headers) onto the new file, for example: `cat *.txt | grep -v HEADER >> plantcv_seed_phenotypes.table`

## Analyze the results using R

In JupyterHub, click on the Jupyter notebook `seed-phenotype-statistics.ipynb` to analyze the data from PlantCV in R.

== USV ==

USV web presence development.

When running locally be sure to use http://127.0.0.1:8888/ (not localhost or 0.0.0.0, etc.) Twitter OAuth is setup to use this address.

Requirements:
	- Be sure to install the required Python modules. (found in requirements.txt)
	- LESS, RECESS, and UglifyJS are also required.
		LESS: npm install -g less
		RECESS: npm install -g recess
		UglifyJS: npm install -g uglify-js

Deployment:
    - `fab <deployment_location> deploy` - Where <deployment_location> is `staging` or `prod`. For more info see fabfile.py in the root directory of the project.

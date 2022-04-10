## rest api for google app engine
The complete API built with flask restfull and made for better communication between personal trading algorithms and monitoring bot.

## Instalation and deployment

Go in the google app engine.
Activate Cloud Shell.
Import project and move to the new directory
```sh
git clone https://github.com/paul-noailly/restApiTradingBotsMonitoring
cd rest-api-for-google-app-engine
```
Create isolated test environment and test app
```sh
virtualenv --python python3 ~/envs/rest-api-for-google-app-engine
source ~/rest-api-for-google-app-engine/hello_world/bin/activate
pip install -r requirements.txt
python main.py
```
Create the app and deploy it
```sh
gcloud app create
gcloud app deploy app.yaml --project ID_PROJECT
```
the url to which the app target is `http://<ID_PROJECT>.appspot.com` or `https://<ID_PROJECT>.ew.r.appspot.com/`
`<ID_PROJECT>` is the ID of the project, you can find it in the url with `?project=` or in `IAM et admin` > `gérer les ressources` 

To consult app flux, go to app engine menu.
Then go to parameter > desactivate if you want to desactivate it.

If you want to delete the app, go to main menu > IAM et admin > gérer les ressources

## ERROR
During deployement:
```sh
Unable to deploy to application [spry-connection-271815] with status [USER_DISABLED]: Deploying to stopped apps is not allowed.
```
The app is not activated. Go to App Engine > Parameter > Activer l'application


```sh
Please make sure you are using the correct project ID and that you have permission to view applications on the project.
```
Incorrect ID, take the one of the project. you can find it in the url with `?project=` or in `IAM et admin` > `gérer les ressources` 


## Documentation 
- Scalling parameter of app.yaml file: https://cloud.google.com/appengine/docs/standard/python3/config/appref#scaling_elements
- instance documentation: https://cloud.google.com/appengine/docs/standard/python3/how-instances-are-managed
- ...


## Notes
in file `app.yaml` we set manual_scalling. This insures that the app engine will not try to optimise the computational time spent by putting the app on & off. If it does, then the app will initialized itself again everytime to the default values.

## Content of the API

For each bot (identified by `name_bot` variable), provides:
-`creds`: credntial like api keys, btc adress, ...
-`params`: parameters


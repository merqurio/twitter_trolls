import connexion

app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('swagger.yaml')
#application = app.app
app.run(server="tornado", port=8080)
import connexion

app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('swagger.yaml')
#application = app.app
app.run(port=80, server=tornado)
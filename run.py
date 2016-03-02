import connexion

app = connexion.App(__name__, specification_dir='swagger/')
app.add_api('swagger.yaml')
app.run(port=8080)
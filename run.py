from app import create_app

app = create_app()

if __name__ == '__main__':
    from app.services.transaccion_async_service import iniciar_hilo

    app = create_app()
    with app.app_context():
        iniciar_hilo()
    app.run(host= "0.0.0.0", port="5000",debug=True,use_reloader=False)

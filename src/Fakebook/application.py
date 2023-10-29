from Fakebook import create_app


##### INITIALIZE FLASK #####
application = create_app() # This needs to be named `application`


# Starts the flask application
if __name__ == "__main__":
    application.run()

from app import create_app

print("Starting to import create_app")
from app import create_app
print("create_app imported successfully")

print("Creating app")
app = create_app()
print("App created successfully")

if __name__ == "__main__":
    print("Running app directly")
    app.run()

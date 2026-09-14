from app.parser.repository_cloner import RepositoryCloner

name, path = RepositoryCloner.clone(
    "https://github.com/Harsharyan05/Cognisys.git"
)

print(f"Repository: {name}")
print(f"Path: {path}")
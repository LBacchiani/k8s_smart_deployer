from exec import execute

if __name__ == '__main__':
    execute(
        "./deployment/pulumi_deployment.yaml",
        "testdsds",
        "deploy",
        "./test"
    )
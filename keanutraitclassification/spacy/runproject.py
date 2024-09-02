import yaml
import subprocess


def run_workflow(yaml_file):
    with open(yaml_file, 'r') as file:
        config = yaml.safe_load(file)

    for command in config['commands']:
        print(f"Running command: {command['name']}")
        subprocess.run(command['script'], shell=True)


if __name__ == "__main__":
    run_workflow('project.yml')

from python_terraform import *
import sys
import logging
import subprocess

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger()


def run_terraform_command(tf, command, var_file, gcloud_env, project_name):
    """
    Runs the specified Terraform command with the provided var file and environment.
    """
    try:
        if command == "init":
            output = tf.init(
                no_color=IsFlagged,
                backend_config={"prefix": f"terraform/{gcloud_env}/{project_name}/"},
            )
        elif command == "plan":
            output = tf.plan(
                no_color=IsFlagged,
                refresh=False,
                var={"gcloud_env": gcloud_env},
                var_file=var_file,
            )
        elif command == "apply":
            output = tf.apply(
                no_color=IsFlagged,
                refresh=False,
                var={"gcloud_env": gcloud_env},
                var_file=var_file,
                skip_plan=True,
            )
        elif command == "destroy":
            output = tf_destroy(
                gcloud_env,
                var_file,
            )
        else:
            raise ValueError(f"Unknown Terraform command: {command}")

        for o in output:
            logger.info(o)
        return output

    except TerraformCommandError as e:
        logger.error(f"Error during {command}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error during {command}: {str(e)}")
        return None


def tf_destroy(gcloud_env, var_file):
    try:
        command = [
            "terraform",
            "destroy",
            f"--var-file={var_file}",
            "-var",
            f"gcloud_env={gcloud_env}",
            "-auto-approve",
        ]

        process = subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        stdout, stderr = process.communicate()
        if stderr:
            logger.error(f"Error during destroy: {stderr}")
            return None

        if process.returncode == 0:
            return stdout.splitlines()

    except Exception as e:
        print(f"Unexpected error with destroy {e}.")


def print_usage():
    """
    Prints usage information for the script.
    """
    print(
        """
        Usage: python wrapper.py <action>
        --var_file=<path_to_var_file> --gcloud_env=<gcloud_env>
        --project_name=<project_name> [--working_dir=<working_directory>]

        Available actions: init, plan, apply, destroy
        With the init action, the combination of <gcloud_env> and <project_name> set 
        the GCS backend_config. ie
        terraform init -backend-config='prefix=terraform/<gcloud_env>/<project_name>/'
        """
    )


if __name__ == "__main__":
    try:
        if sys.argv[1] == "--help":
            print_usage()
            sys.exit(0)
        elif len(sys.argv) < 2:
            print_usage()
            sys.exit(1)

        action = sys.argv[1]
        var_file = None
        gcloud_env = None
        project_name = None
        working_dir = "."

        for arg in sys.argv[2:]:
            if arg.startswith("--var_file="):
                var_file = arg.split("=")[1]
            elif arg.startswith("--gcloud_env="):
                gcloud_env = arg.split("=")[1]
            elif arg.startswith("--project_name="):
                project_name = arg.split("=")[1]
            elif arg.startswith("--working_dir="):
                working_dir = arg.split("=")[1]

        if not var_file or not gcloud_env:
            logger.error("Missing required parameters.")
            print_usage()
            sys.exit(1)

        tf = Terraform(working_dir=working_dir)
        if action in ["init", "plan", "apply", "destroy"]:
            logger.info(f"Running terraform {action}...")
            run_terraform_command(tf, action, var_file, gcloud_env, project_name)
        else:
            logger.error(f"Unknown action: {action}")
            print_usage()
            sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

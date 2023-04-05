# ML pipeline with Mage

Run end-to-end ML training pipeline with Mage.

![Mage](https://github.com/mage-ai/assets/blob/main/mascots/mascots-shorter.jpeg?raw=true)

## Overview

1. Start Mage
1. Trigger pipeline
1. View logs

## Start Mage

1. Clone project:
    ```
    git clone https://github.com/khuyentran1401/cicd-mlops-demo
    ```

1. Change directory into the project:
    ```
    cd cicd-mlops-demo
    ```

1. Start Mage:
    ```
    docker run -it -p 6789:6789 -v $(pwd):/home/src -e USER_CODE_PATH=src \
        mageai/mageai /app/run_app.sh mage start src
    ```
1. Open your browser and go to: [http://localhost:6789/](http://localhost:6789/)

## Trigger pipeline

1. On the pipelines list page, click the row and name that says <b>train_model</b>.

    <sub>Or you can go to http://localhost:6789/pipelines/train_model/triggers</sub>

1. On the next page, click the button in the top right labeled <b>Run pipeline now</b>.

## View logs

1. Click on the logs button item in the left navigation vertical bar.

    <sub>Or you can go to http://localhost:6789/pipelines/train_model/logs</sub>

1. The logs will update every 5 seconds to display the pipeline activity.

# store-item-demand-forecasting
Example repository of how to build a simple microservices setup for deploying a sales forecasting model.

The model was trained on data available from this [Kaggle Competition](https://www.kaggle.com/c/demand-forecasting-kernels-only/data). Model training code was adapted from [this notebook](https://www.kaggle.com/code/ashishpatel26/light-gbm-demand-forecasting/notebook).

## Steps to Execute the Project

1. Install project tooling dependencies:
    * [uv](https://docs.astral.sh/uv/)
    * [pyenv](https://github.com/pyenv/pyenv)
    * [docker](https://www.docker.com/)
2. Install project dependencies and activate environment
    * `uv sync`
    * `source .venv/bin/activate`
3. Train the model by executing the notebook located in `./notebooks/light-gbm-demand-forecasting.ipynb`
    * **Important**: You will need the model URI outputted at the end of the notebook, for example `runs:/f9b9715adcfa4145bd1cec58ddc70fc8/model`
4. Use the previously captured model URI to build the model container by executing the script located at `./deployment/model-docker-build.sh`
    * For example: `./deployment/model-docker-build.sh runs:/f9b9715adcfa4145bd1cec58ddc70fc8/model`
5. Spin up the project by using Docker compose
    * `docker compose up`
6. Hit the *Service Prediction* route by using the provided postman collection. Alternatively, navigate to [http://localhost/docs](http://localhost/docs) to have an interactive Swagger view.

## Explanation

The project follows the project structure outlined in my [Modern ML Microservices Series](https://www.datadelver.com/tags.html#tag:modern-ml-microservices). We employ a two microservice design each with their own responsibilities:

* A Model Service - Responsible for hosting the model and providing a generic inference API. MLFlow is used to wrap the model artifact, creating a generic service that can host any MLFlow model. Enabling easy swapping out of models and frameworks to facilitate quick experimentation and iteration.

* An Orchestration Service - Responsible for translating requests from the downstream consumer into the format the model expects, performing any necessary feature engineering, and post-processing the model output before returning it to the consumer.

This design decouples the mechanics of hosting a model from the business logic surrounding it. Allowing any model to be swapped with the existing model provided the input signature of the model does not change.

This architecture can be further extended to changing data requirements by adding dedicated *data source services* as described in my [CarMax Engineering Blog Post](https://medium.com/carmax-engineering-blog/from-batch-to-stream-bringing-new-school-mlops-to-old-school-analytics-carmax-25660dbb00bf). A fully expanded architecture may look something like this:

![ML Microservice Architecture](https://miro.medium.com/v2/resize:fit:720/format:webp/1*N9T2NIUGSu7D776sMgzb3A.png)

### Model Service

For constructing the model service we simply use the Docker build capabilities built into MLFlow. This minimizes the code surface we have to maintain while still meeting the objectives of providing both an inference and healthcheck route. You can read more about deploying MLFlow models as Docker containers [here](https://mlflow.org/docs/latest/deployment/deploy-model-to-kubernetes/).

**Remaining Optimizations**
* We are allowing MLFlow to infer the model's dependencies from the virtual environment. While this works, MLFlow tends to pull unnecessary dependencies. We could optimize this further by specifying the model dependencies by hand or writing logic to parse them from the `pyproject.toml` file. 

### Orchestrator Service

We call this layer the *Orchestrator* service because in a larger architecture it would be responsible for orchestrating calls out to data source services to fetch the data the model needs as well as making any subsequent calls post model inference.

The code in this service follows a three layer paradigm which I detail in a series of blog posts [here](https://www.datadelver.com/2025/02/05/delve-7-lets-build-a-modern-ml-microservice-application---part-2-the-data-layer.html) and [here](https://www.datadelver.com/2025/02/16/delve-8-lets-build-a-modern-ml-microservice-application---part-3-the-business-logic-and-interface-layers.html). This allows us to separate concerns within our codebase and make it more flexible and robust.

![Three Layer Architecture](https://www.datadelver.com/assets/images/figures/delve8/ThreeTieredApplication.png)

**Remaining Optimizations**
* Within the data layer of the application I have a generic `MLFlowProvider` class which could be used to interface with any MLFlow model, not just the model used in this project. In practice this would be abstracted into an internal shared library so that providers could be re-used by multiple projects instead of copy-pasting them.
* Within the interface layer, error handling is somewhat sparse. In practice you would have a generic base class the main app inherits from that would have more robust error handling available in an internal shared library.
* Unit tests for the app are not fully complete, a sample unit test is provided. As a result, the code coverage fail threshold has been lowered to allow the build script to still pass. In practice all elements should have unit (as well as integration) test coverage and target code coverage should be above 80%.
* No CI/CD pipelines are provided. In practice both build and deploy activities should be orchestrated through a CI/CD pipeline (Github Actions, Azure DevOps, etc.).
* No IaC is provided. In practice any necessary resources for the application should be define in IaC (Cloud Formation, Terraform, Bicep, etc.). 

## Project Structure
```
.
├── Dockerfile                      <- Dockerfile for main application
├── LICENSE                         <- Project LICENSE
├── README.md                       <- Project README
├── compose.yaml                    <- Docker compose file for orchestrating project containers
├── data                            <- Datasets used for model training and evaluation
│   ├── test.csv                    <- Test dataset
│   └── train.csv                   <- Training dataset
├── deployment                      <- Scripts for deployment of the project
│   ├── app-docker-build.sh         <- Script for building the main application docker container
│   ├── app-docker-run.sh           <- Script for running the main application docker container
│   ├── model-docker-build.sh       <- Script for building the model docker container
│   └── model-docker-run.sh         <- Script for running the model docker container
├── docs                            <- Supporting documentation
│   └── postman                     <- Project Postman collection
├── notebooks                       <- Project notebooks
├── pyproject.toml                  <- Project configuration file
├── src                             <- Project source code
├── tests                           <- Project tests
└── uv.lock                         <- Project dependency file
```
## **ENV variables**

An empty `.env` file should be created to run the application locally (the Docker container creates it automatically for you). To create the `.env` file, you can either do so manually or use the `setup_env.sh` bash script with the following command:

```
 sh setup_env.sh
```

### **The following variables SHOULD be provided (fallback otherwise):**

- `pinecone_api_key` - `default = ""`  Pinecone database API key.
- `pinecone_index_name` - `default = "whitepaper-similarity"` - Pinecone index name, which will be created automatically.
- `pinecone_spec_cloud` - `default = "aws"` - pinecone cloud provider
- `pinecone_spec_region` - `default = "us-east-1" ` - pinecone db region
- `pinecone_dimensions` - `default = 1024` - Embedding size (refer to your model documentation).
- `input_pdf_file` - `default = "ai_adoption_framework_whitepaper.pdf"`- Relative path to the PDF file.
- `chunk_length` - `default = 200` -  Chunk size to partition the input PDF text.
- `transformer_name` - [
  `default = "intfloat/multilingual-e5-large"`](https://huggingface.co/intfloat/multilingual-e5-large) - Model name
  from [Hugging Face](https://huggingface.co/)
- `qdrant_host` - `default = "qdrant_db"` -  Address of your `Qdrant` database. Should be set to `qdrant_db` if running it in a Docker container using `docker-compose.yaml`
- `qdrant_port` - `default = 6333` - Port of your Qdrant database.
- `qdrant_index_name` - `default = "whitepaper_similarity"` - - Qdrant collection name, which will be created automatically.
- `x_token` - `default = "super-secret-token"` - Simple secret token for authentication.


By default, the app will use [Qdrant](https://qdrant.tech/) as the database. To use [Pinecone](https://www.pinecone.io/), provide `pinecone_api_key` and modify the code in `app/di.py` as follows:

```python

class Container(containers.DeclarativeContainer):
    # vectordb_service = providers.Singleton(QDrantService)
    vectordb_service = providers.Singleton(PineconeService)
    transformer_service = providers.Singleton(TransformerService)

```

To run the API locally, you still need to run qdrant from `docker-compose.yaml` (if you aren’t using pinecone).

Use the following Docker Compose command:
```
docker compose -f <path to docker-compose.yaml file> -p similarity_search run qdrant_db
```

## Python environment
* Python 3.10 or 3.11

**Important**
Replace `python3` with `python` if you're using Windows or another default Python installation.


### Create a Virtual Environment
Run the following command to create a venv in a directory called venv inside the project folder:
```
python3 -m venv venv
```

### Activate the Virtual Environment:


* macOS/Linux
```
source venv/bin/activate
```
* Windows
```
.\venv\Scripts\activate
```

### Install Project Dependencies
With the environment activated, install dependencies using pip:
```
pip install --no-cache-dir --upgrade -r requirements.txt
```

## Running the app


After setting up your environment, you can run the app locally using the following command in your terminal:
```
python3 -m uvicorn app.main:app --port 8000 --host 0.0.0.0
```

or
```
uvicorn app.main:app --port 8000 --host 0.0.0.0
```

When you run the app for the first time, make sure that you call the `query/restore_embeddings` [endpoint](#post-queryrestore_embeddings`) to fill the database with embeddings from the provided .pdf file.

### Docker

To run the app in a Docker container, use the provided `docker-compose.yaml` with the following command:
```
docker compose up
```

Or, if not in the root directory, use the `-f` parameter:
```
docker compose -f <path to docker-compose.yaml file> up
```



### Tests

To run the tests, install [`pytest`](https://docs.pytest.org/en/stable/)
```
pip install pytest
```

Then, run the tests with the following command:
```
pytest tests/test_main.py
```

## API

There are two available endpoints.
You can import the Postman collection available in the root directory — [Similarity Search.postman_collection.json](Similarity%20Search.postman_collection.json)


Both endpoints require the `x-token` header.

* `x-token` - Secret token for authentication from the `.env` file.

### GET `/query` 
make a query to the database

#### Parameters
* `q` - Query string **(required)**
* `top_k` = Number of top results to return **(default value: 3)**

```shell
curl --location 'http://localhost:8000/query?q=Explainable%20AI&top_k=3' \
--header 'x-token: super-secret-token'
```

#### Response struct

```
{
  "query": "string",
  "matches": [
    {
      "score": 0.0,
      "text": "string"
    }
  ]
}
```


#### Response example
```
{
	"query": "Explainable AI",
	"matches": [
		{
			"score": 0.819863737,
			"text": "blackboxing in ML, where it is hard to explain specific decisions from an ML model. Your AIenabled business may impact, or even redefine, many areas of society. The usefulness and fairness of these AI systems will be gated both by their transparency and by your ability to understand, explain, and control them. Activating the right Google tools and capabilities, such as WhatIf tool, Fairness Indicators, and Explainable AI, will not only speed up and secure the AI journey, it will also enable your organization to stay compliant with current regulations, and to react quickly when they change. 31 Your data governance is streamlined, for example, by using automated workflows to rapidly validate new use cases against your AI principles allowing greater focus and discussion time on the edge cases. A team specialized in AI safety and robustness works to improve the reliability and generalizability of ML models, recognizing the importance of wellcalibrated uncertainty and protecting against adversarial attacks.14 1 14 Adversarial attacks refers to how ML models can be vulnerable to inputs maliciously constructed by adversaries to force misclassification. 32 Automate An organizations maturity in the Automate theme reflects the ability of its AI systems to adapt to changes in"
		},
		{
			"score": 0.806645155,
			"text": "potential biases in humancentric13 2 use cases. Transformational maturity You aim to have a comprehensive understanding of the contents of all your data stores, so as to obtain the threat profiles necessary for designing more effective security and data governance models, models that consider scenarios of both unauthorized and inappropriate access. All Cloud Admin activity and data access logs are regularly audited, while automatic alerts have been configured to watch for patterns that match your threat profiles. Cloud IAM permissions and firewall rules are continuously monitored and corrected. 12 We recognize that technologies that solve important problems also raise important challenges that we need to address clearly, thoughtfully, and affirmatively. Artificial Intelligence at Google Our Principles sets out our commitment to develop technology responsibly and establishes specific application areas we will not pursue. 13 People AI Research PAIR is a multidisciplinary research and development team at Google that explores the human side of AI by working with diverse communities. PAIR released a guidebook to help user experience UX professionals and product managers follow a humancentered approach to AI. Explainable AI Explainable AI methods and techniques render AI solutions and outputs intelligible to human experts. This approach mitigates the concept of"
		},
		{
			"score": 0.800444126,
			"text": "in Practice Specialization helps you to discover the tools that software developers use to build scalable AIpowered algorithms in TensorFlow, a popular opensource machine learning framework. MLOps Continuous delivery and automation in ML discusses techniques for implementing and automating continuous integration CI, continuous delivery CD, and continuous training CT for ML systems. Google Cloud Smart Analytics describes Google Clouds fully managed serverless analytics platform, which can be leveraged to empower the business while eliminating constraints of scale, performance, and cost. Google Cloud AI solutions presents and enables organizations to use highquality, scalable, continuously improving, and fully managed AI solutions. 35"
		}
	]
}
```

### POST `query/restore_embeddings` 
Removes all embeddings from the database and adds new ones after reading the provided PDF file.

```shell
curl --location --request POST 'http://localhost:8000/query/restore_embeddings' \
--header 'x-token: super-secret-token'
```

#### Response struct

```
{
  "number_of_embeddings": 0
}
```



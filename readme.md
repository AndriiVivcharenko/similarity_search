## **ENV variables**

### **The following variables SHOULD be provided (fallback otherwise):**

- `pinecone_api_key` - `default = ""`  Pinecone database api key.
- `pinecone_index_name` - `default = "whitepaper-similarity"` - Pinecone index name. Will be created automatically
- `pinecone_spec_cloud` - `default = "aws"` - pinecone cloud provider
- `pinecone_spec_region` - `default = "us-east-1" ` - pinecone db region
- `pinecone_dimensions` - `default = 1024` - embeddings size (see your model documentation)
- `input_pdf_file` - `default = "ai_adoption_framework_whitepaper.pdf"`- pdf file relative path
- `chunk_length` - `default = 200` - chunk size to partition the input pdf text
- `transformer_name` - [
  `default = "intfloat/multilingual-e5-large"`](https://huggingface.co/intfloat/multilingual-e5-large) - model name
  from [Hugging Face](https://huggingface.co/)
- `qdrant_host` - `default = "localhost"` - address of your qdrant database. Should be set to `qdrant_db` in case you
  are running it in docker container using `docker-compose.yaml` file
- `qdrant_port` - `default = 6333` - port of your qdrant database
- `qdrant_index_name` - `default = "whitepaper_similarity"` - qdrant collection name. Will be created automatically
- `x_token` - `default = "super-secret-token"` - Simple secret token for auth.

## Prerequisites

By default the app will be using [qdrant](https://qdrant.tech/) database. 
In case you want to use [Pinecone](https://www.pinecone.io/) as your database `pinecone_api_key` should be provided AND the following code in `app/di.py` should be changed to
```python

class Container(containers.DeclarativeContainer):
    # vectordb_service = providers.Singleton(QDrantService)
    vectordb_service = providers.Singleton(PineconeService)
    transformer_service = providers.Singleton(TransformerService)

```

In order to run the api locally, you still need to run `qdrant` from `docker-compose.yaml` (if you are not using `pinecone`)

To do this, run the following docker compose command
```
docker compose -f <path to docker-compose.yaml file> -p similarity_search run qdrant_db
```

## Requirements

* Python 3.10 or 3.11
* Install dependencies
```
pip install --no-cache-dir --upgrade -r requirements.txt
```


## Running the app


After setting up your environment you can now run the app locally using the following command in your terminal
```
python -m uvicorn app.main:app --port 8000 --host 0.0.0.0
```

or
```
uvicorn app.main:app --port 8000 --host 0.0.0.0
```


### Docker

If you want to run the app in docker container simply use provided `docker-compose.yaml` with the following command
```
docker compose up
```

or with `-f` parameter if you are not in the root directory
```
docker compose -f <path to docker-compose.yaml file> up
```



### Tests

In order to run the tests you need to install [`pytest`](https://docs.pytest.org/en/stable/)

```
pip install pytest
```

and run the tests with the following command
```
pytest tests/test_main.py
```



## API

There are two endpoint available.

both requires `x_token` header

* `x-token` - secret token for auth from `.env`


### GET `/query` 
make a query to the database

#### Parameters
* `q` - Query string **(required)**
* `top_k` = Number of top results to return **(default value: 3)**

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
Removes all embeddings from the database and adds new ones after reading provided .pdf file

#### Response struct

```
{
  "number_of_embeddings": 0
}
```



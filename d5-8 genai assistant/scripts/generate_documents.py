from pathlib import Path


DOCUMENT_FOLDER = Path("data/documents")


documents = [
    (
        "Reinforcement Learning",
        "This document explains reinforcement learning and how agents learn through interaction with an environment.",
        "Reinforcement Learning requires an environment, an agent, states, actions, rewards, and a learning strategy.",
        "The agent observes the current state, selects an action, receives a reward, and updates its policy based on the experience.",
        "Reinforcement Learning is used in robotics, game playing, recommendation systems, resource allocation, and autonomous decision-making.",
        "Teams should define suitable reward functions, monitor training behavior, and evaluate whether the learned policy performs safely and effectively.",
    ),
    (
        "Data Preprocessing",
        "This document explains the importance of preparing raw data before using it for machine learning.",
        "Data preprocessing requires relevant datasets, cleaning techniques, transformation methods, and validation procedures.",
        "Data is inspected, cleaned, transformed, and prepared before being provided to a machine learning model.",
        "Data preprocessing is used in classification, regression, forecasting, recommendation, and analytics applications.",
        "Teams should maintain data quality, document transformations, and verify that preprocessing does not introduce unintended changes.",
    ),
    (
        "Feature Engineering",
        "This document explains how useful features can be created from raw data for machine learning models.",
        "Feature engineering requires domain understanding, relevant source data, transformation methods, and validation.",
        "Raw attributes are analyzed and transformed into features that provide useful information to the learning algorithm.",
        "Feature engineering is commonly used in prediction, classification, fraud detection, recommendation, and forecasting.",
        "Developers should avoid data leakage, document feature definitions, and evaluate whether engineered features improve model performance.",
    ),
    (
        "Model Training",
        "This document describes the process of training a machine learning model using prepared data.",
        "Model training requires training data, an algorithm, suitable parameters, and computational resources.",
        "The model receives training examples, calculates predictions, measures errors, and updates parameters to improve performance.",
        "Model training is used for classification, regression, image recognition, language processing, and forecasting.",
        "Developers should monitor training metrics, maintain reproducible configurations, and validate model behavior.",
    ),
    (
        "Model Deployment",
        "This document explains how trained machine learning models can be deployed for practical use.",
        "Deployment requires a validated model, an execution environment, an interface, monitoring, and appropriate infrastructure.",
        "The trained model is packaged and integrated into an application or service where it can receive inputs and produce predictions.",
        "Model deployment is used in recommendation services, fraud detection, automation, search systems, and intelligent applications.",
        "Teams should monitor model performance, availability, latency, and changes in input data after deployment.",
    ),
    (
        "Model Monitoring",
        "This document explains how deployed machine learning systems should be monitored over time.",
        "Monitoring requires performance metrics, logging, alerts, data quality checks, and evaluation procedures.",
        "System behavior is continuously observed and important changes are identified through defined monitoring metrics.",
        "Model monitoring is used in production classification, recommendation, forecasting, fraud detection, and automated decision systems.",
        "Teams should investigate performance degradation, data drift, failures, and unexpected prediction behavior.",
    ),
    (
        "Data Validation",
        "This document explains how datasets can be checked for quality before model development.",
        "Data validation requires validation rules, expected schemas, quality thresholds, and representative samples.",
        "Data is checked for missing values, invalid formats, unexpected ranges, duplicates, and schema inconsistencies.",
        "Data validation is used in machine learning pipelines, analytics systems, reporting, and automated data processing.",
        "Teams should document validation rules and prevent invalid data from silently entering downstream processes.",
    ),
    (
        "Data Cleaning",
        "This document describes common techniques for improving the quality of raw datasets.",
        "Data cleaning requires source data, quality rules, transformation logic, and validation checks.",
        "Invalid records, duplicates, missing values, and inconsistent formats are identified and handled according to defined rules.",
        "Data cleaning is used in analytics, machine learning, reporting, and data integration workflows.",
        "Teams should preserve important information, document cleaning decisions, and validate the resulting dataset.",
    ),
    (
        "Supervised Learning",
        "This document explains supervised learning using labeled training examples.",
        "Supervised learning requires labeled data, input features, target values, an algorithm, and an evaluation method.",
        "The algorithm learns relationships between input features and known target values and uses them to make predictions.",
        "Supervised learning is used for classification, regression, forecasting, and many prediction tasks.",
        "Developers should select appropriate evaluation metrics and ensure that training and evaluation data are properly separated.",
    ),
    (
        "Unsupervised Learning",
        "This document introduces unsupervised learning methods that discover patterns without labeled target values.",
        "Unsupervised learning requires relevant datasets, feature representations, and an appropriate discovery algorithm.",
        "The algorithm analyzes the data and identifies structures such as clusters, relationships, or lower-dimensional representations.",
        "Unsupervised learning is used for customer segmentation, anomaly detection, exploratory analysis, and pattern discovery.",
        "Teams should validate whether discovered patterns are meaningful and avoid treating automatically discovered groups as ground truth.",
    ),
    (
        "Classification",
        "This document explains classification as a machine learning task for predicting discrete categories.",
        "Classification requires labeled examples, input features, target classes, and evaluation metrics.",
        "A model learns patterns from labeled examples and assigns an input to one of the defined classes.",
        "Classification is used in spam detection, document categorization, fraud detection, and sentiment analysis.",
        "Developers should evaluate class-specific performance and consider class imbalance when interpreting results.",
    ),
    (
        "Regression",
        "This document explains regression for predicting continuous numerical values.",
        "Regression requires numerical targets, relevant features, training data, and suitable evaluation metrics.",
        "The model learns relationships between features and numerical targets and produces a continuous prediction.",
        "Regression is used for price prediction, demand forecasting, risk estimation, and resource planning.",
        "Teams should evaluate prediction errors and verify that model assumptions are appropriate for the intended problem.",
    ),
    (
        "Clustering",
        "This document explains clustering techniques for grouping similar data points.",
        "Clustering requires feature representations, a similarity concept, and a suitable clustering algorithm.",
        "Data points are analyzed according to their characteristics and assigned to groups based on similarity.",
        "Clustering is used for customer segmentation, document organization, anomaly analysis, and exploratory data analysis.",
        "Teams should evaluate cluster quality and avoid assuming that every discovered cluster has a business meaning.",
    ),
    (
        "Anomaly Detection",
        "This document explains methods for identifying unusual observations in datasets.",
        "Anomaly detection requires representative data, feature definitions, and a method for identifying unusual behavior.",
        "The system learns expected patterns and identifies observations that differ significantly from those patterns.",
        "Anomaly detection is used in fraud detection, network monitoring, manufacturing, and system diagnostics.",
        "Teams should investigate false positives and false negatives and define appropriate response procedures.",
    ),
    (
        "Recommendation Systems",
        "This document explains how recommendation systems provide relevant items to users.",
        "Recommendation systems require user interactions, item information, ranking logic, and evaluation methods.",
        "The system analyzes available information and predicts items that may be useful or relevant to a user.",
        "Recommendation systems are used in e-commerce, streaming platforms, news applications, and content discovery.",
        "Teams should monitor recommendation quality, relevance, diversity, and changes in user behavior.",
    ),
    (
        "Generative AI",
        "This document provides an overview of Generative AI systems that create new content from learned patterns.",
        "Generative AI systems require training data, model architectures, computational resources, and suitable evaluation methods.",
        "A trained model receives an input prompt or condition and generates content based on patterns learned during training.",
        "Generative AI is used for text generation, image generation, coding assistance, summarization, and conversational applications.",
        "Teams should evaluate output quality, reliability, safety, and appropriate usage boundaries.",
    ),
    (
        "Large Language Models",
        "This document explains the basic concept of Large Language Models and their use in language applications.",
        "Large Language Models require large text datasets, model architectures, training procedures, and significant computational resources.",
        "The model learns statistical patterns in language and uses those patterns to generate or transform text.",
        "Large Language Models are used for question answering, summarization, translation, coding assistance, and conversational systems.",
        "Developers should evaluate factual reliability, prompt behavior, output consistency, and application-specific risks.",
    ),
    (
        "Prompt Engineering",
        "This document explains how prompts can be designed to guide language model behavior.",
        "Prompt engineering requires a clear task definition, relevant context, expected output format, and evaluation criteria.",
        "A prompt provides instructions and context to a model, which then generates an output according to the provided information.",
        "Prompt engineering is used in summarization, extraction, classification, question answering, and content generation.",
        "Teams should test prompts with representative inputs and verify that outputs follow the expected format.",
    ),
    (
        "Vector Embeddings",
        "This document explains vector embeddings as numerical representations of text or other information.",
        "Embedding systems require input data, an embedding model, and a method for storing or comparing vectors.",
        "Input information is transformed into numerical vectors that can be compared according to semantic or feature similarity.",
        "Embeddings are used in semantic search, recommendation systems, clustering, and retrieval-augmented applications.",
        "Teams should select appropriate embedding models and verify retrieval quality on representative examples.",
    ),
    (
        "Semantic Search",
        "This document explains search methods that retrieve information based on meaning rather than exact keyword matching.",
        "Semantic search requires documents, embeddings, a vector index, and a similarity search mechanism.",
        "A query is converted into a representation and compared against stored document representations to identify relevant results.",
        "Semantic search is used in knowledge bases, document search, customer support, and enterprise information systems.",
        "Teams should evaluate retrieval relevance and maintain accurate source metadata.",
    ),
    (
        "Retrieval Augmented Generation",
        "This document explains how retrieval can provide relevant external context to a language model.",
        "Retrieval augmented systems require documents, chunking, embeddings, retrieval, and a generation model.",
        "Relevant document chunks are retrieved for a query and supplied as context to the language model before generating an answer.",
        "These systems are used for enterprise assistants, document question answering, and knowledge-base applications.",
        "Teams should preserve source references and evaluate both retrieval quality and generated answer quality.",
    ),
    (
        "Document Chunking",
        "This document explains how large documents can be divided into smaller text segments for retrieval.",
        "Chunking requires source documents, chunk-size rules, overlap settings, and quality checks.",
        "Documents are divided into smaller segments while attempting to preserve enough context for downstream retrieval.",
        "Chunking is used in vector search, document assistants, retrieval pipelines, and knowledge-base systems.",
        "Teams should inspect chunk boundaries, avoid empty chunks, and maintain traceability to source documents.",
    ),
    (
        "Vector Databases",
        "This document explains how vector databases store and retrieve numerical representations.",
        "Vector databases require embeddings, identifiers, metadata, storage, and similarity search capabilities.",
        "Vectors and associated metadata are stored and later searched to find information similar to a query vector.",
        "Vector databases are used in semantic search, recommendation systems, and retrieval-augmented generation.",
        "Teams should maintain consistent identifiers, metadata, embedding configurations, and retrieval evaluation procedures.",
    ),
    (
        "Information Retrieval",
        "This document introduces information retrieval systems that identify relevant information from collections.",
        "Information retrieval requires a document collection, queries, indexing methods, and ranking mechanisms.",
        "Documents are indexed and ranked according to their relevance to a user's query.",
        "Information retrieval is used in search engines, enterprise search, document assistants, and knowledge systems.",
        "Teams should measure retrieval relevance and maintain accurate indexing information.",
    ),
]


def create_document(number, title, purpose, requirements, process, applications, responsibilities):
    return f"""# {title}

## Purpose

{purpose}

## Requirements

{requirements}

## Process

{process}

## Applications

{applications}

## Responsibilities

{responsibilities}
"""


def main():
    DOCUMENT_FOLDER.mkdir(parents=True, exist_ok=True)

    start_number = 6

    for index, document_data in enumerate(documents, start=start_number):
        file_path = DOCUMENT_FOLDER / f"document_{index:03d}.md"

        content = create_document(index, *document_data)

        file_path.write_text(content, encoding="utf-8")

    print(f"Created {len(documents)} additional documents.")
    print(f"Total target documents: {start_number + len(documents) - 1}")


if __name__ == "__main__":
    main()
# Kaggle Server-Side API with BERT and FinLLaMA

Welcome to our hackathon project! This repository contains the server-side implementation of an API hosted on a Kaggle environment using Flask and Ngrok. The API leverages state-of-the-art models, including fine-tuned BERT and a quantized 4-bit FinLLaMA model, trained on a generated dataset.

---

## Table of Contents
1. [Introduction](#introduction)
2. [Features](#features)
3. [Technologies Used](#technologies-used)
4. [Models](#models)
5. [Setup and Installation](#setup-and-installation)
6. [API Endpoints](#api-endpoints)
7. [Usage](#usage)
8. [Contributions](#contributions)
9. [License](#license)

---

## Introduction

This project is designed to demonstrate how cutting-edge machine learning models can be deployed on lightweight servers for real-time inference. It showcases the use of *BERT (Bidirectional Encoder Representations from Transformers)* for natural language understanding tasks and *FinLLaMA*, a finetuned LLaMA model, optimized with 4-bit quantization for reduced computational overhead.

The API was developed as part of a hackathon challenge and is hosted using *Ngrok*, allowing easy public access to the Flask-based server.

---

## Features

- Fine-tuned *BERT* for text classification and natural language processing tasks.
- Quantized 4-bit *FinLLaMA* for efficient performance on a smaller compute footprint.
- Lightweight and portable deployment using *Flask*.
- Public API hosting enabled with *Ngrok*.
- Fully functional demonstration on Kaggle.

---

## Technologies Used

- *Python*: Core programming language.
- *Flask*: Lightweight web framework for API creation.
- *Ngrok*: Tunnel service to expose the server to a public endpoint.
- *Kaggle*: Environment for model deployment.
- *Transformers Library*: For pre-trained and fine-tuned models.
- *Quantization Techniques*: For optimizing model inference.

---

## Models

### 1. *Fine-Tuned BERT*
- *Base Model*: bert-base-uncased
- *Task*: Text classification
- *Dataset*: Generated synthetic dataset tailored for the hackathon task.
- *Performance*: Achieved high accuracy on validation datasets.

### 2. *FinLLaMA with 4-bit Quantization*
- *Base Model*: LLaMA
- *Optimization*: Quantized to 4-bit for efficiency.
- *Task*: Multi-label text processing and summarization.
- *Dataset*: Augmented data specifically designed for fine-tuning.

---

# DP-203T00: Data Engineering on Azure

Welcome to the course DP-203: Data Engineering on Azure. To support this course, we will need to make updates to the course content to keep it current with the Azure services used in the course.  We are publishing the lab instructions and lab files on GitHub to allow for open contributions between the course authors and MCTs to keep the content current with changes in the Azure platform.

## Nouveau mode de fonctionnement

### Installation des labs

Le script pour l'installation des labs a été modifé. Il ne nécessite plus d'interaction lors de la création du lab.

1. Création de l'utilisateur dans le Azure Active Directory choisi: on crée un utilisateur externe dans un Azure Active Directory que l'on a créé au préalable. Lors de cette étape, il est important de noter les mots de passe ainsi que le `tenantId` du Azure Active Directory. (Il est trouvable sur la page d'accueil du Azure Active Directory).
2. Ajout des Azure Pass: Pour chaque utilisateur, on doit ajouter un Azure Pass. Cette manipulation se fait à la main.
3. Installation des labs:

Pour cette étape, il faut une machine sur laquelle Powershell est installé, ainsi que Azure CLI et des modules Powershell Azure (voir le document utilisé par Gaspard). Une fois la machine prête, il faut télécharger le contenu du repo Github modifié (cette étape est un peu longue car le repo est assez lourd). Pour l'instant le nouveau code est sur la branche documentation. Il faut donc changer de branche:

```sh
cd /
mkdir dp-203
git clone https://github.com/DataScientest/DP-203-Data-Engineer.git
git checkout documentation
```

On se déplace au bon endroit dans le repo:

```sh
cd /dp-203/DP-203-Data-Engineer/Allfiles/00/artifacts/environment-setup/automation
```

On peut alors lancer le code en précisant le `tenantId`, le nom d'utilisateur et le mot de passe

```sh
# par exemple avec les arguments suivants:
pwsh ./dp-203-setup.ps1 3670fdab-17f6-4743-b8f8-6ac0784204aa pauldechorgnat@dp203sept.onmicrosoft.com DataScientest123!

```

Le code va tourner pendant une heure. A noter que le mot de passe choisi pour les SQL Server est `Azure2022!`.
Il est possible que le code termine par une erreur de credentials mais ce n'est pas un problème pour la suite.

### Tests des labs

Paul a créé des tests pour vérifier que les resources ont été correctement créées. Le code est disponible dans le [dossier suivant](Allfiles/00/artifacts/environment-setup/tests/test.py).

On peut l'utiliser en faisant:

```sh
cd ../tests

python3 test.py \
-d \
-t 3670fdab-17f6-4743-b8f8-6ac0784204aa \
-u pauldechorgnat@dp203sept.onmicrosoft.com \
-p DataScientest123!
--path /dp-203/DP-203-Data-Engineer/Allfiles/wwi-02
```

- `t` est le `tenantId`
- `u` est le username
- `p` est le mot de passe
- `--path` est le chemin absolu vers le dossier `wwi-02` du repo
- `-d` permet d'imprimer les messages de debug

Ce test permet de tester plusieurs choses:
- vérifier que les ressources ont bien été créées
- vérifier que les ressources ont bien le bon nom
- vérifier que les ressources sont bien localisées au même endroit
- vérifier que les ressources sont bien dans les bons groupes de ressource
- vérifier que les fichiers dans le data lake sont bien les bons

Ce code peut prendre un peu de temps à tourner puisqu'il doit récupérer tous les fichiers du Data Lake (environ 100 000).

## Lab overview

The following is a summary of the lab objectives for each module:

### Day 1

Before starting the Labs, if you received credentials to activate an azure subscription, you need to activate the Azure Pass. To do so:
1. First login into your azure account
2. Go to https://www.microsoftazurepass.com/ and fill the credentials you received

The activation of the Azure subscription may take several minutes before appearing into your Azure account.


#### [Module 00: Lab environment setup](Instructions/Labs/LAB_00_lab_setup_instructions.md)

Complete the lab environment setup for this course.

#### [Module 01: Explore compute and storage options for data engineering workloads](Instructions/Labs/LAB_01_compute_and_storage_options.md)

This lab teaches ways to structure the data lake, and to optimize the files for exploration, streaming, and batch workloads. The student will learn how to organize the data lake into levels of data refinement as they transform files through batch and stream processing. The students will also experience working with Apache Spark in Azure Synapse Analytics.  They will learn how to create indexes on their datasets, such as CSV, JSON, and Parquet files, and use them for potential query and workload acceleration using Spark libraries including Hyperspace and MSSParkUtils.

#### [Module 02: Run interactive queries using Azure Synapse Analytics serverless SQL pools](Instructions/Labs/LAB_02_queries_using_serverless_sql_pools.md)

In this lab, students will learn how to work with files stored in the data lake and external file sources, through T-SQL statements executed by a serverless SQL pool in Azure Synapse Analytics. Students will query Parquet files stored in a data lake, as well as CSV files stored in an external data store. Next, they will create Azure Active Directory security groups and enforce access to files in the data lake through Role-Based Access Control (RBAC) and Access Control Lists (ACLs).

#### [Module 03: Data Exploration and Transformation in Azure Databricks](Instructions/Labs/LAB_03_data_transformation_in_databricks.md)

This lab teaches you how to use various Apache Spark DataFrame methods to explore and transform data in Azure Databricks. You will learn how to perform standard DataFrame methods to explore and transform data. You will also learn how to perform more advanced tasks, such as removing duplicate data, manipulate date/time values, rename columns, and aggregate data. They will provision the chosen ingestion technology and integrate this with Stream Analytics to create a solution that works with streaming data.

### Day 2

#### [Module 04: Explore, transform, and load data into the Data Warehouse using Apache Spark](Instructions/Labs/LAB_04_data_warehouse_using_apache_spark.md)

This lab teaches you how to explore data stored in a data lake, transform the data, and load data into a relational data store. You will explore Parquet and JSON files and use techniques to query and transform JSON files with hierarchical structures. Then you will use Apache Spark to load data into the data warehouse and join Parquet data in the data lake with data in the dedicated SQL pool.

#### [Module 05: Ingest and load data into the data warehouse](Instructions/Labs/LAB_05_load_data_into_the_data_warehouse.md)

This lab teaches students how to ingest data into the data warehouse through T-SQL scripts and Synapse Analytics integration pipelines. The student will learn how to load data into Synapse dedicated SQL pools with PolyBase and COPY using T-SQL. The student will also learn how to use workload management along with a Copy activity in a Azure Synapse pipeline for petabyte-scale data ingestion.

#### [Module 06: Transform data with Azure Data Factory or Azure Synapse Pipelines](Instructions/Labs/LAB_06_transform_data_with_pipelines.md)

This lab teaches students how to build data integration pipelines to ingest from multiple data sources, transform data using mapping data flows and notebooks, and perform data movement into one or more data sinks.

### Day 3

#### [Module 07: Integrate data from Notebooks with Azure Data Factory or Azure Synapse Pipelines](Instructions/Labs/LAB_07_integrate_data_from_notebooks.md)

In the lab, the students will create a notebook to query user activity and purchases that they have made in the past 12 months. They will then add the notebook to a pipeline using the new Notebook activity and execute this notebook after the Mapping Data Flow as part of their orchestration process. While configuring this the students will implement parameters to add dynamic content in the control flow and validate how the parameters can be used.

#### [Module 08: End-to-end security with Azure Synapse Analytics](Instructions/Labs/LAB_08_security_with_synapse_analytics.md)

In this lab, students will learn how to secure a Synapse Analytics workspace and its supporting infrastructure. The student will observe the SQL Active Directory Admin, manage IP firewall rules, manage secrets with Azure Key Vault and access those secrets through a Key Vault linked service and pipeline activities. The student will understand how to implement column-level security, row-level security, and dynamic data masking when using dedicated SQL pools.

#### [Module 09: Support Hybrid Transactional Analytical Processing (HTAP) with Azure Synapse Link](Instructions/Labs/LAB_09_htap_with_azure_synapse_link.md)

This lab teaches you how Azure Synapse Link enables seamless connectivity of an Azure Cosmos DB account to a Synapse workspace. You will understand how to enable and configure Synapse link, then how to query the Azure Cosmos DB analytical store using Apache Spark and SQL Serverless.
### Day 4
#### [Module 10: Real-time Stream Processing with Stream Analytics](Instructions/Labs/LAB_10_stream_analytics.md)

This lab teaches you how to process streaming data with Azure Stream Analytics. You will ingest vehicle telemetry data into Event Hubs, then process that data in real time, using various windowing functions in Azure Stream Analytics. You will output the data to Azure Synapse Analytics. Finally, you will learn how to scale the Stream Analytics job to increase throughput.

#### [Module 11: Create a Stream Processing Solution with Event Hubs and Azure Databricks](Instructions/Labs/LAB_11_stream_with_azure_databricks.md)

This lab teaches you how to ingest and process streaming data at scale with Event Hubs and Spark Structured Streaming in Azure Databricks. You will learn the key features and uses of Structured Streaming. You will implement sliding windows to aggregate over chunks of data and apply watermarking to remove stale data. Finally, you will connect to Event Hubs to read and write streams.

- **Are you a MCT?** - Have a look at our [GitHub User Guide for MCTs](https://microsoftlearning.github.io/MCT-User-Guide/).
                                                                       
## How should I use these files relative to the released MOC files?

- The instructor handbook and PowerPoints are still going to be your primary source for teaching the course content.

- These files on GitHub are designed to be used in conjunction with the student handbook, but are in GitHub as a central repository so MCTs and course authors can have a shared source for the latest lab files.

- the lab instructions for each module are found in the /Instructions/Labs folder. Each subfolder within this location refers to each module. For example, Lab01 relates to module01 etc. A README.md file exists in each folder with the lab instructions that the students will then follow.

- It will be recommended that for every delivery, trainers check GitHub for any changes that may have been made to support the latest Azure services, and get the latest files for their delivery.

- Please note that some of the images that you see in these lab instructions will not neccessarily reflect the state of the lab environment that you will be using in this course. For example, while browsing for files in a data lake, you may see adiitional folders in the images that may not exist in your environment. This is by design, and your lab instructions will still work.

## What about changes to the student handbook?

- We will review the student handbook on a quarterly basis and update through the normal MOC release channels as needed.

## How do I contribute?

- Any MCT can submit a issues to the code or content in the GitHub repro, Microsoft and the course author will triage and include content and lab code changes as needed.

## Classroom Materials

It is strongly recommended that MCTs and Partners access these materials and in turn, provide them separately to students.  Pointing students directly to GitHub to access Lab steps as part of an ongoing class will require them to access yet another UI as part of the course, contributing to a confusing experience for the student. An explanation to the student regarding why they are receiving separate Lab instructions can highlight the nature of an always-changing cloud-based interface and platform. Microsoft Learning support for accessing files on GitHub and support for navigation of the GitHub site is limited to MCTs teaching this course only.

## What are we doing?

- To support this course, we will need to make frequent updates to the course content to keep it current with the Azure services used in the course.  We are publishing the lab instructions and lab files on GitHub to allow for open contributions between the course authors and MCTs to keep the content current with changes in the Azure platform.

- We hope that this brings a sense of collaboration to the labs like we've never had before - when Azure changes and you find it first during a live delivery, go ahead and make an enhancement right in the lab source.  Help your fellow MCTs.

## How should I use these files relative to the released MOC files?

- The instructor handbook and PowerPoints are still going to be your primary source for teaching the course content.

- These files on GitHub are designed to be used in conjunction with the student handbook, but are in GitHub as a central repository so MCTs and course authors can have a shared source for the latest lab files.

- It will be recommended that for every delivery, trainers check GitHub for any changes that may have been made to support the latest Azure services, and get the latest files for their delivery.

## What about changes to the student handbook?

- We will review the student handbook on a quarterly basis and update through the normal MOC release channels as needed.

## How do I contribute?

- Any MCT can submit a pull request to the code or content in the GitHub repro, Microsoft and the course author will triage and include content and lab code changes as needed.

- You can submit bugs, changes, improvement and ideas.  Find a new Azure feature before we have?  Submit a new demo!

## Notes

### Classroom Materials

It is strongly recommended that MCTs and Partners access these materials and in turn, provide them separately to students.  Pointing students directly to GitHub to access Lab steps as part of an ongoing class will require them to access yet another UI as part of the course, contributing to a confusing experience for the student. An explanation to the student regarding why they are receiving separate Lab instructions can highlight the nature of an always-changing cloud-based interface and platform. Microsoft Learning support for accessing files on GitHub and support for navigation of the GitHub site is limited to MCTs teaching this course only.

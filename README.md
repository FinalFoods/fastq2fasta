# fastq2fasta

SAM application that converts a FASTQ S3 file objects into FASTA and QUAL files.

```bash
.
├── README.md                   <-- This README
├── SampleEvent.json            <-- Event payload for local testing
├── src                         <-- Lambda function source code 
│   ├── __init__.py
│   ├── app.py                  <-- Lambda function code
│   ├── requirements.txt        <-- Python dependencies
├── template.yaml               <-- SAM Template
├── requirements.txt             
├── dependencies.zip            <-- Layer package              
└── layer                       <-- Lambda Layer
    └── __init__.py             
    ├── Bio                      <-- BioPython library            
    ├── BioSQL   
    └── numpy
```

## Requirements

* AWS CLI already configured with Administrator permission
* [Python 3 installed](https://www.python.org/downloads/)
* [Docker installed](https://www.docker.com/community-edition)

## Setup process

## Building the project

Create a `S3 bucket` where to upload the deployment package.

```bash
aws s3 mb s3://iaqportal
```

### Create and publish a Lambda layer with the Biopython library

1. Temporarely comment out the Layers property definition in template.yaml
2. Use `sam build` to get dependencies
```bash
sam build -b ./build --use-container -m ./requirements.txt
```
3. Move dependencies into the layer directory
```bash
mv build/FastqConvertFunction/Bio ./layer/
mv build/FastqConvertFunction/BioSQL/ ./layer/
mv build/FastqConvertFunction/numpy ./layer/
```
4. Remove the build directory and its contents
```bash
rm -rf build/
```
5. Make a zip file with the content of the layer directory
```bash
cd layer
zip -r9 ../dependencies.zip .
```
6. Upload the dependencies.zip file to an S3 bucket
```bash
aws s3 cp dependencies.zip s3://iaqportal
```
7. Publish the Lambda layer
```bash
$ aws lambda publish-layer-version \
    --layer-name biopython \
    --description "BioPython layer" \
    --license-info "MIT" \
    --content S3Bucket=iaqportal,S3Key=dependencies.zip \
    --compatible-runtimes python3.6 python3.7 \
    --region us-west-1
```
```    
{
    "LayerVersionArn": "arn:aws:lambda:us-west-1:892335585962:layer:biopython:1", 
    "Description": "BioPython layer", 
    "CreatedDate": "2019-04-07T18:32:01.496+0000", 
    "LayerArn": "arn:aws:lambda:us-west-1:892335585962:layer:biopython", 
    "Content": {
        "CodeSize": 19437516, 
        "CodeSha256": "iYKY1tpOi4xIgc+SgyYCLA8FJOxQFQd9dY8+Vtd0jWQ=", 
        "Location": "https://awslambda-us-west-1-layers.s3.us-west-1.amazonaws.com/snapshots/892335585962/biopython-33d92363-0161-44e4-a2b6-46a646ffb03a?versionId=OSFdKwofe_E4Ep_kFBS_RB6lN7Z_ISI2&X-Amz-Security-Token=AgoJb3JpZ2luX2VjEGkaCXVzLXdlc3QtMSJHMEUCIQCaUT4oDD7t9w8z7SkQLFWf0aDAKEUubBO%2Ft1SveUkRogIgRl%2F24cO7X8LC7ls9F762wjvk8gsVhoaX6JuIie2Xcmkq2gMIMhABGgw0NjA5MzI4NTYyMjYiDKkWoU%2BgwuBR2nEneSq3A%2B%2F859EZRk2lDT8gadr6h%2FhqAgT2OzLwPGUCo1BCV6kMkVVibvykGpj%2BgpUwSUqxQHXLFAe2QipZjbIFFYx%2F8tz8HvHkyX4Y6wXpZRMhmbtjyNAWcKEk9HKdvF4roOKwC3ch62EpElGvGhy%2BymRoSWdZ5l1G4%2FqAvdTcdIeNQbSuWyXPJE6A6D%2F3KNFKh6n2Bxclpwx6GxpGVhyWmMTVeb%2B7XCxJ9SuNmEkSV8zalu%2BpQN2qyFoGdpoObeRWnnIdv0%2BHKchis4maBN0ud4jOpvRhWewBErA95HHeIc9cSPNpjh8syl8LfPj5HlH%2FaVT%2F%2BfLK0ADVauvQA09RPDWWTTSA9mQtgOQ5v5VI3keDzhTF25WeVbtrbw55RV2ifzSzu9TKrkx%2FTpP1ORKZeU7cNshbrZQmOUBqhADLcvlhKcRYgCcifmV58hbaGQQ0w5S%2FDo2Ik8wrLy2%2Ftc8emnxfj%2FDSb%2BR%2FYJQvVQ25xUr%2B9%2Fjmw5FpUex2EefrSQ4AdTjxxnEtEFk%2FnZe6zGLc56LinNXeyM8AyArIFQIXGgnSQNeqz9v0qhw0IgUpFN3clcwGfF9aONMZ3QYwptmo5QU6tAGwYu2MHMYRTmRcrW0DPtt5TVeDZa8PxyLqjgjToftsMYshOT3zEfuykmNMUcUQD4j0HmdbZd48jCPxy7pFWj6ihtv77SwJoIFucDgeXTNFs%2BWdsEfj5zQ57UdqWQu7ZAoleSVUVrsy9sDMomgoede8p1VAhEzPO0FyCru3iEMLGdH0VcYNxq8fZWkT%2BiUu20bDXr8GB8HdxIFtlufx5VP67VqwwQrdNQqMbLL%2Bu3xpLt%2F9ses%3D&X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Date=20190407T183151Z&X-Amz-SignedHeaders=host&X-Amz-Expires=600&X-Amz-Credential=ASIAWWUN5HGREY4RZAQK%2F20190407%2Fus-west-1%2Fs3%2Faws4_request&X-Amz-Signature=9410de109e86ef98eba2c69d578dcae5a743899bb1f4837e2f943d2f86e1962f"
    }, 
    "Version": 1, 
    "CompatibleRuntimes": [
        "python3.6", 
        "python3.7"
    ], 
    "LicenseInfo": "MIT"
}
```

> **The LayerArn can now be added to the Layers section of template.yaml adding the version number**
```
      Layers: 
        - arn:aws:lambda:us-west-1:892335585962:layer:biopython:1
```

### Create the S3 source bucket
This is the bucket where to drop the FASTQ files to convert.
```bash
aws s3 mb s3://iaq-fastq2fasta
```
### Build for local testing

[AWS Lambda requires a flat folder](https://docs.aws.amazon.com/lambda/latest/dg/lambda-python-how-to-create-deployment-package.html) with the application as well as its dependencies in the deployment package.

When the dependencies contain a layer or native modules that need to be compiled specifically for the operating system running on AWS Lambda, build inside a Lambda-like Docker container:
```bash
sam build --use-container
```
This command writes built artifacts to `.aws-sam/build` folder.

> **Insure the source bucket name `iaq-fastq2fasta` is properly specified in SampleEvent.json**

### Invoking the function locally 

Using a local sample payload:

```bash
$ OUTPUT_BUCKET=iaqportal sam local invoke \
    --event SampleEvent.json \
    --region us-west-1
```
>**The `OUTPUT_BUCKET` environmental variable indicates an existing temporary output S3 bucket. A FASTQ file must be uploaded to the source bucket `iaq-fastq2fasta` before invoking the function locally.**

### Package Lambda function defined locally and upload to S3 as an artifact
```bash
sam package \
    --template-file template.yaml \
    --output-template-file packaged.yaml \
    --s3-bucket iaqportal
```

### Deploy SAM template as a CloudFormation stack
```bash
sam deploy \
    --template-file packaged.yaml \
    --stack-name fastq2fasta \
    --capabilities CAPABILITY_IAM \
    --region us-west-1 \
    --parameter-overrides SourceFastqBucket=iaq-fastq2fasta OutputBucket=iaq-fastq2fasta-output
```
> **The SourceFastqBucket will be created by the deployment but the OutputBucket must exist before**

### Tail Lambda function logs
Tail Lambda function Logs using the Logical name defined in SAM Template:
```bash
sam logs -n FastqConvertFunction --stack-name fastq2fasta-2-2 --tail --region us-west-1
```


@echo off
REM Script para copiar imágenes de Docker Hub a AWS ECR
setlocal enabledelayedexpansion

set REGION=us-east-1
set IMAGE_TAG=qa
set DOCKERHUB_USER=carovasco

echo.
echo ================================================
echo  Pushing Docker images to AWS ECR
echo ================================================
echo Region: %REGION%
echo Tag: %IMAGE_TAG%
echo DockerHub User: %DOCKERHUB_USER%
echo.

REM Get AWS Account ID
for /f "tokens=*" %%i in ('aws sts get-caller-identity --query Account --output text 2^>nul') do set AWS_ACCOUNT_ID=%%i

if "%AWS_ACCOUNT_ID%"=="" (
    echo ERROR: No AWS credentials. Run: aws configure
    exit /b 1
)

set ECR_REGISTRY=%AWS_ACCOUNT_ID%.dkr.ecr.%REGION%.amazonaws.com

echo AWS Account ID: %AWS_ACCOUNT_ID%
echo ECR Registry: %ECR_REGISTRY%
echo.

REM Login to ECR
echo Logging in to AWS ECR...
for /f "tokens=*" %%i in ('aws ecr get-login-password --region %REGION% 2^>nul') do (
    echo %%i | docker login --username AWS --password-stdin %ECR_REGISTRY%
)

if %ERRORLEVEL% NEQ 0 (
    echo ERROR: ECR login failed
    exit /b 1
)
echo OK - ECR login successful
echo.

REM Array of images
setlocal enabledelayedexpansion
set "IMAGES[0]=marketplace-gateway"
set "IMAGES[1]=marketplace-auth"
set "IMAGES[2]=marketplace-product"
set "IMAGES[3]=marketplace-order"
set "IMAGES[4]=marketplace-payment"
set "IMAGES[5]=marketplace-notification"
set "IMAGES[6]=marketplace-blockchain"
set "IMAGES[7]=marketplace-category"
set "IMAGES[8]=marketplace-ai"
set "IMAGES[9]=marketplace-admin"
set "IMAGES[10]=marketplace-search"
set "IMAGES[11]=marketplace-user"
set "IMAGES[12]=marketplace-review"
set "IMAGES[13]=marketplace-ad-connector"
set "IMAGES[14]=marketplace-reporting"

set SUCCESS=0
set SKIPPED=0

REM Process each image
for /L %%i in (0,1,14) do (
    set IMAGE=!IMAGES[%%i]!
    if defined IMAGE (
        echo.
        echo Processing: !IMAGE!
        
        echo   - Pulling from Docker Hub...
        docker pull %DOCKERHUB_USER%/!IMAGE!:%IMAGE_TAG% >nul 2>&1
        if !ERRORLEVEL! EQU 0 (
            echo   - Tagging for ECR...
            docker tag %DOCKERHUB_USER%/!IMAGE!:%IMAGE_TAG% %ECR_REGISTRY%/!IMAGE!:%IMAGE_TAG%
            
            echo   - Pushing to ECR...
            docker push %ECR_REGISTRY%/!IMAGE!:%IMAGE_TAG% >nul 2>&1
            if !ERRORLEVEL! EQU 0 (
                echo   ✓ OK
                set /a SUCCESS+=1
            ) else (
                echo   ✗ Push failed
            )
        ) else (
            echo   ⊘ Image not found - SKIPPED
            set /a SKIPPED+=1
        )
    )
)

echo.
echo ================================================
echo  Completed!
echo  Successful: %SUCCESS%
echo  Skipped: %SKIPPED%
echo ================================================
echo Registry: %ECR_REGISTRY%
echo.

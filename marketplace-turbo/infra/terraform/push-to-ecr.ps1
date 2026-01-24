# Script PowerShell para copiar imágenes de Docker Hub a AWS ECR
param(
    [string]$Region = "us-east-1",
    [string]$ImageTag = "qa",
    [string]$DockerHubUser = "carovasco"
)

Write-Host "AWS Region: $Region" -ForegroundColor Cyan
Write-Host "Image Tag: $ImageTag" -ForegroundColor Cyan
Write-Host ""

# Arrays de imágenes
$Images = @(
    "marketplace-gateway",
    "marketplace-auth",
    "marketplace-product",
    "marketplace-order",
    "marketplace-payment",
    "marketplace-notification",
    "marketplace-blockchain",
    "marketplace-category",
    "marketplace-ai",
    "marketplace-admin",
    "marketplace-search",
    "marketplace-user",
    "marketplace-review",
    "marketplace-ad-connector",
    "marketplace-reporting"
)

# Get AWS Account ID
Write-Host "Getting AWS Account ID..." -ForegroundColor Yellow
try {
    $AccountIdOutput = aws sts get-caller-identity --query Account --output text 2>$null
    if ($null -eq $AccountIdOutput) {
        Write-Host "ERROR: No AWS credentials found" -ForegroundColor Red
        Write-Host "Please run: aws configure" -ForegroundColor Yellow
        exit 1
    }
    $AwsAccountId = $AccountIdOutput
    $EcrRegistry = "$AwsAccountId.dkr.ecr.$Region.amazonaws.com"
    Write-Host "Account ID: $AwsAccountId" -ForegroundColor Green
    Write-Host "ECR Registry: $EcrRegistry" -ForegroundColor Green
} catch {
    Write-Host "ERROR: Failed to get AWS Account ID" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Login a ECR
Write-Host "Logging in to AWS ECR..." -ForegroundColor Yellow
$LoginCmd = "aws ecr get-login-password --region $Region 2>nul | docker login --username AWS --password-stdin $EcrRegistry"
$LoginResult = Invoke-Expression $LoginCmd
if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ ECR login successful" -ForegroundColor Green
}
else {
    Write-Host "ERROR: ECR login failed" -ForegroundColor Red
    exit 1
}

Write-Host ""

# Process each image
$SuccessCount = 0
$SkippedCount = 0

foreach ($Image in $Images) {
    Write-Host ""
    Write-Host "Processing: $Image" -ForegroundColor Cyan
    
    # Pull from Docker Hub
    Write-Host "  → Pulling from Docker Hub..." -NoNewline
    $PullResult = docker pull "$DockerHubUser/$Image`:$ImageTag" 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✓" -ForegroundColor Green
    } else {
        Write-Host " ✗ SKIPPED" -ForegroundColor Yellow
        Write-Host "    Image not found in Docker Hub" -ForegroundColor Gray
        $SkippedCount++
        continue
    }
    
    # Tag for ECR
    Write-Host "  → Tagging for ECR..." -NoNewline
    docker tag "$DockerHubUser/$Image`:$ImageTag" "$EcrRegistry/$Image`:$ImageTag" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✓" -ForegroundColor Green
    } else {
        Write-Host " ✗" -ForegroundColor Red
        continue
    }
    
    # Push to ECR
    Write-Host "  → Pushing to ECR..." -NoNewline
    docker push "$EcrRegistry/$Image`:$ImageTag" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) {
        Write-Host " ✓" -ForegroundColor Green
        $SuccessCount++
    } else {
        Write-Host " ✗" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Push to ECR completed!" -ForegroundColor Green
Write-Host "  ✓ Successful: $SuccessCount" -ForegroundColor Green
Write-Host "  ⊘ Skipped: $SkippedCount" -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Green
Write-Host "Registry: $EcrRegistry" -ForegroundColor Cyan

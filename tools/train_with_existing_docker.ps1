$ErrorActionPreference = 'Stop'

$repoPath = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$image = 'cvat.pytorch.ultralytics.yoloe:latest'
$weights = Join-Path $repoPath 'yolo11n.pt'
$epochs = 30
$imgsz = 416
$batch = 1

if (-not (Test-Path -LiteralPath $weights)) {
    throw "Missing detection weights: $weights"
}

docker run --rm --pull=never --gpus all --shm-size=2g `
    -v "${repoPath}:/workspace" `
    -w /workspace `
    $image `
    python -c "from ultralytics import YOLO; model = YOLO('/workspace/yolo11n.pt'); model.train(data='/workspace/data.yaml', epochs=${epochs}, imgsz=${imgsz}, batch=${batch}, device=0, amp=True, workers=0, plots=False, project='/workspace/runs', name='yolo11n_d2', exist_ok=True)"

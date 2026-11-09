$ErrorActionPreference = 'Stop'

$repoPath = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$image = 'cvat.pytorch.ultralytics.yoloe:latest'
$epochs = 30
$imgsz = 416
$batch = 1

docker run --rm --gpus all --shm-size=2g `
    -v "${repoPath}:/workspace" `
    -w /workspace `
    $image `
    python -c "from ultralytics import YOLOE; model = YOLOE('yoloe-26l-seg.pt'); model.train(data='/workspace/data.yaml', epochs=${epochs}, imgsz=${imgsz}, batch=${batch}, device=0, amp=True, workers=0, project='/workspace/runs', name='yoloe26l_d2', exist_ok=True)"

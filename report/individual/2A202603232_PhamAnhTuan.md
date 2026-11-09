# Individual report - Day 2 Object Detection

## 1. Student information

- Name: Pham Anh Tuan
- Student ID: 2A202603232
- Email: Not provided
- Class: L2B
- Repository: https://github.com/AnhTuan2003ml/K5-L2B-Day02-PhamAnhTuan-2A202603232-ObjectDetection
- Colab link: Not used; training was run locally in Docker with NVIDIA GPU.

## 2. Schema and mini guideline

The class definitions and ambiguity decisions are recorded in [GUIDELINE_MINI.md](../../GUIDELINE_MINI.md). The main decisions are to classify small pickups as `car`, box-shaped compact vehicles as `van`, and partially occluded long passenger vehicles as `bus` when the visible structure supports that decision.

## 3. Annotation and self-QC

- Training label files: 50.
- Checker result: 50/50 files valid; class IDs are limited to 0, 1, 2, and 3 and all boxes are normalized and inside image bounds.
- Images reviewed: `drive_001`, `drive_002`, `drive_010`, `drive_020`, `drive_030`, `drive_035`, `drive_040`, `drive_045`, `drive_050`, and `drive_060`.
- Main errors found: duplicate boxes and over-labeling in the earlier labels. The fine-tuned model labels were regenerated with 1024-pixel tiled inference, 20% tile overlap, and confidence 0.20 to improve small-vehicle recall.
- Initial label commit: `786fe1a`.

## 4. Gold QC and rework

| Metric | Before rework | After rework |
|---|---:|---:|
| TP | 462 | 507 |
| FP | 1078 | 183 |
| FN | 191 | 146 |
| Precision | 0.3000 | 0.7348 |
| Recall | 0.7075 | 0.7764 |
| F1 | 0.4213 | 0.7550 |
| mean_iou_of_matches | 0.8239 | 0.8777 |
| passed | false | false |

The final annotation evaluation is stored in `outputs/annotation_evaluation.json`. Tiled inference improved recall and F1, but the result remains below the repository target because small and partially occluded vehicles are still missed.

## 5. YOLO results

- Runtime: Docker with NVIDIA GPU, CUDA 12.4.1, PyTorch 2.6.0+cu124, Ultralytics 8.4.0.
- Model: YOLO26m initialized from the VisDrone vehicle checkpoint and fine-tuned for four repository classes.
- Training: 100 epochs, image size 1024, batch size 1, AMP/FP16, workers 0, seed 20260909.
- Best checkpoint during the local run: `outputs/yolo26_runs/gold_finetune_yolo26m/weights/best.pt`.
- Evaluation previews: `assets/eval_predictions/visuals/drive_051.jpg` through `drive_060.jpg`.
- Training plots and metrics: `assets/yolo26_runs/`.

| Metric on 10 eval images | Value |
|---|---:|
| Precision | 0.4792 |
| Recall | 0.4771 |
| mAP50 | 0.4590 |
| mAP50-95 | 0.3041 |

1. The lowest-recall class is not reliable enough to determine from the aggregate log alone; the class-specific confusion matrix in `assets/yolo26_runs/confusion_matrix.png` is the reference for the per-class comparison. The eval preview files show missed small vehicles.
2. A high mAP50 with lower mAP50-95 indicates that detections overlap the object but boxes are not consistently tight at stricter IoU thresholds. Box edges, partial occlusion, and small-object localization should be reviewed.
3. The most likely class confusion is between `truck`, `bus`, and `van`, because the visible body shape can be ambiguous. The decisions in `GUIDELINE_MINI.md` and the confusion matrix support this interpretation.
4. The 10 eval images must not be used for training because they are reserved for an unbiased comparison. They measure generalization after training and provide the validation metrics reported above.

## 6. Difficulties and handling

| Step | Observed issue | Attempt | Result |
|---|---|---|---|
| Initial auto-label | Many duplicate and false-positive boxes | Used 1024-pixel tiled inference with 20% overlap | Confidence 0.20 gave the best tested F1 and improved small-vehicle recall |
| Fine-tuning | Small dataset and class imbalance | Used pretrained YOLO26m weights, 1024 resolution, 100 epochs, and GPU AMP | Validation metrics were produced, but recall remains limited |
| Export | Repository requires exact YOLO structure | Ran `tools/check_yolo_labels.py` after replacing train labels | 50/50 files passed |

## 7. Rubric self-assessment

Completed: repository structure, 50 train label files, mini guideline, annotation evaluation JSON, training metrics, eval prediction previews, and individual report. Remaining limitation: the final F1 is 0.7550, below the target 0.80, and no Colab link is available because the run used local Docker.

## 8. AI tools and references

- AI assistance was used to inspect the repository, run the local Docker training/evaluation workflow, and review generated outputs. The final labels and reported metrics were checked with repository scripts.
- Ultralytics YOLO26m VisDrone checkpoint: https://huggingface.co/kailunw/visdrone-yolo26m

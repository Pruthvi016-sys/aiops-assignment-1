# AIOps — Module 1 Assignment

This repository contains all deliverables for the Module 1 assignment (Experiment Management & Reproducibility): technical debt diagnosis, MLflow experiment tracking, DVC data versioning, and an end-to-end reproducibility drill.

**1-page written report (Q1 + Q2 analysis, condensed Q3/Q4):** [`1-page_pdf_report.pdf`](./1-page_pdf_report.pdf)

**Demo video (2–5 min walkthrough of all four questions):** `https://drive.google.com/file/d/1vvbegGnXccSS6NMQttJGZ_eb1Pbjq70E/view?usp=sharing

---

## Repository Structure & Where to Find Each Answer

| Question | Location | What's there |
|---|---|---|
| **Q1** — Technical Debt Diagnosis | [`1-page_pdf_report.pdf`](./1-page_pdf_report.pdf) | Full written answer (category identification + mitigation). No separate code/folder — this question was purely conceptual. |
| **Q2** — MLflow Experiment Comparison | [`q2 - Applied: MLflow Experiment Comparison/`](<./q2%20-%20Applied:%20MLflow%20Experiment%20Comparison>) | Notebook, logging code, comparison table screenshot, best-run curves screenshot. Written analysis is in the 1-page report. |
| **Q3** — DVC Data Versioning & Rollback | [`q3-dvc-versioning/`](./q3-dvc-versioning) | DVC-tracked `filenames.csv`, `.dvc` files, rollback proof screenshot, other terminal screenshots. |
| **Q4** — Capstone Reproducibility Drill | [`q4 - Capstone: End-to-End Reproducibility Drill/`](<./q4%20-%20Capstone:%20End-to-End%20Reproducibility%20Drill>) | My (Partner B) reproduction screenshots + `note.txt` pointing to the shared repo with Partner A. |

---

## Question 2 — MLflow Experiment Comparison (MNIST + MLP)

**Folder:** `q2 - Applied: MLflow Experiment Comparison/`

| File | Description |
|---|---|
| `Exercise1_MNIST_MLP_Question2.ipynb` | Full notebook — loads MNIST, trains `MLPClassifier` across a 3×3 grid of `learning_rate_init` × `batch_size` (9 runs), logs params/metrics per epoch to MLflow. |
| `mlflow-codesnippet.py` | The exact `mlflow.log_param` / `mlflow.log_metric` code added to the starter script (Deliverable 3). |
| `screenshot-mlflow-run-comparision-table.png`  | The 9-run comparison table from the MLflow UI (Deliverable 1). |
| `curves-best-run.png` | train_loss / train_accuracy / val_accuracy curves for the best run (used as evidence for the overfitting analysis). |

**Written analysis** (best run, overfitting evidence, hyperparameter comparison) is in the 1-page report.

**To reproduce:** open the notebook in Jupyter/VS Code, run cells top to bottom, with a local MLflow tracking server running at `http://localhost:5000` (see Q4's setup steps below for the server command — it's the same one).

---

## Question 3 — DVC Data Versioning & Rollback

**Folder:** `q3-dvc-versioning/`

**What was done:**
1. Initialized a DVC project (`dvc init --subdir`) inside this folder, with a **Git repo** as the parent.
2. Configured an **SSH remote** pointing to a partner's machine (`ssh://<user>@<host>/home/<user>/dvc-remote-storage`) — satisfies the assignment's "SSH remote or S3 bucket only" requirement.
3. Generated `filenames.csv` from the class `data.zip` (1800 files → 1801 rows with header), tracked it with `dvc add`, committed as **v1**, and pushed to the remote with `dvc push`.
4. Extracted `new-labels.zip`, regenerated `filenames.csv` (2800 files → 2801 rows with header), re-ran `dvc add`, committed as **v2** with a clear commit message, and pushed.
5. Demonstrated rollback: `git checkout v1 -- filenames.csv.dvc` followed by `dvc checkout` restored the working file to exactly **1801 rows**, matching v1 exactly (proof in `roll-back-terminal-output.jpeg`).

**Key commands used (full sequence):**
```bash
dvc init --subdir
dvc remote add -d myremote ssh://<user>@<host>/home/<user>/dvc-remote-storage

# v1
(echo "filename" && find data -type f | sed 's|^data/||' | sort) > filenames.csv
dvc add filenames.csv
git add filenames.csv.dvc .gitignore
git commit -m "Add filenames.csv v1 (1800 files + header)"
git tag v1
dvc push

# v2 (after unzipping new-labels.zip into data/)
(echo "filename" && find data -type f | sed 's|^data/||' | sort) > filenames.csv
dvc add filenames.csv
git add filenames.csv.dvc
git commit -m "Update filenames.csv to v2 (2800 files + header = 2801 rows, added new-labels.zip data)"
git tag v2
dvc push

# Rollback to v1
git checkout v1 -- filenames.csv.dvc
dvc checkout
wc -l filenames.csv   # -> 1801, matching v1 exactly
```

**Files:**
- `filenames.csv.dvc` — current DVC pointer file (tracks the actual data, which lives on the SSH remote, not in Git).
- `.dvc/`, `.dvcignore`, `.gitignore` — DVC project config.
- `roll-back-terminal-output.jpeg` — terminal proof of the v2 → v1 rollback (row count verification).
- `other-screenshots/` — supporting screenshots (v1/v2 push confirmations, data extraction, etc.).

**To reproduce:** you'd need access to the same SSH remote (not portable as-is, since it points to a specific machine) — the terminal screenshots serve as the proof of execution for grading.

---

## Question 4 — End-to-End Reproducibility Drill (my role: Partner B)

**Folder:** `q4 - Capstone: End-to-End Reproducibility Drill/`

**Important:** For this question, my partner (Mohammed Khaja - DA24B015) and I worked in **Partner A's repository** together (as collaborators), rather than a separate third repo, since the assignment only requires that both partners' work live in one shared repo and be clearly attributable by commit — it does not require a brand-new repo. That shared repo is:

**Partner A's repository (shared, contains all Q4 work):** https://github.com/raisserv2/aiops-assignment1

My commits in that repository are under my own GitHub account(Pruthvi016-sys) and can be checked directly there for reference (see `note.txt` in this folder for the same pointer).

**What Partner A did (their part, 6 marks):** trained an MLP on MNIST, logged the run to MLflow with params, metrics, seed, a `git_commit` tag, and the model artifact; versioned the dataset with DVC; committed code + `.dvc` file together in one commit; registered the model and moved it to `Staging`.

**What I did as Partner B (my part, 6 + 3 marks):**
1. `git clone https://github.com/raisserv2/aiops-assignment1.git`
2. `git checkout <partner A's pinned commit>` (tag: `capstone`)
3. `conda activate aiops-m1`
4. `dvc checkout` to restore the DVC-tracked dataset
5. Started the local MLflow tracking server and reran the training script with the exact same hyperparameters and seed:
   ```bash
   python train.py --lr 0.001 --hidden "256,128" --epochs 20 --batch_size 200 --seed 42
   ```
6. Logged a reproducibility note directly onto the MLflow run via `MlflowClient().set_tag(...)`, and committed the verification back to the shared repo.

**Result:**
- Partner A's reported accuracy: **0.9782**
- My (Partner B) reproduced accuracy: **0.9784**
- Difference: **0.0002**, well within the stated tolerance of 0.005 → **match confirmed**

**Files in this folder:**
- `Screenshot From 2026-08-30 19-38-51.png`, `Screenshot From 2026-08-30 19-39-02.png` — terminal output of the clone/checkout/env-create/dvc-checkout/rerun steps and the final accuracy.
- `mlflow-server.png` — MLflow server running, confirming the run and its logged metrics/tags.
- `reran and logged the note.png` — the reproducibility note being logged and committed.
- `note.txt` — pointer to the shared repository and my commits there.

**How to run (from the shared repo's own README, reproduced here for convenience):**
```bash
# 1. Clone and checkout
git clone https://github.com/raisserv2/aiops-assignment1.git
cd aiops-assignment1
git checkout capstone   # or the pinned commit hash

# 2. Create environment
conda env create -f environment.yml
conda activate aiops-m1

# 3. Restore DVC-tracked data
dvc checkout   # requires SSH access to the DVC remote

# 4. Start MLflow server (Terminal 1)
mlflow server --backend-store-uri sqlite:///mlflow.db \
    --default-artifact-root ./mlruns --host 0.0.0.0 --port 5000

# 5. Run training (Terminal 2)
python train.py --lr 0.001 --hidden "256,128" --epochs 20 --batch_size 200 --seed 42
# Expected output: Final accuracy ≈ 0.9782–0.9784
```

---

## AI Usage Disclosure

Per assignment guidelines, AI tool usage is disclosed per question below. **Tool used: Claude (Anthropic).**

| Question | AI usage |
|---|---|
| **Q1** | No AI usage. |
| **Q2** | Used for help writing the MLP training/logging code (converting the starter script from RandomForest+Iris to MLPClassifier+MNIST, and structuring the per-epoch MLflow logging loop). |
| **Q3** | Used for the SSH commands needed to connect to and verify the DVC remote (a partner's laptop) — e.g. setting up `openssh-server`, testing connectivity, and constructing the `dvc remote add ssh://...` command. |
| **Q4** | Used for some general Linux/terminal commands during setup and troubleshooting (environment/package installation, Git/SSH configuration issues). |

**Overall impact:** Claude was helpful mainly for boilerplate code, exact command syntax, and troubleshooting environment/networking issues (e.g. SSH connectivity, package installation errors). The actual experimental design, hyperparameter choices, analysis and interpretation of results, and all the DVC/Git/MLflow workflow decisions were done manually. Overall, AI assistance had **less impact on the core work and more on manual/setup tasks** — most of the actual assignment work (running experiments, reading results, writing the analysis, doing the DVC versioning and reproducibility steps) was done by hand.

---

## Demo Video

A 2–5 minute video walking through the working demo and explanation of all four questions is available here: `https://drive.google.com/file/d/1vvbegGnXccSS6NMQttJGZ_eb1Pbjq70E/view?usp=sharing

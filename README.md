# Scientific Claim Verifier

WEX 428 full-stack NLI project.

## Core task

Given a `premise` and a `hypothesis`, the model predicts:

- `0` — Entailment
- `1` — Neutral
- `2` — Contradiction

The university-provided MultiNLI files are used for training and evaluation.
Ready-made LLM APIs are not used for the core prediction task.

## Planned stack

- AI/NLP: PyTorch + Hugging Face Transformers
- Backend: FastAPI
- Frontend: React
- Database: PostgreSQL
- Authentication: JWT
- Charts: Recharts
- Deployment: Docker Compose

The exact PyTorch installation command will be selected after checking whether
the development computer has a compatible NVIDIA GPU.

## First setup on Windows 11

1. Install Python 3.12 and Git.
2. Open PowerShell in this project directory.
3. Run:

   ```powershell
   Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
   .\setup_windows.ps1
   ```

4. Copy the three CSV files into `data/raw/`.
5. Run the audit:

   ```powershell
   .\.venv\Scripts\Activate.ps1
   python -m src.data.audit_dataset
   ```

6. Prepare the cleaned training file:

   ```powershell
   python -m src.data.prepare_dataset
   ```

## Important data policy

The raw CSV files and generated model files are excluded from Git. Code,
configuration, documentation, and compact evaluation reports will be committed.

## Arabic guide

هذا هو الهيكل الأولي الرسمي للمشروع. في البداية نشغّل فحص الجهاز والبيانات،
ثم نختار أمر تثبيت PyTorch المناسب حسب وجود كرت NVIDIA، وبعد ذلك نبدأ تجربة
Baseline صغيرة قبل التدريب الكامل.

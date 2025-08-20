# Quick Sales Dashboard (1-file Streamlit Cloud)

Siêu gọn để deploy nhanh:
- **Chỉ 1 file `app.py`** (tự sinh dữ liệu giả lập)
- `requirements.txt` (streamlit + pandas)

## Deploy (2 bước)
1) Tạo repo GitHub, push 2 file: `app.py`, `requirements.txt`.
2) Vào https://streamlit.io/cloud → New app → chọn repo, main file: `app.py` → Deploy.

## Chạy local
```bash
pip install -r requirements.txt
streamlit run app.py
```

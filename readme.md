1)Initial activation
python -m venv venv

venv\Scripts\activate

pip install -r requirements.txt

uvicorn main:app --reload

deactivate

2)Subsequent activations
venv\Scripts\activate

uvicorn main:app --reload

deactivate
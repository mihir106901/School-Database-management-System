# School DBMS (Modular CLI + MySQL)

A modular, menu-driven CLI application for managing:
- Student Records
- Fees/Payment Records
- Library Records
- Exam Records (includes optional matplotlib plot)

## Requirements
- Python 3.9+
- MySQL 8.0+
- Python packages:
  - mysql-connector-python
  - prettytable
  - matplotlib (optional; only for plotting exam performance)

Install:
```bash
pip install mysql-connector-python prettytable matplotlib
```

## Setup (recommended)
1. Create a `.env` file (copy from `.env.example`) and fill credentials.
2. Initialize DB + tables:
```bash
python init_db.py
```
3. Run the app:
```bash
python main.py
```

## Notes
- Uses parameterized SQL queries to avoid SQL injection.
- Schema uses foreign keys with `ON DELETE CASCADE` so deleting a student removes associated records.


## Authors

- **Mihir Patel**  
  GitHub: https://github.com/mihir106901 

- **Ishaan Ray**   
  GitHub: https://github.com/Cipher-Shadow-IR

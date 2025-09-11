## 1. Core functions (core/)

- flattener.py

    - Flatten object lồng sâu → {"a":{"b":{"c":1}}} → {"a.b.c":1}

    - Config delimiter (., _, custom).

    - Xử lý array: primitive, object, nested.

- relation.py

    -  Sinh bảng quan hệ (1–N, N–N).

    - Tạo bảng con & junction table khi cần.

- null_handler.py

    - Chuẩn hóa null → None.

    - Tự động thêm cột bị thiếu (fill None).

- type_cast.py

    - Ép kiểu string → int/float/bool/date theo schema.

    - Cho phép custom rules.

- dedup.py

    - Loại bỏ phần tử trùng trong array.

    - Loại bỏ record trùng khi map sang bảng con.

- transformer.py

    - Schema-driven transformation.

    - Input JSON + schema mapping → output dict[table] hoặc DataFrame.

2. Helper / Utility (utils/)

- config.py

    - Config toàn cục: delimiter, explode mode, naming convention.

- naming.py

    - Chuyển đổi key: snake_case, camelCase, giữ nguyên.

    - Xử lý ký tự đặc biệt (-, space, unicode).

- validation.py

    - Kiểm tra dữ liệu theo schema.

    - Báo lỗi khi mismatch type.

- error_handler.py

    - Logging: cảnh báo khi ép kiểu fail, JSON quá sâu.

    - Error handling strategy (raise/skip/warn).

- output.py

    - Chuyển kết quả sang:

        - Python dict (table_name → list[dict]).

        - Pandas DataFrame.

        - SQLAlchemy ORM/Table.

3. Tests (tests/)

- Kiểm tra toàn bộ edge cases bạn liệt kê (A → G).

- Đảm bảo module hoạt động đúng trong mọi tình huống, kể cả mixed types và nested phức tạp.

4. Examples (examples/)

- Code mẫu để developer nhanh chóng thử:

    - Flatten object cơ bản.

    - Sinh bảng quan hệ 1–N.

    - Schema mapping nâng cao.

5. Extensions (extensions/) (optional/future)

- schema_infer.py: đoán schema từ nhiều record JSON.

- streaming.py: xử lý stream từ Kafka/logs.

- parallel.py: normalize theo batch (multiprocessing).

- integration.py: load trực tiếp sang PostgreSQL/MySQL.

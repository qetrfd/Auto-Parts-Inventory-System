from __future__ import annotations
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
import sqlite3
import os
import shutil
from datetime import datetime

HEADERS = [
    "id",
    "nombre_producto",
    "costo",
    "precio",
    "precio_mayoreo",
    "tipo_producto",
    "marca",
    "calidad",
    "garantia_meses",
    "disponibilidad",
    "vida_util_meses",
]


@dataclass
class Articulo:
    id: str
    nombre_producto: str
    costo: float
    precio: float
    precio_mayoreo: float
    tipo_producto: str
    marca: str
    calidad: str
    garantia_meses: int
    disponibilidad: int
    vida_util_meses: int


class Inventario:
    def __init__(self, db_path: str = "inventario.db") -> None:
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self._init_db()
        self.items: List[Articulo] = []

    def close(self) -> None:
        try:
            self.conn.close()
        except Exception:
            pass

    def _init_db(self) -> None:
        cur = self.conn.cursor()
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS inventario
                    (
                        id
                        TEXT
                        PRIMARY
                        KEY,
                        nombre_producto
                        TEXT
                        NOT
                        NULL,
                        costo
                        REAL
                        NOT
                        NULL,
                        precio
                        REAL
                        NOT
                        NULL,
                        precio_mayoreo
                        REAL
                        NOT
                        NULL,
                        tipo_producto
                        TEXT
                        NOT
                        NULL,
                        marca
                        TEXT
                        NOT
                        NULL,
                        calidad
                        TEXT
                        NOT
                        NULL,
                        garantia_meses
                        INTEGER
                        NOT
                        NULL,
                        disponibilidad
                        INTEGER
                        NOT
                        NULL,
                        vida_util_meses
                        INTEGER
                        NOT
                        NULL
                    );
                    """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_marca ON inventario(marca);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_tipo ON inventario(tipo_producto);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_calidad ON inventario(calidad);")
        cur.execute("""
                    CREATE TABLE IF NOT EXISTS logs
                    (
                        id
                        INTEGER
                        PRIMARY
                        KEY
                        AUTOINCREMENT,
                        ts
                        TEXT
                        NOT
                        NULL,
                        action
                        TEXT
                        NOT
                        NULL,
                        item_id
                        TEXT
                        NOT
                        NULL,
                        field
                        TEXT,
                        before
                        TEXT,
                        after
                        TEXT
                    );
                    """)
        cur.execute("CREATE INDEX IF NOT EXISTS idx_logs_item ON logs(item_id);")
        cur.execute("CREATE INDEX IF NOT EXISTS idx_logs_ts ON logs(ts);")
        self.conn.commit()

    def cargar(self) -> None:
        self.items.clear()
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM inventario ORDER BY id;")
        rows = cur.fetchall()
        for r in rows:
            self.items.append(Articulo(
                id=r["id"],
                nombre_producto=r["nombre_producto"],
                costo=float(r["costo"]),
                precio=float(r["precio"]),
                precio_mayoreo=float(r["precio_mayoreo"]),
                tipo_producto=r["tipo_producto"],
                marca=r["marca"],
                calidad=r["calidad"],
                garantia_meses=int(r["garantia_meses"]),
                disponibilidad=int(r["disponibilidad"]),
                vida_util_meses=int(r["vida_util_meses"]),
            ))

    def guardar(self) -> None:
        self.conn.commit()

    def backup(self) -> str:
        os.makedirs("backups", exist_ok=True)
        stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        dst = os.path.join("backups", f"inventario_{stamp}.db")
        self.conn.commit()
        try:
            shutil.copy2(self.db_path, dst)
        except Exception:
            pass
        return dst

    def _log(self, action: str, item_id: str, field: Optional[str], before: Optional[str],
             after: Optional[str]) -> None:
        cur = self.conn.cursor()
        cur.execute("""
                    INSERT INTO logs (ts, action, item_id, field, before, after)
                    VALUES (?, ?, ?, ?, ?, ?);
                    """, (datetime.now().isoformat(timespec="seconds"), action, item_id, field, before, after))
        self.conn.commit()

    def get_logs(self, item_id: str, limit: int = 10) -> List[dict]:
        cur = self.conn.cursor()
        cur.execute("""
                    SELECT ts, action, item_id, field, before, after
                    FROM logs
                    WHERE item_id = ?
                    ORDER BY id DESC
                        LIMIT ?;
                    """, (item_id.strip(), int(limit)))
        return [dict(r) for r in cur.fetchall()]

    def buscar_por_id(self, item_id: str) -> Optional[Articulo]:
        item_id = item_id.strip()
        for it in self.items:
            if it.id == item_id:
                return it
        return None

    def distinct_values(self) -> Dict[str, List[str]]:
        cur = self.conn.cursor()
        out: Dict[str, List[str]] = {}
        for field in ("marca", "tipo_producto", "calidad"):
            cur.execute(f"SELECT DISTINCT {field} AS v FROM inventario ORDER BY v;")
            out[field] = [r["v"] for r in cur.fetchall() if r["v"] is not None]
        return out

    def next_id(self, prefix: str = "BMW") -> str:
        cur = self.conn.cursor()
        cur.execute("SELECT id FROM inventario WHERE id LIKE ?;", (f"{prefix}-%",))
        ids = [r["id"] for r in cur.fetchall()]
        max_n = 0
        for s in ids:
            try:
                part = s.split("-", 1)[1]
                n = int(part)
                if n > max_n:
                    max_n = n
            except Exception:
                continue
        return f"{prefix}-{max_n + 1:04d}"

    def _exists_id(self, item_id: str) -> bool:
        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM inventario WHERE id = ? LIMIT 1;", (item_id.strip(),))
        return cur.fetchone() is not None

    def agregar(self, articulo: Articulo) -> None:
        if not articulo.id.strip():
            raise ValueError("El ID es obligatorio.")
        if self._exists_id(articulo.id):
            raise ValueError(f"Ya existe un artículo con ID: {articulo.id}")
        self.backup()
        cur = self.conn.cursor()
        cur.execute("""
                    INSERT INTO inventario
                    (id, nombre_producto, costo, precio, precio_mayoreo, tipo_producto, marca, calidad,
                     garantia_meses, disponibilidad, vida_util_meses)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    """, (
                        articulo.id.strip(),
                        articulo.nombre_producto.strip(),
                        float(articulo.costo),
                        float(articulo.precio),
                        float(articulo.precio_mayoreo),
                        articulo.tipo_producto.strip(),
                        articulo.marca.strip(),
                        articulo.calidad.strip(),
                        int(articulo.garantia_meses),
                        int(articulo.disponibilidad),
                        int(articulo.vida_util_meses),
                    ))
        self.conn.commit()
        self._log("ADD", articulo.id.strip(), None, None, "CREATED")
        self.cargar()

    def actualizar(self, item_id: str, campo: str, valor) -> None:
        item_id = item_id.strip()
        if campo not in HEADERS or campo == "id":
            raise ValueError("Campo inválido o no editable.")
        cur = self.conn.cursor()
        cur.execute(f"SELECT {campo} AS v FROM inventario WHERE id = ?;", (item_id,))
        row = cur.fetchone()
        if not row:
            raise ValueError("No se encontró el artículo para actualizar.")
        before = None if row["v"] is None else str(row["v"])
        self.backup()
        if campo in ("costo", "precio", "precio_mayoreo"):
            v = float(valor)
        elif campo in ("garantia_meses", "disponibilidad", "vida_util_meses"):
            v = int(valor)
        else:
            v = str(valor).strip()
        cur.execute(f"UPDATE inventario SET {campo} = ? WHERE id = ?;", (v, item_id))
        self.conn.commit()
        self._log("UPDATE", item_id, campo, before, str(v))
        self.cargar()

    def eliminar(self, item_id: str) -> None:
        item_id = item_id.strip()
        self.backup()
        cur = self.conn.cursor()
        cur.execute("DELETE FROM inventario WHERE id = ?;", (item_id,))
        self.conn.commit()
        self._log("DELETE", item_id, None, "EXISTED", "DELETED")
        self.cargar()
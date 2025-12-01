import csv
import mysql.connector

# Configuración de conexión
DB_CONFIG = {
    "host": "mysql",
    "user": "root",
    "password": "6FNEUhPC",
    "database": "openedx"
}

# ID del curso fijo
COURSE_ID = "course-v1:asdasd+123+prueba.123"

# Archivo de salida en carpeta compartida
OUTPUT_FILE = "/openedx/shared/usuarios_discusion_reciente.csv"

print("\n📌 Exportando usuarios que han comentado en el curso:")
print(f"    {COURSE_ID}\n")

# Conexión
conn = mysql.connector.connect(**DB_CONFIG)
cur = conn.cursor()

# Consulta sin fecha
query = """
SELECT DISTINCT
    au.username AS usuario,
    au.id AS user_id
FROM
    forum_comment AS fc
JOIN
    auth_user AS au ON au.id = fc.author_id
WHERE
    fc.course_id = %s;
"""

cur.execute(query, (COURSE_ID,))
rows = cur.fetchall()

# Generar CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Username", "User ID"])
    writer.writerows(rows)

if not rows:
    print("⚠️ No se encontraron usuarios (pero el CSV se generó igual).")
else:
    print(f"✅ Archivo generado con {len(rows)} usuarios únicos.")

print("\n📂 Archivo disponible en:")
print(f"   {OUTPUT_FILE}")
print("💻 También en tu host: ~/openedx_shared/\n")

# Cerrar conexión
cur.close()
conn.close()

